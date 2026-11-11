import json, html, os, re
OUT = os.path.join(os.path.dirname(__file__), '..', 'site')
PHONE_LOCAL = '01113144573'
PHONE_INTL = '+201113144573'
WA = 'https://wa.me/201113144573'
MAP = 'https://maps.app.goo.gl/m8B1rjm5BPKrYKun6'
FB = 'https://www.facebook.com/profile.php?id=61566491782382'
IG = 'https://www.instagram.com/dr_seham_chest'
TT = 'https://www.tiktok.com/@dr.seham.chest'
YT = 'https://www.youtube.com/@drsehammostafasalemchestclinic'
ADDRESS = ('شارع عباس العقاد الرئيسي، عمارة ٢٤، الدور السادس، العيادة يمين الأسانسير، بجوار معرض عباس العقاد التجاري '
           'ومحل يو-تيرن، أمام مطعم بازوكا ومحل LC Waikiki، مكتوب على مدخل العمارة "Snowwhite"، المنطقة الأولى، مدينة نصر.')
ADDRESS_SHORT = 'شارع عباس العقاد، المنطقة الأولى، مدينة نصر'

NAV = [('index.html', 'الرئيسية'), ('services.html', 'الخدمات'), ('testimonials.html', 'آراء المرضى'), ('contact.html', 'اتصل بنا')]

SERVICES = [
    ('search-heart', 'تشخيص ومتابعة الأمراض الصدرية المختلفة', 'باستخدام التحاليل والإشاعات المناسبة واختبارات وظائف التنفس.'),
    ('flower1', 'استشارة أمراض الحساسية', 'تقييم وعلاج حالات الحساسية والأمراض التنفسية الموسمية.'),
    ('virus', 'استشارة الدرن (السل)', 'تشخيص ومتابعة حالات الدرن (السل) للرئة.'),
    ('clipboard2-pulse', 'متابعة الأمراض المزمنة للصدر', 'متابعة الحالات المزمنة مثل الربو والتهاب الشعب الهوائية المزمن.'),
    ('moon-stars', 'تشخيص اضطرابات النوم', 'تقييم حالات انقطاع النفس الانسدادي والنوم لدى البالغين والسمنة.'),
    ('balloon-heart', 'استشارات للأطفال من 6 أشهر', 'رعاية طبية للأطفال بدءًا من عمر 6 أشهر.'),
    ('wind', 'علاج الربو', 'خطط علاجية فردية للسيطرة على الربو والوقاية من النوبات.'),
    ('lungs', 'علاج التهابات الرئة المزمنة', 'علاج الالتهابات الرئوية المزمنة والمتكررة لتخفيف الأعراض وتحسين التنفس.'),
    ('lungs', 'علاج الانسداد الرئوي المزمن', 'علاج مرض الانسداد الرئوي المزمن لتحسين التنفس وجودة الحياة.'),
    ('droplet', 'التهاب الشعب الهوائية الحاد والمزمن', 'معالجة التهاب الشعب الهوائية للحد من الأعراض وتحسين التنفس.'),
    ('activity', 'الفشل التنفسي والأكسجين المنزلي', 'متابعة الحالات الحرجة التي تحتاج إلى دعم تنفسي.'),
    ('eyedropper', 'اختبارات الدم لأمراض الصدر', 'تحاليل دم لتشخيص الأمراض التنفسية والالتهابات الرئوية.'),
    ('heart-pulse', 'تقييم ضيق التنفس', 'تقييم أسباب ضيق التنفس المزمن أو المفاجئ لتحديد العلاج المناسب.'),
    ('virus2', 'التهاب الرئة الفيروسي والبكتيري', 'علاج الالتهابات الرئوية الناتجة عن الفيروسات والبكتيريا.'),
    ('shield-check', 'الدرن (السل) الكامن', 'تحديد وعلاج حالات الدرن الكامن لمنع تطور المرض.'),
    ('bandaid', 'المتابعة بعد الجراحة الرئوية', 'متابعة المرضى بعد عمليات الرئة لضمان الشفاء الكامل.'),
]

FEATURES = [
    ('mortarboard', 'خبرة واسعة', 'أمراض الصدر والدرن والعناية المركزة والباطنة، مع خطط علاج مخصصة وفحص شامل ومتابعة بقياس الأكسجين.'),
    ('eyedropper', 'معمل تحاليل داخل العيادة', 'نتائج سريعة ودقيقة دون الحاجة للذهاب إلى معامل خارجية.'),
    ('people', 'رعاية شاملة', 'رعاية طبية لطيفة لكبار السن والبالغين والأطفال فوق 6 أشهر.'),
    ('clock-history', 'مواعيد مرنة', 'مواعيد صباحية ومسائية طوال الأسبوع وفي عطلة نهاية الأسبوع.'),
    ('hospital', 'التأمين الطبي', 'تقبل العيادة تعاقدات العديد من شركات التأمين والنقابات.'),
    ('percent', 'خصومات خاصة', 'خصومات للمتابعة الشهرية وللأشقاء.'),
    ('whatsapp', 'تواصل مريح', 'إرسال المتابعة ونتائج التحاليل والأشعة مباشرة عبر واتساب.'),
    ('house-heart', 'زيارات منزلية', 'زيارات منزلية لكبار السن وذوي الاحتياجات الخاصة.'),
    ('camera-video', 'استشارات عن بُعد', 'جلسات أونلاين لتوفير الرعاية من أي مكان.'),
    ('translate', 'التواصل باللغتين', 'تتحدث الدكتورة سهام الإنجليزية بطلاقة لتسهيل التواصل.'),
    ('lock-fill', 'خصوصية المرضى', 'خصوصية المرضى من أهم المبادئ الأساسية في العيادة.'),
    ('tags', 'خصومات التحاليل والأشعة', 'خصومات خاصة على جميع التحاليل والأشعة المطلوبة.'),
    ('building-up', 'تجهيزات العيادة', 'مصعد وتكييف ووسائل دفع إلكتروني (إنستاباي وفودافون كاش).'),
]

