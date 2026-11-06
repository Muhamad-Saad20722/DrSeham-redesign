/* Shared behaviour: scroll reveal, video modal, CSRF injection */
(function () {
  'use strict';

  // Scroll reveal (falls back to visible when IntersectionObserver is unavailable)
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // YouTube modal: load the iframe only when opened, clear on close
  var modal = document.getElementById('videoModal');
  if (modal) {
    var frame = document.getElementById('videoFrame');
    modal.addEventListener('show.bs.modal', function (ev) {
      var id = ev.relatedTarget && ev.relatedTarget.getAttribute('data-video');
      if (id) frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
    });
    modal.addEventListener('hidden.bs.modal', function () { frame.src = ''; });
  }

  // Copy the CSRF token (injected by the server into the meta tag) into any form
  var meta = document.querySelector('meta[name="csrf-token"]');
  if (meta && meta.content) {
    document.querySelectorAll('input[name="_token"]').forEach(function (i) { i.value = meta.content; });
  }
})();
