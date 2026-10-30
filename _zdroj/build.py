"""Generátor podstránok služieb LIBES zo šablóny + dát.
Číta štýly a ikonový sprite z page.html (hlavná stránka), aby bol dizajn jednotný.
Výstup: v3/sluzby/<slug>/index.html  (cesty k obrázkom ../../img/...)
"""
import os, re, json, html
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import TOOLS, TOOL_CSS, COMMON_JS

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'page.html'), encoding='utf-8').read()

STYLE = src[src.index('<style>') + 7: src.index('</style>')]
sp_a = src.index('<svg width="0" height="0"')
SPRITE = src[sp_a: src.index('</svg>', src.index('</defs>')) + 6]
FONTS = src[src.index('<link rel="preconnect"'): src.index('<style>')]

# --- znovupoužiteľné interaktívne prvky z hlavnej stránky ---
_pa = src.index('<!-- ================= PLÁNOVAČ ================= -->')
_pb = src.index('<!-- ================= REALIZÁCIE ================= -->')
PLANNER_HTML = re.sub(r'(?<=[\s"\'(,])img/', '../../img/', src[_pa:_pb])
_ja = src.index('  /* --- pred / po --- */')
_jb = src.index('  /* odkaz z podstránky')
PLANNER_JS = src[_ja:_jb].replace("'img/tex-", "'../../img/tex-")
_sa = PLANNER_JS.index("  document.getElementById('pSend')")
_se = PLANNER_JS.index('  buildOpts();draw();')
PLANNER_JS = PLANNER_JS[:_sa] + '''  document.getElementById('pSend').addEventListener('click',function(ev){
    ev.preventDefault();
    var v=P.type==='beton'?'Betónové ploty':'3D ploty';
    var t='Plot z plánovača: '+(P.type==='beton'?'betónový':'3D panel')+', '+P.dec+', výška '+fmt(P.h*10)+' mm, dĺžka cca '+P.len+' m ('+document.getElementById('bFields').textContent+' polí, '+document.getElementById('bPosts').textContent+' stĺpikov).';
    location.href='../../index.html?sluzba='+encodeURIComponent(v)+'&popis='+encodeURIComponent(t)+'#objednavka';
  });
''' + PLANNER_JS[_se:]
_ba = src.index('    <div class="ba-head">')
_bb = src.index('    <div class="gal" id="gallery">')
BA_HTML = re.sub(r'(?<=[\s"\'(,])img/', '../../img/', src[_ba:_bb])

PHONE = '0951 565 717'
TEL = '+421951565717'
R = '../../'
HOME = R + 'index.html'

