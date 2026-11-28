/* Appointment booking — same endpoints and field names as the original site.
 * Set window.CLINIC_API_BASE (e.g. "https://drsehamsalem.com") before this script
 * if the pages are not served from the same origin as the Laravel backend. */
/*(function () {
 "use strict";
  var API = (window.CLINIC_API_BASE || "").replace(/\/$/, "");
  var form = document.getElementById("frontAppointmentBook");
  var slotData = document.getElementById("slotData");
  var dateInput = document.getElementById("appointmentDate");
  var successDiv = document.getElementById("successDiv");
  var errorDiv = document.getElementById("errorDiv");
  var submitBtn = document.getElementById("send_message");
  var EN = document.documentElement.lang === "en";
  var M = EN
    ? {
        pick: "Choose a date to see available times.",
        loading: "Loading available times...",
        none: "No available times on this day.",
        fail: "Could not load times, please try again.",
        chooseSlot: "Please choose an available time.",
        ok: "Appointment booked successfully",
        err: "An error occurred while submitting the booking.",
        errNet:
          "An error occurred while submitting. Please try again or contact us on WhatsApp.",
      }
    : {
        pick: "اختر التاريخ لعرض الأوقات المتاحة.",
        loading: "جاري تحميل الأوقات المتاحة...",
        none: "لا توجد أوقات متاحة في هذا اليوم.",
        fail: "تعذر تحميل الأوقات، حاول مرة أخرى.",
        chooseSlot: "من فضلك اختر وقتًا متاحًا للحجز.",
        ok: "تم حجز الموعد بنجاح",
        err: "حدث خطأ أثناء إرسال الحجز.",
        errNet:
          "حدث خطأ أثناء إرسال الحجز، حاول مرة أخرى أو تواصل معنا عبر واتساب.",
      };
  var csrf =
    (document.querySelector('meta[name="csrf-token"]') || {}).content || "";

  // Minimum date = today (local time)
  var t = new Date();
  dateInput.min =
    t.getFullYear() +
    "-" +
    String(t.getMonth() + 1).padStart(2, "0") +
    "-" +
    String(t.getDate()).padStart(2, "0");

  function msg(el, text) {
    el.textContent = text;
    el.classList.remove("d-none");
  }
  function hide(el) {
    el.classList.add("d-none");
  }
  function setSlotsMessage(text, cls) {
    slotData.innerHTML = "";
    var p = document.createElement("p");
    p.className = "mb-0 w-100 text-center " + (cls || "text-muted-2");
    p.textContent = text;
    slotData.appendChild(p);
  }
  function branch() {
    var r = form.querySelector('input[name="branch_id"]:checked');
    return r ? r.value : "";
  }

  function selectSlot(el) {
    slotData.querySelectorAll(".time-slot").forEach(function (s) {
      s.classList.remove("active");
      s.setAttribute("aria-pressed", "false");
    });
    el.classList.add("active");
    el.setAttribute("aria-pressed", "true");
    var parts = el.textContent.split("-");
    if (parts.length === 2) {
      document.getElementById("timeSlot").value = parts[0].trim();
      document.getElementById("toTime").value = parts[1].trim();
    }
  }

  // Clinic working hours (index = Date.getDay(): 0 Sunday ... 6 Saturday), 30-minute slots
  var HOURS = {
    0: ["18:30", "21:00"],
    1: ["18:30", "21:00"],
    2: ["15:30", "18:30"],
    3: ["18:30", "21:00"],
    4: ["16:30", "19:00"],
    5: ["19:00", "21:00"],
    6: ["15:30", "18:30"],
  };
  var STEP = 30;
  function toMin(t) {
    var p = t.split(":");
    return +p[0] * 60 + +p[1];
  }
  function fmt(m) {
    return (
      String(Math.floor(m / 60)).padStart(2, "0") +
      ":" +
      String(m % 60).padStart(2, "0")
    );
  }
  function localSlots(dateStr) {
    var d = dateStr.split("-");
    var day = new Date(+d[0], +d[1] - 1, +d[2]);
    var h = HOURS[day.getDay()];
    var out = [];
    if (!h) return out;
    var now = new Date();
    var isToday = day.toDateString() === now.toDateString();
    var nowMin = now.getHours() * 60 + now.getMinutes();
    for (var m = toMin(h[0]); m + STEP <= toMin(h[1]); m += STEP) {
      if (isToday && m <= nowMin) continue; // already passed
      out.push(fmt(m) + " - " + fmt(m + STEP));
    }
    return out;
  }

  function renderSlots(slots, booked) {
    slotData.innerHTML = "";
    slots.forEach(function (slot) {
      var s = document.createElement("button");
      s.type = "button";
      s.textContent = slot;
      s.setAttribute("dir", "ltr");
      s.className = "time-slot";
      if (booked.indexOf(slot) !== -1) {
        s.classList.add("booked");
        s.disabled = true;
      } else
        s.addEventListener("click", function () {
          selectSlot(s);
        });
      slotData.appendChild(s);
    });
  }

  function fetchSlots() {
    document.getElementById("timeSlot").value = "";
    document.getElementById("toTime").value = "";
    var doctor = document.getElementById("doctor_id").value,
      date = dateInput.value,
      b = branch();
    if (!date) {
      setSlotsMessage(M.pick);
      return;
    }
    var slots = localSlots(date);
    if (!slots.length) {
      setSlotsMessage(M.none);
      return;
    }
    renderSlots(slots, []);
    // Optional: grey out slots already booked, when the booking server is reachable.
    // If the request fails the slots stay available (no error is shown).
    var url =
      API +
      "/doctor-session-time?adminAppointmentDoctorId=" +
      encodeURIComponent(doctor) +
      "&date=" +
      encodeURIComponent(date) +
      "&branch_id=" +
      encodeURIComponent(b) +
      "&timezone_offset_minutes=" +
      new Date().getTimezoneOffset();
    fetch(url, { headers: { Accept: "application/json" } })
      .then(function (r) {
        return r.json();
      })
      .then(function (res) {
        if (dateInput.value !== date || !res || !res.bookedSlot) return;
        var chosen = document.getElementById("timeSlot").value;
        var booked = res.bookedSlot.filter(function (x) {
          return slots.indexOf(x) !== -1;
        });
        if (booked.length) {
          renderSlots(slots, booked);
          if (chosen) {
            slotData.querySelectorAll(".time-slot").forEach(function (el) {
              if (el.textContent.split("-")[0].trim() === chosen) selectSlot(el);
            });
          }
        }
      })
      .catch(function () {});
  }

  dateInput.addEventListener("change", fetchSlots);
  form.querySelectorAll('input[name="branch_id"]').forEach(function (r) {
    r.addEventListener("change", fetchSlots);
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    hide(successDiv);
    hide(errorDiv);
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    if (!document.getElementById("timeSlot").value) {
      msg(errorDiv, M.chooseSlot);
      return;
    }
    submitBtn.disabled = true;
    fetch(
      form.getAttribute("action") ? API + form.getAttribute("action") : "",
      {
        method: "POST",
        headers: { "X-CSRF-TOKEN": csrf, Accept: "application/json" },
        body: new FormData(form),
      },
    )
      .then(function (r) {
        return r.json();
      })
      .then(function (res) {
        if (res.success) {
          msg(successDiv, res.message || M.ok);
          form.reset();
          setSlotsMessage(M.pick);
          successDiv.scrollIntoView({ behavior: "smooth", block: "center" });
        } else {
          msg(errorDiv, res.message || M.err);
        }
      })
      .catch(function () {
        msg(errorDiv, M.errNet);
      })
      .then(function () {
        submitBtn.disabled = false;
      });
  });
})();
*/

