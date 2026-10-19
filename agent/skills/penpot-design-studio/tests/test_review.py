import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from PIL import Image

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review

class ReviewChecks(unittest.TestCase):
    def test_bridge_requires_positive_result(self):
        for text in ('Tool execution failed: frozen', 'No active file', 'OMP_REVIEW_V1 null'):
            with self.assertRaises(ValueError):review.result_json({'result':{'content':[{'type':'text','text':text}]}})
        for text in ('OMP_REVIEW_V1 {"fileId":"f"}',json.dumps('OMP_REVIEW_V1 {"fileId":"f"}')):
            self.assertEqual(review.result_json({'result':{'content':[{'type':'text','text':text}]}}),{'fileId':'f'})

    def test_explicit_error_is_not_success(self):
        with self.assertRaises(ValueError):review.result_json({'result':{'isError':True,'content':[{'type':'text','text':'OMP_REVIEW_V1 {}'}]}})

    def test_fixture_rejects_duplicate_targets_and_bad_scale(self):
        change={'shapeId':'11111111-1111-1111-1111-111111111111','characters':'Fictional long name'}
        valid={'name':'long-v1','changes':[change],'fontScale':2}
        self.assertEqual(review.validate_fixture(valid),valid)
        for value in ({**valid,'changes':[change,change]},{**valid,'fontScale':4},{**valid,'fontScale':True}):
            with self.assertRaises(ValueError):review.validate_fixture(value)

    def test_lint_uses_geometry_visibility_and_font_evidence(self):
        shape={'id':'t','type':'text','visible':True,'bounds':{'x':0,'y':0,'width':50,'height':20},
            'textBounds':{'x':0,'y':0,'width':90,'height':20},'fontAvailable':False}
        data={'fileId':'f','pageId':'p','revision':1,'boards':[{'id':'b','bounds':{'x':0,'y':0,'width':390,'height':844},'shapes':[shape]}]}
        self.assertEqual({x['code'] for x in review.lint(data)['findings']},{'font-unavailable','text-overflow'})
        shape['visible']=False
        self.assertEqual(review.lint(data)['findings'],[])

    def test_compare_preserves_baselines_and_rejects_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);manifests=[]
            for i,color in enumerate(('red','blue')):
                image=root/f'{i}.png';Image.new('RGBA',(40,80),color).save(image)
                manifest={'fixture':'v1','theme':'dark','captureConditions':'test','complete':True,
                    'boards':[{'name':str(i),'png':image.name,'sha256':hashlib.sha256(image.read_bytes()).hexdigest()}]}
                path=root/f'{i}.json';path.write_text(json.dumps(manifest));manifests.append(path)
            review.compare(manifests,root/'comparison.png')
            with Image.open(root/'comparison.png') as comparison:
                self.assertEqual(comparison.size,(128,144))
            with self.assertRaises(FileExistsError):review.compare(manifests,root/'comparison.png')
            changed=json.loads(manifests[1].read_text());changed['theme']='light';manifests[1].write_text(json.dumps(changed))
            with self.assertRaises(ValueError):review.compare(manifests,root/'wrong.png')
            Image.new('RGBA',(40,80),'green').save(root/'0.png')
            with self.assertRaises(ValueError):review.compare(manifests,root/'tampered.png',allow_mismatch=True)

if __name__=='__main__':unittest.main()