SERVICES = [
  dict(slug='murarske-prace', no='01', name='Murárske práce', short='Murárske práce',
       title='Murárske práce Ružomberok a okolie | LIBES s.r.o.',
       desc='Murárske práce v Ružomberku a okolí — základy, murivo, priečky, omietky a drobné stavebné úpravy. Obhliadka a cenová ponuka zdarma.',
       h1='Murárske práce', h1b='od základov po omietku.',
       lead='Hrubá stavba aj dokončovacie práce pri rodinných domoch, prístavbách a rekonštrukciách. Prídeme, zameriame, nacenime a postavíme — s jedným kontaktom od začiatku do konca.',
       hero=None, hero_tex='tex-tehla.webp', icon='i-brick',
       chips=['novostavby', 'prístavby', 'rekonštrukcie'],
       scope=[('Základy', 'základové pásy a dosky pod stavbu, oporné múriky'),
              ('Murivo', 'nosné a obvodové murivo z tvárnic aj tehál'),
              ('Priečky', 'deliace priečky a úpravy dispozície'),
              ('Omietky', 'vnútorné aj vonkajšie omietky a vyrovnávanie stien'),
              ('Drobné úpravy', 'otvory, zamurovanie, opravy a menšie stavebné zásahy'),
              ('Kombinácia prác', 'murovanie spolu s prenosom materiálu a upratovaním v jednej zákazke')],
       forwho=['Stavebníci rodinných domov', 'Majitelia, ktorí rekonštruujú alebo prestavujú', 'Firmy, ktoré potrebujú murárov na časť stavby'],
       gallery=[], gallery_note='Fotografie z murárskych zákaziek doplníme — zatiaľ si pozrite naše realizácie plotov.',
       faq=[('Robíte aj menšie murárske zákazky?', 'Napíšte nám, o akú prácu ide. Aj menšie zákazky radi posúdime a dohodneme termín, ktorý vám vyhovuje.'),
            ('Zabezpečíte aj materiál?', 'Podľa dohody — materiál vieme zabezpečiť a doviezť, alebo pracujeme s vaším. Všetko upresníme pri obhliadke a v cenovej ponuke.'),
            ('Ako rýchlo viete začať?', 'Termín závisí od rozsahu a aktuálnej vyťaženosti. Po obhliadke vám povieme presný dátum začatia a dobu trvania prác.')]),
  dict(slug='pomocne-prace', no='02', name='Pomocné práce', short='Pomocné práce',
       title='Pomocné stavebné práce Ružomberok | LIBES s.r.o.',
       desc='Pomocné stavebné práce v Ružomberku a okolí — výkopy, príprava terénu, miešanie betónu, nosenie materiálu a asistencia remeselníkom.',
       h1='Pomocné práce', h1b='keď stavba potrebuje ruky.',
       lead='Výkopy, príprava terénu, betonáž a všetko, čo musí byť hotové, aby mohli remeselníci pracovať. Posilníme vašu partiu alebo pripravíme stavenisko vopred.',
       hero='r016.webp', hero_alt='Osadené stĺpiky a výkopy na pozemku', icon='i-trowel',
       chips=['výkopy', 'betonáž', 'príprava stavby'],
       scope=[('Výkopy', 'ručné výkopy pre základy, pätky a prípojky'),
              ('Príprava terénu', 'vyrovnanie, odstránenie porastu a príprava plochy'),
              ('Betonáž', 'miešanie betónu a malty, betonáž pätiek a základov'),
              ('Nosenie materiálu', 'presun materiálu po stavenisku tam, kde je potrebný'),
              ('Asistencia', 'pomocník pre murárov, tesárov a ďalších remeselníkov'),
              ('Dokončenie', 'odpratanie a príprava pre ďalšiu fázu stavby')],
       forwho=['Stavebníci, ktorí stavajú svojpomocne', 'Remeselníci, ktorí potrebujú posilu', 'Majitelia pozemkov pred výstavbou'],
       gallery=[('r016.webp', 'Výkopy a osadené stĺpiky'), ('r014.webp', 'Príprava pätiek pre stĺpiky')],
       faq=[('Dá sa objednať pomocník len na pár dní?', 'Áno, rozsah dohodneme podľa toho, čo stavba potrebuje — či ide o jeden deň alebo dlhšiu spoluprácu.'),
            ('Pracujete aj s inými remeselníkmi na stavbe?', 'Áno. Pomocné práce často robíme popri iných remeselníkoch, aby mohli pracovať rýchlejšie.'),
            ('Ako sa pomocné práce účtujú?', 'Podľa rozsahu prác. Po obhliadke alebo telefonickom popise pošleme cenovú ponuku.')]),
  dict(slug='prenos-materialu', no='03', name='Prenos materiálu', short='Prenos materiálu',
       title='Prenos a manipulácia so stavebným materiálom | LIBES s.r.o.',
       desc='Prenos stavebného materiálu v Ružomberku a okolí — vykládka, presun na pozemok, na poschodia aj na ťažko dostupné miesta.',
       h1='Prenos materiálu', h1b='aj tam, kam auto nedôjde.',
       lead='Paleta zostala pred bránou a materiál treba na dvor, do záhrady alebo na poschodie? Vyložíme, prenesieme, uložíme a zakryjeme — bez poškodenia a bez zdržania stavby.',
       hero='r086.webp', hero_alt='Betónové dosky na paletách pripravené na prenos', icon='i-cart',
       chips=['vykládka', 'poschodia', 'ťažký prístup'],
       scope=[('Vykládka', 'vyloženie materiálu z dodávky alebo kamióna'),
              ('Prenos na pozemok', 'presun na dvor, do záhrady alebo za dom'),
              ('Prenos na poschodia', 'vynesenie materiálu do vyšších podlaží'),
              ('Ťažký prístup', 'úzke prechody, svahy a miesta bez príjazdu'),
              ('Uskladnenie', 'uloženie na palety a zakrytie pred počasím'),
              ('Odvoz zvyškov', 'odnesenie obalov a zvyškov materiálu')],
       forwho=['Stavebníci, ktorým prišiel materiál', 'Majitelia domov s ťažkým prístupom', 'Firmy, ktoré potrebujú pracovnú silu na manipuláciu'],
       gallery=[('r086.webp', 'Dosky s kamenným dekorom na paletách'), ('r084.webp', 'Materiál pripravený na montáž'), ('r091.webp', 'Dosky s tehlovým dekorom')],
       faq=[('Prenášate aj ťažký materiál?', 'Áno, bežne manipulujeme s betónovými doskami, tvárnicami a ďalším stavebným materiálom. Pri veľmi ťažkých kusoch dohodneme postup vopred.'),
            ('Dá sa prenos spojiť s inými prácami?', 'Áno. Prenos materiálu najčastejšie robíme spolu s murovaním, pomocnými prácami alebo montážou plota.'),
            ('Koľko vopred treba prenos objednať?', 'Čím skôr, tým lepšie — ideálne hneď, ako poznáte termín dodania materiálu.')]),
  dict(slug='upratovacie-prace', no='04', name='Upratovacie práce', short='Upratovacie práce',
       title='Upratovanie po stavbe Ružomberok | LIBES s.r.o.',
       desc='Upratovacie práce po stavbe v Ružomberku a okolí — odvoz sutiny, čistenie po stavebných prácach a úprava pozemku.',
       h1='Upratovacie práce', h1b='odovzdáme hotové.',
       lead='Po stavbe zostáva sutina, prach a neporiadok na pozemku. Upraceme ho za vás — preberáte hotový dom a pozemok, nie stavenisko.',
       hero='r093.webp', hero_alt='Upratený pozemok s hotovým plotom', icon='i-broom',
       chips=['sutina', 'čistenie', 'pozemok'],
       scope=[('Sutina', 'zhromaždenie a odvoz stavebnej sutiny a odpadu'),
              ('Hrubé čistenie', 'odstránenie prachu a zvyškov po stavebných prácach'),
              ('Pozemok', 'vyčistenie a úprava pozemku po stavbe'),
              ('Terén', 'zarovnanie terénu po výkopoch a montáži'),
              ('Obaly a zvyšky', 'odnesenie paliet, obalov a nepotrebného materiálu'),
              ('Na záver zákazky', 'upratanie ako súčasť každej našej realizácie')],
       forwho=['Majitelia po dokončení stavby', 'Stavebníci pred kolaudáciou', 'Domácnosti po rekonštrukcii'],
       gallery=[('r093.webp', 'Pozemok po dokončení plota'), ('r094.webp', 'Upravený terén pri plote'), ('r101.webp', 'Hotová realizácia')],
       faq=[('Odvážate aj sutinu?', 'Áno, sutinu a stavebný odpad zhromaždíme a zabezpečíme odvoz. Spôsob a cenu dohodneme podľa množstva.'),
            ('Upracete aj po prácach iných firiem?', 'Áno, upratovanie objednávate aj samostatne, nielen po našich prácach.'),
            ('Je upratanie súčasťou vašich realizácií?', 'Áno. Po každej našej zákazke po sebe uprateme.')]),
  dict(slug='ploty-betonove', no='05', name='Betónové ploty', short='Betónové ploty',
       title='Betónové ploty na kľúč Ružomberok | LIBES s.r.o. (BP ploty)',
       desc='Betónové ploty na kľúč v Ružomberku a okolí — vibrolisovaný betón v dekore kameň, drevo a tehla, výška až 200 cm. Predtým BP ploty.',
       h1='Betónové ploty', h1b='na kľúč.',
       lead='Vibrolisovaný betón s reliéfnym povrchom — masívny, nepriehľadný a bez údržby na desaťročia. Dovezieme, postavíme a po sebe uprateme. Ploty, ktoré ste poznali ako BP ploty.',
       hero='g-stone.webp', hero_alt='Betónový plot s kamenným dekorom', icon='i-wall', legacy=True,
       chips=['výška do 200 cm', '3 dekory', 'bez údržby'],
       scope=[('Zameranie', 'obhliadka pozemku a návrh výšky, dekoru a stĺpikov'),
              ('Dovoz', 'doprava materiálu priamo na pozemok'),
              ('Základy', 'osadenie a zabetónovanie stĺpikov'),
              ('Montáž', 'skladanie dosiek až do výšky 200 cm'),
              ('Bránky a brány', 'riešenie vstupu podľa dohody'),
              ('Upratanie', 'odvoz zvyškov a úprava terénu po montáži')],
       forwho=['Rodinné domy, ktoré chcú súkromie', 'Hranice pozemku pri ceste alebo susedoch', 'Majitelia, ktorí nechcú plot natierať'],
       variants=('Dekory', [('Kameň', 'tex-kamen.webp', 'hlboký reliéf, masívny vzhľad'), ('Drevodekor', 'tex-drevo.webp', 'kresba drevených latí so sukmi'), ('Tehla', 'tex-tehla.webp', 'murovaný tehlový vzor')]),
       specs=[('Materiál', 'vibrolisovaný betón'), ('Výška', '100 – 200 cm'), ('Šírka poľa', 'bežne 2,0 m'), ('Doska', 'bežne 50 cm'), ('Údržba', 'žiadna — bez natierania'), ('Montáž', 'na kľúč vrátane upratania')],
       gallery=[('g-stone-garden.webp', 'Plot v kvitnúcej záhrade'), ('r054.webp', 'Detail kamenného dekoru'), ('r039.webp', 'Drevodekor pri starom dome'),
                ('r064.webp', 'Drevodekor pri novostavbe'), ('r060.webp', 'Kamenný dekor pri rodinnom dome'), ('r003.webp', 'Súkromie terasy')],
       planner=True, ba=True,
       faq=[('Akú maximálnu výšku plota viete postaviť?', 'Betónové ploty realizujeme do výšky 200 cm. Pre rodinný dom sa najčastejšie volí 150 – 180 cm, pri väčšom dôraze na súkromie 180 – 200 cm.'),
            ('Aký je rozdiel medzi kamenným a drevodekorom?', 'Kamenný dekor má hlbší, hrubší reliéf a pôsobí masívnejšie. Drevodekor má jemnejšiu kresbu so sukmi a pripomína drevené laťovanie. Oba sú rovnako odolný vibrolisovaný betón.'),
            ('Potrebuje betónový plot údržbu?', 'Nie. Vibrolisovaný betón nevyžaduje natieranie ani impregnáciu.'),
            ('Potrebujem na plot stavebné povolenie?', 'Bežný plot do 2 m spravidla nevyžaduje stavebné povolenie, pravidlá sa však môžu líšiť podľa obce. Odporúčame overiť si to na miestnom stavebnom úrade.'),
            ('Dá sa stavať aj v zime?', 'Betónovanie vyžaduje teploty nad bodom mrazu, takže pri silných mrazoch práce pozastavíme. Inak pracujeme celý rok.')]),
  dict(slug='ploty-3d', no='06', name='3D ploty', short='3D ploty',
       title='3D ploty a plotové panely Ružomberok | LIBES s.r.o. (BP ploty)',
       desc='3D plotové panely s montážou v Ružomberku a okolí — zelená, hnedá a antracit, podhrabové dosky, bránky a brány. Predtým BP ploty.',
       h1='3D ploty', h1b='vzdušné a pevné.',
       lead='Zvárané kovové panely s prelisom — ľahké, priehľadné a rýchle na montáž aj na svahovitom teréne. S podhrabovou doskou, bránkou aj bránou na mieru.',
       hero='r106.webp', hero_alt='3D plotový panel v antracitovej farbe', icon='i-mesh', legacy=True,
       chips=['3 farby', 'podhrabové dosky', 'svahy'],
       scope=[('Zameranie', 'obhliadka a návrh výšky, farby a riešenia na svahu'),
              ('Stĺpiky', 'osadenie a zabetónovanie stĺpikov'),
              ('Podhrabové dosky', 'betónová doska pod panelom proti podhrabaniu'),
              ('Panely', 'montáž 3D panelov v zvolenej farbe a výške'),
              ('Bránky a brány', 'vstupy a vjazdy podľa dohody'),
              ('Upratanie', 'odvoz zvyškov a úprava terénu')],
       forwho=['Záhrady a pozemky, kde chcete výhľad', 'Svahovité pozemky', 'Firemné a hospodárske plochy'],
       variants=('Farby', [('Zelená', 'c3d-zeleny.webp', 'splynie so zeleňou záhrady'), ('Hnedá', 'c3d-hnedy.webp', 'teplý odtieň k dreveným stavbám'), ('Antracit', 'c3d-antracit.webp', 'moderný, elegantný vzhľad')]),
       specs=[('Typ', 'zváraný panel s 3D prelisom'), ('Farby', 'zelená, hnedá, antracit'), ('Šírka panela', 'bežne 2,5 m'), ('Podhrab', 'betónová podhrabová doska'), ('Terén', 'aj svahy a nerovný terén'), ('Montáž', 'na kľúč vrátane upratania')],
       gallery=[('r106.webp', 'Antracitový panel s podhrabom'), ('r045.webp', 'Zelený panel pri záhrade'), ('r110.webp', 'Panel s tujami'),
                ('r029.webp', 'Plot pri rodinnom dome'), ('r037.webp', 'Panel pri dlažbe')],
       planner=True,
       faq=[('Aký je rozdiel medzi betónovým a 3D plotom?', 'Betónový plot je masívny a nepriehľadný. 3D plot je zváraný kovový panel — ľahší, priehľadnejší, rýchlejšie sa montuje a je vo viacerých farbách.'),
            ('Dá sa 3D plot postaviť na svahu?', 'Áno, 3D panely sa dajú osadiť aj na svahovitom a nerovnom teréne. Riešenie navrhneme pri obhliadke.'),
            ('Na čo slúži podhrabová doska?', 'Betónová doska pod panelom bráni podhrabaniu zvieratami, drží burinu mimo plota a pôsobí upravene.')]),
]
BY = {s['slug']: s for s in SERVICES}

