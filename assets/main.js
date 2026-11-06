(function () {
  "use strict";
  var ENDPOINT = "https://formsubmit.co/ajax/solo.studios.co@gmail.com";

  // header: shadow on scroll, mobile menu
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  var btn = document.getElementById("menuBtn"), mob = document.getElementById("mobileNav");
  if (btn && mob) btn.addEventListener("click", function () {
    var open = mob.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });

  // scroll animations: reveal with stagger, parallax orbs, progress bar, hero words, timeline
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var root = document.documentElement;
  // stagger children inside grids
  [].slice.call(document.querySelectorAll(".grid")).forEach(function (g) {
    [].slice.call(g.children).forEach(function (c, i) { if (c.classList.contains("reveal")) c.style.transitionDelay = Math.min(i * 90, 540) + "ms"; });
  });
  // hero headline words
  var h1 = document.querySelector(".hero h1");
  if (h1 && !reduce) {
    (function split(node) {
      [].slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (t) {
            if (!t) return;
            if (/^\s+$/.test(t)) { frag.appendChild(document.createTextNode(" ")); return; }
            var w = document.createElement("span"); w.className = "w"; var i = document.createElement("span"); i.textContent = t; w.appendChild(i); frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1) split(n);
      });
    })(h1);
    [].slice.call(h1.querySelectorAll(".w>span")).forEach(function (sp, i) { sp.style.transitionDelay = (0.15 + i * 0.07) + "s"; });
    h1.classList.remove("reveal"); h1.style.opacity = 1; h1.style.transform = "none";
    setTimeout(function () { h1.classList.add("words-in"); }, 60);
  }
  // orbs in hero
  var hero = document.querySelector(".hero");
  if (hero && !reduce) { ["sky", "gold"].forEach(function (c) { var o = document.createElement("div"); o.className = "orb " + c; hero.appendChild(o); }); }
  // progress bar
  var bar = document.createElement("div"); bar.className = "scroll-progress"; document.body.appendChild(bar);
  var tl = document.querySelector(".timeline");
  var ticking = false;
  function frame() {
    ticking = false;
    var y = window.scrollY, max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    bar.style.transform = "scaleX(" + Math.min(1, y / max) + ")";
    if (!reduce) root.style.setProperty("--sy", y);
    if (tl) { var r = tl.getBoundingClientRect(); root.style.setProperty("--tl", Math.max(0, Math.min(1, (window.innerHeight * 0.7 - r.top) / r.height))); }
    revealCheck();
  }
  function onS() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener("scroll", onS, { passive: true }); window.addEventListener("resize", onS);

  var targets = [].slice.call(document.querySelectorAll(".reveal, .pp-gallery"));
  function revealCheck() {
    // fallback in case an observer entry is missed: reveal anything already above the fold line
    targets.forEach(function (t) { if (!t.classList.contains("in") && t.getBoundingClientRect().top < window.innerHeight * 0.92) t.classList.add("in"); });
  }
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0, rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t) { io.observe(t); });
  } else { targets.forEach(function (t) { t.classList.add("in"); }); }
  frame(); setTimeout(frame, 120);

  // count-up numbers
  [].slice.call(document.querySelectorAll("[data-count]")).forEach(function (el) {
    var end = parseFloat(el.getAttribute("data-count")), dec = parseInt(el.getAttribute("data-dec") || "0", 10), suf = el.getAttribute("data-suffix") || "";
    var final = end.toFixed(dec) + suf; el.textContent = final;
    if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var seen = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; seen.unobserve(el);
        var t0 = performance.now();
        (function tick(now) {
          var p = Math.min((now - t0) / 1300, 1), v = end * (1 - Math.pow(1 - p, 3));
          el.textContent = v.toFixed(dec) + suf; if (p < 1) requestAnimationFrame(tick); else el.textContent = final;
        })(t0);
      });
    }, { threshold: 0.4 });
    seen.observe(el);
  });

  function post(data) {
    return fetch(ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || j.success === "false") throw new Error("send"); return j; }); });
  }
  function val(form, name) { var f = form.elements[name]; return f && f.value ? f.value.trim() : ""; }
  function checked(form, name) { return [].slice.call(form.querySelectorAll('input[name="' + name + '"]:checked')).map(function (i) { return i.value; }); }

  // multi-step application form
  var af = document.getElementById("applyForm");
  if (af) {
    var steps = [].slice.call(af.querySelectorAll("fieldset")), cur = 0;
    var bar = document.getElementById("bar"), count = document.getElementById("stepCount"), pct = document.getElementById("stepPct");
    var back = document.getElementById("back"), next = document.getElementById("next"), submit = document.getElementById("submit");
    var err = document.getElementById("formError"), done = document.getElementById("done"), nav = document.getElementById("formNav");
    var params = new URLSearchParams(location.search), pre = params.get("type");
    if (pre) { var r = af.querySelector('input[name="type"][value="' + pre + '"]'); if (r) r.checked = true; }
    function show(i) {
      cur = i; steps.forEach(function (s, k) { s.classList.toggle("active", k === i); });
      var p = Math.round(((i + 1) / steps.length) * 100); bar.style.width = p + "%"; count.textContent = "Step " + (i + 1) + " of " + steps.length; pct.textContent = p + "%";
      back.style.visibility = i === 0 ? "hidden" : "visible"; next.hidden = i === steps.length - 1; submit.hidden = i !== steps.length - 1; err.textContent = "";
      window.scrollTo({ top: af.getBoundingClientRect().top + window.scrollY - 110, behavior: "smooth" });
    }
    var BIZ = ["Clothing or product brand", "E-commerce store or community", "Company or service business"];
    function notFit() {
      var tp = checked(af, "type")[0] || "", inv = checked(af, "invest")[0] || "";
      if (BIZ.indexOf(tp) > -1 && inv === "Under \u00a33k") {
        err.textContent = "Our plans start at \u00a33,000 a month plus ad spend, so we are not the right fit yet. Come back when you are ready to invest more.";
        return true;
      }
      return false;
    }
    function valid(i) {
      if (i === 2 && notFit()) return false;
      var ok = true, s = steps[i];
      [].slice.call(s.querySelectorAll("[required]")).forEach(function (el) {
        if (el.type === "radio" || el.type === "checkbox") return;
        var good = el.checkValidity() && el.value.trim() !== ""; el.classList.toggle("invalid", !good); if (!good) ok = false;
      });
      var groups = {}; [].slice.call(s.querySelectorAll('input[type="radio"][required]')).forEach(function (r) { groups[r.name] = true; });
      Object.keys(groups).forEach(function (n) { if (!af.querySelector('input[name="' + n + '"]:checked')) ok = false; });
      var cb = s.querySelector("input[data-need]"); if (cb && !cb.checked) ok = false;
      var any = s.querySelector("[data-any]"); if (any && !s.querySelector('input[data-any]:checked')) ok = false;
      err.textContent = ok ? "" : "Please answer everything marked required before continuing."; return ok;
    }
    next.addEventListener("click", function () { if (valid(cur)) show(cur + 1); });
    back.addEventListener("click", function () { show(cur - 1); });
    af.addEventListener("submit", function (e) {
      e.preventDefault(); if (notFit() || !valid(cur)) return;
      if (val(af, "_honey")) return;
      var data = {
        _subject: "New application: " + val(af, "name") + ", " + (checked(af, "type")[0] || "") + ", revenue " + (checked(af, "revenue")[0] || "n/a"),
        _template: "table", _captcha: "false",
        snapshot: "Stage: " + (checked(af, "stage")[0] || "n/a") + " | Revenue: " + (checked(af, "revenue")[0] || "n/a") + " | Profit: " + (checked(af, "profit")[0] || "n/a") + " | Marketing spend now: " + (checked(af, "spend")[0] || "n/a") + " | Can invest: " + (checked(af, "invest")[0] || "n/a"),
        name: val(af, "name"), email: val(af, "email"), phone: val(af, "phone"), business: val(af, "business"), links: val(af, "links"),
        type: checked(af, "type")[0] || "", stage: checked(af, "stage")[0] || "", monthly_revenue: checked(af, "revenue")[0] || "", monthly_profit: checked(af, "profit")[0] || "",
        current_marketing_spend: checked(af, "spend")[0] || "", can_invest_monthly: checked(af, "invest")[0] || "", needs: checked(af, "needs").join(", "),
        biggest_blocker: val(af, "blocker"), twelve_month_goal: val(af, "goal"), start: checked(af, "start")[0] || "", heard_from: val(af, "heard"), consent: "Agreed to be contacted"
      };
      submit.disabled = true; submit.textContent = "Sending...";
      post(data).then(function () {
        steps.forEach(function (s) { s.classList.remove("active"); }); nav.style.display = "none"; document.querySelector(".progress").style.display = "none"; document.querySelector(".step-count").style.display = "none";
        done.classList.add("show");
      }).catch(function () {
        submit.disabled = false; submit.textContent = "Send application";
        err.textContent = "Something went wrong. Please email solo.studios.co@gmail.com instead.";
      });
    });
    show(0);
  }

  // contact form
  var cf = document.getElementById("contactForm");
  if (cf) {
    var cerr = document.getElementById("contactError"), cdone = document.getElementById("contactDone"), cbtn = document.getElementById("contactSend");
    cf.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      [].slice.call(cf.querySelectorAll("[required]")).forEach(function (el) { var g = el.checkValidity() && el.value.trim() !== ""; el.classList.toggle("invalid", !g); if (!g) ok = false; });
      if (!ok) { cerr.textContent = "Please fill in every field."; return; }
      if (val(cf, "_honey")) return;
      cbtn.disabled = true; cbtn.textContent = "Sending...";
      post({ _subject: "SOLO enquiry: " + val(cf, "role") + ", " + val(cf, "name"), _template: "table", _captcha: "false", name: val(cf, "name"), email: val(cf, "email"), role: val(cf, "role"), message: val(cf, "message") })
        .then(function () { cf.style.display = "none"; cdone.classList.add("show"); })
        .catch(function () { cbtn.disabled = false; cbtn.textContent = "Send message"; cerr.textContent = "Something went wrong. Please email solo.studios.co@gmail.com instead."; });
    });
  }
})();
