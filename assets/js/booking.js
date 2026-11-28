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

    // Messages / labels per page language
    const isEnglish = document.documentElement.lang === "en";
    const MSG = isEnglish
      ? {
          needContact: "Please enter your first name, last name and phone number.",
          needChoices: "Please choose an examination method and a payment method.",
        }
      : {
          needContact: "من فضلك أدخل الاسم الأول واسم العائلة ورقم الهاتف.",
          needChoices: "من فضلك اختر طريقة الكشف وطريقة الدفع.",
        };

    function showError(text) {
      if (errorDiv) {
        errorDiv.textContent = text;
        errorDiv.classList.remove("d-none");
        errorDiv.scrollIntoView({ behavior: "smooth", block: "center" });
      } else {
        alert(text);
      }
    }

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
        showError(MSG.needContact);
        return;
      }

      if (!branch || !payment) {
        showError(MSG.needChoices);
        return;
      }

      // Prepare WhatsApp message
      const message = isEnglish
        ? [
            "** New Appointment Booking Request **",
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
            "** طلب حجز موعد جديد **",
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