FAQ_HOME = [
    ('هل ممارسة الرياضة المنتظمة تضر الأطفال المصابين بالربو؟', 'على عكس الاعتقاد الشائع بأن ممارسة الرياضة غير مناسبة للأطفال المصابين بالربو، فإن ممارسة الرياضة المنتظمة وخاصة السباحة ثبتت بالعديد من الدراسات أنها مفيدة جدًا للأطفال المصابين بالربو.'),
    ('هل عدوى الدرن (السل) في الغدد الليمفاوية معدية لأفراد العائلة؟', 'لا، العدوى غير معدية إلا إذا كان المريض يعاني من الدرن (السل) الرئوي النشط الذي يمكن أن ينتشر عبر الهواء أثناء التحدث أو السعال أو العطس.'),
    ('هل التهاب الأنف التحسسي يسبب الربو القصبي؟', 'لا، لا يمكن أن يسبب الربو القصبي مباشرة، لكن كلا المرضين مرتبطان بحالات التهابية مزمنة تؤثر على المجاري الهوائية العليا والسفلى. كما أن الالتهاب الناتج عن التهاب الأنف التحسسي قد يزيد من شدة الربو، ومع علاج التهاب الأنف بالدواء يمكن تحسين السيطرة على الربو وتقليل الحاجة للطوارئ، لذا يوصى بتشخيص وعلاج كلا المرضين.'),
    ('ما هي الآثار الجانبية للقاح الإنفلونزا الموسمية؟', 'ألم واحمرار وتورم في موقع الحقن. الأعراض الأقل شيوعًا تشمل الصداع، التعب، وارتفاع طفيف في درجة الحرارة. ومع ذلك، من المهم الوقاية من العدوى الشديدة بالإنفلونزا والالتهاب الرئوي الفيروسي، خاصة للمرضى المصابين بالربو القصبي، أمراض الانسداد الرئوي المزمن، الأمراض الرئوية الخلالية، الأمراض القلبية المزمنة والسكري.'),
    ('ما هي عدوى الدرن (السل) الكامنة وهل يحتاج جميع الحالات للعلاج؟', 'عدوى الدرن (السل) الكامنة هي حالة استجابة مناعية مستمرة لمستضدات متفطرة الدرنية (السلية) باستخدام اختبار الجلد للسل أو اختبار إطلاق إنترفيرون جاما (IGRA) بدون أي دليل على وجود الدرن (السل) النشط. في هذه الحالة، يُعالج فقط الأفراد ذوي المناعة الضعيفة، والذين كانوا على اتصال وثيق بأشخاص مصابين بالدرن (السل) الرئوي النشط.'),
]
FAQ_CONTACT = [
    ('متى يجب أن أزور عيادة الصدر؟', 'يجب زيارة عيادة الصدر إذا كنت تعاني من سعال مستمر، ضيق في التنفس، أزيز، ألم في الصدر، أو أي صعوبات في التنفس تستمر لأكثر من بضعة أيام.'),
    ('هل يمكن أن يؤثر التدخين أو الفيبينغ على وظيفة الرئة حتى لو كنت شابًا؟', 'نعم. يمكن أن يسبب التدخين والفيبينغ التهابًا مبكرًا في المجاري الهوائية، ويقلل من سعة الرئة، ويؤدي إلى السعال المزمن، ويزيد من خطر الإصابة بالربو، ويسبب مشاكل تنفسية طويلة المدى حتى في سن مبكرة.'),
    ('هل تعالجون الربو، الانسداد الرئوي المزمن والحساسية؟', 'نعم، نتعامل مع الأمراض التنفسية المزمنة مثل الربو، الانسداد الرئوي المزمن، التهاب الشعب الهوائية، انقطاع النفس أثناء النوم، والحساسية التنفسية بخطط علاجية مخصصة.'),
]
REVIEWS = [tuple(x) for x in json.load(open(os.path.join(os.path.dirname(__file__), 'testimonials.json'), encoding='utf8'))]
# a clean "featured" subset with substantive text for the home carousel
FEATURED = [r for r in REVIEWS if len(r[0]) > 18 and 'خمس نجوم' not in r[0]][:9]
VIDEOS = ['4fR9_fc_RaU', 'LbKGTHSXQtw', 'dNXVVzcuNfY']


def e(s):
    return html.escape(s, quote=True)


def head(title, desc, active, extra_head=''):
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<script id="lang-redirect">try{{if(localStorage.getItem('clinic-lang')==='en'&&!/[?&]lang=ar/.test(location.search)){{location.replace('en/'+(location.pathname.split('/').pop()||'index.html')+location.search+location.hash)}}}}catch(e){{}}</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0d3a30">
<meta name="author" content="MAZCODEX">
<link rel="alternate" hreflang="ar" href="{active}">
<link rel="alternate" hreflang="en" href="en/{active}">
<!-- Laravel: inject the CSRF token here, e.g. content="{{{{ csrf_token() }}}}" -->
<meta name="csrf-token" content="">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/doctor.webp">
<link rel="icon" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/favicon.png">
<link rel="stylesheet" href="assets/css/bootstrap.rtl.min.css">
<link rel="stylesheet" href="assets/css/bootstrap-icons.min.css">
<link rel="stylesheet" href="assets/css/site.css">
{extra_head}</head>
<body>
<a class="skip-link" href="#main">تخطي إلى المحتوى</a>
<div class="topbar d-none d-lg-block">
  <div class="container d-flex justify-content-between align-items-center py-2">
    <span><i class="bi bi-geo-alt"></i>{ADDRESS_SHORT}</span>
    <span class="d-flex gap-4">
      <a href="tel:{PHONE_INTL}"><i class="bi bi-telephone"></i><span class="ltr">{PHONE_LOCAL}</span></a>
      <a href="{WA}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i>واتساب</a>
    </span>
  </div>
