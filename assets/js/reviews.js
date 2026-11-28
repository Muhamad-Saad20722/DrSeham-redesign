/* Patient reviews: builds the cards from a JSON file so new reviews only need a new line in
 * assets/data/reviews.json. Add data-src="<path to json>" on the #reviewsList container.
 * Each review: { "name": "اسم ا.", "text": "نص الرأي", "rating": 5 }  (rating optional, default 5)
 * Note: fetch() needs the site to be served over http(s) (not opened via file://). */
(function () {
  "use strict";

  var list = document.getElementById("reviewsList");
  if (!list) return;

  var EN = document.documentElement.lang === "en";
  var MAX_STARS = 5;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function clampRating(r) {
    r = Math.round(Number(r));
    if (!isFinite(r)) return MAX_STARS;
    return Math.min(MAX_STARS, Math.max(1, r));
  }

  function card(r) {
    var rating = clampRating(r.rating);
    var box = el("div", "card-soft review-card");

    var stars = el("div", "rating-stars");
    stars.setAttribute(
      "aria-label",
      EN ? rating + " out of 5" : rating + " من 5",
    );
    for (var i = 0; i < rating; i++) stars.appendChild(el("i", "bi bi-star-fill"));
    box.appendChild(stars);

    var p = el("p", null, r.text);
    p.lang = "ar";
    p.dir = "rtl";
    box.appendChild(p);

    var name = String(r.name || "").trim();
    var who = el("div", "who");
    var avatar = el("span", "avatar", name.charAt(0));
    avatar.setAttribute("aria-hidden", "true");
    avatar.lang = "ar";
    var nameEl = el("span", null, name);
    nameEl.lang = "ar";
    nameEl.dir = "rtl";
    who.appendChild(avatar);
    who.appendChild(nameEl);
    box.appendChild(who);
    return box;
  }

  function showError() {
    list.textContent = "";
    var p = el(
      "p",
      "text-center text-muted-2",
      EN
        ? "Reviews could not be loaded right now. Please try again later."
        : "تعذر تحميل الآراء حاليًا، حاول مرة أخرى لاحقًا.",
    );
    list.appendChild(p);
  }

  fetch(list.getAttribute("data-src"), { headers: { Accept: "application/json" } })
    .then(function (res) {
      if (!res.ok) throw new Error(res.status);
      return res.json();
    })
    .then(function (data) {
      var items = (Array.isArray(data) ? data : data && data.items) || [];
      var frag = document.createDocumentFragment();
      items.forEach(function (r) {
        if (r && r.text && r.name) frag.appendChild(card(r));
      });
      list.textContent = "";
      list.appendChild(frag);
      list.removeAttribute("aria-busy");
    })
    .catch(showError);
})();
