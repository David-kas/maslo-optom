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

  function setNavOpen(open) {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-nav');
    if (!toggle || !nav) return;
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('is-nav-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    if (!open) closeAllSubmenus();
  }

  function initNav() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      setNavOpen(!nav.classList.contains('is-open'));
    });
    nav.querySelectorAll('a').forEach(function (a) {
      if (a.hasAttribute('data-nav-submenu-trigger')) return;
      a.addEventListener('click', function () {
        setNavOpen(false);
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setNavOpen(false);
    });
    document.addEventListener('click', function (e) {
      if (!nav.classList.contains('is-open')) return;
      if (e.target.closest('.site-nav') || e.target.closest('.nav-toggle')) return;
      setNavOpen(false);
    });
    window.addEventListener('resize', function () {
      if (window.matchMedia('(min-width: 1025px)').matches) setNavOpen(false);
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
        e.preventDefault();
        e.stopPropagation();
        if (wrap.classList.contains('is-open')) {
          wrap.classList.remove('is-open');
          trigger.setAttribute('aria-expanded', 'false');
          return;
        }
        closeAllSubmenus();
        wrap.classList.add('is-open');
        trigger.setAttribute('aria-expanded', 'true');
      });
    });
    document.addEventListener('click', function (e) {
      if (e.target.closest('.submenu-wrap') || e.target.closest('.nav-toggle')) return;
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

  function initGuideOpen() {
    document.querySelectorAll('[data-open-guide]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        var panel = document.querySelector('.guide-disclosure');
        if (!panel) return;
        e.preventDefault();
        panel.setAttribute('open', '');
        var target = document.querySelector(link.getAttribute('href'));
        if (target) {
          var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
          target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initTheme();
      initNav();
      initSubmenu();
      initGuideOpen();
      initBackTop();
    });
  } else {
    initTheme();
    initNav();
    initSubmenu();
    initGuideOpen();
    initBackTop();
  }
})();
