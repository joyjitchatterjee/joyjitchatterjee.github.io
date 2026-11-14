const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
function redirect(hash) {
  let result;
  vm.runInNewContext(fs.readFileSync('assets/restore-route.js','utf8'), {
    URL, document: {getElementById: () => ({href:'https://joyjitchatterjee.github.io/index.html#work'})},
    window: {location: {hash, replace: url => result=url}}
  });
  return result;
}
test('temporary topic URLs return to the restored homepage and preserve deep links', () => {
  assert.equal(redirect(''),'https://joyjitchatterjee.github.io/index.html#work');
  assert.equal(redirect('#procurement-ai'),'https://joyjitchatterjee.github.io/index.html#procurement-ai');
  assert.equal(redirect('#https://example.com'),'https://joyjitchatterjee.github.io/index.html#https://example.com');
});
