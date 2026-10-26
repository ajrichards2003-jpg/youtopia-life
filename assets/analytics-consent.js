/* Netlify provides server-side analytics. No cookies, browser storage,
 * identifiers, tracking pixels or additional analytics requests are used here.
 * Carry only public campaign labels through the current navigation journey. */
(() => {
  'use strict';
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  const params = new URLSearchParams(location.search);
  const campaign = {};
  for (const key of keys) {
    const value = params.get(key) || '';
    // Public campaign tokens only; never copy free text, emails or arbitrary queries.
    if (/^[a-z0-9_-]{1,120}$/i.test(value)) campaign[key] = value;
  }
  function prepare() {
    for (const anchor of document.querySelectorAll('a[href]')) {
      const raw = anchor.getAttribute('href');
      if (!raw || raw.startsWith('#') || anchor.hasAttribute('download')) continue;
      let url;
      try { url = new URL(raw, location.href); } catch (_) { continue; }
      if (url.origin === location.origin &&
          !/^(\/api\/|\/.netlify\/|\/assets\/)/.test(url.pathname) &&
          !/\.[a-z0-9]+$/i.test(url.pathname.replace(/\.html$/i, ''))) {
        for (const key of keys) {
          if (campaign[key] && !url.searchParams.has(key)) url.searchParams.set(key, campaign[key]);
        }
        if (Object.keys(campaign).length) anchor.setAttribute('href', url.pathname + url.search + url.hash);
      }
      // Public placement labels in the existing Awin reporting account.
      if (url.hostname === 'www.awin1.com' && url.pathname === '/cread.php' &&
          url.searchParams.get('awinaffid') === '3106417' && !url.searchParams.has('clickref')) {
        const page = location.pathname.replace(/[^a-z0-9]+/gi, '_').replace(/^_|_$/g, '').toLowerCase() || 'home';
        const label = ('yl_' + (campaign.utm_term || campaign.utm_source || 'direct') + '_' + page).slice(0, 50);
        const destination = url.searchParams.get('ued');
        url.searchParams.delete('ued');
        url.searchParams.set('clickref', label);
        if (destination !== null) url.searchParams.set('ued', destination);
        anchor.setAttribute('href', url.href);
      }
    }
    for (const form of document.querySelectorAll('form[name="youtopia-weekly"], form[name="youtopia-contact"], form[name="first-collection-interest"], form[name="merch-interest"], form[name="wallpaper-signup"], form[name="youtopia-signup"]')) {
      for (const key of keys) {
        let input = form.elements.namedItem(key);
        if (!input && campaign[key]) {
          input = document.createElement('input');
          input.type = 'hidden'; input.name = key; form.appendChild(input);
        }
        if (input && campaign[key]) input.value = campaign[key];
      }
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', prepare, {once: true});
  else prepare();
})();