EXTRA_CSS = r'''
.foot-grid .fh{font-family:var(--f-mono);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--bone);font-weight:500;margin:0 0 16px}
.fab{transition:opacity .25s,transform .25s}.fab.fab-off{opacity:0;transform:translateY(20px);pointer-events:none}
/* ===== podstránky ===== */
.crumbs{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-family:var(--f-mono);font-size:.72rem;letter-spacing:.06em;color:var(--stone-d);margin-bottom:26px}
.crumbs a{text-decoration:none;color:var(--stone-d)}.crumbs a:hover{color:var(--brass-hi)}
.crumbs i{font-style:normal;opacity:.5}
.crumbs b{color:var(--bone);font-weight:500}
.p-hero{position:relative;overflow:hidden;background:radial-gradient(1000px 520px at 85% 0%,rgba(198,155,91,.10),transparent 60%),var(--coal);padding-block:56px 72px}
.p-hero::after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.07;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.p-hero>.wrap{position:relative;z-index:1}
.p-grid{display:grid;gap:48px;align-items:center}
@media (min-width:1000px){.p-grid{grid-template-columns:1.1fr .9fr;gap:64px}}
.p-hero h1{font-family:var(--f-display);font-weight:700;text-transform:uppercase;font-size:clamp(2.8rem,7vw,5.4rem);line-height:1.12;margin-top:18px}
.p-hero h1 span{display:block;color:var(--brass);font-weight:600}
.p-hero .lead{color:#C9D3CC;max-width:54ch}
.p-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.p-chips span{font-family:var(--f-mono);font-size:.72rem;letter-spacing:.04em;padding:6px 12px;border-radius:999px;border:1px solid var(--line-d);color:var(--bone);background:rgba(234,229,216,.04)}
.p-photo{position:relative;padding-left:26px;min-width:0}
.p-photo::before{content:"";position:absolute;left:0;top:30px;bottom:-30px;width:48px;background:repeating-linear-gradient(90deg,var(--brass) 0 5px,transparent 5px 13px);opacity:.85}
.p-photo .frame{position:relative;border-radius:var(--r);overflow:hidden;aspect-ratio:5/4;max-width:100%;background:var(--coal-3);box-shadow:0 40px 80px -30px rgba(0,0,0,.7)}
.p-photo .frame img{width:100%;height:100%;object-fit:cover}
.p-photo .frame.tex{background-size:cover;background-position:center;display:flex;align-items:center;justify-content:center}
.p-photo .frame.tex::before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,rgba(var(--rgb),.85),rgba(var(--rgb),.55))}
.p-photo .frame.tex svg{position:relative;width:120px;height:120px;color:var(--brass-hi)}
.p-photo .legacy{position:absolute;left:44px;bottom:16px;z-index:2;font-family:var(--f-mono);font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;background:var(--brass);color:#1B1408;padding:5px 10px;border-radius:999px}
@media (prefers-reduced-motion:no-preference){.p-photo::before{transform-origin:top;animation:grow 1.1s cubic-bezier(.6,0,.2,1) .1s both}}
.scope-grid{display:grid;gap:44px}
@media (min-width:980px){.scope-grid{grid-template-columns:1.35fr .65fr;gap:56px;align-items:start}}
.scope{display:grid;grid-template-columns:1fr;gap:1px;background:var(--line-l);border:1px solid var(--line-l);border-radius:var(--r);overflow:hidden}
@media (min-width:640px){.scope{grid-template-columns:1fr 1fr}}
.scope div{background:var(--bone-2);padding:24px 22px;min-width:0}
.scope h3{font-family:var(--f-display);text-transform:uppercase;font-weight:600;font-size:1.3rem;letter-spacing:.01em;display:flex;gap:10px;align-items:center}
.scope h3::before{content:"";width:14px;height:9px;flex:none;background:repeating-linear-gradient(90deg,var(--brass-deep) 0 2px,transparent 2px 4px)}
.scope p{color:var(--stone-l);font-size:.92rem;margin-top:8px}
.forwho{background:var(--coal);color:var(--bone);border-radius:var(--r);padding:30px;position:relative;overflow:hidden}
.forwho::after{content:"";position:absolute;right:-40px;bottom:-40px;width:160px;height:160px;background:repeating-linear-gradient(90deg,rgba(198,155,91,.15) 0 6px,transparent 6px 16px)}
.forwho h3{font-family:var(--f-display);text-transform:uppercase;font-weight:600;font-size:1.5rem}
.forwho ul{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:12px;position:relative;z-index:1}
.forwho li{display:flex;gap:12px;font-size:.95rem;color:#D3DBD5}
.forwho li svg{width:18px;height:18px;flex:none;color:var(--brass);margin-top:3px}
.forwho .btn{margin-top:24px;position:relative;z-index:1}
.var-grid{display:grid;gap:40px}
@media (min-width:980px){.var-grid{grid-template-columns:1.2fr .8fr;gap:56px;align-items:start}}
.variants{display:grid;gap:14px;grid-template-columns:1fr}
@media (min-width:640px){.variants{grid-template-columns:repeat(3,1fr)}}
.variant{border-radius:var(--r);overflow:hidden;border:1px solid var(--line-d);background:var(--coal-3);min-width:0}
.variant .img{aspect-ratio:4/3;background-size:cover;background-position:center}
.variant div.t{padding:16px 18px}
.variant b{font-family:var(--f-display);text-transform:uppercase;font-weight:600;font-size:1.35rem;letter-spacing:.01em;display:block}
.variant span{display:block;color:var(--stone-d);font-size:.86rem;margin-top:4px}
.specs{border:1px solid var(--line-d);border-radius:var(--r);overflow:hidden}
.specs div{display:flex;justify-content:space-between;gap:16px;padding:14px 18px;border-bottom:1px solid var(--line-d);font-size:.92rem}
.specs div:last-child{border-bottom:0}
.specs dt{font-family:var(--f-mono);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--stone-d);padding-top:3px}
.specs dd{margin:0;font-weight:600;text-align:right}
.specs-note{font-family:var(--f-mono);font-size:.68rem;color:var(--stone-d);margin-top:12px}
.planner-cta{margin-top:20px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:18px 20px;border-radius:var(--r);background:rgba(198,155,91,.1);border:1px solid rgba(198,155,91,.35)}
.planner-cta p{font-size:.92rem;color:var(--bone);max-width:34ch}
.gal.sub{grid-auto-rows:220px}
@media (min-width:900px){.gal.sub{grid-template-columns:repeat(3,1fr);grid-auto-rows:260px}}
.gal-empty{border:1.5px dashed rgba(122,86,38,.35);border-radius:var(--r);padding:40px 28px;text-align:center;color:var(--stone-l)}
.gal-empty b{display:block;font-family:var(--f-display);text-transform:uppercase;font-size:1.4rem;color:var(--ink);margin-bottom:8px;font-weight:600}
.related{display:grid;gap:14px;grid-template-columns:1fr}
@media (min-width:700px){.related{grid-template-columns:repeat(3,1fr)}}
.rel{display:flex;gap:14px;align-items:center;padding:14px;border-radius:var(--r);border:1px solid var(--line-l);background:var(--bone-2);text-decoration:none;color:var(--ink);transition:border-color .18s,transform .18s;min-width:0}
.rel:hover{border-color:rgba(122,86,38,.45);transform:translateY(-2px)}
.rel .th{width:72px;height:60px;border-radius:4px;flex:none;background-size:cover;background-position:center;background-color:var(--coal-2)}
.rel b{display:block;font-family:var(--f-display);text-transform:uppercase;font-weight:600;font-size:1.15rem;letter-spacing:.01em}
.rel small{display:block;font-family:var(--f-mono);font-size:.66rem;color:var(--stone-l);margin-top:2px}
.rel .ar{margin-left:auto;color:var(--brass-deep)}
'''

