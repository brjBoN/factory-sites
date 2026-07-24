(function () {
  "use strict";
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("nav-open", open);
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("open");
        toggle.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-open");
      });
    });
  }
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var items = document.querySelectorAll(".reveal");
  if (reduced || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    items.forEach(function (el) { io.observe(el); });
  }
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
  // search
  var inp = document.getElementById("qt-search");
  var res = document.getElementById("qt-results");
  if (inp && res) {
    function run() {
      var q = inp.value.trim().toLowerCase();
      if (q.length < 2 || !window.QT_INDEX) { res.hidden = true; res.innerHTML = ""; return; }
      var terms = q.split(/\s+/);
      var hits = window.QT_INDEX.map(function (it) {
        var t = it.t.toLowerCase(); var score = 0;
        terms.forEach(function (w) { if (t.indexOf(w) === 0) score += 3; else if (t.indexOf(w) !== -1) score += 2; });
        return { it: it, score: score };
      }).filter(function (h) { return h.score >= terms.length * 2; })
        .sort(function (a, b) { return b.score - a.score; }).slice(0, 9);
      if (!hits.length) { res.innerHTML = '<div class="none">No matches — try "monogram", "tree", "patina"…</div>'; }
      else {
        res.innerHTML = hits.map(function (h) {
          var ext = h.it.u.indexOf("http") === 0 ? ' target="_blank" rel="noopener"' : "";
          return '<a href="' + h.it.u + '"' + ext + '><span>' + h.it.t + '</span><span class="rp">' + (h.it.p || "") + "</span></a>";
        }).join("");
      }
      res.hidden = false;
    }
    inp.addEventListener("input", run);
    inp.addEventListener("focus", run);
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".searchbox")) { res.hidden = true; }
    });
  }
  // collapse two-column grids on small screens
  function collapse() {
    document.querySelectorAll("[data-collapse]").forEach(function (el) {
      el.style.gridTemplateColumns = window.innerWidth < 880 ? "1fr" : "";
    });
  }
  collapse();
  window.addEventListener("resize", collapse);
})();
