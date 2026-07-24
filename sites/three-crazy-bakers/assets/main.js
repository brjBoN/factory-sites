(function () {
  var t = document.querySelector('.nav-toggle');
  if (t) {
    t.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('nav.primary a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('nav-open');
        t.setAttribute('aria-expanded', 'false');
      });
    });
  }
})();
