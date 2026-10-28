"""Zostaví ostrú verziu webu LIBES s.r.o. do repozitára bp-ploty.
Vstup: koncept (page.html + build.py výstupy v3/), výstup: REPO.
Spustenie: python3 build.py && python3 prod.py
"""
import os, re, json, html, shutil, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/claude/bp-ploty'

# ---------------- konfigurácia firmy ----------------
SITE = 'https://www.bpploty.sk'          # zmeniť pri prechode na novú doménu (+ CNAME)
FORM_EMAIL = 'bpploty@gmail.com'          # kam chodia objednávky (FormSubmit) — po aktivácii libes@gmail.com prepnúť
EMAIL = 'libes@gmail.com'
PHONE, TEL = '0951 565 717', '+421951565717'
ICO = '57 955 531'
DIC = None                               # doplniť, keď príde (napr. '2123456789')
ULICA = 'Nábrežie M. R. Štefánika 1684/3'
SIDLO = ULICA + ', 034 01 Ružomberok'
ZAPIS = '27. 10. 2026'
GA = 'G-FCX9F0HGDW'
INSTAGRAM = 'https://www.instagram.com/bpploty'
TODAY = '2026-10-28'
SLUGS = ['murarske-prace', 'pomocne-prace', 'prenos-materialu', 'upratovacie-prace', 'ploty-betonove', 'ploty-3d']

def esc(t): return html.escape(t, quote=True)
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

# ---------------- spoločné časti hlavičky ----------------
def head_extra(path, title, desc, robots='index, follow', og='/img/og.jpg'):
    return f'''<link rel="canonical" href="{SITE}{path}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0A1D16">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="sk_SK">
<meta property="og:site_name" content="LIBES s.r.o.">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script>
  window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}
  gtag('consent','default',{{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'}});
  try{{if(localStorage.getItem('bp_cookie_consent')==='granted')gtag('consent','update',{{analytics_storage:'granted'}})}}catch(e){{}}
  gtag('js',new Date());gtag('config','{GA}');
  window.addEventListener('load',function(){{var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id={GA}';document.head.appendChild(s)}});
</script>
'''

COOKIE = '''
<div class="cookie" id="cookieBanner" hidden role="dialog" aria-label="Súhlas s cookies">
  <p>Používame len anonymnú analytiku návštevnosti (Google Analytics), aby sme vedeli, čo na webe funguje. Žiadne reklamné cookies. <a href="/ochrana-osobnych-udajov/#cookies">Viac</a></p>
  <div class="cookie-act"><button type="button" class="btn btn-line btn-sm" id="cookieDecline">Odmietnuť</button><button type="button" class="btn btn-brass btn-sm" id="cookieAccept">Prijať</button></div>
</div>
<style>
.cookie{position:fixed;left:max(16px,env(safe-area-inset-left,0px));right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:70;max-width:560px;margin-inline:auto;background:var(--coal-2);color:var(--bone);border:1px solid var(--line-d);border-radius:10px;padding:18px 20px;box-shadow:0 30px 60px -20px rgba(0,0,0,.6);display:grid;gap:14px}
.cookie p{font-size:.88rem;color:#C9D3CC;line-height:1.5}.cookie a{color:var(--brass-hi)}
.cookie-act{display:flex;gap:10px;justify-content:flex-end;flex-wrap:wrap}
@media (max-width:759px){.cookie{bottom:calc(84px + env(safe-area-inset-bottom,0px))}}
.cookie-link{background:none;border:0;padding:0;font:inherit;color:inherit;text-decoration:underline;cursor:pointer}
</style>
<script>
(function(){var b=document.getElementById('cookieBanner'),K='bp_cookie_consent';
  function get(){try{return localStorage.getItem(K)}catch(e){return null}}
  function set(v){try{localStorage.setItem(K,v)}catch(e){}gtag('consent','update',{analytics_storage:v==='granted'?'granted':'denied'});b.hidden=true}
  if(!get())b.hidden=false;
  document.getElementById('cookieAccept').onclick=function(){set('granted')};
  document.getElementById('cookieDecline').onclick=function(){set('denied')};
  document.querySelectorAll('[data-cookie-settings]').forEach(function(x){x.addEventListener('click',function(){b.hidden=false})});
})();
</script>
'''

