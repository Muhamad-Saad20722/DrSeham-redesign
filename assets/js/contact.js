/* Contact form: sends the message through WhatsApp (same number as the booking form). */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("enquiryForm");
    if (!form) return;

    var errorDiv = document.getElementById("enquiryError");
    var whatsappNumber = "201113144573";
    var EN = document.documentElement.lang === "en";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (errorDiv) {
        errorDiv.classList.add("d-none");
        errorDiv.textContent = "";
      }
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      function val(id) {
        return document.getElementById(id).value.trim();
      }
      var name = val("c_name"),
        email = val("c_email"),
        phone = val("c_phone"),
        msg = val("c_msg");

      var text = (
        EN
          ? [
              "** New message from the website **",
              "",
              " Name:  " + name,
              " Email:  " + email,
              " Phone Number:  " + phone,
              "",
              " Message: ",
              msg,
            ]
          : [
              "** رسالة جديدة من الموقع **",
              "",
              " الاسم:  " + name,
              " البريد الإلكتروني:  " + email,
              " رقم الهاتف:  " + phone,
              "",
              " الرسالة: ",
              msg,
            ]
      ).join("\n");

      var url =
        "https://wa.me/" + whatsappNumber + "?text=" + encodeURIComponent(text);
      var w = window.open(url, "_blank");
      if (!w) window.location.href = url; // popup blocked
    });
  });
})();