def e(t):
    return html.escape(t, quote=True)

def thumb(f):
    return R + 'img/s/' + f

def srcset(f, sizes):
    return f'src="{thumb(f)}" srcset="{thumb(f)} 640w, {img_url(f)} 1400w" sizes="{sizes}"'

def img_url(f):
    return R + 'img/' + f

def header(active):
    nav = [('Služby', HOME + '#sluzby'), ('Plánovač', HOME + '#planovac'), ('Realizácie', HOME + '#realizacie'), ('Postup', HOME + '#postup'), ('Kontakt', HOME + '#objednavka')]
    links = ''.join(f'<a href="{h}">{t}</a>' for t, h in nav)
    return f'''
<section class="topbar" aria-label="Kontakt a otváracie hodiny"><div class="wrap">
  <span><i class="dot"></i> Po – Pia <b>7:00 – 16:00</b><span class="hide-sm">&nbsp;· Ružomberok a okolie</span></span>
  <span><span class="concept">KONCEPT</span><span class="hide-sm">&nbsp;·&nbsp;<a href="mailto:libes.sro@gmail.com" style="text-decoration:none">libes.sro@gmail.com</a>&nbsp;·&nbsp;<a href="tel:{TEL}" style="text-decoration:none;color:var(--bone)">{PHONE}</a></span></span>
</div></section>
<header class="site"><div class="wrap">
  <a class="logo" href="{HOME}"><svg viewBox="0 0 107 163" fill="#EAE5D8" aria-hidden="true"><use href="#mark"/></svg><span class="word">LIBES</span><span class="sro">s.r.o.</span></a>
  <nav class="nav" aria-label="Hlavná navigácia">{links}</nav>
  <div class="head-actions">
    <a class="head-phone" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>{PHONE}</a>
    <a class="btn btn-brass btn-sm hide-xs" href="{HOME}?sluzba={e(active)}#objednavka">Vytvoriť objednávku</a>
    <button type="button" class="burger" id="burger" aria-label="Otvoriť menu" aria-expanded="false" aria-controls="mnav"><i></i><i></i><i></i></button>
  </div>
</div></header>
<div class="mnav" id="mnav" hidden>
  <nav aria-label="Mobilná navigácia">
    <a href="{HOME}">Domov</a>{''.join(f'<a href="../{s["slug"]}/index.html">{s["short"]}</a>' for s in SERVICES)}<a href="{HOME}#objednavka">Objednávka a kontakt</a>
  </nav>
  <div class="mnav-foot">
    <a class="btn btn-brass" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>{PHONE}</a>
    <a class="btn btn-line" href="https://wa.me/421951565717" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>WhatsApp</a>
    <span>Po – Pia 7:00 – 16:00 · Ružomberok a okolie</span>
  </div>
</div>'''