def company_line():
    nb = lambda x: x.replace(' ', '\u00a0')
    s = nb(f'IČO {ICO}')
    if DIC: s += ' · ' + nb(f'DIČ {DIC}')
    return s

def finish(page):
    """Úpravy spoločné pre všetky stránky: koncept preč, údaje firmy, cookies, Instagram."""
    page = page.replace('<span class="concept">KONCEPT</span><span class="hide-sm">&nbsp;·&nbsp;', '<span class="hide-sm">')
    page = re.sub(r'IČO a sídlo doplníme po zápise s\.r\.o\.', f'LIBES s.r.o. · {company_line()} · {SIDLO.replace("034 01", "034\u00a001")} · <button type="button" class="cookie-link" data-cookie-settings>Nastavenia cookies</button>', page)
    page = page.replace('<li>Ružomberok a okolie</li></ul>', f'<li>Ružomberok a okolie</li><li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @bpploty</a></li></ul>')
    page = page.replace('<li>Ružomberok a okolie</li>\n        </ul>', f'<li>Ružomberok a okolie</li>\n          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @bpploty</a></li>\n        </ul>')
    page = page.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    css = COOKIE[COOKIE.index('<style>'):COOKIE.index('</style>') + 8]
    page = page.replace('</head>', css + '\n</head>', 1)
    page = page.replace('</body>', COOKIE.replace(css, '') + '</body>')
    return page

def abs_links(p, depth):
    """Relatívne odkazy konceptu -> absolútne cesty od koreňa webu."""
    up = '../' * depth
    if depth:
        p = p.replace(up + 'index.html', '/')
        p = p.replace(up + 'img/', '/img/')
        p = p.replace(up + 'ochrana-osobnych-udajov/index.html', '/ochrana-osobnych-udajov/')
        for s in SLUGS:
            p = p.replace(f'../sluzby/{s}/index.html', f'/sluzby/{s}/').replace(f'../{s}/index.html', f'/sluzby/{s}/')
    p = p.replace('/?sluzba=', '/?sluzba=')
    return p

# ================= HLAVNÁ STRÁNKA =================
src = rd(os.path.join(HERE, 'page.html'))
a = src.index('<link rel="preconnect"'); b = src.index('</style>') + len('</style>')
head_assets, body = src[a:b], src[b:]
# odkazy
for s in SLUGS: body = body.replace(f'sluzby/{s}/index.html', f'/sluzby/{s}/')
body = body.replace('href="ochrana-osobnych-udajov/index.html"', 'href="/ochrana-osobnych-udajov/"')
body = re.sub(r'(?<=[\s"\'(,])img/', '/img/', body)
# texty konceptu
body = body.replace('<p class="wz-note">V ostrej verzii sa objednávka doručí na libes@gmail.com cez FormSubmit (rovnako ako na súčasnom webe) a zákazník dostane automatické potvrdenie. V tomto koncepte sa nič neodosiela.</p>',
    '<p class="send-err" id="sendErr" hidden>Odoslanie sa nepodarilo. Skúste to znova alebo nám zavolajte na <a href="tel:' + TEL + '">' + PHONE + '</a>.</p>\n        <p class="wz-note">Dopyt príde priamo nám. Ozveme sa do 24 hodín.</p>')
