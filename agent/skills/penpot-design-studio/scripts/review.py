#!/usr/bin/env python3
"""Scoped native inspection/capture, copy-only content stress, and offline comparisons."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import uuid
from doctor import Client

ROOT = Path(__file__).resolve().parent


def result_json(response):
    result = response.get('result', {})
    if 'error' in response or result.get('isError'):
        raise ValueError('MCP operation failed')
    for block in result.get('content', []):
        if block.get('type') != 'text':
            continue
        value = block.get('text', '')
        for _ in range(4):
            try:
                decoded = json.loads(value)
                if isinstance(decoded, str):
                    value = decoded
                    continue
            except ValueError:
                pass
            marker = 'OMP_REVIEW_V1 '
            if marker in value:
                candidate = value.split(marker, 1)[1]
                for attempt in (candidate, candidate.replace('\\"', '"')):
                    try:
                        data, _ = json.JSONDecoder().raw_decode(attempt)
                        if isinstance(data, dict):
                            return data
                    except ValueError:
                        pass
            break
    raise ValueError('No verified result; check the connected Penpot tab')


def connect():
    config = json.loads((Path.home()/'.omp/agent/mcp.json').read_text())['mcpServers']['penpot']
    client = Client(config, max_response_bytes=32_000_000, timeout=45)
    response = client.call('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {},
        'clientInfo': {'name': 'omp-design-review', 'version': '1.0'}})
    if 'result' not in response:
        raise ValueError('MCP initialization failed')
    client.headers['MCP-Protocol-Version'] = response['result']['protocolVersion']
    client.call('notifications/initialized', notification=True)
    return client


def execute(client, request):
    code = (ROOT/'review_native.js').read_text().replace('__REQUEST_JSON__', json.dumps(request, ensure_ascii=True), 1)
    return result_json(client.call('tools/call', {'name': 'execute_code', 'arguments': {'code': code}}))


def exceeds(inner, outer, tolerance=1):
    if not inner or not outer:
        return False
    return (inner['x'] < outer['x']-tolerance or inner['y'] < outer['y']-tolerance
            or inner['x']+inner['width'] > outer['x']+outer['width']+tolerance
            or inner['y']+inner['height'] > outer['y']+outer['height']+tolerance)


def lint(snapshot):
    findings = []
    for board in snapshot['boards']:
        for shape in board['shapes']:
            if not shape.get('visible', True):
                continue
            base = {'boardId': board['id'], 'shapeId': shape['id'], 'name': shape.get('name')}
            def add(code, detail, severity='review'):
                findings.append(dict(base, code=code, detail=detail, severity=severity))
            if shape.get('fontAvailable') is False:
                add('font-unavailable', 'Font ID absent from the current font catalog', 'needs-fix')
            if not shape.get('rotation') and not next((s.get('rotation') for s in board['shapes'] if s['id']==board['id']), 0):
                if shape.get('textBounds') and exceeds(shape['textBounds'], shape.get('bounds')):
                    add('text-overflow', 'Rendered text bounds exceed the text frame; inspect the export')
                if shape['id'] != board['id'] and exceeds(shape.get('bounds'), board['bounds']):
                    add('outside-board', 'Visible shape extends beyond board; may be intentional decoration')
            if shape.get('instance') and not shape.get('componentId'):
                add('component-unresolved', 'Instance reports no component ID; investigate linkage')
            fills = shape.get('fills', [])
            if shape.get('type') in ('text', 'rectangle', 'board') and not shape.get('tokens', {}).get('fill'):
                if any(f.get('color') and not f.get('reference') and not f.get('image') for f in fills):
                    add('literal-fill', 'Literal fill has no reported token/color reference; review system consistency', 'info')
    return {'schema': 1, 'fileId': snapshot['fileId'], 'pageId': snapshot['pageId'],
        'revision': snapshot['revision'], 'findings': findings,
        'limitations': ['Geometric checks are review hints, not a visual/a11y score.',
            'Rotated bounds, mixed text runs, font loading and intentional clipping need visual review.',
            'No automatic fixes; asset colors may intentionally be literal.']}


def validate_fixture(fixture):
    if not isinstance(fixture.get('name'), str) or not fixture['name'].strip():
        raise ValueError('Fixture requires a name')
    changes = fixture.get('changes')
    if not isinstance(changes, list) or len(changes)>200:
        raise ValueError('Fixture changes must be a list of at most 200 entries')
    seen = set()
    for entry in changes:
        identity = str(uuid.UUID(entry['shapeId']))
        if identity in seen or not isinstance(entry.get('characters'), str) or len(entry['characters'])>10000:
            raise ValueError('Duplicate target or invalid fixture text')
        seen.add(identity)
    scale = fixture.get('fontScale', 1)
    if isinstance(scale, bool) or not isinstance(scale, (float, int)) or not 0.5 <= scale <= 3:
        raise ValueError('fontScale must be between 0.5 and 3')
    return fixture


def write_json(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def compare(paths, output, overlay=False, allow_mismatch=False):
    from PIL import Image, ImageChops, ImageDraw
    captures = [json.loads(Path(p).read_text()) for p in paths]
    if len(captures)<2 or len(captures)>10:
        raise ValueError('Compare 2–10 capture manifests')
    signature = lambda m: (m['fixture'], m['theme'], m['captureConditions'])
    if not allow_mismatch and any(signature(c)!=signature(captures[0]) for c in captures[1:]):
        raise ValueError('Capture conditions differ; pass --allow-mismatch for exploratory contact sheets')
    images = []
    for manifest, path in zip(captures, paths):
        if not manifest.get('complete'):
            raise ValueError('Incomplete capture')
        for board in manifest['boards']:
            file = Path(path).resolve().parent/board['png']
            if hashlib.sha256(file.read_bytes()).hexdigest()!=board['sha256']:
                raise ValueError('Capture image changed')
            im = Image.open(file).convert('RGBA')
            images.append((im, board['name']))
    if len(images)>30 or any(im.width*im.height>12_000_000 for im,_ in images):
        raise ValueError('Comparison exceeds size limit')
    if overlay:
        if len(images)!=2 or images[0][0].size!=images[1][0].size:
            raise ValueError('Overlay requires exactly two equal-size boards')
        result = Image.blend(images[0][0], images[1][0], 0.5)
    else:
        widths = [im.width for im,_ in images]; heights=[im.height for im,_ in images]
        if not allow_mismatch and len(set(zip(widths, heights)))!=1:
            raise ValueError('Dimensions differ')
        if (sum(widths)+24*len(images))*(max(heights)+64)>60_000_000:
            raise ValueError('Contact sheet too large')
        result = Image.new('RGBA', (sum(widths)+24*len(images),max(heights)+64),'#182026')
        draw=ImageDraw.Draw(result);x=12
        for i,(im,label) in enumerate(images):
            draw.text((x,12),f'{i+1}: {label[:40]}',fill='white')
            result.alpha_composite(im,(x,44));x+=im.width+24
    with output.open('xb') as stream:
        result.save(stream,format='PNG')
    return {'output':str(output),'boards':len(images),'scale':'1:1',
        'note':'Comparison image only; no automatic assessment of visual quality'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest='action',required=True)
    for name in ('capture','lint','stress'):
        p=subs.add_parser(name)
        p.add_argument('--file',required=True,type=lambda s:str(uuid.UUID(s)))
        p.add_argument('--page',required=True,type=lambda s:str(uuid.UUID(s)))
        p.add_argument('--ids',required=True,nargs='+',type=lambda s:str(uuid.UUID(s)))
        p.add_argument('--out',required=True,type=Path)
        if name=='capture':
            p.add_argument('--fixture',required=True);p.add_argument('--theme',required=True)
            p.add_argument('--conditions',required=True,help='Browser/font/capture conditions, honestly stated')
        if name=='stress':
            p.add_argument('--fixture',required=True,type=Path)
            p.add_argument('--width',type=int);p.add_argument('--apply',action='store_true')
    p=subs.add_parser('compare');p.add_argument('manifests',nargs='+',type=Path)
    p.add_argument('--out',required=True,type=Path);p.add_argument('--overlay',action='store_true')
    p.add_argument('--allow-mismatch',action='store_true')
    args=parser.parse_args()
    if args.out.exists():raise ValueError('Output exists; choose a new output path')
    if not args.out.parent.is_dir():raise ValueError('Output parent must exist before starting the operation')
    if args.action=='compare':
        print(json.dumps(compare(args.manifests,args.out,args.overlay,args.allow_mismatch)));return
    if not 1<=len(args.ids)<=20 or len(set(args.ids))!=len(args.ids):raise ValueError('Choose 1–20 distinct targets')
    request={'action':'snapshot','fileId':args.file,'pageId':args.page,'ids':args.ids}
    if args.action=='stress':
        if args.width is not None and not 100<=args.width<=4096:raise ValueError('Width outside supported review range')
        request.update(action='stress',fixture=validate_fixture(json.loads(args.fixture.read_text())),
            apply=args.apply,width=args.width,runId=uuid.uuid4().hex[:10])
    client=connect();snapshot=execute(client,request)
    if args.action=='stress':write_json(args.out,snapshot)
    elif args.action=='lint':write_json(args.out,lint(snapshot))
    else:
        args.out.mkdir(parents=True,exist_ok=False)
        manifest={**snapshot,'fixture':args.fixture,'theme':args.theme,'captureConditions':args.conditions,
            'complete':False,'boards':[]}
        for board in snapshot['boards']:
            response=client.call('tools/call',{'name':'export_shape','arguments':{'shapeId':board['id'],'format':'png'}})
            value=response.get('result',{})
            if 'error' in response or value.get('isError'):raise ValueError('Export failed')
            block=next((b for b in value.get('content',[]) if b.get('type')=='image' and b.get('mimeType')=='image/png'),None)
            if not block:raise ValueError('No inline PNG returned; use supported native export and record limitation')
            data=base64.b64decode(block['data'],validate=True)
            if not data.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid PNG response')
            filename=board['id']+'.png';(args.out/filename).write_bytes(data)
            manifest['boards'].append({**board,'png':filename,'sha256':hashlib.sha256(data).hexdigest()})
        after=execute(client,request)
        if after['revision']!=snapshot['revision']:raise ValueError('Revision changed during capture; retry into a fresh directory')
        manifest['complete']=True;write_json(args.out/'capture.json',manifest)
    print(json.dumps({'action':args.action,'output':str(args.out),'verified_response':True}))


if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,FileNotFoundError) as error:
        print(json.dumps({'error':str(error)}),file=sys.stderr);sys.exit(1)
    except Exception as error:
        # Transport exceptions can contain credential-bearing URLs.
        print(json.dumps({'error_type':type(error).__name__,'detail':'Operation failed; check doctor and output state'}),file=sys.stderr);sys.exit(1)
