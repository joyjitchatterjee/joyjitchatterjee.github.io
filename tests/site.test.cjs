const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
function element(textContent = '', kind) {
  const classes = new Set();
  return {textContent, dataset: {kind}, value: '', hidden: false, handlers: {}, attrs: {},
    classList: {toggle(c) { if (classes.has(c)) { classes.delete(c); return false; } classes.add(c); return true; }, remove(c) { classes.delete(c); }, contains(c) { return classes.has(c); }},
    addEventListener(type, fn) {this.handlers[type] = fn;},
    setAttribute(k, v) {this.attrs[k] = v;}, focus() {this.focused = true;}};
}
function setup() {
  const nodes = {'nav-links': element(), search: element(), kind: element(), 'result-count': element(), 'empty-results': element(), 'print-profile': element()};
  const menu = element(); const papers = [element('Wind knowledge graph', 'journal'), element('Graph agent', 'conference'), element('Delivery planning', 'conference')];
  nodes.kind.value = 'all';
  const document = {handlers: {}, querySelector: () => menu, getElementById: id => nodes[id], querySelectorAll: () => papers, addEventListener(type, fn) {this.handlers[type] = fn;}};
  const window = {print() {window.printed = true;}};
  vm.runInNewContext(fs.readFileSync('assets/site.js', 'utf8'), {document, window});
  return {nodes, menu, papers, document, window};
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
