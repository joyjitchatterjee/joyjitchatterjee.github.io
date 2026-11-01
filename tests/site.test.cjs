const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
function element(textContent = '', kind) {
  const classes = new Set();
  return {textContent, dataset: {kind}, value: '', hidden: false, open: false, handlers: {}, attrs: {}, children: [],
    matches(selector) {return selector === '[data-cv-details]' && kind === 'details';},
    querySelectorAll(selector) {return selector === '[data-cv-details]' ? this.children : [];},
    classList: {toggle(c) { if (classes.has(c)) { classes.delete(c); return false; } classes.add(c); return true; }, remove(c) { classes.delete(c); }, contains(c) { return classes.has(c); }},
    addEventListener(type, fn) {this.handlers[type] = fn;},
    setAttribute(k, v) {this.attrs[k] = v;}, focus() {this.focused = true;}};
}
function setup(hash = '') {
  const nodes = {'nav-links': element(), search: element(), kind: element(), 'result-count': element(), 'empty-results': element(), 'print-profile': element(), 'expand-details': element(), 'experience-lead-data-scientist': element()};
  const details = [element('', 'details'), element('', 'details')];
  nodes['experience-lead-data-scientist'].children = [details[0]];
  const menu = element(); const papers = [element('Wind knowledge graph', 'journal'), element('Graph agent', 'conference'), element('Delivery planning', 'conference')];
  nodes.kind.value = 'all';
  const document = {handlers: {}, querySelector: () => menu, getElementById: id => nodes[id], querySelectorAll: selector => selector === '[data-cv-details]' ? details : papers, addEventListener(type, fn) {this.handlers[type] = fn;}};
  const window = {location: {hash}, handlers: {}, addEventListener(type, fn) {this.handlers[type] = fn;}, print() {window.printed = true;}};
  vm.runInNewContext(fs.readFileSync('assets/site.js', 'utf8'), {document, window});
  return {nodes, menu, papers, document, window, details};
}
test('search and type filter compose; zero results are announced', () => {
  const {nodes, papers} = setup(); nodes.search.value = 'graph'; nodes.search.handlers.input();
  assert.equal(papers.filter(p => !p.hidden).length, 2);
  nodes.kind.value = 'conference'; nodes.kind.handlers.change();
  assert.equal(papers.filter(p => !p.hidden).length, 1);
  nodes.search.value = 'no matches'; nodes.search.handlers.input();
  assert.equal(nodes['result-count'].textContent, '0 publications'); assert.equal(nodes['empty-results'].hidden, false);
  nodes.search.value = ''; nodes.kind.value = 'all'; nodes.kind.handlers.change();
  assert.equal(papers.filter(p => !p.hidden).length, 3);
});
test('menu state and Escape restore keyboard focus', () => {
  const {nodes, menu, document} = setup(); menu.handlers.click();
  assert.equal(menu.attrs['aria-expanded'], 'true');
  document.handlers.keydown({key: 'Escape'});
  assert.equal(menu.attrs['aria-expanded'], 'false'); assert.equal(menu.focused, true);
  assert.equal(nodes['nav-links'].classList.contains('open'), false);
});
test('print profile triggers browser print', () => {const {nodes, window} = setup(); nodes['print-profile'].handlers.click(); assert.equal(window.printed, true);});

test('expand and collapse all details keeps the control state accurate', () => {
  const {nodes, details} = setup();
  nodes['expand-details'].handlers.click();
  assert.ok(details.every(item => item.open));
  assert.equal(nodes['expand-details'].attrs['aria-pressed'], 'true');
  details[0].open = false; details[0].handlers.toggle();
  assert.equal(nodes['expand-details'].textContent, 'Expand all details');
  nodes['expand-details'].handlers.click();
  nodes['expand-details'].handlers.click();
  assert.ok(details.every(item => !item.open));
});
test('career deep links open the relevant detail without opening unrelated entries', () => {
  const {details, window} = setup('#experience-lead-data-scientist');
  assert.equal(details[0].open, true); assert.equal(details[1].open, false);
  details[0].open = false;
  window.handlers.hashchange();
  assert.equal(details[0].open, true);
  window.location.hash = '#%invalid';
  assert.doesNotThrow(() => window.handlers.hashchange());
});
test('printing includes all detail and restores the reading state afterwards', () => {
  const {details, window} = setup();
  details[1].open = true;
  window.handlers.beforeprint();
  assert.ok(details.every(item => item.open));
  window.handlers.beforeprint();
  window.handlers.afterprint();
  assert.equal(details[0].open, false); assert.equal(details[1].open, true);
});
