'use strict';
// Progressive enhancement: every source and photograph remains a working link.
const mediaFilters = document.querySelector('.media-filters');
const mediaItems = [...document.querySelectorAll('[data-media-category]')];
if (mediaFilters && mediaItems.length) {
  const filters = [...mediaFilters.querySelectorAll('[data-media-filter]')];
  const count = document.getElementById('media-count');
  mediaFilters.hidden = false;
  if (count) count.hidden = false;
  function filterMedia(category) {
    let visible = 0;
    mediaItems.forEach(item => {
      item.hidden = category !== 'all' && item.dataset.mediaCategory !== category;
      if (!item.hidden) visible++;
    });
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.mediaFilter === category)));
    if (count) count.textContent = `${visible} ${visible === 1 ? 'feature' : 'features'}`;
  }
  filters.forEach(button => button.addEventListener('click', () => filterMedia(button.dataset.mediaFilter)));
  filterMedia('all');
}
const viewer = document.getElementById('media-viewer');
if (viewer && typeof viewer.showModal === 'function') {
  const content = document.getElementById('viewer-content');
  const title = document.getElementById('viewer-title');
  const caption = document.getElementById('viewer-caption');
  const original = document.getElementById('viewer-original');
  const close = document.getElementById('viewer-close');
  let opener = null;
  for (const link of document.querySelectorAll('[data-viewer]')) {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || (event.button !== undefined && event.button !== 0)) return;
      const kind = link.dataset.viewer;
      let node;
      if (kind === 'image') {
        node = document.createElement('img');
        node.src = link.href;
        node.alt = link.querySelector('img')?.alt || link.dataset.title;
      } else if (kind === 'youtube' && /^[A-Za-z0-9_-]{11}$/.test(link.dataset.videoId || '')) {
        node = document.createElement('iframe');
        node.src = `https://www.youtube-nocookie.com/embed/${link.dataset.videoId}?rel=0`;
        node.title = link.dataset.title;
        node.allow = 'encrypted-media; picture-in-picture; fullscreen';
        node.allowFullscreen = true;
        node.referrerPolicy = 'strict-origin-when-cross-origin';
      } else if (kind === 'video' && link.href.startsWith('https://www.greentalents.de/Video/')) {
        node = document.createElement('video');
        node.controls = true;
        node.preload = 'metadata';
        node.src = link.href;
        node.setAttribute('aria-label', link.dataset.title);
      } else return;
      event.preventDefault();
      opener = link;
      title.textContent = link.dataset.title;
      caption.textContent = link.dataset.caption;
      original.href = link.href;
      content.replaceChildren(node);
      viewer.showModal();
      close.focus();
    });
  }
  close.addEventListener('click', () => viewer.close());
  viewer.addEventListener('click', event => { if (event.target === viewer) viewer.close(); });
  viewer.addEventListener('close', () => {
    // Unmounting stops playback and releases any third-party iframe immediately.
    content.replaceChildren();
    opener?.focus();
  });
}