</div>
<header class="sticky-top">
<nav class="navbar navbar-expand-lg site-nav" aria-label="القائمة الرئيسية">
  <div class="container">
    <a class="navbar-brand" href="index.html" aria-label="د. سهام سالم - عيادة الصدر"><img src="assets/img/logo.webp" alt="شعار عيادة د. سهام سالم للصدر" width="78" height="52"></a>
    <a class="lang-switch order-lg-3" href="en/{active}" hreflang="en" lang="en" data-lang-switch="en" aria-label="Switch to English"><i class="bi bi-translate"></i><span>EN</span></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav" aria-controls="nav" aria-expanded="false" aria-label="فتح القائمة"><span class="navbar-toggler-icon"></span></button>
    <div class="collapse navbar-collapse" id="nav">
      <ul class="navbar-nav mx-lg-auto mb-2 mb-lg-0 gap-lg-1">
{''.join(f'        <li class="nav-item"><a class="nav-link{" active" if h == active else ""}" href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' + chr(10) for h, t in NAV)}      </ul>
      <a class="btn btn-primary" href="appointment.html"><i class="bi bi-calendar-check me-1"></i> احجز موعدك</a>
    </div>
  </div>
</nav>
</header>
<main id="main">
'''


def foot():
    links = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV + [('appointment.html', 'حجز موعد')])
    return f'''</main>
<footer class="site-footer">
  <div class="container">
    <div class="row g-4">
      <div class="col-lg-5">
        <a class="footer-logo mb-3" href="index.html"><img src="assets/img/logo.webp" alt="عيادة د. سهام سالم للصدر" width="81" height="54" loading="lazy"></a>
        <p class="mt-3 pe-lg-5">عيادة متخصصة في أمراض الصدر والحساسية والدرن (السل)، بخبرة تزيد عن ٢٠ عامًا ورعاية تهتم بالتفاصيل.</p>
        <div class="social d-flex gap-2 mt-3">
          <a href="{FB}" target="_blank" rel="noopener" aria-label="فيسبوك"><i class="bi bi-facebook"></i></a>
          <a href="{IG}" target="_blank" rel="noopener" aria-label="إنستغرام"><i class="bi bi-instagram"></i></a>
          <a href="{TT}" target="_blank" rel="noopener" aria-label="تيك توك"><i class="bi bi-tiktok"></i></a>
          <a href="{YT}" target="_blank" rel="noopener" aria-label="يوتيوب"><i class="bi bi-youtube"></i></a>
        </div>
      </div>
      <div class="col-6 col-lg-3"><h4>روابط سريعة</h4><ul>{links}</ul></div>
      <div class="col-6 col-lg-4">
        <h4>تواصل معنا</h4>
        <ul>
          <li><i class="bi bi-telephone me-2 text-amber"></i><a href="tel:{PHONE_INTL}" class="ltr">{PHONE_LOCAL}</a></li>
          <li><i class="bi bi-whatsapp me-2 text-amber"></i><a href="{WA}" target="_blank" rel="noopener">واتساب</a></li>
          <li><i class="bi bi-geo-alt me-2 text-amber"></i><a href="{MAP}" target="_blank" rel="noopener">{ADDRESS_SHORT}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom d-flex flex-column flex-md-row justify-content-between gap-2">
      <span>© 2026 د. سهام سالم — جميع الحقوق محفوظة</span>
      <span>Powered by MAZCODEX</span>
    </div>
  </div>
</footer>
<div class="fab-stack">
  <a class="fab map" href="{MAP}" target="_blank" rel="noopener" aria-label="موقع العيادة على الخريطة"><i class="bi bi-geo-alt-fill"></i></a>
  <a class="fab wa" href="{WA}" target="_blank" rel="noopener" aria-label="تواصل عبر واتساب"><i class="bi bi-whatsapp"></i></a>
</div>
<div class="mobile-cta">
  <a class="btn btn-outline-primary" href="tel:{PHONE_INTL}"><i class="bi bi-telephone me-1"></i> اتصال</a>
  <a class="btn btn-primary" href="appointment.html"><i class="bi bi-calendar-check me-1"></i> احجز موعد</a>
</div>
<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/js/main.js"></script>
'''


def page_hero(title, sub, crumb):
    return f'''<section class="page-hero">
  <div class="container">
    <nav aria-label="مسار التنقل"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="index.html">الرئيسية</a></li><li class="breadcrumb-item active" aria-current="page">{crumb}</li></ol></nav>
    <h1>{title}</h1>
    <p>{sub}</p>
  </div>
</section>
'''


def service_card(s, i=0):
    return f'''<div class="col-sm-6 col-lg-4 reveal"><article class="card-soft service-card"><span class="icon-tile"><i class="bi bi-{s[0]}"></i></span><h3>{s[1]}</h3><p>{s[2]}</p></article></div>
'''


def feature_item(f):
    return f'''<div class="col-md-6 col-xl-4 reveal"><div class="card-soft feature-item"><span class="icon-tile amber"><i class="bi bi-{f[0]}"></i></span><div><h3>{f[1]}</h3><p>{f[2]}</p></div></div></div>
'''


def faq(items, pid):
    out = f'<div class="accordion" id="{pid}">'
    for i, (q, a) in enumerate(items):
        out += f'''<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button{'' if i == 0 else ' collapsed'}" type="button" data-bs-toggle="collapse" data-bs-target="#{pid}-{i}" aria-expanded="{'true' if i == 0 else 'false'}" aria-controls="{pid}-{i}">{q}</button></h3><div id="{pid}-{i}" class="accordion-collapse collapse{' show' if i == 0 else ''}" data-bs-parent="#{pid}"><div class="accordion-body">{a}</div></div></div>'''
    return out + '</div>'


