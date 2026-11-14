/* Delegated cookieless analytics events. The PostHog token is not in this file;
   scripts/build-public.py injects the loader. Campaign values come from the
   sanitised labels in analytics-consent.js (window.youtopiaCampaign). */
(() => {
  'use strict';
  const UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  const FORMS = new Set([
    'youtopia-weekly',
    'youtopia-contact',
    'first-collection-interest',
    'merch-interest',
    'wallpaper-signup',
    'youtopia-signup',
  ]);
  // Affiliate destinations used on the site, including partner pages that are
  // not all published yet. awin1.com clicks use the ued merchant when present.
  const PARTNERS = [
    ['ultrahuman.com', 'ultrahuman'],
    ['otraeyewear.com', 'otra'],
    ['einstar.com', 'einstar'],
    ['apebornfitness.com', 'ape-born'],
    ['sinocare.com', 'sinocare'],
    ['aeternum.site', 'aeternum'],
    ['awin1.com', 'awin'],
  ];
  const played = new Set();

  function dntOn() {
    return navigator.doNotTrack === '1' || window.doNotTrack === '1' || navigator.msDoNotTrack === '1';
  }

  function pageSlug() {
    return location.pathname.replace(/[^a-z0-9]+/gi, '_').replace(/^_|_$/g, '').toLowerCase() || 'home';
  }

  function clip(value, max) {
    return String(value || '').replace(/\s+/g, ' ').trim().slice(0, max);
  }

  function utmProps() {
    const campaign = window.youtopiaCampaign || {};
    const props = {};
    for (const key of UTM_KEYS) {
      const value = campaign[key];
      if (typeof value === 'string' && /^[a-z0-9_-]{1,120}$/i.test(value)) props[key] = value;
    }
    return props;
  }

  function capture(name, props, beacon) {
    try {
      if (dntOn()) return;
      if (typeof window.youtopiaBootPosthog === 'function') window.youtopiaBootPosthog();
      const body = Object.assign({}, utmProps(), props);
      const opts = beacon ? {transport: 'sendBeacon'} : undefined;
      if (window.posthog && typeof window.posthog.capture === 'function') {
        window.posthog.capture(name, body, opts);
        return;
      }
      (window.__youtopiaEventQueue = window.__youtopiaEventQueue || []).push([name, body, opts]);
    } catch (_) {}
  }

  function posthogReady() {
    return !!(window.posthog && window.posthog.__loaded);
  }

  function partnerName(hostname) {
    const host = String(hostname || '').toLowerCase().replace(/^www\./, '');
    for (const [domain, name] of PARTNERS) {
      if (host === domain || host.endsWith('.' + domain)) return name;
    }
    return '';
  }

  function affiliateInfo(anchor) {
    let url;
    try { url = new URL(anchor.href, location.href); } catch (_) { return null; }
    if (url.origin === location.origin) return null;
    let destHost = url.hostname.toLowerCase();
    let partner = partnerName(destHost);
    if (destHost === 'www.awin1.com' || destHost === 'awin1.com') {
      const ued = url.searchParams.get('ued');
      if (ued) {
        try {
          const dest = new URL(ued);
          if (dest.hostname) {
            destHost = dest.hostname.toLowerCase();
            partner = partnerName(destHost) || partner;
          }
        } catch (_) {}
      }
    }
    if (!partner) return null;
    const clickref = url.searchParams.get('clickref') || '';
    return {
      partner,
      destination_host: destHost,
      clickref: /^[a-z0-9_-]{1,80}$/i.test(clickref) ? clickref : '',
    };
  }

  function labelOf(el) {
    return clip(el.getAttribute('data-cta-label') || el.getAttribute('aria-label') || el.innerText || el.textContent, 80);
  }

  function placementFor(el) {
    const placed = el.closest('[data-placement]');
    const section = el.closest('section[id], article[id], header[id], footer[id]');
    const bits = [pageSlug()];
    const explicit = placed && placed.getAttribute('data-placement');
    if (explicit) bits.push(clip(explicit, 60));
    else if (section && section.id) bits.push(section.id);
    const label = labelOf(el);
    if (label) bits.push(label);
    return bits.join(' / ').slice(0, 160);
  }

  function destinationOf(el) {
    const raw = el.getAttribute('href') || '';
    if (!raw) return '';
    try {
      const url = new URL(raw, location.href);
      if (url.protocol === 'mailto:' || url.protocol === 'tel:') return url.protocol.replace(':', '');
      if (url.origin === location.origin) return clip(url.pathname + url.hash, 180);
      return clip(url.host + url.pathname, 180);
    } catch (_) {
      return clip(raw, 180);
    }
  }

  function isCta(el) {
    if (el.hasAttribute('data-cta')) return true;
    const c = el.classList;
    if (c.contains('btn') && c.contains('primary')) return true;
    if (c.contains('pe-button')) return true;
    if (c.contains('oe-button') && !c.contains('oe-outline')) return true;
    if (c.contains('ei-btn') && !c.contains('alt')) return true;
    return false;
  }

  function sameTab(event, anchor) {
    if (event.defaultPrevented || event.button !== 0) return false;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return false;
    if (anchor.target && anchor.target !== '_self') return false;
    const href = anchor.getAttribute('href') || '';
    return !!href && !href.startsWith('#');
  }

  function videoIdFromSrc(src) {
    try {
      const url = new URL(src, location.href);
      const embed = url.pathname.match(/\/embed\/([^/?#]+)/);
      if (embed) return decodeURIComponent(embed[1]).slice(0, 120);
      const base = decodeURIComponent(url.pathname.split('/').pop() || '');
      return base.split('?')[0].slice(0, 120);
    } catch (_) {
      return clip(String(src).split('/').pop(), 120);
    }
  }

  function videoPlay(id) {
    const video = clip(id, 120);
    if (!video || played.has(video)) return;
    played.add(video);
    capture('video_play', {video, page: pageSlug()}, true);
  }

  document.addEventListener('click', event => {
    const cta = event.target instanceof Element ? event.target.closest('a, button') : null;
    if (cta && isCta(cta)) {
      capture('cta_click', {
        cta: labelOf(cta) || 'cta',
        destination: destinationOf(cta),
        page: pageSlug(),
      }, true);
    }
    const anchor = event.target instanceof Element ? event.target.closest('a[href]') : null;
    if (!anchor) return;
    const info = affiliateInfo(anchor);
    if (!info) return;
    const props = {
      partner: info.partner,
      placement: placementFor(anchor),
      destination_host: info.destination_host,
    };
    if (info.clickref) props.clickref = info.clickref;
    if (sameTab(event, anchor) && !posthogReady()) {
      event.preventDefault();
      const href = anchor.href;
      let tries = 0;
      const timer = window.setInterval(() => {
        tries += 1;
        if (posthogReady() || tries > 30) {
          window.clearInterval(timer);
          capture('affiliate_click', props, true);
          window.setTimeout(() => { location.assign(href); }, 40);
        }
      }, 50);
      return;
    }
    capture('affiliate_click', props, true);
  }, true);

  document.addEventListener('submit', event => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    const formName = form.getAttribute('name') || '';
    if (!form.hasAttribute('data-netlify') && !FORMS.has(formName)) return;
    capture('form_submit', {form_name: formName || 'netlify-form', page: pageSlug()}, true);
  }, true);

  document.addEventListener('play', event => {
    const video = event.target;
    if (!(video instanceof HTMLVideoElement)) return;
    const source = video.currentSrc || (video.querySelector('source') || {}).src || video.getAttribute('src') || '';
    videoPlay(videoIdFromSrc(source) || 'video');
  }, true);

  document.addEventListener('click', event => {
    const trigger = event.target instanceof Element
      ? event.target.closest('[data-video], [data-intro-video]')
      : null;
    if (!trigger) return;
    videoPlay(trigger.getAttribute('data-video') || trigger.getAttribute('data-intro-video'));
  }, true);

  window.addEventListener('message', event => {
    if (event.origin !== 'https://www.youtube-nocookie.com' && event.origin !== 'https://www.youtube.com') return;
    let data = event.data;
    if (typeof data === 'string') {
      try { data = JSON.parse(data); } catch (_) { return; }
    }
    if (!data || typeof data !== 'object') return;
    const state = data.info && typeof data.info === 'object' ? data.info.playerState : data.info;
    const playing = (data.event === 'onStateChange' || data.event === 'infoDelivery') && state === 1;
    if (!playing) return;
    const frame = Array.from(document.querySelectorAll('iframe')).find(node => node.contentWindow === event.source);
    const src = frame ? (frame.getAttribute('src') || '') : '';
    videoPlay(videoIdFromSrc(src) || 'youtube');
  });
})();