body = body.replace(' <em>(Ukážka — v koncepte sa nič neodoslalo.)</em>', '')
body = body.replace('<form id="orderForm" novalidate>', '<form id="orderForm" novalidate>\n        <input type="text" name="_honey" id="o-honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">')
# ostré odoslanie cez FormSubmit (AJAX)
old = body[body.index("    form.hidden=true;\n    document.querySelector('.wz-bar').hidden=true;"): body.index("    document.getElementById('done').hidden=false;\n  });") + len("    document.getElementById('done').hidden=false;\n")]
new = f"""    if(document.getElementById('o-honey').value)return;
    var btn=document.getElementById('wzSubmit'),lab=btn.firstChild,err=document.getElementById('sendErr'),ref='LB-'+String(Math.floor(1000+Math.random()*9000));
    btn.disabled=true;lab.textContent='Odosielam… ';err.hidden=true;
    var data={{_subject:'Nový dopyt '+ref+' — '+selected().join(', '),_template:'table',_captcha:'false',
      'Číslo dopytu':ref,'Práce':selected().join(', '),'Miesto':val('o-loc')||'—','Začiatok':val('o-when'),'Objekt':radio('obj'),
      'Popis':val('o-msg')||'—','Meno':val('o-name'),'Telefón':val('o-phone'),'Ozvať sa':radio('pref')}};
    if(val('o-email')){{data.email=val('o-email');data._autoresponse='Ďakujeme, váš dopyt '+ref+' sme prijali. Ozveme sa do 24 hodín. LIBES s.r.o., {PHONE}'}}
    fetch('https://formsubmit.co/ajax/{FORM_EMAIL}',{{method:'POST',headers:{{'Content-Type':'application/json','Accept':'application/json'}},body:JSON.stringify(data)}})
      .then(function(r){{return r.json().catch(function(){{return {{}}}}).then(function(j){{if(!r.ok||String(j.success)==='false')throw new Error(j.message||r.status)}})}})
      .then(function(){{
        form.hidden=true;document.querySelector('.wz-bar').hidden=true;document.querySelector('.wz-labels').hidden=true;
        document.getElementById('wzCount').textContent='Odoslané';document.getElementById('ref').textContent='Číslo dopytu: '+ref;
        document.getElementById('done').hidden=false;
        try{{gtag('event','generate_lead',{{form:'objednavka',services:selected().join(', ')}})}}catch(e){{}}
      }})
      .catch(function(){{err.hidden=false}})
      .then(function(){{btn.disabled=false;lab.textContent='Odoslať objednávku '}});
"""
body = body.replace(old, new)
body = body.replace('.wz-note{', '.send-err{margin-top:14px;padding:12px 14px;border-radius:6px;background:#FBEAE6;color:#8E2F1E;font-size:.86rem}.send-err a{color:inherit;font-weight:600}\n.wz-note{') if '.wz-note{' in body else body
head_assets = head_assets.replace('.wz-note{', '.send-err{margin-top:14px;padding:12px 14px;border-radius:6px;background:#FBEAE6;color:#8E2F1E;font-size:.86rem}.send-err a{color:inherit;font-weight:600}\nbutton:disabled{opacity:.6;cursor:wait}\n.wz-note{')
# štruktúrované dáta
faq = re.findall(r'<details[^>]*><summary><span><span class="cat">[^<]*</span>(.*?)</span><i class="pm"></i></summary><div class="ans">(.*?)</div></details>', body, re.S)
biz = {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": SITE + "/#business",
       "name": "LIBES s.r.o.", "alternateName": "BP ploty", "url": SITE + "/", "image": SITE + "/img/og.jpg", "logo": SITE + "/apple-touch-icon.png",
       "description": "Murárske a pomocné práce, prenos materiálu, upratovanie stavieb a montáž betónových a 3D plotov v Ružomberku a okolí.",
       "telephone": TEL, "email": EMAIL, "identifier": {"@type": "PropertyValue", "propertyID": "IČO", "value": ICO.replace(' ', '')},
       "address": {"@type": "PostalAddress", "streetAddress": ULICA, "postalCode": "034 01", "addressLocality": "Ružomberok", "addressCountry": "SK"},
       "areaServed": [{"@type": "City", "name": "Ružomberok"}, {"@type": "AdministrativeArea", "name": "Žilinský kraj"}],
       "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "16:00"},
       "sameAs": [INSTAGRAM],
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Služby", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": f"{SITE}/sluzby/{s}/"}} for n, s in zip(['Murárske práce', 'Pomocné práce', 'Prenos materiálu', 'Upratovacie práce', 'Betónové ploty', '3D ploty'], SLUGS)]}}
if DIC: biz["taxID"] = DIC
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub('<[^>]+>', '', a_))}} for q, a_ in faq]}
title = 'LIBES s.r.o. — stavebné práce a ploty na kľúč | Ružomberok (BP ploty)'
desc = 'Murárske a pomocné práce, prenos materiálu, upratovanie stavieb a betónové a 3D ploty na kľúč v Ružomberku a okolí. Obhliadka zdarma, odpoveď do 24 hodín.'
home = f'''<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{head_extra('/', title, desc)}<script type="application/ld+json">{json.dumps(biz, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<link rel="preload" as="image" href="/img/s/hero.webp" imagesrcset="/img/s/hero.webp 640w, /img/hero.webp 1400w" imagesizes="(min-width:1000px) 560px, 100vw">
{head_assets}
</head>
<body>
{body.strip()}
</body>
</html>
'''
wr(f'{REPO}/index.html', finish(home))