def review_card(r):
    text, name = r
    ini = name.strip()[0]
    return f'''<div class="card-soft review-card"><div class="rating-stars" aria-label="5 من 5"><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i></div><p lang="ar" dir="rtl">{e(text)}</p><div class="who"><span class="avatar" aria-hidden="true" lang="ar">{e(ini)}</span><span lang="ar" dir="rtl">{e(name)}</span></div></div>'''


def cta_band():
    return f'''<section class="section pt-0">
  <div class="container">
    <div class="cta-band">
      <div class="row align-items-center g-4 position-relative" style="z-index:1">
        <div class="col-lg-8">
          <h2 class="h1 fs-2 mb-2">صحة رئتيك تبدأ بموعد واحد</h2>
          <p class="mb-0 fs-5">احجز كشفًا في العيادة أو زيارة منزلية أو استشارة عن بُعد — في الوقت الذي يناسبك.</p>
        </div>
        <div class="col-lg-4 d-flex flex-wrap gap-2 justify-content-lg-end">
          <a class="btn btn-amber btn-lg" href="appointment.html"><i class="bi bi-calendar-check me-1"></i> احجز الآن</a>
          <a class="btn btn-outline-light-2 btn-lg" href="{WA}" target="_blank" rel="noopener"><i class="bi bi-whatsapp me-1"></i> واتساب</a>
        </div>
      </div>
    </div>
  </div>
</section>
'''


def write(name, body):
    with open(os.path.join(OUT, name), 'w', encoding='utf8') as f:
        f.write(body)


# ------------------------------------------------------------------ INDEX
jsonld = json.dumps({
    "@context": "https://schema.org", "@type": "Physician", "name": "د. سهام سالم",
    "medicalSpecialty": "Pulmonary", "description": "استشارية أمراض الصدر والحساسية والدرن (السل)",
    "telephone": PHONE_INTL, "address": {"@type": "PostalAddress", "addressLocality": "مدينة نصر", "addressCountry": "EG", "streetAddress": ADDRESS_SHORT},
    "sameAs": [FB, IG, TT, YT], "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.98", "reviewCount": "722"}
}, ensure_ascii=False)

idx = head('د. سهام سالم | استشارية أمراض الصدر والحساسية والدرن - مدينة نصر',
           'عيادة د. سهام سالم لأمراض الصدر والحساسية والدرن (السل) بمدينة نصر. أكثر من ٢٠ عامًا خبرة، كشف بالعيادة وزيارات منزلية واستشارات عن بُعد. احجز موعدك الآن.',
           'index.html', f'<script type="application/ld+json">{jsonld}</script>\n')
