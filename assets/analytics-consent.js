/* Youtopia Life: load Google Analytics only after an affirmative choice. */
(() => {
  'use strict';
  const key = 'youtopia-analytics-choice-v1';
  const measurementId = 'G-0W7LG09JBP';
  const style = document.createElement('style');
  style.textContent = `.privacy-choice{position:fixed;left:16px;right:16px;bottom:max(12px,env(safe-area-inset-bottom));z-index:2147483647;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:6px 12px;border:1px solid #42665d;border-radius:12px;background:#082019f5;color:#f7f1e6;box-shadow:0 6px 24px #0005;font:12px/1.4 system-ui,sans-serif}.privacy-choice p{margin:0;max-width:780px}.privacy-choice a{color:#a7ead4;text-underline-offset:3px}.privacy-choice-actions{display:flex;gap:8px;flex-shrink:0}.privacy-choice button,.privacy-reopen{border:1px solid #719c8f;border-radius:7px;padding:10px 16px;min-height:44px;background:#153c30;color:#f7f1e6;font:600 13px system-ui;cursor:pointer}.privacy-choice button:hover{background:#205542}.privacy-choice button:focus-visible,.privacy-choice a:focus-visible,.privacy-reopen:focus-visible{outline:2px solid #66dfb9;outline-offset:3px}.privacy-reopen{position:static;display:inline-flex;margin:12px 0;padding:7px 10px;min-height:36px;background:#10271ee8;font-size:12px}@media(max-width:650px){.privacy-choice{left:8px;right:8px;gap:8px;padding:5px 8px;font-size:11px;line-height:1.35}.privacy-choice p{flex:1;min-width:0}.privacy-choice-actions{margin-left:auto}.privacy-choice button{padding:8px 10px;font-size:12px}.privacy-reopen{left:12px;right:auto}}`;
  document.head.append(style);

  let choice;
  try { choice = localStorage.getItem(key); } catch (_) { choice = null; }
  let loaded = false;
  function loadAnalytics() {
    window['ga-disable-' + measurementId] = false;
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', measurementId, { allow_google_signals: false, allow_ad_personalization_signals: false });
    const tag = document.createElement('script');
    tag.async = true;
    tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
    document.head.append(tag);
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (choice !== 'yes' || !loaded || !link || typeof window.gtag !== 'function') return;
    let url; try { url = new URL(link.href); } catch (_) { return; }
    const affiliate = /(^|\.)(awin1\.com|iherb\.com|ultrahuman\.com)$/.test(url.hostname);
    if (affiliate) {
      const merchant = url.searchParams.get('awinmid');
      const supplier = url.hostname.includes('iherb') || merchant === '76736' ? 'iherb' : url.hostname.includes('ultrahuman') || merchant === '69428' ? 'ultrahuman' : 'other';
      window.gtag('event', 'supplier_click', { supplier, link_url: url.href, link_text: link.textContent.trim().slice(0,100), transport_type: 'beacon' });
    } else if (url.origin === location.origin) {
      window.gtag('event', 'site_navigation_click', { link_path: url.pathname + url.hash, link_text: link.textContent.trim().slice(0,100), transport_type: 'beacon' });
    }
  });

  function save(value) {
    try { localStorage.setItem(key, value); } catch (_) { /* Session choice still applies. */ }
    choice = value;
    if (value === 'yes') loadAnalytics();
    if (value === 'no' && loaded) {
      window['ga-disable-' + measurementId] = true;
      // A prior session's data cannot be retracted from here; stop future hits.
    }
    render();
  }

  let panel, reopen;
  function render(open = false) {
    if (panel) panel.remove();
    if (reopen) reopen.remove();
    if (choice && !open) {
      reopen = document.createElement('button');
      reopen.className = 'privacy-reopen';
      reopen.type = 'button';
      reopen.textContent = 'Privacy choices';
      reopen.addEventListener('click', () => render(true));
      const footer = document.querySelector('footer') || document.querySelector('.hosting-credit') || document.body; footer.append(reopen);
      return;
    }
    panel = document.createElement('aside');
    panel.className = 'privacy-choice';
    panel.setAttribute('aria-label', 'Optional analytics choice');
    panel.innerHTML = '<p>Optional Google Analytics measures visits. <a href="/privacy/">Privacy</a>.</p><div class="privacy-choice-actions"><button type="button" data-choice="yes">Accept</button><button type="button" class="secondary" data-choice="no">Decline</button></div>';
    panel.querySelector('[data-choice="yes"]').addEventListener('click', () => save('yes'));
    panel.querySelector('[data-choice="no"]').addEventListener('click', () => save('no'));
    document.body.append(panel);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => { if (choice === 'yes') loadAnalytics(); render(); }, { once: true });
  else { if (choice === 'yes') loadAnalytics(); render(); }
})();