# ================= PODSTRÁNKY SLUŽIEB =================
for s in SLUGS:
    p = rd(os.path.join(HERE, 'sluzby', s, 'index.html'))
    p = abs_links(p, 2)
    t = re.search(r'<title>(.*?)</title>', p).group(1); d = re.search(r'<meta name="description" content="(.*?)">', p).group(1)
    p = p.replace('<meta name="robots" content="index, follow">\n<meta name="theme-color" content="#0A1D16">\n', '')
    p = re.sub(r'<meta property="og:type".*?<meta property="og:description" content="[^"]*">\n', '', p, flags=re.S)
    p = p.replace('</title>', '</title>\n' + head_extra(f'/sluzby/{s}/', html.unescape(t), html.unescape(d)).rstrip(), 1)
    # breadcrumb v schéme s plnými URL
    p = p.replace('"item": "/"', f'"item": "{SITE}/"').replace('"item": "/#sluzby"', f'"item": "{SITE}/#sluzby"').replace(f'"item": "/sluzby/{s}/"', f'"item": "{SITE}/sluzby/{s}/"')
    wr(f'{REPO}/sluzby/{s}/index.html', finish(p))

# ================= ŠABLÓNA PRE ĎALŠIE STRÁNKY (z ochrany údajov) =================
pp = rd(os.path.join(HERE, 'ochrana-osobnych-udajov', 'index.html'))
pp = pp.replace('href="../index.html', 'href="/index.html').replace('href="/index.html"', 'href="/"').replace('href="/index.html#', 'href="/#')
pp = pp.replace('href="../sluzby/', 'href="/sluzby/').replace('../img/', '/img/')
for s in SLUGS: pp = pp.replace(f'/sluzby/{s}/index.html', f'/sluzby/{s}/')
pp = pp.replace('href="index.html"', 'href="/ochrana-osobnych-udajov/"')
pp = pp.replace('/index.html?sluzba=', '/?sluzba=')
pre, rest = pp.split('<main>', 1); main_pp, post = rest.split('</main>', 1)