idx += f'''
<section class="hero">
  <div class="container">
    <div class="row align-items-center gy-5 gx-lg-5">
      <div class="col-lg-7 pb-lg-5">
        <span class="hero-badge mb-3"><i class="bi bi-patch-check-fill"></i> استشارية أمراض الصدر والحساسية والدرن (السل)</span>
        <h1 class="mb-3">تنفّس براحة مع <span class="accent">د. سهام سالم</span></h1>
        <p class="lead mb-4">أكثر من ٢٠ عامًا من الخبرة في تشخيص وعلاج أمراض الصدر والدرن (السل)، بما في ذلك وحدات العناية المركزة — في عيادة هادئة تهتم بكل مريض.</p>
        <div class="d-flex flex-wrap gap-3">
          <a class="btn btn-amber btn-lg" href="appointment.html"><i class="bi bi-calendar-check me-1"></i> احجز موعدك</a>
          <a class="btn btn-outline-light-2 btn-lg" href="{WA}" target="_blank" rel="noopener"><i class="bi bi-whatsapp me-1"></i> تحدث معنا عبر واتساب</a>
        </div>
        <div class="d-flex flex-wrap gap-4 mt-4 pt-2 text-white-50">
          <span><i class="bi bi-hospital text-amber me-1"></i> نقبل التأمين الطبي</span>
          <span><i class="bi bi-house-heart text-amber me-1"></i> زيارات منزلية</span>
          <span><i class="bi bi-camera-video text-amber me-1"></i> استشارات عن بُعد</span>
        </div>
      </div>
      <div class="col-lg-5">
        <div class="hero-figure">
          <img src="assets/img/doctor.webp" alt="د. سهام سالم، استشارية أمراض الصدر" width="700" height="765" fetchpriority="high">
          <div class="float-card fc-1"><span class="ico"><i class="bi bi-star-fill"></i></span><div><strong class="ltr">4.98 / 5</strong><small>٧٢٢+ تقييم من المرضى</small></div></div>
          <div class="float-card fc-2"><span class="ico"><i class="bi bi-people-fill"></i></span><div><strong>+١٠٬٠٠٠</strong><small>مريض يثقون بها</small></div></div>
        </div>
      </div>
    </div>
  </div>
  <div class="stat-strip">
    <div class="container">
      <div class="row g-0">
        <div class="col-6 col-md-3 stat"><div class="num">+٢٠</div><div class="lbl">عامًا من الخبرة</div></div>
        <div class="col-6 col-md-3 stat"><div class="num">+١٠٬٠٠٠</div><div class="lbl">مريض يثقون بنا</div></div>
        <div class="col-6 col-md-3 stat"><div class="num">٩٨٪</div><div class="lbl">ملاحظات إيجابية حقيقية</div></div>
        <div class="col-6 col-md-3 stat"><div class="num">+٤</div><div class="lbl">سنوات في العناية المركزة</div></div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="about">
  <div class="container">
    <div class="row align-items-center gy-5 gx-lg-5">
      <div class="col-lg-5 reveal">
        <div class="about-photo">
          <img class="main" src="assets/img/xray-review.webp" alt="مراجعة أشعة الصدر مع الطبيبة" width="900" height="676" loading="lazy">
          <div class="tag"><strong>المركز الثاني</strong>على خريجي الزمالة المصرية لأمراض الصدر</div>
        </div>
      </div>
      <div class="col-lg-7 reveal">
        <span class="eyebrow">عن الدكتورة</span>
        <h2 class="section-title">د. سهام سالم — استشارية أمراض الصدر والحساسية والدرن (السل)</h2>
        <p class="lead-sm mb-4">حاصلة على ماجستير أمراض الصدر والدرن (السل) من جامعة القاهرة والزمالة المصرية لأمراض الصدر، وعملت في وحدات العناية المركزة وعدد من أكبر مستشفيات الصدر.</p>
        <ul class="cred-list">
          <li><i class="bi bi-check2-circle"></i><span>أكثر من ٢٠ عامًا خبرة في أمراض الصدر والدرن (السل)</span></li>
          <li><i class="bi bi-check2-circle"></i><span>مستشفيات صدر العباسية، ومستشفى التأمين الصحي بمدينة نصر، ومستشفى النصر التخصصي (رابعة العدوية سابقًا)</span></li>
          <li><i class="bi bi-check2-circle"></i><span>أكثر من ٤ سنوات خبرة في وحدة العناية المركزة</span></li>
          <li><i class="bi bi-check2-circle"></i><span>ماجستير أمراض الصدر والدرن (السل) — القصر العيني، جامعة القاهرة</span></li>
          <li><i class="bi bi-check2-circle"></i><span>الزمالة المصرية لأمراض الصدر</span></li>
        </ul>
        <div class="d-flex flex-wrap gap-2 mt-4">
          <a class="btn btn-primary" href="appointment.html">احجز كشف</a>
          <a class="btn btn-outline-primary" href="testimonials.html">آراء المرضى</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section bg-green-50" id="services">
  <div class="container">
    <div class="row align-items-end g-3 mb-5">
      <div class="col-md-8 reveal">
        <span class="eyebrow">خدمات العيادة</span>
        <h2 class="section-title mb-0">خدمات عيادة الصدر المتميزة</h2>
      </div>
      <div class="col-md-4 text-md-start reveal"><a class="btn btn-outline-primary" href="services.html">جميع الخدمات <i class="bi bi-arrow-left ms-1"></i></a></div>
    </div>
    <div class="row g-4">
{''.join(service_card(s) for s in SERVICES[1:7])}    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="row gy-5 gx-lg-5 align-items-center">
      <div class="col-lg-5 reveal">
        <span class="eyebrow">لماذا عيادتنا</span>
        <h2 class="section-title">نحرص على راحتك وصحتك</h2>
        <p class="lead-sm">خدمات متميزة تلبي احتياجات المرضى مع الحفاظ على راحتهم وخصوصيتهم.</p>
        <img class="rounded-4 w-100 mt-3 d-none d-lg-block" src="assets/img/clinic-desk.webp" alt="الدكتورة سهام في العيادة" width="200" height="200" loading="lazy" style="max-width:220px;box-shadow:0 20px 40px -24px rgba(13,58,48,.5)">
        <a class="btn btn-primary mt-4" href="contact.html">تواصل معنا</a>
      </div>
      <div class="col-lg-7">
        <div class="row g-3">
{''.join(f'<div class="col-sm-6 reveal"><div class="card-soft feature-item"><span class="icon-tile amber"><i class="bi bi-{f[0]}"></i></span><div><h3>{f[1]}</h3><p>{f[2]}</p></div></div></div>' + chr(10) for f in [FEATURES[3], FEATURES[4], FEATURES[7], FEATURES[8], FEATURES[1], FEATURES[12]])}        </div>
      </div>
    </div>
  </div>
</section>

<section class="section bg-green-50">
  <div class="container">
    <div class="text-center mb-5 reveal"><span class="eyebrow">خطوات بسيطة</span><h2 class="section-title">اعثر على الرعاية المناسبة لك</h2></div>
    <div class="row g-4">
      <div class="col-md-4 step reveal"><div class="n">1</div><h3 class="h5">استشارة الدكتورة سهام</h3><p class="text-muted-2 mb-0">استشر الدكتورة لأمراض الصدر والحساسية والدرن (السل).</p></div>
      <div class="col-md-4 step reveal"><div class="n">2</div><h3 class="h5">حجز موعد</h3><p class="text-muted-2 mb-0">حدد موعدًا بسهولة — بالعيادة أو زيارة منزلية أو عن بُعد.</p></div>
      <div class="col-md-4 step reveal"><div class="n">3</div><h3 class="h5">المتابعة والدفع</h3><p class="text-muted-2 mb-0">استلم المتابعات وأكمل الدفع نقدًا أو إلكترونيًا.</p></div>
    </div>
  </div>
</section>

<section class="section" id="reviews">
  <div class="container">
    <div class="row gy-5 gx-lg-5 align-items-center">
      <div class="col-lg-4 reveal">
        <span class="eyebrow">آراء المرضى</span>
        <h2 class="section-title">ثقة تتحدث عنها كلمات مرضانا</h2>
        <div class="reviews-score mt-4">
          <div class="big">4.98</div>
          <div class="rating-stars my-2 fs-5"><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i></div>
          <div class="text-white-50">٧٢٢+ تقييم 5 نجوم من مرضانا الراضين — أكثر من ١٠٬٠٠٠ مريض يثقون في علاج د. سهام سالم</div>
        </div>
        <a class="btn btn-outline-primary mt-4" href="testimonials.html">كل الآراء <i class="bi bi-arrow-left ms-1"></i></a>
      </div>
      <div class="col-lg-8 reveal">
        <div id="reviewsCarousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="6000" aria-label="آراء المرضى">
          <div class="carousel-inner">
{''.join('<div class="carousel-item' + (' active' if i == 0 else '') + '"><div class="row g-3">' + ''.join(f'<div class="col-md-6">{review_card(r)}</div>' for r in FEATURED[i:i+2]) + '</div></div>' + chr(10) for i in range(0, len(FEATURED) - 1, 2))}          </div>
          <div class="carousel-nav d-flex gap-2 justify-content-center mt-4">
            <button class="btn btn-outline-primary" data-bs-target="#reviewsCarousel" data-bs-slide="prev" aria-label="السابق"><i class="bi bi-chevron-right"></i></button>
            <button class="btn btn-outline-primary" data-bs-target="#reviewsCarousel" data-bs-slide="next" aria-label="التالي"><i class="bi bi-chevron-left"></i></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section bg-green-900" id="videos">
  <div class="container">
    <div class="text-center mb-5 reveal"><span class="eyebrow" style="color:#f0b968">فيديوهات</span><h2 class="section-title text-white">تعرّف على العيادة والدكتورة</h2></div>
    <div class="row g-4">
{''.join(f'<div class="col-md-4 reveal"><button type="button" class="video-card" data-bs-toggle="modal" data-bs-target="#videoModal" data-video="{v}" aria-label="تشغيل الفيديو"><img src="https://img.youtube.com/vi/{v}/hqdefault.jpg" alt="" loading="lazy"><span class="play"><span><i class="bi bi-play-fill"></i></span></span></button></div>' + chr(10) for v in VIDEOS)}    </div>
    <div class="text-center mt-4"><a class="btn btn-outline-light-2" href="{YT}" target="_blank" rel="noopener"><i class="bi bi-youtube me-1"></i> قناتنا على يوتيوب</a></div>
  </div>
</section>
<div class="modal fade" id="videoModal" tabindex="-1" aria-label="مشغل الفيديو" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered modal-lg"><div class="modal-content bg-black border-0 rounded-4 overflow-hidden">
    <button type="button" class="btn-close btn-close-white position-absolute top-0 start-0 m-3" style="z-index:2" data-bs-dismiss="modal" aria-label="إغلاق"></button>
    <div class="ratio ratio-16x9"><iframe id="videoFrame" src="" title="فيديو" allow="accelerometer; autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>
  </div></div>
</div>

<section class="section" id="faq">
  <div class="container">
    <div class="row gy-5 gx-lg-5">
      <div class="col-lg-4 reveal"><span class="eyebrow">أسئلة شائعة</span><h2 class="section-title">نحن هنا لرعايتك بكل اهتمام</h2><p class="lead-sm">إجابات مختصرة على أكثر الأسئلة التي تصلنا من المرضى.</p></div>
      <div class="col-lg-8 reveal">{faq(FAQ_HOME, 'faqHome')}</div>
    </div>
  </div>
</section>
{cta_band()}
'''
idx += foot() + '</body>\n</html>\n'
write('index.html', idx)