def footer():
    svc = ''.join(f'<li><a href="../{s["slug"]}/index.html">{s["name"]}</a></li>' for s in SERVICES)
    return f'''
<footer class="site">
  <div class="wrap"><div class="foot-grid">
    <div class="foot-about"><a class="logo" href="{HOME}"><svg viewBox="0 0 107 163" fill="#EAE5D8" aria-hidden="true"><use href="#mark"/></svg><span class="word">LIBES</span><span class="sro">s.r.o.</span></a>
      <p>Stavebné a pomocné práce, prenos materiálu, upratovanie a montáž plotov. Ružomberok a okolie. Predtým BP ploty.</p></div>
    <div><h2 class="fh">Služby</h2><ul>{svc}</ul></div>
    <div><h2 class="fh">Web</h2><ul><li><a href="{HOME}#planovac">Plánovač plota</a></li><li><a href="{HOME}#realizacie">Realizácie</a></li><li><a href="{HOME}#faq">Časté otázky</a></li><li><a href="{HOME}#objednavka">Objednávka</a></li></ul></div>
    <div><h2 class="fh">Kontakt</h2><ul><li><a href="tel:{TEL}" style="color:var(--bone);font-family:var(--f-mono)">{PHONE}</a></li><li><a href="mailto:libes.sro@gmail.com">libes.sro@gmail.com</a></li><li>Po – Pia 7:00 – 16:00</li><li>Ružomberok a okolie</li></ul></div>
  </div></div>
  <div class="giant" aria-hidden="true"><svg viewBox="-1 -1 109 165"><use href="#mark"/></svg><span>LIBES</span></div>
  <div class="wrap foot-bottom"><span>© 2026 LIBES s.r.o.</span><span><a href="../../ochrana-osobnych-udajov/index.html" style="color:inherit">Ochrana osobných údajov</a> · IČO a sídlo doplníme po zápise s.r.o.</span></div>
</footer>
<aside aria-label="Rýchly kontakt"><a class="fab" href="tel:{TEL}"><span class="ring"><svg><use href="#i-phone"/></svg></span><span><small>Zavolajte nám</small><b>{PHONE}</b></span></a></aside>
<nav class="mbar" aria-label="Rýchly kontakt">
  <a class="call" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>Zavolať</a>
  <a class="wa" href="https://wa.me/421951565717" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>WhatsApp</a>
  <a class="order" href="{HOME}#objednavka">Objednať <svg><use href="#i-arrow"/></svg></a>
</nav>
<div class="lightbox" id="lb" hidden role="dialog" aria-modal="true" aria-label="Fotografia realizácie">
  <button type="button" class="lb-btn lb-close" id="lbClose" aria-label="Zavrieť">✕</button>
  <button type="button" class="lb-btn lb-prev" id="lbPrev" aria-label="Predchádzajúca">←</button>
  <figure><img id="lbImg" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt=""><figcaption><span id="lbCap"></span><span id="lbNum"></span></figcaption></figure>
  <button type="button" class="lb-btn lb-next" id="lbNext" aria-label="Ďalšia">→</button>
</div>'''

