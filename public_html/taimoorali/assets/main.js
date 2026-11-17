/* Taimoor Ali site — vanilla JS, no dependencies */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  // sticky header border on scroll
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

 // mobile menu
  var burger = document.querySelector(".burger");
  var menu = document.querySelector(".mobile-menu");
  if (burger && menu) {
    var setOpen = function (open) {
      menu.classList.toggle("open", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    };
    burger.addEventListener("click", function (e) {
      e.stopPropagation();
      setOpen(!menu.classList.contains("open"));
    });
    // kisi link pe click -> band
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
    // menu ke bahar kahin click -> band
    document.addEventListener("click", function (e) {
      if (menu.classList.contains("open") && !menu.contains(e.target) && !burger.contains(e.target)) {
        setOpen(false);
      }
    });
    // Escape -> band
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
  }

  // current year
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // scroll reveal
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window && !reduce) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          ro.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { ro.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }


  // hero diagram link draw on load
  if (!reduce) {
    requestAnimationFrame(function () {
      document.querySelectorAll(".sys-link").forEach(function (l, i) {
        l.classList.add("draw");
        l.style.animationDelay = (0.15 + i * 0.12) + "s";
      });
    });
  }

  // booking form mail fallback (replace data-mailto with your preferred inbox or scheduler endpoint later)
  var form = document.querySelector("#bookingForm");
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = document.querySelector("#formMsg");
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = new FormData(form);
      var to = form.getAttribute("data-mailto") || "bookings@taimoorproject.site";
      var lines = [
        "New Shopify operations call request", "",
        "Name: " + (data.get("name") || ""),
        "Work email: " + (data.get("email") || ""),
        "Brand / store: " + (data.get("brand") || ""),
        "Platform: " + (data.get("platform") || ""),
        "Revenue / volume: " + (data.get("rev") || ""),
        "Role: " + (data.get("role") || ""),
        "Timeline: " + (data.get("timeline") || ""), "",
        "Problem:", (data.get("problem") || "")
      ];
      var subject = encodeURIComponent("Shopify operations call request");
      var body = encodeURIComponent(lines.join("\n"));
      window.location.href = "mailto:" + encodeURIComponent(to) + "?subject=" + subject + "&body=" + body;
      if (msg) {
        msg.classList.add("show");
        msg.textContent = "Your email app should open with the request prepared. Send it from there, and I’ll reply within one business day.";
      }
    });
  }
})();