# ------------------------------------------------------------------ SERVICES
sv = head('الخدمات | عيادة د. سهام سالم للصدر', 'جميع خدمات عيادة د. سهام سالم: الربو، الحساسية، الدرن (السل)، الانسداد الرئوي المزمن، اضطرابات النوم، الأطفال من 6 أشهر وغيرها.', 'services.html')
sv += page_hero('علاجاتنا وخدماتنا', 'نقبل تعاقدات شركات التأمين والنقابات المختلفة — خدمات عيادة الصدر المتميزة.', 'الخدمات')
sv += f'''<section class="section">
  <div class="container">
    <div class="mb-5 reveal"><span class="eyebrow">العلاجات المتخصصة</span><h2 class="section-title">ما الذي نعالجه؟</h2></div>
    <div class="row g-4">
{''.join(service_card(s) for s in SERVICES)}    </div>
  </div>
</section>
<section class="section bg-green-50">
  <div class="container">
    <div class="mb-5 reveal"><span class="eyebrow">الخدمات والمميزات</span><h2 class="section-title">رعاية متكاملة في مكان واحد</h2></div>
    <div class="row g-3">
{''.join(feature_item(f) for f in FEATURES)}    </div>
  </div>
</section>
{cta_band()}
'''
sv += foot() + '</body>\n</html>\n'
write('services.html', sv)

# ------------------------------------------------------------------ TESTIMONIALS
tm = head('آراء المرضى | عيادة د. سهام سالم للصدر', 'اقرأ آراء مرضى د. سهام سالم: أكثر من ٧٢٢ تقييم بدرجة 4.98 من 5.', 'testimonials.html')
tm += page_hero('آراء المرضى', 'أكثر من ١٠٬٠٠٠ مريض يثقون في علاج د. سهام سالم.', 'آراء المرضى')
tm += f'''<section class="section">
  <div class="container">
    <div class="row g-4 mb-5 align-items-center reveal">
      <div class="col-lg-4"><div class="reviews-score text-center"><div class="big">4.98</div><div class="rating-stars my-2 fs-5"><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i></div><div class="text-white-50">٧٢٢+ تقييم — ٩٨٪ ملاحظات إيجابية</div></div></div>
      <div class="col-lg-8"><h2 class="section-title">ثقة بُنيت على مدى سنوات</h2><p class="lead-sm mb-0">نعتز بكل كلمة من مرضانا، وهذه بعض الآراء التي وصلتنا.</p></div>
    </div>
    <div class="masonry">
{''.join(review_card(r) + chr(10) for r in REVIEWS)}    </div>
  </div>
</section>
{cta_band()}
'''
tm += foot() + '</body>\n</html>\n'
write('testimonials.html', tm)

