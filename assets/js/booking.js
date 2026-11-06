/* Appointment booking — same endpoints and field names as the original site.
 * Set window.CLINIC_API_BASE (e.g. "https://drsehamsalemchestclinic.com") before this script
 * if the pages are not served from the same origin as the Laravel backend. */
(function () {
  'use strict';
  var API = (window.CLINIC_API_BASE || '').replace(/\/$/, '');
  var form = document.getElementById('frontAppointmentBook');
  var slotData = document.getElementById('slotData');
  var dateInput = document.getElementById('appointmentDate');
  var successDiv = document.getElementById('successDiv');
  var errorDiv = document.getElementById('errorDiv');
  var submitBtn = document.getElementById('send_message');
  var csrf = (document.querySelector('meta[name="csrf-token"]') || {}).content || '';

  // Minimum date = today (local time)
  var t = new Date();
  dateInput.min = t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0');

  function msg(el, text) { el.textContent = text; el.classList.remove('d-none'); }
  function hide(el) { el.classList.add('d-none'); }
  function setSlotsMessage(text, cls) {
    slotData.innerHTML = '';
    var p = document.createElement('p');
    p.className = 'mb-0 w-100 text-center ' + (cls || 'text-muted-2');
    p.textContent = text;
    slotData.appendChild(p);
  }
  function branch() { var r = form.querySelector('input[name="branch_id"]:checked'); return r ? r.value : ''; }

  function selectSlot(el) {
    slotData.querySelectorAll('.time-slot').forEach(function (s) { s.classList.remove('active'); s.setAttribute('aria-pressed', 'false'); });
    el.classList.add('active'); el.setAttribute('aria-pressed', 'true');
    var parts = el.textContent.split('-');
    if (parts.length === 2) {
      document.getElementById('timeSlot').value = parts[0].trim();
      document.getElementById('toTime').value = parts[1].trim();
    }
  }

  function fetchSlots() {
    document.getElementById('timeSlot').value = '';
    document.getElementById('toTime').value = '';
    var doctor = document.getElementById('doctor_id').value, date = dateInput.value, b = branch();
    if (!doctor || !date || !b) { setSlotsMessage('اختر التاريخ لعرض الأوقات المتاحة.'); return; }
    setSlotsMessage('جاري تحميل الأوقات المتاحة...');
    var url = API + '/doctor-session-time?adminAppointmentDoctorId=' + encodeURIComponent(doctor) +
      '&date=' + encodeURIComponent(date) + '&branch_id=' + encodeURIComponent(b) +
      '&timezone_offset_minutes=' + new Date().getTimezoneOffset();
    fetch(url, { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        slotData.innerHTML = '';
        if (res.success && res.slots && res.slots.length) {
          var booked = res.bookedSlot || [];
          res.slots.forEach(function (slot) {
            var s = document.createElement('button');
            s.type = 'button'; s.textContent = slot; s.className = 'time-slot';
            if (booked.indexOf(slot) !== -1) { s.classList.add('booked'); s.disabled = true; }
            else s.addEventListener('click', function () { selectSlot(s); });
            slotData.appendChild(s);
          });
        } else {
          setSlotsMessage('لا توجد أوقات متاحة في هذا اليوم.');
        }
      })
      .catch(function () { setSlotsMessage('تعذر تحميل الأوقات، حاول مرة أخرى.', 'text-danger'); });
  }

  dateInput.addEventListener('change', fetchSlots);
  form.querySelectorAll('input[name="branch_id"]').forEach(function (r) { r.addEventListener('change', fetchSlots); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    hide(successDiv); hide(errorDiv);
    if (!form.checkValidity()) { form.reportValidity(); return; }
    if (!document.getElementById('timeSlot').value) { msg(errorDiv, 'من فضلك اختر وقتًا متاحًا للحجز.'); return; }
    submitBtn.disabled = true;
    fetch(form.getAttribute('action') ? API + form.getAttribute('action') : '', {
      method: 'POST',
      headers: { 'X-CSRF-TOKEN': csrf, 'Accept': 'application/json' },
      body: new FormData(form)
    })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res.success) {
          msg(successDiv, res.message || 'تم حجز الموعد بنجاح');
          form.reset(); setSlotsMessage('اختر التاريخ لعرض الأوقات المتاحة.');
          successDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else { msg(errorDiv, res.message || 'حدث خطأ أثناء إرسال الحجز.'); }
      })
      .catch(function () { msg(errorDiv, 'حدث خطأ أثناء إرسال الحجز، حاول مرة أخرى أو تواصل معنا عبر واتساب.'); })
      .then(function () { submitBtn.disabled = false; });
  });
})();