JS = r'''
<script>
(function(){
  var bg=document.getElementById('burger'), mn=document.getElementById('mnav');
  function menu(o){mn.hidden=!o;bg.setAttribute('aria-expanded',String(o));document.body.classList.toggle('menu-open',o);if(o){var f=mn.querySelector('a');f&&f.focus()}else{bg.focus()}}
  bg.addEventListener('click',function(){menu(mn.hidden)});
  mn.addEventListener('click',function(e){if(e.target.closest('a'))menu(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!mn.hidden)menu(false)});
  var items=[].slice.call(document.querySelectorAll('#gallery button'));
  var lb=document.getElementById('lb'),li=document.getElementById('lbImg'),lc=document.getElementById('lbCap'),ln=document.getElementById('lbNum'),cur=0;
  var lastF;function show(i){if(lb.hidden)lastF=document.activeElement;cur=(i+items.length)%items.length;var im=items[cur].querySelector('img');li.src=im.dataset.full||im.src;li.alt=im.alt;lc.textContent=im.alt;ln.textContent=(cur+1)+' / '+items.length;lb.hidden=false;document.getElementById('lbClose').focus()}
  function closeLb(){lb.hidden=true;if(lastF)lastF.focus()}
  items.forEach(function(b,i){b.addEventListener('click',function(){show(i)})});
  document.getElementById('lbClose').onclick=closeLb;
  document.getElementById('lbPrev').onclick=function(){show(cur-1)};
  document.getElementById('lbNext').onclick=function(){show(cur+1)};
  lb.addEventListener('click',function(e){if(e.target===lb)closeLb()});
  document.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')closeLb();if(e.key==='ArrowRight')show(cur+1);if(e.key==='ArrowLeft')show(cur-1)});
  var fab=document.querySelector('.fab');
  if(fab&&'IntersectionObserver' in window){var vis=new Set(),io=new IntersectionObserver(function(es){es.forEach(function(x){x.isIntersecting?vis.add(x.target):vis.delete(x.target)});fab.classList.toggle('fab-off',vis.size>0)},{rootMargin:'0px 0px -10% 0px'});
    document.querySelectorAll('.cta,footer.site,.sheet-foot,#objednavka').forEach(function(el){io.observe(el)})}
})();
</script>'''

