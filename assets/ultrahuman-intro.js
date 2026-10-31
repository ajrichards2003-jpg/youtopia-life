/* November editorial highlight reel. No forced product video or player takeover. */
(() => {
  'use strict';
  const host = document.querySelector('.ultra-intro');
  if (!host) return;

  const slides = Array.from(host.querySelectorAll('.intro-slide'));
  const dots = Array.from(host.querySelectorAll('.intro-dot'));
  const counter = host.querySelector('.intro-counter');
  const pauseButton = host.querySelector('.intro-pause');
  const prevButton = host.querySelector('.intro-prev');
  const nextButton = host.querySelector('.intro-next');
  const modal = host.querySelector('.intro-video-overlay');
  const player = modal?.querySelector('iframe');
  const closeButton = modal?.querySelector('[data-intro-video-close]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!slides.length || slides.length !== dots.length) return;

  let index = 0;
  let timer = null;
  let paused = reducedMotion.matches;
  let videoOpen = false;
  let focusReturn = null;

  function show(n) {
    index = ((n % slides.length) + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      const active = i === index;
      slide.classList.toggle('active', active);
      slide.setAttribute('aria-hidden', String(!active));
      slide.inert = !active;
      slide.querySelectorAll('a, button').forEach(control => {
        control.tabIndex = active ? 0 : -1;
      });
    });
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
      dot.setAttribute('aria-pressed', String(i === index));
    });
    if (counter) counter.textContent =
      String(index + 1).padStart(2, '0') + ' / ' +
      String(slides.length).padStart(2, '0');
  }

  function schedule() {
    window.clearTimeout(timer);
    if (pauseButton) {
      pauseButton.textContent = paused ? 'Play' : 'Pause';
      pauseButton.setAttribute('aria-label', paused ? 'Play highlights' : 'Pause highlights');
      pauseButton.setAttribute('aria-pressed', String(paused));
    }
    if (paused || videoOpen || document.hidden) return;
    timer = window.setTimeout(() => {
      show(index + 1);
      schedule();
    }, 7600);
  }

  function go(n) {
    show(n);
    schedule();
  }

  function closeVideo() {
    if (!videoOpen) return;
    videoOpen = false;
    if (player) player.removeAttribute('src');
    modal.hidden = true;
    host.classList.remove('intro-video-open');
    focusReturn?.focus();
    schedule();
  }

  function openVideo(trigger) {
    const id = trigger.getAttribute('data-intro-video');
    if (!modal || !player || !closeButton || id !== '-sDcFyZLxTY') return;
    window.clearTimeout(timer);
    focusReturn = trigger;
    videoOpen = true;
    host.classList.add('intro-video-open');
    modal.hidden = false;
    player.src = 'https://www.youtube-nocookie.com/embed/' + id +
      '?autoplay=1&rel=0&playsinline=1';
    closeButton.focus();
  }

  dots.forEach((dot, i) => dot.addEventListener('click', () => go(i)));
  prevButton?.addEventListener('click', () => go(index - 1));
  nextButton?.addEventListener('click', () => go(index + 1));
  pauseButton?.addEventListener('click', () => {
    paused = !paused;
    schedule();
  });

  host.addEventListener('click', event => {
    const watch = event.target.closest('[data-intro-video]');
    if (watch) {
      event.preventDefault();
      openVideo(watch);
    }
  });
  closeButton?.addEventListener('click', closeVideo);
  modal?.addEventListener('click', event => {
    if (event.target === modal) closeVideo();
  });
  host.addEventListener('keydown', event => {
    if (videoOpen) return;
    if (event.target.matches('input, textarea, select')) return;
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      go(index + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && videoOpen) closeVideo();
  });
  document.addEventListener('visibilitychange', schedule);
  reducedMotion.addEventListener?.('change', event => {
    if (event.matches) paused = true;
    schedule();
  });

  show(0);
  schedule();
})();