# ------------------------------------------------------------------ APPOINTMENT
ap = head('حجز موعد | عيادة د. سهام سالم للصدر', 'احجز موعدًا مع د. سهام سالم: كشف بالعيادة، زيارة منزلية، مكالمة هاتفية أو استشارة عبر زوم.', 'appointment.html')
ap += page_hero('حجز موعد', 'اختر نوع الكشف والتاريخ والوقت المناسب لك، وسيصلك تأكيد الحجز.', 'حجز موعد')
visit = [('1', 'building', 'موعد بالعيادة'), ('2', 'house-heart', 'زيارة منزلية'), ('3', 'telephone', 'مكالمة هاتفية'), ('4', 'camera-video', 'استشارة عبر زووم')]
pay = [('0', 'cash-coin', 'Cash'), ('1', 'phone', 'Vodafone Cash'), ('2', 'credit-card-2-front', 'Instapay')]
ap += f'''<section class="section">
  <div class="container">
    <div class="row g-4">
      <div class="col-lg-8">
        <form class="form-card" id="frontAppointmentBook" action="/front-appointment-book" method="post" novalidate>
          <input type="hidden" name="_token" value="">
          <input type="radio" name="gender" value="1" checked hidden>
          <input type="hidden" name="doctor_id" id="doctor_id" value="1163">
          <h2 class="h4 mb-4"><span class="text-amber">1.</span> بياناتك</h2>
          <div class="row g-3 mb-4">
            <div class="col-md-4"><label class="form-label" for="first_name">الاسم الأول</label><input type="text" class="form-control" name="first_name" id="first_name" required autocomplete="given-name"></div>
            <div class="col-md-4"><label class="form-label" for="last_name">اسم العائلة</label><input type="text" class="form-control" name="last_name" id="last_name" required autocomplete="family-name"></div>
            <div class="col-md-4"><label class="form-label" for="contact">رقم الهاتف</label><input type="tel" class="form-control" name="contact" id="contact" required autocomplete="tel" inputmode="tel" dir="ltr" placeholder="01XXXXXXXXX"></div>
          </div>
          <h2 class="h4 mb-3"><span class="text-amber">2.</span> اختر طريقة الكشف</h2>
          <div class="choice-grid cols-4 mb-4" role="radiogroup" aria-label="طريقة الكشف">
{''.join(f'<div class="choice"><input type="radio" name="branch_id" id="branch{v}" value="{v}"{" checked" if v == "1" else ""}><label for="branch{v}"><i class="bi bi-{ic}"></i>{t}</label></div>' + chr(10) for v, ic, t in visit)}          </div>
          <h2 class="h4 mb-3"><span class="text-amber">3.</span> التاريخ والوقت</h2>
          <div class="row g-3 mb-3">
            <div class="col-md-6"><label class="form-label" for="appointmentDate">تاريخ الحجز</label><input class="form-control" id="appointmentDate" type="date" name="date" required></div>
          </div>
          <input type="hidden" name="from_time" id="timeSlot" value=""><input type="hidden" name="to_time" id="toTime" value="">
          <label class="form-label">الأوقات المتاحة</label>
          <div class="slots-box mb-4" id="slotsBox" aria-live="polite"><div class="slots" id="slotData"><p class="mb-0 text-muted-2 w-100 text-center">اختر التاريخ لعرض الأوقات المتاحة.</p></div></div>
          <h2 class="h4 mb-3"><span class="text-amber">4.</span> طريقة الدفع</h2>
          <div class="choice-grid cols-3 mb-4" role="radiogroup" aria-label="طريقة الدفع">
{''.join(f'<div class="choice"><input type="radio" name="payment_method" id="pay{v}" value="{v}"{" checked" if v == "0" else ""}><label for="pay{v}"><i class="bi bi-{ic}"></i>{t}</label></div>' + chr(10) for v, ic, t in pay)}          </div>
          <div class="mb-4"><label class="form-label" for="description">ملاحظات (اختياري)</label><textarea class="form-control" name="description" id="description" rows="3" placeholder="اكتب أي معلومات تود إخبارنا بها"></textarea></div>
          <div id="successDiv" class="alert alert-success d-none" role="status"></div>
          <div id="errorDiv" class="alert alert-danger d-none" role="alert"></div>
          <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
            <p class="mb-0 small text-muted-2"><i class="bi bi-lock-fill me-1"></i> نحن ملتزمون بحماية خصوصيتك. لن نجمع أي معلومات عنك بدون موافقتك الصريحة.</p>
            <button class="btn btn-primary btn-lg" type="submit" id="send_message"><i class="bi bi-calendar-check me-1"></i> تأكيد الحجز</button>
          </div>
        </form>
      </div>
      <div class="col-lg-4"><div class="position-sticky" style="top:100px">
        <aside class="aside-card mb-4 reveal">
          <h3 class="mb-3">لماذا تحجز معنا؟</h3>
          <ul class="list-unstyled mb-0">
            <li><i class="bi bi-patch-check-fill"></i><span>طبيبة محترفة بخبرة أكثر من ٢٠ عامًا</span></li>
            <li><i class="bi bi-hospital"></i><span>نقبل التأمينات والنقابات</span></li>
            <li><i class="bi bi-percent"></i><span>خصم للأسرة وللمتابعة الشهرية</span></li>
            <li><i class="bi bi-chat-heart"></i><span>دعم المرضى والمتابعة عبر واتساب</span></li>
          </ul>
        </aside>
        <aside class="card-soft p-4 h-auto reveal">
          <h3 class="h5 mb-3">تفضل التواصل المباشر؟</h3>
          <p class="text-muted-2">لا تتردد في التواصل مع موظفي الاستقبال لأي استفسار طبي.</p>
          <a class="btn btn-primary w-100 mb-2" href="tel:{PHONE_INTL}"><i class="bi bi-telephone me-1"></i> <span class="ltr">{PHONE_LOCAL}</span></a>
          <a class="btn btn-whatsapp w-100" href="{WA}" target="_blank" rel="noopener"><i class="bi bi-whatsapp me-1"></i> واتساب</a>
        </aside>
      </div></div>
    </div>
  </div>
</section>
'''
ap += foot() + '<script src="assets/js/booking.js"></script>\n</body>\n</html>\n'
write('appointment.html', ap)

