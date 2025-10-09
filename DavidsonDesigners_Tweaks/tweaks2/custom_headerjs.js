document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('nt-storeModal');
  const openBtn = document.getElementById('store-locator');
  if (!modal || !openBtn) { console.warn('Store Locator: modal or trigger not found'); return; }

  const closeBtn = modal.querySelector('.nt-store-close');
  const iframe = document.getElementById('nt-storeMap');
  let lastFocused = null;

  const focusableSelector = 'a[href], area[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), iframe, [tabindex]:not([tabindex="-1"])';
  function getFocusable(el) { return Array.from(el.querySelectorAll(focusableSelector)).filter(e => e.offsetParent !== null); }

  function openModal() {
    lastFocused = document.activeElement;
    // lazy-load the map once
    if (iframe && iframe.dataset && iframe.dataset.src && !iframe.src) {
      iframe.src = iframe.dataset.src;
    }
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    const focusable = getFocusable(modal);
    if (focusable.length) focusable[0].focus();
    document.addEventListener('keydown', onKeyDown, true);
    modal.addEventListener('click', onOutsideClick);
  }

  function closeModal() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    document.removeEventListener('keydown', onKeyDown, true);
    modal.removeEventListener('click', onOutsideClick);
    if (lastFocused) lastFocused.focus();
  }

  function onKeyDown(e) {
    if (e.key === 'Escape') { e.preventDefault(); closeModal(); return; }
    if (e.key === 'Tab') {
      const focusable = getFocusable(modal);
      if (focusable.length === 0) { e.preventDefault(); return; }
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  }

  function onOutsideClick(e) {
    if (e.target === modal) closeModal();
  }

  openBtn.addEventListener('click', function (ev) { ev.preventDefault(); openModal(); });
  closeBtn.addEventListener('click', function () { closeModal(); });

  // Safety: if user navigates back/forward ensure modal closed
  window.addEventListener('pagehide', function () { closeModal(); });
});
