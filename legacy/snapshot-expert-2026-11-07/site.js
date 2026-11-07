(function () {
  'use strict';

  var THEME_KEY = 'kfh-malyshev-theme';

  function getPreferred() {
    try {
      var saved = localStorage.getItem(THEME_KEY);
      if (saved === 'light' || saved === 'dark') return saved;
    } catch (e) {}
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    var btn = document.querySelector('[data-theme-toggle]');
    if (btn) {
      btn.setAttribute(
        'aria-label',
        theme === 'dark' ? 'Включить светлую тему' : 'Включить тёмную тему'
      );
    }
  }

  function initTheme() {
    applyTheme(getPreferred());
    var btn = document.querySelector('[data-theme-toggle]');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var cur = document.documentElement.getAttribute('data-theme') || 'light';
      var next = cur === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
      applyTheme(next);
    });
  }

  function initNav() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      if (a.hasAttribute('data-nav-submenu-trigger')) return;
      a.addEventListener('click', function () {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        closeAllSubmenus();
      }
    });
  }

  function closeAllSubmenus() {
    document.querySelectorAll('.submenu-wrap.is-open').forEach(function (wrap) {
      wrap.classList.remove('is-open');
      var tr = wrap.querySelector('[data-nav-submenu-trigger]');
      if (tr) tr.setAttribute('aria-expanded', 'false');
    });
  }

  function initSubmenu() {
    document.querySelectorAll('.submenu-wrap').forEach(function (wrap) {
      var trigger = wrap.querySelector('[data-nav-submenu-trigger]');
      var submenu = wrap.querySelector('.submenu');
      if (!trigger || !submenu) return;
      trigger.addEventListener('click', function (e) {
        if (!window.matchMedia('(max-width: 1024px)').matches) return;
        if (wrap.classList.contains('is-open')) return;
        e.preventDefault();
        closeAllSubmenus();
        wrap.classList.add('is-open');
        trigger.setAttribute('aria-expanded', 'true');
      });
    });
    document.addEventListener('click', function (e) {
      if (e.target.closest('.submenu-wrap')) return;
      closeAllSubmenus();
    });
  }

  function initBackTop() {
    var btn = document.querySelector('.back-top');
    if (!btn) return;
    var onScroll = function () {
      if (window.scrollY > 420) btn.classList.add('is-visible');
      else btn.classList.remove('is-visible');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    btn.addEventListener('click', function () {
      var smooth = !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
      window.scrollTo({ top: 0, behavior: smooth ? 'smooth' : 'auto' });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initTheme();
      initNav();
      initSubmenu();
      initBackTop();
    });
  } else {
    initTheme();
    initNav();
    initSubmenu();
    initBackTop();
  }
})();