# ------------------------------------------------------------------ CONTACT
ct = head('اتصل بنا | عيادة د. سهام سالم للصدر', 'تواصل مع عيادة د. سهام سالم للصدر بمدينة نصر عبر الهاتف أو واتساب أو احجز موعدًا أونلاين.', 'contact.html')
ct += page_hero('اتصل بنا', 'جاهزون لمساعدتك — تواصل معنا بالطريقة الأنسب لك.', 'اتصل بنا')
ct += f'''<section class="section">
  <div class="container">
    <div class="row g-4 mb-5">
      <div class="col-md-6 col-lg-3 reveal"><div class="card-soft contact-card"><span class="icon-tile"><i class="bi bi-whatsapp"></i></span><h3>واتساب</h3><a class="strong" href="{WA}" target="_blank" rel="noopener">+20 111 314 4573</a></div></div>
      <div class="col-md-6 col-lg-3 reveal"><div class="card-soft contact-card"><span class="icon-tile"><i class="bi bi-telephone"></i></span><h3>اتصل بنا</h3><a class="strong" href="tel:{PHONE_INTL}">{PHONE_LOCAL}</a></div></div>
      <div class="col-md-6 col-lg-3 reveal"><div class="card-soft contact-card"><span class="icon-tile amber"><i class="bi bi-calendar-check"></i></span><h3>استشارة الطبيب</h3><a class="strong" href="appointment.html" style="direction:rtl">احجز الآن أونلاين</a></div></div>
      <div class="col-md-6 col-lg-3 reveal"><div class="card-soft contact-card"><span class="icon-tile amber"><i class="bi bi-geo-alt"></i></span><h3>الموقع</h3><a class="strong" href="{MAP}" target="_blank" rel="noopener" style="direction:rtl;font-size:1rem">افتح على خرائط جوجل</a></div></div>
    </div>
    <div class="row g-4">
      <div class="col-lg-6 reveal">
        <div class="card-soft p-4 h-100">
          <h2 class="h4 mb-3"><i class="bi bi-geo-alt-fill text-amber me-2"></i>عنوان العيادة</h2>
          <p class="mb-4">{ADDRESS}</p>
          <a class="btn btn-primary" href="{MAP}" target="_blank" rel="noopener"><i class="bi bi-map me-1"></i> الاتجاهات على الخريطة</a>
          <hr class="my-4">
          <h3 class="h6 mb-3">تجهيزات العيادة</h3>
          <div class="d-flex flex-wrap gap-2">
            <span class="badge rounded-pill text-bg-light border fw-semibold px-3 py-2"><i class="bi bi-building-up text-amber me-1"></i> مصعد</span>
            <span class="badge rounded-pill text-bg-light border fw-semibold px-3 py-2"><i class="bi bi-snow text-amber me-1"></i> تكييف</span>
            <span class="badge rounded-pill text-bg-light border fw-semibold px-3 py-2"><i class="bi bi-credit-card-2-front text-amber me-1"></i> إنستاباي</span>
            <span class="badge rounded-pill text-bg-light border fw-semibold px-3 py-2"><i class="bi bi-phone text-amber me-1"></i> فودافون كاش</span>
            <span class="badge rounded-pill text-bg-light border fw-semibold px-3 py-2"><i class="bi bi-eyedropper text-amber me-1"></i> معمل تحاليل داخل العيادة</span>
          </div>
        </div>
      </div>
      <div class="col-lg-6 reveal">
        <form class="form-card" method="POST" action="/enquiries" id="enquiryForm">
          <input type="hidden" name="_token" value="">
          <h2 class="h4 mb-4">أرسل لنا رسالة</h2>
          <div class="mb-3"><label class="form-label" for="c_name">الاسم</label><input type="text" id="c_name" name="name" class="form-control" required autocomplete="name"></div>
          <div class="row g-3 mb-3">
            <div class="col-md-6"><label class="form-label" for="c_email">البريد الإلكتروني</label><input type="email" id="c_email" name="email" class="form-control" required autocomplete="email" dir="ltr"></div>
            <div class="col-md-6"><label class="form-label" for="c_phone">رقم الهاتف</label><input type="tel" id="c_phone" name="phone" class="form-control" required autocomplete="tel" dir="ltr"></div>
          </div>
          <div class="mb-4"><label class="form-label" for="c_msg">رسالتك</label><textarea id="c_msg" name="message" class="form-control" rows="4" required></textarea></div>
          <button class="btn btn-primary btn-lg" type="submit"><i class="bi bi-send me-1"></i> إرسال الرسالة</button>
        </form>
      </div>
    </div>
  </div>
</section>
<section class="section bg-green-50">
  <div class="container">
    <div class="row gy-5 gx-lg-5">
      <div class="col-lg-4 reveal"><span class="eyebrow">أسئلة شائعة</span><h2 class="section-title">جاهزون لمساعدتك</h2></div>
      <div class="col-lg-8 reveal">{faq(FAQ_CONTACT, 'faqContact')}</div>
    </div>
  </div>
</section>
'''
ct += foot() + '</body>\n</html>\n'
write('contact.html', ct)
print('built')
