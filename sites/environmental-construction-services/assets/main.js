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

  // The worksheet never posts to this site. It prepares a message locally and
  // hands it to the visitor's own email application for review and sending.
  var requestForm = document.querySelector('[data-ecs-request]');
  if (requestForm) {
    requestForm.addEventListener('submit', function (event) {
      event.preventDefault();

      var field = function (name) {
        return requestForm.querySelector('[name="' + name + '"]');
      };
      var value = function (name) {
        var control = field(name);
        return control ? control.value.trim() : '';
      };
      var name = value('name');
      var phone = value('phone');
      var email = value('email');
      var location = value('location');
      var service = value('service');
      var issue = value('issue');
      var timing = value('timing');
      var notes = value('notes');
      var status = requestForm.querySelector('.form-status');

      requestForm.querySelectorAll('[aria-invalid="true"]').forEach(function (control) {
        control.removeAttribute('aria-invalid');
      });

      var missing = !name ? field('name') :
        (!phone && !email) ? field('phone') :
        !service ? field('service') :
        !issue ? field('issue') : null;

      if (missing) {
        if (status) {
          status.textContent = 'Please add your name, one way to reach you, the service, and a short description of the issue.';
        }
        missing.setAttribute('aria-invalid', 'true');
        missing.focus();
        return;
      }

      var subject = 'Website request — ' + service + ' — ' + name;
      var body = [
        'Name: ' + name,
        'Phone: ' + (phone || 'Not provided'),
        'Email: ' + (email || 'Not provided'),
        'Property location: ' + (location || 'Not provided'),
        'Service: ' + service,
        'Timing: ' + (timing || 'Not provided'),
        '',
        'What is happening:',
        issue,
        '',
        'Additional notes:',
        notes || 'None'
      ].join('\n');

      if (status) {
        status.textContent = 'Your email app is opening with this request prepared. Review it, then press send.';
      }
      window.location.href = 'mailto:ecs.outdoorcustoms@gmail.com?subject=' +
        encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }
})();
