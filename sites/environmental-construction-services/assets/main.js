(function () {
  var t = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-navigation-mobile');
  if (t && nav) {
    var setMenu = function (open, returnFocus) {
      document.body.classList.toggle('nav-open', open);
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
      t.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (!open && returnFocus) t.focus();
    };

    t.addEventListener('click', function () {
      setMenu(!document.body.classList.contains('nav-open'), false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
        setMenu(false, true);
        return;
      }

      if (e.key === 'Tab' && document.body.classList.contains('nav-open')) {
        var links = Array.prototype.slice.call(nav.querySelectorAll('a[href]'));
        var stops = [t].concat(links);
        var first = stops[0];
        var last = stops[stops.length - 1];

        if (e.shiftKey && (document.activeElement === first || !stops.includes(document.activeElement))) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });

    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        setMenu(false, false);
      });
    });

    var desktop = window.matchMedia('(min-width: 1101px)');
    var closeForDesktop = function (event) {
      if (event.matches) setMenu(false, false);
    };
    if (desktop.addEventListener) desktop.addEventListener('change', closeForDesktop);
    else desktop.addListener(closeForDesktop);
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
