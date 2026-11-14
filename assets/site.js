'use strict';
const menu = document.querySelector('.menu-button');
const nav = document.getElementById('nav-links');
function closeMenu() { nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); }
menu.addEventListener('click', () => { const open = nav.classList.toggle('open'); menu.setAttribute('aria-expanded', String(open)); });
nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); menu.focus(); } });
const search = document.getElementById('search');
const kind = document.getElementById('kind');
if (search && kind) {
  const publications = [...document.querySelectorAll('#publications .publication')];
  const filter = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const publication of publications) {
      const visible = (kind.value === 'all' || publication.dataset.kind === kind.value) && publication.textContent.toLocaleLowerCase().includes(query);
      publication.hidden = !visible;
      if (visible) count++;
    }
    document.getElementById('result-count').textContent = `${count} ${count === 1 ? 'publication' : 'publications'}`;
    document.getElementById('empty-results').hidden = count !== 0;
  };
  search.addEventListener('input', filter);
  kind.addEventListener('change', filter);
}
document.getElementById('print-profile')?.addEventListener('click', () => window.print());

const careerDetails = [...document.querySelectorAll('[data-cv-details]')];
const expandDetails = document.getElementById('expand-details');
function syncDetailsButton() {
  if (!expandDetails) return;
  const allOpen = careerDetails.length > 0 && careerDetails.every(item => item.open);
  expandDetails.textContent = allOpen ? 'Collapse all details' : 'Expand all details';
  expandDetails.setAttribute('aria-pressed', String(allOpen));
}
expandDetails?.addEventListener('click', () => {
  const open = !careerDetails.every(item => item.open);
  careerDetails.forEach(item => { item.open = open; });
  syncDetailsButton();
});
careerDetails.forEach(item => item.addEventListener('toggle', syncDetailsButton));
function revealLinkedDetails() {
  let id;
  try { id = decodeURIComponent(window.location.hash.slice(1)); } catch { return; }
  if (!id) return;
  const target = document.getElementById(id);
  if (!target) return;
  const details = target.matches('[data-cv-details]') ? [target] : [...target.querySelectorAll('[data-cv-details]')];
  details.forEach(item => { item.open = true; });
  syncDetailsButton();
}
window.addEventListener('hashchange', revealLinkedDetails);
revealLinkedDetails();
let printDetailState = null;
window.addEventListener('beforeprint', () => {
  if (printDetailState !== null) return;
  printDetailState = careerDetails.map(item => item.open);
  careerDetails.forEach(item => { item.open = true; });
});
window.addEventListener('afterprint', () => {
  if (printDetailState === null) return;
  careerDetails.forEach((item, index) => { item.open = printDetailState[index]; });
  printDetailState = null;
  syncDetailsButton();
});

for (const button of document.querySelectorAll('[data-copy-pdf]')) {
  button.addEventListener('click', async () => {
    const input = document.getElementById(button.dataset.copyPdf);
    const status = document.getElementById(`${button.dataset.copyPdf}-status`);
    if (!input || !status) return;
    try {
      if (!window.navigator?.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await window.navigator.clipboard.writeText(input.value);
      status.textContent = 'PDF link copied.';
    } catch {
      input.focus();
      input.select();
      status.textContent = 'Link selected. Copy it using your browser or keyboard.';
    }
  });
}
