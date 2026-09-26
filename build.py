"""Builds index.html (ko) and en/index.html from src/content.json. Run: python3 build.py"""
import json, html, os

HERE = os.path.dirname(os.path.abspath(__file__))

COPY = json.load(open(os.path.join(HERE, 'src', 'content.json'), encoding='utf-8'))
OUT = HERE
STORE_URL = '#'  # TODO: replace with the Chrome Web Store listing URL once published

IMG = {
    '레트로 러닝화': 'shoe.webp', 'Retro running shoes': 'shoe.webp',
    '노이즈 캔슬링 헤드폰': 'headphones.webp', 'Noise-canceling headphones': 'headphones.webp',
    '오메가3 1,000mg': 'supplement.webp',
    'Hydrating serum 30ml': 'serum.webp',
}
META = {
    'ko': {
        'title': 'pricetag — 가격을 드래그하면 내 통화로',
        'desc': '해외 쇼핑몰에서 가격을 선택하면 바로 아래에 내 통화로 환산된 금액이 말풍선으로 뜨는 크롬 확장 프로그램. 166개 통화 지원, 무료.',
        'skip': '본문으로 건너뛰기',
        'dotsLabel': '상품 선택', 'emailLabel': '이메일 주소', 'brandHome': 'pricetag 홈',
        'popupsLabel': 'Pro 화면 미리보기',
    },
    'en': {
        'title': 'pricetag — Drag a price. See it in your currency.',
        'desc': 'A Chrome extension that converts any price you select into your currency, right below it in a speech bubble. 166 currencies. Free.',
        'skip': 'Skip to content',
        'dotsLabel': 'Choose a product', 'emailLabel': 'Email address', 'brandHome': 'pricetag home',
        'popupsLabel': 'Pro screens preview',
    },
}
ON, LAZY = ' class="is-on"', ' loading="lazy"'
e = lambda s: html.escape(str(s), quote=True)


def page(lang):
    c = COPY[lang]
    m = META[lang]
    base = '' if lang == 'ko' else '../'
    a = base + 'assets/'
    other_href = 'en/' if lang == 'ko' else '../'
    ko_href = './' if lang == 'ko' else '../'
    en_href = 'en/' if lang == 'ko' else './'
    first = c['heroItems'][0]

    hero_imgs = '\n'.join(
        f'            <img src="{a}img/{IMG[it["name"]]}" alt="{e(it["name"])}"{ON if i == 0 else ""}{LAZY if i else ""} width="960" height="500">'
        for i, it in enumerate(c['heroItems']))
    dots = '\n'.join(
        f'        <button type="button" aria-label="{e((str(i+1) + c["slideLabel"]) if lang == "ko" else (c["slideLabel"] + str(i+1)))}" aria-current="{"true" if i == 0 else "false"}"><span></span></button>'
        for i in range(len(c['heroItems'])))
    hero_json = json.dumps([{k: it[k] for k in ('name', 'original', 'converted')} for it in c['heroItems']], ensure_ascii=False)

    steps = '\n'.join(f'''        <div class="step stack" style="gap:14px">
          <span class="step-n" aria-hidden="true">{e(s["n"])}</span>
          <h3 class="step-t" style="margin:0">{e(s["title"])}</h3>
          <p>{e(s["text"])}</p>
        </div>''' for s in c['steps'])

    feats = '\n'.join(f'''        <article class="card">
          <h3 class="card-t" style="margin:0">{e(f["title"])}</h3>
          <p>{e(f["text"])}</p>
          <div class="chips">{"".join(f'<span class="num">{e(ch)}</span>' for ch in f["chips"])}</div>
        </article>''' for f in c['features'])

    pro_points = '\n'.join(f'''          <div class="pro-point"><i aria-hidden="true"></i><div><b>{e(p["title"])}</b><span>{e(p["text"])}</span></div></div>''' for p in c['proFeatures'])

    history = '\n'.join(f'''          <span class="chat chat-from num">{e(h["from"])}</span>
          <span class="chat chat-to num">{e(h["to"])}</span>''' for h in c['history'])

    wish = '\n'.join(f'''          <div class="wish">
            <div class="wish-l">
              <img src="{a}img/{IMG[w["name"]]}" alt="" width="40" height="40" loading="lazy">
              <div style="min-width:0"><div class="wish-name">{e(w["name"])}</div><div class="wish-note num">{e(w["note"])}</div></div>
            </div>
            <span class="wish-price num">{e(w["price"])}</span>
          </div>''' for w in c['wish'])

    free_items = ''.join(f'<li>{e(x)}</li>' for x in c['freeItems'])
    pro_items = ''.join(f'<li>{e(x)}</li>' for x in c['proItems'])
    faqs = '\n'.join(f'''        <details{" open" if i == 0 else ""}>
          <summary>{e(q["q"])}</summary>
          <p>{e(q["a"])}</p>
        </details>''' for i, q in enumerate(c['faqs']))

    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(m["title"])}</title>
