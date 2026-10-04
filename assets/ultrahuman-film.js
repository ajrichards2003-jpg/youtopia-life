/* Preview: reveal the official film only after the player confirms playback. */
(() => {
  'use strict';
  const host = document.querySelector('.ultra-intro');
  const panel = document.querySelector('.ultra-film');
  if (!host || !panel) return;
  const screen = panel.querySelector('.ultra-film-screen');
  const play = panel.querySelector('[data-film-play]');
  const sound = panel.querySelector('[data-film-sound]');
  const skip = panel.querySelector('[data-film-skip]');
  const replay = host.querySelector('.intro-replay');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let frame, timer, muted = true, started = false;
  const command = (func, args = []) => frame?.contentWindow?.postMessage(JSON.stringify({event:'command', func, args}), 'https://www.youtube-nocookie.com');
  const track = action => {
    try {
      if (typeof window.gtag === 'function' && localStorage.getItem('youtopia-analytics-choice-v1') === 'yes') {
        window.gtag('event', 'intro_video_' + action, {video_title:'Ultrahuman Ring AIR official film', video_provider:'youtube'});
      }
    } catch (_) {}
  };
  function finish(action = 'complete') {
    clearTimeout(timer);
    command('pauseVideo');
    host.classList.remove('film-open', 'film-playing');
    panel.hidden = true;
    panel.inert = true;
    panel.setAttribute('aria-hidden', 'true');
    frame?.remove();
    frame = null;
    host.querySelectorAll('.intro-slide').forEach(el => el.setAttribute('aria-hidden', String(!el.classList.contains('active'))));
    host.dispatchEvent(new Event('ultra-film-ended'));
    if (started) track(action);
    started = false;
  }
  function reveal() {
    if (started || document.hidden) return;
    started = true;
    clearTimeout(timer);
    panel.inert = false;
    panel.setAttribute('aria-hidden', 'false');
    host.classList.add('film-open', 'film-playing');
    host.querySelectorAll('.intro-slide').forEach(el => el.setAttribute('aria-hidden', 'true'));
    track('start');
  }
  function open() {
    clearTimeout(timer);
    frame?.remove();
    started = false;
    muted = true;
    panel.hidden = false;
    panel.inert = true;
    panel.setAttribute('aria-hidden', 'true');
    host.classList.remove('film-open', 'film-playing');
    sound.textContent = 'Sound on';
    sound.setAttribute('aria-pressed', 'false');
    play.textContent = 'Replay';
    frame = document.createElement('iframe');
    frame.title = 'Ultrahuman Ring AIR official product film';
    frame.tabIndex = -1;
    const url = new URL('https://www.youtube-nocookie.com/embed/35wj28s34nc');
    Object.entries({autoplay:1,mute:1,playsinline:1,enablejsapi:1,controls:0,rel:0,origin:location.origin}).forEach(([key,value]) => url.searchParams.set(key,value));
    frame.src = url.href;
    frame.allow = 'autoplay; encrypted-media; picture-in-picture';
    frame.allowFullscreen = true;
    frame.addEventListener('load', () => {
      frame?.contentWindow?.postMessage(JSON.stringify({event:'listening',id:'ultra-home-intro'}), 'https://www.youtube-nocookie.com');
      command('addEventListener', ['onStateChange']);
      command('addEventListener', ['onError']);
      command('mute');
      command('playVideo');
    });
    screen.append(frame);
    timer = setTimeout(() => {if (!started) finish('unavailable');}, 4500);
  }
  play.addEventListener('click', () => {command('seekTo', [0,true]); command('playVideo'); track('replay');});
  sound.addEventListener('click', () => {
    muted = !muted;
    command(muted ? 'mute' : 'unMute');
    sound.textContent = muted ? 'Sound on' : 'Sound off';
    sound.setAttribute('aria-pressed', String(!muted));
  });
  skip.addEventListener('click', () => finish('skip'));
  replay.addEventListener('click', () => {open(); track('play_request');});
  window.addEventListener('message', event => {
    if (event.origin !== 'https://www.youtube-nocookie.com' || event.source !== frame?.contentWindow) return;
    let data; try {data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;} catch (_) {return;}
    if (data.event === 'onError') {finish('unavailable'); return;}
    const state = data.event === 'onStateChange' ? data.info : data.event === 'infoDelivery' ? data.info?.playerState : null;
    if (state === 1) reveal();
    if (state === 0 && started) finish();
    if (started && data.event === 'infoDelivery' && data.info?.currentTime >= 30) finish();
  });
  document.addEventListener('visibilitychange', () => {if (document.hidden && frame) finish('hidden');});
  new IntersectionObserver(entries => {if (!entries[0].isIntersecting && started) finish('offscreen');}, {threshold:.1}).observe(host);
  if (!reduced.matches) open();
})();
