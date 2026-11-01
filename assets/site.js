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
