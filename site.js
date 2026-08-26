/* Europe4strays bespoke layer: folio chapter marker, the 260-paw trace rail,
   the colophon heart of paws, and the IBAN copy button.
   Engine untouched; everything here reads scroll state or its own observers. */
(function () {
  var DOGS = 260;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* deterministic jitter */
  function jit(i, salt) {
    var x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453;
    return x - Math.floor(x);
  }

  var PAW = "M0,-2.7 a1.05,1.3 0 1,0 0.01,0 M-2.4,-1.5 a0.95,1.15 0 1,0 0.01,0 M2.4,-1.5 a0.95,1.15 0 1,0 0.01,0 M0,1.4 a2.1,1.75 0 1,0 0.01,0";

  /* ---------- folio: which chapter is on screen ---------- */
  var folio = document.getElementById("folioCh");
  var folioBox = document.getElementById("folio");
  var current = "ch0";
  var folioVis = function () {};
  if (folioBox) {
    var folioTick = false;
    folioVis = function () {
      folioTick = false;
      var show = window.scrollY > innerHeight * 0.5 && current !== "ch6";
      if (show === folioBox.hasAttribute("hidden")) {
        if (show) folioBox.removeAttribute("hidden");
        else folioBox.setAttribute("hidden", "");
      }
    };
    window.addEventListener("scroll", function () {
      if (!folioTick) { folioTick = true; requestAnimationFrame(folioVis); }
    }, { passive: true });
    folioVis();
  }
  function folioText() {
    if (!folio) return;
    folio.textContent = (window.E4S_I18N ? E4S_I18N.t("ch_" + current) : "") || "";
  }
  var marked = document.querySelectorAll("[data-chapter-key]");
  if ("IntersectionObserver" in window && folio) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          current = en.target.getAttribute("data-chapter-key") || current;
          folioText();
          folioVis();
          var dark = en.target.classList.contains("ch-dark");
          document.body.classList.toggle("on-dark", dark);
        }
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    marked.forEach(function (s) { io.observe(s); });
  }
  document.addEventListener("e4s:lang", folioText);

  /* ---------- the paw trace rail (signature move) ---------- */
  var railSvg = document.getElementById("pawRail");
  var lit = -1;
  if (railSvg && !reduced) {
    var railBox = railSvg.parentElement.getBoundingClientRect();
    var W = 40, H = Math.max(400, Math.round(W * (railBox.height / Math.max(1, railBox.width))));
    railSvg.removeAttribute("preserveAspectRatio");
    railSvg.setAttribute("viewBox", "0 0 " + W + " " + H);
    var frag = document.createDocumentFragment();
    var top = 24, bottom = H - 64;
    for (var i = 0; i < DOGS; i++) {
      var y = top + (bottom - top) * (i / (DOGS - 1));
      var x = W / 2 + (i % 2 ? 6.5 : -6.5) + (jit(i, 1) - 0.5) * 3;
      var r = (jit(i, 2) - 0.5) * 30;
      var s = 0.42 + jit(i, 3) * 0.16;
      var p = document.createElementNS("http://www.w3.org/2000/svg", "path");
      p.setAttribute("d", PAW);
      p.setAttribute("class", "paw");
      p.setAttribute("transform", "translate(" + x.toFixed(1) + "," + y.toFixed(1) + ") rotate(" + r.toFixed(0) + ") scale(" + s.toFixed(2) + ")");
      frag.appendChild(p);
    }
    var tally = document.createElementNS("http://www.w3.org/2000/svg", "text");
    tally.setAttribute("x", W / 2);
    tally.setAttribute("y", H - 34);
    tally.setAttribute("text-anchor", "middle");
    tally.setAttribute("class", "tally");
    tally.textContent = "0";
    frag.appendChild(tally);
    var unit = document.createElementNS("http://www.w3.org/2000/svg", "text");
    unit.setAttribute("x", W / 2);
    unit.setAttribute("y", H - 18);
    unit.setAttribute("text-anchor", "middle");
    unit.setAttribute("class", "tally");
    unit.textContent = "/ " + DOGS;
    frag.appendChild(unit);
    railSvg.appendChild(frag);
    var paws = railSvg.querySelectorAll(".paw");

    var ticking = false;
    function railUpdate() {
      ticking = false;
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      var n = Math.round(p * DOGS);
      if (n === lit) return;
      var lo = Math.min(lit, n), hi = Math.max(lit, n);
      for (var i = Math.max(0, lo); i < hi; i++) {
        if (paws[i]) paws[i].classList.toggle("lit", i < n);
      }
      lit = n;
      tally.textContent = String(n);
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(railUpdate); }
    }, { passive: true });
    railUpdate();
  }

  /* ---------- colophon heart of 260 paws ---------- */
  var heart = document.getElementById("heartPaws");
  if (heart) {
    /* param heart curve, filled row-sampling for interior points */
    function heartPt(t, sc) {
      var x = 16 * Math.pow(Math.sin(t), 3);
      var y = 13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t);
      return [100 + x * sc, 86 - y * sc];
    }
    var pts = [];
    var OUT = 150, sc = 4.7;
    for (var i = 0; i < OUT; i++) {
      pts.push(heartPt((i / OUT) * Math.PI * 2, sc));
    }
    var IN = DOGS - OUT, sc2 = 3.1;
    for (var j = 0; j < IN; j++) {
      var t2 = (j / IN) * Math.PI * 2;
      var k = 0.35 + 0.65 * jit(j, 7);
      var q = heartPt(t2, sc2 * k);
      pts.push([q[0], 86 - (86 - q[1]) * 0.96]);
    }
    var hfrag = document.createDocumentFragment();
    pts.forEach(function (pt, idx) {
      var p = document.createElementNS("http://www.w3.org/2000/svg", "path");
      p.setAttribute("d", PAW);
      p.setAttribute("class", "hp");
      var rr = (jit(idx, 4) - 0.5) * 70;
      var ss = 0.8 + jit(idx, 5) * 0.45;
      p.setAttribute("transform", "translate(" + pt[0].toFixed(1) + "," + pt[1].toFixed(1) + ") rotate(" + rr.toFixed(0) + ") scale(" + ss.toFixed(2) + ")");
      p.style.transitionDelay = (jit(idx, 6) * 420).toFixed(0) + "ms";
      hfrag.appendChild(p);
    });
    heart.appendChild(hfrag);
    var hps = heart.querySelectorAll(".hp");
    var colo = heart.closest("[data-sc-act]");
    var armed = false;
    function heartTick() {
      var p = parseFloat(getComputedStyle(colo).getPropertyValue("--sc-p")) || 0;
      var shown = reduced ? hps.length : Math.round(Math.min(1, p * 2.2) * hps.length);
      if (!armed || shown > 0) {
        for (var i = 0; i < hps.length; i++) hps[i].classList.toggle("lit", i < shown);
        armed = true;
      }
      requestAnimationFrame(heartTick);
    }
    if (colo) requestAnimationFrame(heartTick);
  }

  /* ---------- IBAN copy ---------- */
  var btn = document.getElementById("copyIban");
  if (btn) {
    btn.addEventListener("click", function () {
      var iban = "RO91BTRLEURCRT0409910001";
      function done() {
        btn.textContent = (window.E4S_I18N ? E4S_I18N.t("h1btnDone") : "Copied");
        setTimeout(function () {
          btn.textContent = (window.E4S_I18N ? E4S_I18N.t("h1btn") : "Copy IBAN");
        }, 1600);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(iban).then(done, done);
      } else { done(); }
    });
  }
})();