<meta name="description" content="{e(m["desc"])}">
<meta name="theme-color" content="#2E39A9">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(m["title"])}">
<meta property="og:description" content="{e(m["desc"])}">
<meta property="og:locale" content="{"ko_KR" if lang == "ko" else "en_US"}">
<link rel="alternate" hreflang="ko" href="{ko_href}">
<link rel="alternate" hreflang="en" href="{en_href}">
<link rel="icon" href="{a}img/pricetag-mark.svg" type="image/svg+xml">
<link rel="preload" href="{a}fonts/Pretendard-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{a}site.css">
<script>
  (function () {{
    try {{
      var t = localStorage.getItem("pt-theme");
      if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
      var l = localStorage.getItem("pt-lang");
      if (l && l !== "{lang}") location.replace("{other_href}");
    }} catch (e) {{}}
  }})();
</script>
</head>
<body>
<a class="visually-hidden" href="#main">{e(m["skip"])}</a>

<header class="header">
  <a class="brand" href="{ko_href if lang == "ko" else en_href}" aria-label="{e(m["brandHome"])}">
    <img src="{a}img/pricetag-mark.svg" alt="" width="34" height="34">
    <span>pricetag</span>
  </a>
  <div class="header-tools">
    <nav class="lang" aria-label="Language">
      <a href="{ko_href}" hreflang="ko" lang="ko" data-lang-link="ko" aria-current="{"true" if lang == "ko" else "false"}">한국어</a>
      <a href="{en_href}" hreflang="en" lang="en" data-lang-link="en" aria-current="{"true" if lang == "en" else "false"}">English</a>
    </nav>
    <button class="icon-btn" id="theme-toggle" type="button" aria-label="">
      <svg class="moon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      <svg class="sun" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    </button>
    <a class="btn btn-primary btn-small" href="{STORE_URL}">{e(c["ctaShort"])}</a>
  </div>
</header>

