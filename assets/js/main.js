/* Shared behaviour: scroll reveal, video modal, language preference + suggestion */
(function () {
  "use strict";

  // Scroll reveal (falls back to visible when IntersectionObserver is unavailable)
  var items = document.querySelectorAll(".reveal");
  if (
    "IntersectionObserver" in window &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add("in");
            io.unobserve(en.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" },
    );
    items.forEach(function (el) {
      io.observe(el);
    });
  } else {
    items.forEach(function (el) {
      el.classList.add("in");
    });
  }

  // YouTube modal: load the iframe only when opened, clear on close
  var modal = document.getElementById("videoModal");
  if (modal) {
    var frame = document.getElementById("videoFrame");
    modal.addEventListener("show.bs.modal", function (ev) {
      var id = ev.relatedTarget && ev.relatedTarget.getAttribute("data-video");
      if (id)
        frame.src =
          "https://www.youtube-nocookie.com/embed/" +
          encodeURIComponent(id) +
          "?autoplay=1&rel=0";
    });
    modal.addEventListener("hidden.bs.modal", function () {
      frame.src = "";
    });
  }

  // Language preference. Visitors are never redirected automatically (that hurts SEO and
  // breaks shared links); if they previously chose the other language we only offer a link.
  var current = document.documentElement.lang === "en" ? "en" : "ar";

  function savePref(lang) {
    try {
      localStorage.setItem("clinic-lang", lang);
    } catch (e) {}
  }

  document.querySelectorAll("[data-lang-switch]").forEach(function (a) {
    a.addEventListener("click", function () {
      savePref(a.getAttribute("data-lang-switch"));
    });
  });

  var preferred = null;
  try {
    preferred = localStorage.getItem("clinic-lang");
  } catch (e) {}
  var target =
    preferred && preferred !== current
      ? document.querySelector('[data-lang-switch="' + preferred + '"]')
      : null;
  if (target) {
    // Shown in the language being offered, because that is the one the visitor reads.
    var TEXT = {
      en: {
        msg: "This page is also available in English.",
        go: "View in English",
        close: "Dismiss",
      },
      ar: {
        msg: "هذه الصفحة متاحة أيضًا باللغة العربية.",
        go: "عرض بالعربية",
        close: "إغلاق",
      },
    }[preferred];
    if (TEXT) {
      var bar = document.createElement("div");
      bar.className = "lang-suggest";
      bar.lang = preferred;
      bar.dir = preferred === "ar" ? "rtl" : "ltr";
      bar.setAttribute("role", "region");
      bar.setAttribute("aria-label", TEXT.msg);

      var span = document.createElement("span");
      span.textContent = TEXT.msg;
      var go = document.createElement("a");
      go.href = target.getAttribute("href");
      go.textContent = TEXT.go;
      var close = document.createElement("button");
      close.type = "button";
      close.className = "lang-suggest-close";
      close.setAttribute("aria-label", TEXT.close);
      close.textContent = "×";
      close.addEventListener("click", function () {
        savePref(current); // stop asking
        bar.remove();
      });
      bar.appendChild(span);
      bar.appendChild(go);
      bar.appendChild(close);
      document.body.insertBefore(bar, document.body.firstChild);
    }
  }
})();