def page(s):
    order = f'{HOME}?sluzba={e(s["name"])}#objednavka'
    if s.get('hero'):
        frame = f'<div class="frame"><img {srcset(s["hero"], "(min-width:1000px) 520px, 100vw")} alt="{e(s["hero_alt"])}" fetchpriority="high" width="1200" height="960"></div>'
    else:
        frame = f'<div class="frame tex" style="background-image:url({img_url(s["hero_tex"])})"><svg><use href="#{s["icon"]}"/></svg></div>'
    legacy = '<span class="legacy">pôvodne BP ploty</span>' if s.get('legacy') else ''
    chips = ''.join(f'<span>{e(c)}</span>' for c in s['chips'])
    scope = ''.join(f'<div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in s['scope'])
    forwho = ''.join(f'<li><svg><use href="#i-check"/></svg>{e(x)}</li>' for x in s['forwho'])

    variants_html = ''
    if s.get('variants'):
        vt, vs = s['variants']
        cards = ''.join(f'<div class="variant"><div class="img" style="background-image:url({thumb(f)})" role="img" aria-label="{e(n)}"></div><div class="t"><b>{e(n)}</b><span>{e(d)}</span></div></div>' for n, f, d in vs)
        specs = ''.join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in s['specs'])
        planner = f'<div class="planner-cta"><p>Vyskúšajte si výšku, dĺžku a {vt.lower()[:-1]+"u" if vt=="Farby" else "dekor"} v plánovači s výkresom.</p><a class="btn btn-brass btn-sm" href="#planovac">Otvoriť plánovač <svg><use href="#i-arrow"/></svg></a></div>' if s.get('planner') else ''
        variants_html = f'''
<section class="band dark-2">
  <div class="wrap">
    <div class="sec-head split"><div><span class="eyebrow"><i class="stripes"></i>{vt} a parametre</span><h2 class="h-sec">Vyberte si<br>vzhľad.</h2></div>
      <p class="lead">Všetky varianty montujeme na kľúč. Pri obhliadke vám ukážeme vzorky a poradíme, čo sa hodí k vášmu domu.</p></div>
    <div class="var-grid">
      <div class="variants">{cards}</div>
      <div><dl class="specs" style="margin:0">{specs}</dl><p class="specs-note">Rozmery sú orientačné; presné riešenie navrhneme po zameraní.</p>{planner}</div>
    </div>
  </div>
</section>'''

    if s['gallery']:
        btns = ''.join(f'<button type="button" data-i="{i}"><img {srcset(f, "(min-width:900px) 33vw, 50vw")} data-full="{img_url(f)}" alt="{e(c)}" loading="lazy"><span class="cap" aria-hidden="true">{e(c)}</span></button>' for i, (f, c) in enumerate(s['gallery']))
        gallery = f'<div class="gal sub" id="gallery">{btns}</div>'
    else:
        gallery = f'<div id="gallery"></div><div class="gal-empty"><b>Fotky pripravujeme</b>{e(s["gallery_note"])}<div style="margin-top:18px"><a class="btn btn-ink btn-sm" href="{HOME}#realizacie">Realizácie plotov <svg><use href="#i-arrow"/></svg></a></div></div>'

    faq = ''.join(f'<details{" open" if i == 0 else ""}><summary><span>{e(q)}</span><i class="pm"></i></summary><div class="ans">{e(a)}</div></details>' for i, (q, a) in enumerate(s['faq']))

    tool_html, tool_js = TOOLS.get(s['slug'], ('', ''))
    tool_anchor = 'planovac' if s.get('planner') else 'nastroj'
    tool_label = 'Navrhnite si plot v plánovači' if s.get('planner') else {'murarske-prace': 'Spočítajte si tvárnice', 'pomocne-prace': 'Spočítajte si výkop', 'prenos-materialu': 'Spočítajte váhu materiálu', 'upratovacie-prace': 'Zistite veľkosť kontajnera'}[s['slug']]
    planner_html = ''
    if s.get('planner'):
        planner_html = PLANNER_HTML.replace('href="#objednavka" id="pSend"', f'href="{HOME}#objednavka" id="pSend"')
    ba_html = BA_HTML if s.get('ba') else ''

    others = [x for x in SERVICES if x['slug'] != s['slug']]
    # pre ploty ukáž najprv druhý plot, inak najprv susedné služby
    others.sort(key=lambda x: (0 if ('ploty' in x['slug']) == ('ploty' in s['slug']) else 1))
    rel = ''.join(
        f'<a class="rel" href="../{x["slug"]}/index.html"><span class="th" style="background-image:url({thumb(x.get("hero") or x.get("hero_tex"))})"></span><span><b>{e(x["name"])}</b><small>/sluzby/{x["slug"]}</small></span><span class="ar">→</span></a>'
        for x in others[:3])

    ld = [
        {"@context": "https://schema.org", "@type": "Service", "name": s['name'], "serviceType": s['name'],
         "description": s['desc'], "areaServed": [{"@type": "City", "name": "Ružomberok"}, {"@type": "AdministrativeArea", "name": "Žilinský kraj"}],
         "provider": {"@type": "HomeAndConstructionBusiness", "name": "LIBES s.r.o.", "telephone": TEL, "email": "libes.sro@gmail.com"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Domov", "item": "/"},
            {"@type": "ListItem", "position": 2, "name": "Služby", "item": "/#sluzby"},
            {"@type": "ListItem", "position": 3, "name": s['name'], "item": f"/sluzby/{s['slug']}/"}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s['faq']]},
    ]
    ld_html = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)

    return f'''<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<title>{e(s['title'])}</title>
<meta name="description" content="{e(s['desc'])}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0A1D16">
<meta property="og:type" content="website"><meta property="og:locale" content="sk_SK"><meta property="og:site_name" content="LIBES s.r.o.">
<meta property="og:title" content="{e(s['title'])}"><meta property="og:description" content="{e(s['desc'])}">
{ld_html}
{FONTS}<style>{STYLE}{EXTRA_CSS}{TOOL_CSS}</style>
</head>
<body>
{SPRITE}
{header(s['name'])}
<main>
<section class="p-hero">
  <div class="wrap p-grid">
    <div>
      <nav class="crumbs" aria-label="Omrvinky"><a href="{HOME}">Domov</a><i>/</i><a href="{HOME}#sluzby">Služby</a><i>/</i><b>{e(s['name'])}</b></nav>
      <span class="eyebrow"><i class="stripes"></i>Služba {s['no']} / 06 · Ružomberok a okolie</span>
      <h1>{e(s['h1'])}<span>{e(s['h1b'])}</span></h1>
      <p class="lead" style="margin-top:22px">{e(s['lead'])}</p>
      <div class="hero-cta">
        <a class="btn btn-brass" href="{order}">{e({'ploty-3d':'Objednať 3D plot','ploty-betonove':'Objednať betónový plot'}.get(s['slug'],'Objednať '+s['name'].lower()))} <svg><use href="#i-arrow"/></svg></a>
        <a class="btn btn-line" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>{PHONE}</a>
      </div>
      <div class="p-chips">{chips}</div>
      <a href="#{tool_anchor}" class="tool-link">{tool_label} ↓</a>
    </div>
    <div class="p-photo">{frame}{legacy}</div>
  </div>
</section>

<section class="band light">
  <div class="wrap">
    <div class="sec-head split"><div><span class="eyebrow"><i class="stripes"></i>Čo zahŕňa</span><h2 class="h-sec">Čo pre vás<br>urobíme.</h2></div>
      <p class="lead">Rozsah prác prispôsobíme stavbe. Môžete objednať všetko naraz alebo len to, čo práve potrebujete.</p></div>
    <div class="scope-grid">
      <div class="scope">{scope}</div>
      <aside class="forwho"><h3>Pre koho</h3><ul>{forwho}</ul><a class="btn btn-brass btn-sm" href="{order}">Nezáväzná ponuka <svg><use href="#i-arrow"/></svg></a></aside>
    </div>
  </div>
</section>
{tool_html}
{variants_html}
{planner_html}
<section class="band light-2">
  <div class="wrap">
    <div class="sec-head split"><div><span class="eyebrow"><i class="stripes"></i>Realizácie</span><h2 class="h-sec">Z našich<br>zákaziek.</h2></div>
      <p class="lead">Fotografie z reálnych stavieb v Ružomberku a okolí. Kliknutím zväčšíte.</p></div>
    {ba_html}{gallery}
  </div>
</section>

<section class="band dark">
  <div class="wrap">
    <div class="sec-head split"><div><span class="eyebrow"><i class="stripes"></i>Ako to prebieha</span><h2 class="h-sec">Štyri kroky<br>k hotovej práci.</h2></div>
      <p class="lead">Od prvého telefonátu po upratané stavenisko.</p></div>
    <div class="steps">
      <div class="step"><h3>Ozvete sa</h3><p>Zavoláte, napíšete na WhatsApp alebo vyplníte objednávku.</p><span class="tag">odpoveď do 24 h</span></div>
      <div class="step"><h3>Obhliadka</h3><p>Prídeme na miesto, zameriame a poradíme s riešením.</p><span class="tag">zdarma</span></div>
      <div class="step"><h3>Cenová ponuka</h3><p>Jasná kalkulácia — práca, materiál aj doprava.</p><span class="tag">nezáväzne</span></div>
      <div class="step"><h3>Realizácia</h3><p>V dohodnutom termíne odvedieme prácu a uprateme.</p><span class="tag">na kľúč</span></div>
    </div>
  </div>
</section>

<section class="band light">
  <div class="wrap faq-grid">
    <div class="faq-aside"><span class="eyebrow"><i class="stripes"></i>Otázky</span><h2 class="h-sec">{e(s['name'])}:<br>časté otázky.</h2>
      <p class="lead">Nenašli ste odpoveď? Zavolajte, vysvetlíme to osobne.</p>
      <a class="btn btn-ink" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>{PHONE}</a></div>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="band light-2" style="padding-block:64px">
  <div class="wrap">
    <span class="eyebrow"><i class="stripes"></i>Ďalšie služby</span>
    <h2 class="h-sec" style="font-size:clamp(1.8rem,3.6vw,2.6rem);margin-bottom:28px">Môžete objednať aj</h2>
    <div class="related">{rel}</div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <div><h2>{e(s['name'])}?<br>Zavolajte.</h2><a class="num" href="tel:{TEL}">{PHONE}</a></div>
    <div class="cta-actions">
      <a class="btn btn-ink" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>Zavolať teraz</a>
      <a class="btn btn-line" href="https://wa.me/421951565717" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>WhatsApp</a>
      <a class="btn btn-line" href="{order}">Objednávka online</a>
    </div>
  </div>
</section>
</main>
{footer()}
{JS}
{('<script>(function(){'+COMMON_JS+tool_js+'})();</script>') if tool_js else ''}
{('<script>(function(){function fmt(n){return String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g,"\\u2009")}function say(){}\n'+PLANNER_JS+("  document.querySelector('#pType button[data-v=\"3d\"]').click();\n" if s['slug']=='ploty-3d' else '')+'})();</script>') if s.get('planner') else ''}
</body>
</html>'''