/* Appointment booking via WhatsApp */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("frontAppointmentBook");

    if (!form) return;

    const submitBtn = document.getElementById("send_message");
    const errorDiv = document.getElementById("errorDiv");

    // WhatsApp number in international format
    const whatsappNumber = "201113144573";

    const branchNames = {
      1: "موعد بالعيادة",
      2: "زيارة منزلية",
      3: "مكالمة هاتفية",
      4: "استشارة عبر زووم",
    };

    const paymentNames = {
      0: "Cash",
      1: "Vodafone Cash",
      2: "Instapay",
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // Hide previous errors
      if (errorDiv) {
        errorDiv.classList.add("d-none");
        errorDiv.textContent = "";
      }

      // Validate required fields
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      // Patient information
      const firstName = document.getElementById("first_name").value.trim();

      const lastName = document.getElementById("last_name").value.trim();

      const phone = document.getElementById("contact").value.trim();

      const notes = document.getElementById("description").value.trim();

      // Examination method
      const branch = form.querySelector('input[name="branch_id"]:checked');

      // Payment method
      const payment = form.querySelector(
        'input[name="payment_method"]:checked',
      );

      if (!firstName || !lastName || !phone) {
        alert("من فضلك أدخل الاسم الأول واسم العائلة ورقم الهاتف.");
        return;
      }

      if (!branch || !payment) {
        alert("من فضلك اختر طريقة الكشف وطريقة الدفع.");
        return;
      }

      // Detect page language
      const isEnglish = document.documentElement.lang === "en";

      // Prepare WhatsApp message
      const message = isEnglish
        ? [
            " New Appointment Booking Request ",
            "",
            " Name:  " + firstName + " " + lastName,
            "",
            " Phone Number:  " + phone,
            "",
            " Examination Method:  " +
              {
                1: "Clinic Appointment",
                2: "Home Visit",
                3: "Phone Consultation",
                4: "Zoom Consultation",
              }[branch.value],
            "",
            " Payment Method:  " +
              {
                0: "Cash",
                1: "Vodafone Cash",
                2: "Instapay",
              }[payment.value],
            "",
            " Notes: ",
            notes || "No additional notes",
          ].join("\n")
        : [
            " طلب حجز موعد جديد ",
            "",
            " الاسم:  " + firstName + " " + lastName,
            "",
            " رقم الهاتف:  " + phone,
            "",
            " طريقة الكشف:  " + branchNames[branch.value],
            "",
            " طريقة الدفع:  " + paymentNames[payment.value],
            "",
            " الملاحظات: ",
            notes || "لا توجد ملاحظات",
          ].join("\n");

      const whatsappURL =
        "https://wa.me/" +
        whatsappNumber +
        "?text=" +
        encodeURIComponent(message);

      // Open WhatsApp
      const whatsappWindow = window.open(whatsappURL, "_blank");

      // Handle popup blocking
      if (!whatsappWindow) {
        window.location.href = whatsappURL;
      }
    });
  });
})();
