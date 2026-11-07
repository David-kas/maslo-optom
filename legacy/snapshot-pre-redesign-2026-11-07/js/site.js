(function () {
  'use strict';

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var backTop = document.querySelector('.back-top');
  if (backTop) {
    var onScroll = function () {
      if (window.scrollY > 400) {
        backTop.classList.add('is-visible');
      } else {
        backTop.classList.remove('is-visible');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    backTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'matchMedia' in window && window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    });
  }
})();
