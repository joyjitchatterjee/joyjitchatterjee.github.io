const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
function node(dataset={}) {
  return {dataset, hidden:false, handlers:{},attrs:{},children:[],textContent:'',
    addEventListener(name,fn){this.handlers[name]=fn;},setAttribute(name,value){this.attrs[name]=value;},
    replaceChildren(...children){this.children=children;},focus(){this.focused=true;},querySelector(){return null;}};
}
function setup({dialog=true}={}) {
  const buttons=['all','watch','read','recognition'].map(mediaFilter=>node({mediaFilter}));
  const cards=['watch','read','watch','recognition'].map(mediaCategory=>node({mediaCategory}));
  const filters=node();filters.hidden=true;filters.querySelectorAll=()=>buttons;
  const viewer=node();viewer.showModal=dialog?()=>{viewer.open=true;}:undefined;
  viewer.close=()=>{viewer.open=false;viewer.handlers.close();};
  const nodes={'media-count':node(),'media-viewer':viewer,'viewer-content':node(),'viewer-title':node(),'viewer-caption':node(),'viewer-original':node(),'viewer-close':node()};
  const links=[node({viewer:'youtube',videoId:'FXgvSQKDZzs',title:'Podcast',caption:'Conversation'}),node({viewer:'image',title:'Lecture',caption:'Loughborough'}),node({viewer:'video',title:'Film',caption:'Research'})];
  links[0].href='https://www.youtube.com/watch?v=FXgvSQKDZzs';links[1].href='https://joyjitchatterjee.github.io/assets/images/lecture-loughborough.jpg';links[2].href='https://www.greentalents.de/Video/Awardees%202021%20Videos/CHATTERJEE%20Joyjit.mp4';
  const created=[];
  const document={querySelector:()=>filters,querySelectorAll:s=>s==='[data-media-category]'?cards:links,getElementById:id=>nodes[id],createElement:tag=>{const n=node();n.tag=tag;created.push(n);return n;}};
  vm.runInNewContext(fs.readFileSync('assets/experience.js','utf8'),{document});
  return {buttons,cards,filters,nodes,links,created,viewer};
}
function click(target,extra={}){let prevented=false;target.handlers.click({button:0,preventDefault(){prevented=true;},...extra});return prevented;}
test('media categories filter cards, announce count and restore all features',()=>{
  const s=setup();assert.equal(s.filters.hidden,false);assert.equal(s.nodes['media-count'].textContent,'4 features');
  click(s.buttons[1]);assert.deepEqual(s.cards.map(c=>c.hidden),[false,true,false,true]);assert.equal(s.buttons[1].attrs['aria-pressed'],'true');assert.equal(s.nodes['media-count'].textContent,'2 features');
  click(s.buttons[3]);assert.equal(s.nodes['media-count'].textContent,'1 feature');
  click(s.buttons[0]);assert.ok(s.cards.every(c=>!c.hidden));assert.equal(s.buttons[1].attrs['aria-pressed'],'false');
});
test('video loads only after activation, uses privacy-enhanced host and unloads on close',()=>{
  const s=setup();assert.equal(s.created.length,0);assert.equal(click(s.links[0]),true);
  const iframe=s.nodes['viewer-content'].children[0];assert.equal(iframe.tag,'iframe');assert.match(iframe.src,/^https:\/\/www.youtube-nocookie.com\/embed\/FXgvSQKDZzs/);assert.ok(!iframe.src.includes('autoplay'));
  assert.equal(s.nodes['viewer-close'].focused,true);click(s.nodes['viewer-close']);assert.equal(s.nodes['viewer-content'].children.length,0);assert.equal(s.links[0].focused,true);assert.equal(s.viewer.open,false);
});
test('photographs and research films keep captions and original links',()=>{
  const s=setup();click(s.links[1]);assert.equal(s.nodes['viewer-content'].children[0].alt,'Lecture');assert.equal(s.nodes['viewer-caption'].textContent,'Loughborough');assert.equal(s.nodes['viewer-original'].href,s.links[1].href);
  click(s.nodes['viewer-close']);click(s.links[2]);assert.equal(s.nodes['viewer-content'].children[0].tag,'video');assert.equal(s.nodes['viewer-content'].children[0].controls,true);
});
test('new-tab gestures, unsupported dialogs and invalid embed IDs preserve normal navigation',()=>{
  const s=setup();assert.equal(click(s.links[0],{metaKey:true}),false);assert.equal(s.created.length,0);
  s.links[0].dataset.videoId='invalid/iframe';assert.equal(click(s.links[0]),false);assert.equal(s.created.length,0);
  const fallback=setup({dialog:false});assert.equal(fallback.links[0].handlers.click,undefined);
});
