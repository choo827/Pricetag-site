/* pricetag landing — behaviour. No dependencies. */
(function () {
  "use strict";

  // ---------- settings you may change ----------
  var MAILCHIMP_URL = "https://gmail.us15.list-manage.com/subscribe/post?u=7a4b34e1ab518009c85cb469d&id=03c1a33707&f_id=00147be0f0";
  var SLIDE_SECONDS = 4;

  var root = document.documentElement;
  var lang = root.lang === "en" ? "en" : "ko";

  function store(key, value) {
    try { if (value === undefined) return localStorage.getItem(key); localStorage.setItem(key, value); } catch (e) { return null; }
  }

  // ---------- theme ----------
  var themeBtn = document.getElementById("theme-toggle");
  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function labelTheme() {
    if (!themeBtn) return;
    var dark = isDark();
    themeBtn.setAttribute("aria-label", lang === "ko"
      ? (dark ? "라이트 모드로 전환" : "다크 모드로 전환")
      : (dark ? "Switch to light mode" : "Switch to dark mode"));
  }
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store("pt-theme", next);
      labelTheme();
    });
    labelTheme();
  }

  // ---------- language: remember an explicit choice ----------
  Array.prototype.forEach.call(document.querySelectorAll("[data-lang-link]"), function (a) {
    a.addEventListener("click", function () { store("pt-lang", a.getAttribute("data-lang-link")); });
  });

  // ---------- hero demo ----------
  var dataEl = document.getElementById("hero-data");
  var items = dataEl ? JSON.parse(dataEl.textContent) : [];
  var imgs = document.querySelectorAll(".product-img img");
  var nameEl = document.getElementById("hero-name");
  var priceBtn = document.getElementById("hero-price");
  var bubble = document.getElementById("hero-bubble");
  var dots = document.querySelectorAll(".dots button");
  var demo = document.querySelector(".browser");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var current = 0, timer = null, popTimer = null, paused = false;

  function showBubble(on, animate) {
    if (!bubble || !priceBtn) return;
    bubble.hidden = !on;
    priceBtn.setAttribute("aria-pressed", on ? "true" : "false");
    bubble.classList.remove("pop");
    if (on && animate) { void bubble.offsetWidth; bubble.classList.add("pop"); }
  }
  function go(i) {
    if (!items.length) return;
    current = (i + items.length) % items.length;
    var it = items[current];
    Array.prototype.forEach.call(imgs, function (im, k) { im.classList.toggle("is-on", k === current); });
    Array.prototype.forEach.call(dots, function (d, k) { d.setAttribute("aria-current", k === current ? "true" : "false"); });
    nameEl.textContent = it.name;
    priceBtn.textContent = it.original;
    bubble.textContent = it.converted;
    showBubble(false);
    clearTimeout(popTimer);
    popTimer = setTimeout(function () { showBubble(true, true); }, reduce ? 0 : 450);
  }
  function start() {
    clearInterval(timer);
    if (reduce || items.length < 2) return;
    timer = setInterval(function () { if (!paused) go(current + 1); }, SLIDE_SECONDS * 1000);
  }
  if (priceBtn) {
    priceBtn.addEventListener("click", function () { showBubble(bubble.hidden, true); });
    Array.prototype.forEach.call(dots, function (d, k) { d.addEventListener("click", function () { go(k); start(); }); });
    if (demo) {
      demo.addEventListener("mouseenter", function () { paused = true; });
      demo.addEventListener("mouseleave", function () { paused = false; });
      demo.addEventListener("focusin", function () { paused = true; });
      demo.addEventListener("focusout", function () { paused = false; });
    }
    start();
  }

  // ---------- Mailchimp signup (JSONP, stays on the page) ----------
  var form = document.getElementById("signup");
  var statusEl = document.getElementById("signup-status");
  var T = {
    ko: {
      sending: "보내는 중이에요…",
      ok: "확인 메일을 보냈어요. 메일함에서 링크를 눌러 주시면 등록이 끝나요.",
      already: "이미 등록된 이메일이에요. 출시 소식을 보내 드릴게요.",
      invalid: "이메일 주소를 다시 확인해 주세요.",
      fail: "지금은 등록하지 못했어요. 잠시 후 다시 시도해 주세요."
    },
    en: {
      sending: "Sending…",
      ok: "Check your inbox and tap the link in our email to confirm.",
      already: "You’re already on the list. We’ll let you know at launch.",
      invalid: "Please check your email address.",
      fail: "We couldn’t sign you up just now. Please try again in a moment."
    }
  }[lang];

  function say(msg, kind) {
    statusEl.textContent = msg;
    statusEl.className = "status" + (kind ? " is-" + kind : "");
  }

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var email = form.elements.EMAIL.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { say(T.invalid, "err"); form.elements.EMAIL.focus(); return; }

      var btn = form.querySelector("button");
      btn.disabled = true;
      say(T.sending);

      var cb = "ptmc" + Date.now();
      var params = new URLSearchParams();
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.name) params.append(el.name, el.value.trim());
      });
      params.append("c", cb);
      var url = MAILCHIMP_URL.replace("/post?", "/post-json?") + "&" + params.toString();

      var script = document.createElement("script");
      var done = false;
      function finish() {
        done = true; btn.disabled = false;
        try { delete window[cb]; } catch (x) { window[cb] = undefined; }
        if (script.parentNode) script.parentNode.removeChild(script);
      }
      window[cb] = function (res) {
        finish();
        var msg = String((res && res.msg) || "").toLowerCase();
        if (res && res.result === "success") { say(T.ok, "ok"); form.reset(); }
        else if (msg.indexOf("already") !== -1) { say(T.already, "ok"); }
        else if (msg.indexOf("email") !== -1 && msg.indexOf("invalid") !== -1) { say(T.invalid, "err"); }
        else { say(T.fail, "err"); }
      };
      script.onerror = function () { if (!done) { finish(); say(T.fail, "err"); } };
      setTimeout(function () { if (!done) { finish(); say(T.fail, "err"); } }, 12000);
      script.src = url;
      document.body.appendChild(script);
    });
  }
})();
