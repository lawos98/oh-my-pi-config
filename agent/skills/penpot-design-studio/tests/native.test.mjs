import assert from 'node:assert/strict';
import fs from 'node:fs';
const source=fs.readFileSync(new URL('../scripts/review_native.js',import.meta.url),'utf8');
const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
let checkpoints=0,blocks=0,finished=0;
function shape(id,type='board') {
  return {id,type,name:id,x:0,y:0,width:390,height:844,bounds:{x:0,y:0,width:390,height:844},
    children:[],tokens:{},fills:[],isComponentInstance:()=>false,isComponentMainInstance:()=>false,
    setPluginData(){},resize(w,h){this.width=w;this.height=h;},remove(){this.parent.children=this.parent.children.filter(s=>s!==this);}};
}
const root=shape('root'),board=shape('board'),text=shape('text','text');
root.children=[board];board.parent=root;board.children=[text];text.parent=board;text.characters='Original';text.fontSize='16';
board.clone=()=>{const copy=shape('copy');copy.parent=root;const clonedText=shape('copy-text','text');
  clonedText.parent=copy;clonedText.characters=text.characters;clonedText.fontSize=text.fontSize;copy.children=[clonedText];root.children.push(copy);return copy;};
const file={id:'file',revn:2,saveVersion:async()=>{checkpoints++;return {id:'checkpoint'};}};
const page={id:'page',root,getShapeById:id=>root.children.find(s=>s.id===id)};
const penpot={currentFile:file,currentPage:page,fonts:{findById:()=>null},
  history:{undoBlockBegin(){blocks++;return Symbol();},undoBlockFinish(){finished++;}}};
const request={action:'stress',fileId:'file',pageId:'page',ids:['board'],runId:'test',fixture:{name:'long-v1',changes:[{shapeId:'text',characters:'A much longer fictional value'}],fontScale:2}};
async function run(req){const fn=new AsyncFunction('penpot',source.replace('__REQUEST_JSON__',JSON.stringify(req)));return fn(penpot);}
await assert.rejects(run({...request,fileId:'wrong'}));assert.equal(checkpoints,0);
await assert.rejects(run({...request,fixture:{name:'bad',changes:[{shapeId:'outside',characters:'bad'}]}}));assert.equal(checkpoints,0);
text.isComponentMainInstance=()=>true;
await assert.rejects(run({...request,apply:true}));assert.equal(checkpoints,0);assert.equal(root.children.length,1);
text.isComponentMainInstance=()=>false;
await run(request);assert.equal(root.children.length,1);assert.equal(checkpoints,0);
const response=await run({...request,apply:true,width:320});
assert.ok(response.includes('copy'));assert.equal(root.children.length,2);assert.equal(board.width,390);
assert.equal(text.characters,'Original');assert.equal(root.children[1].children[0].characters,'A much longer fictional value');
assert.equal(root.children[1].children[0].fontSize,'32');assert.equal(root.children[1].width,320);
assert.equal(checkpoints,1);assert.equal(blocks,finished);
const snapshot=await run({action:'snapshot',fileId:'file',pageId:'page',ids:['board']});
assert.ok(snapshot.includes('Original'));
console.log('PASS: target guard, fixture scope, dry run, checkpoint, copy-only mutation, layout probe and undo grouping.');