def page_from_template(path, title, desc, main_html, robots='index, follow', extra_css='', ld=None):
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', pre)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', h)
    h = h.replace('<meta name="robots" content="noindex, follow">\n', '')
    h = h.replace('</title>', '</title>\n' + head_extra(path, title, desc, robots).rstrip(), 1)
    if extra_css: h = h.replace('</style>', extra_css + '</style>', 1)
    if ld: h = h.replace('</head>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld) + '\n</head>')
    return finish(h + '<main>' + main_html + '</main>' + post)

def crumbs(name): return f'<nav class="crumbs" aria-label="Omrvinky"><a href="/">Domov</a><i>/</i><b>{name}</b></nav>'
def bc_ld(name, path): return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Domov", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}

# ---- ochrana osobných údajov (vyplnená) ----
m = main_pp
m = m.replace('<p class="pp-note">NÁVRH TEXTU — pred zverejnením doplniť údaje firmy a nechať skontrolovať (právnik / GDPR poradca).</p>', '')
m = re.sub(r'LIBES s\.r\.o\., sídlo: <mark>\[doplniť\]</mark>, IČO: <mark>\[doplniť\]</mark>, zapísaná v Obchodnom registri <mark>\[doplniť\]</mark>\.',
           f'LIBES s.r.o., so sídlom {SIDLO}, IČO: {ICO}{", DIČ: " + DIC if DIC else ""}, spoločnosť s ručením obmedzeným zapísaná v Obchodnom registri dňa {ZAPIS}.', m)
m = m.replace(' <mark>[overiť konkrétnych poskytovateľov a prípadný prenos mimo EÚ]</mark>',
              ' Ide o tieto služby: e‑mailová schránka Gmail (Google), doručovanie formulára FormSubmit, hosting webu GitHub Pages a — iba s vaším súhlasom — Google Analytics. Niektorí z týchto poskytovateľov môžu údaje spracúvať aj mimo EÚ (USA); prenos prebieha na základe rámca EU‑US Data Privacy Framework alebo štandardných zmluvných doložiek.')
m = re.sub(r'<section class="pp-sec"><h2>Cookies</h2><p>.*?</p></section>',
           '<section class="pp-sec" id="cookies"><h2>Cookies</h2><p>Nevyhnutné nastavenia (napríklad vaša voľba súhlasu) si web ukladá vo vašom prehliadači. Analytické cookies Google Analytics používame len vtedy, keď na to dáte súhlas v lište — slúžia na anonymné meranie návštevnosti, nie na reklamu. Súhlas môžete kedykoľvek zmeniť cez odkaz „Nastavenia cookies“ v päte stránky.</p></section>', m, flags=re.S)
m = m.replace('<section class="band light" style="padding-block:56px"><div class="wrap pp">', f'<section class="band light" style="padding-block:56px"><div class="wrap pp"><p class="pp-note">Platné od {ZAPIS}</p>')
wr(f'{REPO}/ochrana-osobnych-udajov/index.html', page_from_template('/ochrana-osobnych-udajov/', 'Ochrana osobných údajov | LIBES s.r.o.', 'Ako LIBES s.r.o. spracúva osobné údaje z dopytov a objednávok a ako používa cookies.', m, robots='noindex, follow'))

# ---- realizácie: všetkých 112 fotiek ----
old = rd(f'{REPO}/realizacie/index.html') if os.path.exists(f'{REPO}/realizacie/index.html') else ''
dims = dict(re.findall(r'realizacia-(\d+)-thumb\.webp" width="\d+" height="(\d+)"', old))
nums = sorted({n for n in re.findall(r'realizacia-(\d+)-thumb\.webp', ' '.join(os.listdir(f'{REPO}/images/realizacie')))})
btns = ''.join(f'<button type="button" data-i="{i}"><img src="/images/realizacie/realizacia-{n}-thumb.webp" data-full="/images/realizacie/realizacia-{n}-full.webp" width="640" height="{dims.get(n, "480")}" alt="Realizácia LIBES (BP ploty) č. {int(n)} — Ružomberok a okolie" loading="lazy" decoding="async"></button>' for i, n in enumerate(nums))
real_css = '.gal.all{grid-template-columns:repeat(2,1fr);grid-auto-rows:auto}.gal.all button{aspect-ratio:4/3}@media (min-width:700px){.gal.all{grid-template-columns:repeat(3,1fr)}}@media (min-width:1100px){.gal.all{grid-template-columns:repeat(4,1fr)}}'
real_main = f'''
<section class="p-hero" style="padding-block:48px 56px"><div class="wrap">
  {crumbs('Realizácie')}
  <span class="eyebrow"><i class="stripes"></i>{len(nums)} fotografií z našich zákaziek</span>
  <h1 style="font-size:clamp(2.6rem,6.5vw,4.8rem)">Realizácie<span>z Ružomberka a okolia.</span></h1>
  <p class="lead" style="margin-top:18px">Betónové ploty v dekore kameň, drevo aj tehla, 3D panely a práca na stavbách. Kliknutím fotku zväčšíte, šípkami listujete.</p>
  <div class="hero-cta"><a class="btn btn-brass" href="/#objednavka">Chcem podobnú realizáciu <svg><use href="#i-arrow"/></svg></a><a class="btn btn-line" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>{PHONE}</a></div>
</div></section>
<section class="band light-2" style="padding-block:56px"><div class="wrap"><div class="gal all" id="gallery">{btns}</div></div></section>
'''
wr(f'{REPO}/realizacie/index.html', page_from_template('/realizacie/', f'Realizácie — {len(nums)} fotiek hotových plotov | LIBES s.r.o. (BP ploty) Ružomberok',
   'Pozrite si viac ako 100 fotiek betónových a 3D plotov, ktoré sme postavili v Ružomberku a okolí — kamenný, drevený aj tehlový dekor.', real_main, extra_css=real_css, ld=[bc_ld('Realizácie', '/realizacie/')]))

# ---- kontakt ----
items = [('i-phone', 'Zavolať', PHONE, f'tel:{TEL}', ''), ('i-wa', 'WhatsApp', 'pošlite aj fotky pozemku', 'https://wa.me/421951565717', ' wa'),
         ('i-vb', 'Viber', PHONE, 'viber://chat?number=%2B421951565717', ' vb'), ('i-sms', 'SMS', 'zavoláme vám späť', f'sms:{TEL}', ''), ('i-mail', 'E‑mail', EMAIL, f'mailto:{EMAIL}', '')]
cl = ''.join(f'<a class="c-item{c}" href="{h}"{" target=\"_blank\" rel=\"noopener\"" if h.startswith("http") else ""}><span class="ic"><svg><use href="#{i}"/></svg></span><span class="tx"><b>{t}</b><small>{s_}</small></span><span class="arr">→</span></a>' for i, t, s_, h, c in items)
kontakt_main = f'''
<section class="p-hero" style="padding-block:48px 64px"><div class="wrap p-grid" style="align-items:start">
  <div>
    {crumbs('Kontakt')}
    <span class="eyebrow"><i class="stripes"></i>Odpoveď do 24 hodín</span>
    <h1 style="font-size:clamp(2.6rem,6.5vw,4.8rem)">Kontakt<span>zavolajte alebo napíšte.</span></h1>
    <p class="lead" style="margin-top:18px">Obhliadka aj cenová ponuka sú zdarma a nezáväzné. Najrýchlejšie nás zastihnete telefonicky v pracovných dňoch od 7:00 do 16:00.</p>
    <div class="hero-cta"><a class="btn btn-brass" href="/#objednavka">Vytvoriť objednávku online <svg><use href="#i-arrow"/></svg></a></div>
    <div class="hours" style="margin-top:34px"><div><span>Pondelok – Piatok</span><b>7:00 – 16:00</b></div><div><span>Sobota – Nedeľa</span><b>správy a WhatsApp</b></div><div><span>Oblasť</span><b>Ružomberok a okolie</b></div></div>
  </div>
  <div><div class="contact-list" style="margin-top:0">{cl}</div>
    <div class="hours" style="margin-top:26px"><div><span>Firma</span><b>LIBES s.r.o.</b></div><div><span>Sídlo</span><b>{SIDLO}</b></div><div><span>IČO</span><b>{ICO}</b></div>{f"<div><span>DIČ</span><b>{DIC}</b></div>" if DIC else ""}<div><span>Instagram</span><b><a href="{INSTAGRAM}" target="_blank" rel="noopener" style="color:inherit">@bpploty</a></b></div></div>
  </div>
</div></section>
'''
wr(f'{REPO}/kontakt/index.html', page_from_template('/kontakt/', 'Kontakt — nezáväzná cenová ponuka | LIBES s.r.o. (BP ploty) Ružomberok',
   'Zavolajte, napíšte na WhatsApp alebo vytvorte objednávku online. Obhliadka a cenová ponuka zdarma, odpoveď do 24 hodín. Ružomberok a okolie.', kontakt_main, ld=[bc_ld('Kontakt', '/kontakt/')]))

# ---- 404 ----
links = ''.join(f'<a class="rel" href="/sluzby/{s}/" style="background:var(--coal-2);color:var(--bone);border-color:var(--line-d)"><span><b>{n}</b></span><span class="ar">→</span></a>' for s, n in zip(SLUGS, ['Murárske práce', 'Pomocné práce', 'Prenos materiálu', 'Upratovacie práce', 'Betónové ploty', '3D ploty']))
nf_main = f'''
<section class="p-hero" style="padding-block:64px 80px"><div class="wrap">
  <span class="eyebrow"><i class="stripes"></i>Chyba 404</span>
  <h1 style="font-size:clamp(2.6rem,6.5vw,4.8rem)">Táto stránka<span>tu nie je.</span></h1>
  <p class="lead" style="margin-top:18px">Adresa sa mohla zmeniť pri prechode z BP ploty na LIBES s.r.o. Skúste niektorú zo služieb alebo nám rovno zavolajte.</p>
  <div class="hero-cta"><a class="btn btn-brass" href="/">Na hlavnú stránku <svg><use href="#i-arrow"/></svg></a><a class="btn btn-line" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>{PHONE}</a></div>
  <div class="related" style="margin-top:40px">{links}</div>
</div></section>'''
wr(f'{REPO}/404.html', page_from_template('/404.html', 'Stránka sa nenašla | LIBES s.r.o.', 'Hľadaná stránka neexistuje.', nf_main, robots='noindex'))

# ================= OBRÁZKY, SITEMAP, ROBOTS, LLMS =================
used = set()
for f in glob.glob(f'{REPO}/**/*.html', recursive=True):
    used |= set(re.findall(r'/img/((?:s/)?[\w-]+\.webp)', rd(f)))
os.makedirs(f'{REPO}/img/s', exist_ok=True)
for u in sorted(used):
    if os.path.exists(os.path.join(HERE, 'img', u)): shutil.copy(os.path.join(HERE, 'img', u), f'{REPO}/img/{u}')
print('obrázkov skopírovaných:', len(used))

urls = [('/', '1.0', 'monthly')] + [(f'/sluzby/{s}/', '0.9', 'monthly') for s in SLUGS] + [('/realizacie/', '0.8', 'weekly'), ('/kontakt/', '0.7', 'yearly')]
wr(f'{REPO}/sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
   ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n' for u, p, c in urls) + '</urlset>\n')
wr(f'{REPO}/robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
wr(f'{REPO}/llms.txt', f'''# LIBES s.r.o. (predtým BP ploty)

> Stavebná firma z Ružomberka: murárske a pomocné práce, prenos materiálu, upratovanie stavieb a montáž betónových a 3D plotov na kľúč. Pôsobí v Ružomberku a okolitých obciach Žilinského kraja.

LIBES s.r.o. pokračuje v činnosti BP ploty s rovnakým tímom a rozšírenou ponukou. Obhliadka a cenová ponuka sú zdarma, odpoveď na dopyt do 24 hodín. Na webe sú interaktívne nástroje: plánovač plota s výkresom, kalkulačka steny, výkopu, hmotnosti materiálu a veľkosti kontajnera.

## Kontakt
- Telefón: {TEL}
- E-mail: {EMAIL}
- Instagram: {INSTAGRAM}
- Firma: LIBES s.r.o., IČO {ICO}, {SIDLO}
- Oblasť pôsobenia: Ružomberok a okolie, Žilinský kraj (pri väčších zákazkách aj ďalej)
- Prevádzková doba: pondelok–piatok 7:00–16:00

## Stránky
- [Domovská stránka]({SITE}/) — služby, plánovač plota, realizácie, časté otázky, objednávka
''' + ''.join(f'- [{n}]({SITE}/sluzby/{s}/)\n' for s, n in zip(SLUGS, ['Murárske práce', 'Pomocné práce', 'Prenos materiálu', 'Upratovacie práce', 'Betónové ploty', '3D ploty'])) +
f'''- [Realizácie]({SITE}/realizacie/) — {len(nums)} fotiek hotových zákaziek
- [Kontakt]({SITE}/kontakt/) — telefón, WhatsApp, Viber, e-mail, údaje firmy
''')
print('hotovo:', REPO)