<main id="main">
  <section class="hero">
    <div class="wrap row">
      <div class="stack" style="gap:24px">
        <span class="eyebrow">Currency translator for your browser</span>
        <h1 class="h1">{e(c["h1a"])}<br>{e(c["h1b"])}</h1>
        <p class="lead">{e(c["sub"])}</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="{STORE_URL}">{e(c["ctaLong"])}</a>
          <span class="cta-note">{e(c["ctaNote"])}</span>
        </div>
      </div>

      <div class="demo">
        <div class="browser">
          <div class="browser-bar" aria-hidden="true"><i></i><i></i><i></i><b></b></div>
          <div class="page">
            <div class="product-img">
{hero_imgs}
            </div>
            <div class="product-name" id="hero-name">{e(first["name"])}</div>
            <div class="price-wrap">
              <button class="price num" id="hero-price" type="button" aria-pressed="true" aria-controls="hero-bubble" aria-label="{e(c["demoAria"])}">{e(first["original"])}</button>
              <div class="bubble num" id="hero-bubble" aria-live="polite">{e(first["converted"])}</div>
            </div>
            <span class="try">{e(c["tryIt"])}</span>
          </div>
        </div>
        <div class="dots" role="group" aria-label="{e(m["dotsLabel"])}">
{dots}
        </div>
        <script type="application/json" id="hero-data">{hero_json}</script>
      </div>
    </div>
  </section>

  <section class="section band" aria-labelledby="how-t">
    <div class="wrap stack" style="max-width:1080px;gap:56px">
      <h2 class="h2" id="how-t">{e(c["howTitle"])}</h2>
      <div class="grid3">
{steps}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="feat-t">
    <div class="wrap stack" style="max-width:1080px;gap:48px">
      <div class="stack" style="gap:12px;max-width:640px">
        <h2 class="h2" id="feat-t">{e(c["featTitle"])}</h2>
        <p class="lead">{e(c["featSub"])}</p>
      </div>
      <div class="grid2">
{feats}
      </div>
    </div>
  </section>

  <section class="section band" aria-labelledby="pro-t">
    <div class="wrap row" style="gap:72px">
      <div class="stack" style="gap:22px;flex-basis:300px">
        <span class="eyebrow">pricetag Pro</span>
        <h2 class="h2" id="pro-t" style="font-size:clamp(28px,4vw,40px)">{e(c["proShowTitleA"])}<br>{e(c["proShowTitleB"])}</h2>
        <p class="lead" style="font-size:18px;max-width:440px">{e(c["proShowSub"])}</p>
        <div class="pro-points">
{pro_points}
        </div>
      </div>
      <div class="popups" style="flex-basis:300px" role="img" aria-label="{e(m["popupsLabel"])}">
        <div class="popup">
          <span class="popup-t">{e(c["histTitle"])}</span>
{history}
        </div>
        <div class="popup" style="gap:0">
          <span class="popup-t" style="padding-bottom:12px">{e(c["wishTitle"])}</span>
{wish}
        </div>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="price-t">
    <div class="wrap stack" style="max-width:880px;gap:48px">
      <div class="stack" style="gap:12px">
        <h2 class="h2" id="price-t">{e(c["priceTitle"])}</h2>
        <p class="lead">{e(c["priceSub"])}</p>
      </div>
      <div class="grid2">
        <div class="plan plan-free">
          <div class="stack" style="gap:6px"><span class="plan-name">{e(c["freeName"])}</span><span class="plan-price num">{e(c["freePrice"])}</span></div>
          <ul>{free_items}</ul>
          <a class="btn btn-outline" href="{STORE_URL}">{e(c["ctaShort"])}</a>
        </div>
        <div class="plan plan-pro">
          <div class="stack" style="gap:6px"><span class="plan-name">Pro</span><span class="plan-price">{e(c["proPrice"])}</span></div>
          <ul>{pro_items}</ul>
          <a class="btn btn-white" href="#waitlist">{e(c["proCta"])}</a>
        </div>
      </div>
      <p class="note">{e(c["rateNote"])}</p>
    </div>
  </section>

  <section class="section band faq" aria-labelledby="faq-t" style="border-bottom:none">
    <div class="wrap stack" style="max-width:760px;gap:32px">
      <h2 class="h2" id="faq-t">{e(c["faqTitle"])}</h2>
      <div>
{faqs}
      </div>
    </div>
  </section>
</main>

<footer class="footer" id="waitlist">
  <div class="footer-in">
    <img src="{a}img/pricetag-mark-inverse.svg" alt="" width="56" height="56">
    <h2>{e(c["footTitle"])}</h2>
    <form class="signup" id="signup" action="https://gmail.us15.list-manage.com/subscribe/post?u=7a4b34e1ab518009c85cb469d&amp;id=03c1a33707&amp;f_id=00147be0f0" method="post" target="_blank" novalidate>
      <label class="visually-hidden" for="email">{e(m["emailLabel"])}</label>
      <input id="email" type="email" name="EMAIL" autocomplete="email" placeholder="{e(c["email"])}" required>
      <input type="hidden" name="LANG" value="{lang}">
      <div class="hp" aria-hidden="true"><input type="text" name="b_7a4b34e1ab518009c85cb469d_03c1a33707" tabindex="-1" value="" autocomplete="off"></div>
      <button type="submit">{e(c["notify"])}</button>
    </form>
    <p class="status" id="signup-status" role="status" aria-live="polite"></p>
    <small><span>© pricetag</span></small>
  </div>
</footer>

<script src="{a}site.js" defer></script>
</body>
</html>
'''


os.makedirs(os.path.join(OUT, 'en'), exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page('ko'))
open(os.path.join(OUT, 'en', 'index.html'), 'w', encoding='utf-8').write(page('en'))
print('ok')
