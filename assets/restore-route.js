'use strict';
// Preserve deep links from the temporary multi-page layout.
const restoredHome = document.getElementById('restored-home');
if (restoredHome) {
  const target = new URL(restoredHome.href);
  if (window.location.hash) target.hash = window.location.hash;
  window.location.replace(target.href);
}
