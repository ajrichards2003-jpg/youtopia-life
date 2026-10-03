/* Youtopia Life: load Google Analytics only after an affirmative choice. */
(() => {
  'use strict';
  const key = 'youtopia-analytics-choice-v1';
  const measurementId = 'G-0W7LG09JBP';
  const style = document.createElement('style');
  style.textContent = '.privacy-choice{position:fixed;right:16px;bottom:16px;z-index:9999;max-width:min(440px,calc(100vw - 32px));padding:18px 20px;border:1px solid #ac9167;border-radius:16px;background:#09221df5;color:#f7f1e6;box-shadow:0 16px 60px #0009;font:15px/1.5 system-ui,sans-serif}.privacy-choice h2{font-size:1.1rem;margin:0 0 7px}.privacy-choice p{margin:0 0 14px}.privacy-choice a{color:#efd19a}.privacy-choice-actions{display:flex;flex-wrap:wrap;gap:8px}.privacy-choice button,.privacy-reopen{border:1px solid #b59a6b;border-radius:8px;padding:9px 13px;background:#e4c98c;color:#10221c;font:700 14px system-ui;cursor:pointer}.privacy-choice button.secondary{background:transparent;color:#f7f1e6}.privacy-reopen{position:fixed;right:16px;bottom:16px;z-index:9998;padding:7px 10px;background:#10271ee8;color:#f7f1e6;font-size:12px}@media(max-width:650px){.privacy-choice{left:12px;right:12px;bottom:12px;max-width:none}.privacy-reopen{right:12px;bottom:12px}}';
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
    if (affiliate) window.gtag('event', 'supplier_click', { supplier: url.hostname.includes('iherb') ? 'iherb' : 'ultrahuman', link_url: url.href, link_text: link.textContent.trim().slice(0,100), transport_type: 'beacon' });
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
      document.body.append(reopen);
      return;
    }
    panel = document.createElement('aside');
    panel.className = 'privacy-choice';
    panel.setAttribute('aria-label', 'Optional analytics choice');
    panel.innerHTML = '<h2>Your privacy choice</h2><p>May we use Google Analytics to understand which Youtopia pages are useful? It is optional. The site works without it. <a href="/privacy/">Read our privacy notice</a>.</p><div class="privacy-choice-actions"><button type="button" data-choice="yes">Allow analytics</button><button type="button" class="secondary" data-choice="no">No thanks</button></div>';
    panel.querySelector('[data-choice="yes"]').addEventListener('click', () => save('yes'));
    panel.querySelector('[data-choice="no"]').addEventListener('click', () => save('no'));
    document.body.append(panel);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => { if (choice === 'yes') loadAnalytics(); render(); }, { once: true });
  else { if (choice === 'yes') loadAnalytics(); render(); }
})();
