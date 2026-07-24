(function () {
  var t = document.querySelector('.nav-toggle');
  var nav = document.querySelector('nav.primary');
  if (t && nav) {
    t.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
        document.body.classList.remove('nav-open');
        t.setAttribute('aria-expanded', 'false');
        t.focus();
      }
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('nav-open');
        t.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Bounded parallax on the desktop hero art (max 16px), reduced-motion aware.
  var art = document.querySelector('.hero-art.desktop img');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (art && !reduced) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = Math.max(-16, Math.min(16, window.scrollY * 0.04));
        art.style.transform = 'translateY(' + y + 'px)';
        ticking = false;
      });
    }, { passive: true });
  }
})();