for s in SERVICES:
    d = os.path.join(HERE, 'sluzby', s['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(s))
print('vygenerovaných podstránok:', len(SERVICES))


# ---------------------------------------------------------------- OCHRANA OSOBNÝCH ÚDAJOV
def privacy_page():
    sections = [
        ('Prevádzkovateľ', 'LIBES s.r.o., sídlo: <mark>[doplniť]</mark>, IČO: <mark>[doplniť]</mark>, zapísaná v Obchodnom registri <mark>[doplniť]</mark>. Kontakt: <a href="mailto:libes.sro@gmail.com">libes.sro@gmail.com</a>, <a href="tel:+421951565717">0951 565 717</a>.'),
        ('Aké údaje spracúvame', 'Údaje, ktoré nám pošlete cez objednávkový formulár, e‑mail, telefón, WhatsApp alebo Viber: meno a priezvisko, telefónne číslo, e‑mail, miesto realizácie a popis požadovaných prác vrátane údajov z kalkulačiek na webe.'),
        ('Na aký účel a na akom základe', 'Údaje používame výhradne na vybavenie vášho dopytu — spätný kontakt, obhliadku, prípravu cenovej ponuky a prípadné uzavretie a plnenie zmluvy. Právnym základom je vykonanie opatrení pred uzavretím zmluvy a plnenie zmluvy (čl. 6 ods. 1 písm. b) nariadenia GDPR). Pri účtovných dokladoch je základom splnenie zákonnej povinnosti (čl. 6 ods. 1 písm. c) GDPR).'),
        ('Ako dlho údaje uchovávame', 'Ak zmluva nevznikne, údaje z dopytu vymažeme najneskôr do 12 mesiacov od posledného kontaktu. Ak zmluva vznikne, uchovávame ich po dobu jej plnenia a záručnej doby; účtovné doklady po dobu stanovenú zákonom o účtovníctve.'),
        ('Komu údaje poskytujeme', 'Údaje nepredávame ani neposkytujeme na marketing. K údajom môžu mať prístup len poskytovatelia technických služieb, ktoré používame (poskytovateľ e‑mailu, služba na doručovanie formulára z webu, hosting webu). <mark>[overiť konkrétnych poskytovateľov a prípadný prenos mimo EÚ]</mark>'),
        ('Vaše práva', 'Máte právo na prístup k svojim údajom, ich opravu, vymazanie, obmedzenie spracúvania, prenosnosť a právo namietať. Stačí nám napísať na libes.sro@gmail.com. Ak sa domnievate, že s údajmi zaobchádzame nesprávne, môžete podať návrh Úradu na ochranu osobných údajov SR, Hraničná 12, 820 07 Bratislava, www.dataprotection.gov.sk.'),
        ('Cookies', 'Tento web nepoužíva reklamné ani analytické cookies. Ak sa v budúcnosti pridá napríklad návštevnosť cez Google Analytics, doplníme lištu so súhlasom a túto časť aktualizujeme.'),
    ]
    body = ''.join(f'<section class="pp-sec"><h2>{t}</h2><p>{c}</p></section>' for t, c in sections)
    hdr = header('Iné').replace('?sluzba=Iné', '')
    ftr = footer()
    def fix(x):
        x = x.replace('../../', '§§/')
        for sv in SERVICES:
            x = x.replace(f'href="../{sv["slug"]}/', f'href="§§/sluzby/{sv["slug"]}/')
        x = x.replace('§§/ochrana-osobnych-udajov/', '')  # odkaz na seba
        return x.replace('§§/', '../')
    css = '''.pp{max-width:760px}.pp-sec{padding-block:26px;border-bottom:1px solid var(--line-l)}.pp-sec:last-child{border-bottom:0}
.pp-sec h2{font-family:var(--f-display);text-transform:uppercase;font-weight:600;font-size:1.6rem;line-height:1.2}
.pp-sec p{color:#3D382F;margin-top:10px;font-size:1rem;line-height:1.7}.pp-sec a{color:var(--brass-deep)}
mark{background:#F3E2BF;color:#5A3E12;padding:0 4px;border-radius:3px}
.pp-note{font-family:var(--f-mono);font-size:.74rem;color:var(--brass-deep);background:#FBF5EA;border:1px dashed rgba(122,86,38,.4);border-radius:6px;padding:12px 14px;margin-bottom:12px}'''
    html_out = f'''<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<title>Ochrana osobných údajov | LIBES s.r.o.</title>
<meta name="description" content="Ako LIBES s.r.o. spracúva osobné údaje z dopytov a objednávok.">
<meta name="robots" content="noindex, follow">
{FONTS}<style>{STYLE}{EXTRA_CSS}{css}</style>
</head>
<body>
{SPRITE}
{fix(hdr)}
<main>
<section class="p-hero" style="padding-block:48px 56px"><div class="wrap">
  <nav class="crumbs" aria-label="Omrvinky"><a href="../index.html">Domov</a><i>/</i><b>Ochrana osobných údajov</b></nav>
  <h1 style="font-size:clamp(2.4rem,6vw,4.2rem)">Ochrana osobných údajov<span>jednoducho a zrozumiteľne.</span></h1>
</div></section>
<section class="band light" style="padding-block:56px"><div class="wrap pp">
  <p class="pp-note">NÁVRH TEXTU — pred zverejnením doplniť údaje firmy a nechať skontrolovať (právnik / GDPR poradca).</p>
  {body}
</div></section>
</main>
{fix(ftr)}
{fix(JS)}
</body>
</html>'''
    d = os.path.join(HERE, 'ochrana-osobnych-udajov')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html_out)
    print('vygenerovaná stránka: ochrana osobných údajov')

privacy_page()
