// Executed only through the local Penpot MCP bridge. Targets are explicit.
const request = __REQUEST_JSON__;
const file = penpot.currentFile, page = penpot.currentPage;
if (!file || !page) throw new Error('No active file/page');
if (file.id !== request.fileId || page.id !== request.pageId) throw new Error('Active target changed');
const roots = request.ids.map(id => page.getShapeById(id));
if (roots.some(s => !s || s.id === page.root.id)) throw new Error('Missing or invalid target');
function walk(s, rows = [], visible = true) {
  visible = visible && !s.hidden;
  rows.push({shape: s, visible});
  for (const child of s.children || []) walk(child, rows, visible);
  return rows;
}
function snapshot(root) {
  const rows = walk(root);
  if (rows.length > 5000) throw new Error('Target exceeds 5000 shapes');
  return {id: root.id, name: root.name, bounds: root.bounds, shapes: rows.map(({shape: s, visible}) => {
    const item = {id: s.id, name: s.name, type: s.type, parentId: s.parent?.id,
      bounds: s.bounds, rotation: s.rotation, visible, tokens: s.tokens || {},
      instance: s.isComponentInstance(), mainInstance: s.isComponentMainInstance(),
      fills: Array.isArray(s.fills) ? s.fills.map(f => ({color: f.fillColor, opacity: f.fillOpacity,
        reference: f.fillColorRefId || null, image: !!f.fillImage})) : [],
      componentId: s.isComponentInstance() ? (s.component()?.id || null) : null};
    if (s.type === 'text') Object.assign(item, {characters: s.characters, fontId: s.fontId,
      fontFamily: s.fontFamily, fontSize: s.fontSize, growType: s.growType, textBounds: s.textBounds,
      fontAvailable: !s.fontId || s.fontId === 'mixed' ? null : !!penpot.fonts.findById(s.fontId)});
    return item;
  })};
}
let result;
if (request.action === 'snapshot') {
  result = {schema: 1, fileId: file.id, pageId: page.id, revision: file.revn,
    capturedAt: new Date().toISOString(), boards: roots.map(snapshot)};
} else if (request.action === 'stress') {
  if (roots.length !== 1) throw new Error('Stress requires one board');
  const source = roots[0];
  if (source.type !== 'board' || source.parent?.id !== page.root.id || source.isComponentMainInstance())
    throw new Error('Stress requires a top-level board that is not a main component');
  const original = walk(source), byId = new Map(original.map(x => [x.shape.id, x.shape]));
  if (original.some(({shape}) => shape.isComponentMainInstance()))
    throw new Error('Stress cannot copy a board containing main components');
  for (const change of request.fixture.changes) {
    if (byId.get(change.shapeId)?.type !== 'text') throw new Error('Fixture target must be text inside source board');
  }
  if (!request.apply) {
    result = {dryRun: true, sourceId: source.id, changes: request.fixture.changes.length,
      width: request.width || source.width, fixture: request.fixture.name};
  } else {
    const version = await file.saveVersion('Before OMP content stress ' + request.runId);
    const block = penpot.history.undoBlockBegin();
    let copy;
    try {
      copy = source.clone();
      copy.name = '[STRESS ' + request.runId + '] ' + request.fixture.name;
      copy.setPluginData('omp-review-stress', request.runId);
      const clones = walk(copy);
      if (clones.length !== original.length) throw new Error('Clone structure mismatch');
      const mapping = new Map(original.map((entry, i) => [entry.shape.id, clones[i].shape]));
      for (let i = 0; i < original.length; i++) {
        if (original[i].shape.type !== clones[i].shape.type) throw new Error('Clone type mismatch');
      }
      copy.x = Math.max(...page.root.children.filter(s => s.id !== copy.id).map(s => s.x + s.width), source.x + source.width) + 120;
      copy.y = source.y;
      if (request.width) copy.resize(request.width, source.height);
      for (const change of request.fixture.changes) mapping.get(change.shapeId).characters = change.characters;
      if (request.fixture.fontScale) for (const {shape} of clones) {
        if (shape.type === 'text' && Number.isFinite(Number(shape.fontSize)))
          shape.fontSize = String(Number(shape.fontSize) * request.fixture.fontScale);
      }
      result = {sourceId: source.id, copyId: copy.id, name: copy.name, fileId: file.id,
        pageId: page.id, checkpointId: version.id, fixture: request.fixture.name,
        note: 'Copy created. Capture and inspect after layout settles; no usability result implied.'};
    } catch (error) {
      if (copy) copy.remove();
      throw error;
    } finally { penpot.history.undoBlockFinish(block); }
  }
} else throw new Error('Unknown operation');
return 'OMP_REVIEW_V1 ' + JSON.stringify(result);
