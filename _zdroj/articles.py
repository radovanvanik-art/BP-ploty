"""Poradňa LIBES — texty článkov. HTML telo článku je v 'body'.
Pri zmene zákona alebo postupu aktualizujte 'modified'.
"""

def fig(img, alt, cap):
    return (f'<figure class="art-fig"><img src="/img/s/{img}" srcset="/img/s/{img} 640w, /img/{img} 1400w" '
            f'sizes="(min-width:800px) 720px, 100vw" alt="{alt}" loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>')

def cta(text, href, label):
    return f'<aside class="art-cta"><p>{text}</p><a class="btn btn-brass btn-sm" href="{href}">{label} <svg><use href="#i-arrow"/></svg></a></aside>'

ARTICLES = [
dict(
  slug='betonovy-alebo-3d-plot',
  title='Betónový alebo 3D plot? Porovnanie a ako si vybrať | LIBES Ružomberok',
  desc='Betónový alebo 3D plot? Porovnanie súkromia, vzhľadu, údržby, montáže a povolenia podľa nového stavebného zákona. Rady od firmy, ktorá stavia oba typy.',
  h1='Betónový alebo 3D plot?', h1b='Porovnanie, ktoré pomôže vybrať.',
  lead='Oba typy plotov staviame pri rodinných domoch v Ružomberku a okolí každý týždeň. Tu je poctivé porovnanie — bez marketingových rečí.',
  minutes=5, image='g-stone.webp', published='2026-10-31', modified='2026-10-31',
  body=f'''
<h2>Rýchle porovnanie</h2>
<div class="tbl-wrap"><table class="cmp">
<thead><tr><th>Vlastnosť</th><th>Betónový plot</th><th>3D plot (panel)</th></tr></thead>
<tbody>
<tr><th>Súkromie</th><td>Úplné — plot je nepriehľadný</td><td>Malé — panel je priehľadný</td></tr>
<tr><th>Vzhľad</th><td>Masívny; dekor kameň, drevo alebo tehla</td><td>Vzdušný, moderný; zelená, hnedá, antracit</td></tr>
<tr><th>Údržba</th><td>Žiadna, netreba natierať</td><td>Minimálna, panel je povrchovo upravený</td></tr>
<tr><th>Hluk a vietor</th><td>Tlmí hluk z ulice, chráni pred vetrom</td><td>Hluk ani vietor netlmí</td></tr>
<tr><th>Svah a nerovný terén</th><td>Dá sa, ale náročnejšie (stupňovanie polí)</td><td>Jednoduchšie, panel sa ľahko prispôsobí</td></tr>
<tr><th>Rýchlosť montáže</th><td>Pomalšia — ťažké dosky, betónovanie stĺpikov</td><td>Rýchlejšia — ľahké panely</td></tr>
<tr><th>Ohlásenie stačí do výšky</th><td>1,6 m</td><td>2 m</td></tr>
</tbody></table></div>

<h2>Betónový plot: kedy je to správna voľba</h2>
<p>Betónový plot sa skladá zo stĺpikov a vibrolisovaných dosiek, ktoré sa do nich zasúvajú. Bežne má pole šírku 2 m a doska výšku 50 cm, takže výška plota rastie po pol metri. Povrch má reliéf — <strong>kameň</strong>, <strong>drevodekor</strong> alebo <strong>tehlu</strong>.</p>
<ul>
<li><strong>Chcete súkromie.</strong> Cez betónový plot nevidno, záhrada je naozaj vaša.</li>
<li><strong>Bývate pri rušnej ceste.</strong> Masívna stena tlmí hluk a zachytí prach.</li>
<li><strong>Nechcete sa o plot starať.</strong> Betón netreba natierať ani impregnovať.</li>
</ul>
<p>Na čo myslieť: betónový plot je ťažký, potrebuje poriadne zabetónované stĺpiky a na svahu sa polia stupňujú. A pri výške nad 1,6 m už nejde o drobnú stavbu — viac v článku <a href="/poradna/plot-a-stavebne-povolenie/">Plot a nový stavebný zákon</a>.</p>
{fig('r060.webp', 'Betónový plot s kamenným dekorom pri rodinnom dome v okolí Ružomberka', 'Betónový plot s kamenným dekorom — realizácia LIBES (BP ploty).')}

<h2>3D plot: kedy je to správna voľba</h2>
<p>3D plot tvoria zvárané kovové panely s prelisom (preto „3D“), ktoré sa pripevnia na stĺpiky. Pod panel sa dáva <strong>podhrabová doska</strong> — betónový pás, ktorý bráni zvieratám v podhrabaní a drží trávu mimo plota.</p>
<ul>
<li><strong>Chcete výhľad.</strong> Panel záhradu ohraničí, ale neuzavrie.</li>
<li><strong>Pozemok je vo svahu.</strong> Panely sa terénu prispôsobia jednoduchšie ako betónové polia.</li>
<li><strong>Oplocujete dlhý úsek.</strong> Montáž je rýchlejšia a plot pôsobí ľahko aj na desiatkach metrov.</li>
</ul>
<p>Na čo myslieť: 3D plot súkromie nedá. Ak ho chcete časom „zahustiť“, môžete pozdĺž neho vysadiť tuje alebo živý plot.</p>
{fig('r106.webp', '3D plotový panel v antracitovej farbe s podhrabovou doskou', '3D panel v antracitovej farbe s podhrabovou doskou.')}

<h2>Ako sa rozhodnúť: tri otázky</h2>
<ol>
<li><strong>Má byť cez plot vidieť?</strong> Nie → betónový. Áno → 3D.</li>
<li><strong>Aký vysoký má byť?</strong> Plný plot do 1,6 m a priehľadný do 2 m stačí ohlásiť. Vyšší potrebuje rozhodnutie o stavebnom zámere.</li>
<li><strong>Kde plot stojí?</strong> Pri ulici a susedoch často vyhrá betón (súkromie), smerom do poľa či lesa 3D panel (výhľad, nižšie náklady na dlhý úsek).</li>
</ol>
<p>Pokojne môžete aj kombinovať: betónový plot do ulice, kde chcete súkromie, a 3D panel na zadnej hranici pozemku.</p>
{cta('Vyskúšajte si oba typy v plánovači — nakreslí plot s rozmermi a spočíta polia, stĺpiky aj dosky.', '/#planovac', 'Otvoriť plánovač plota')}
''',
  faq=[('Je betónový plot drahší ako 3D plot?', 'Záleží od dĺžky, výšky a terénu. Pri dlhých úsekoch vychádza 3D panel spravidla výhodnejšie, pri plote do ulice ľudia často volia betón kvôli súkromiu. Presnú cenu pripravíme po bezplatnej obhliadke.'),
       ('Dá sa 3D plot neskôr zmeniť na nepriehľadný?', 'Úplne nie. Súkromie sa dá doplniť výsadbou živého plota alebo tují pozdĺž panelov.'),
       ('Ktorý plot vydrží dlhšie?', 'Oba sú určené na dlhé roky. Betón nevyžaduje údržbu, 3D panel má povrchovú úpravu proti korózii.')],
  related=['ploty-betonove', 'ploty-3d'],
),
dict(
  slug='plot-a-stavebne-povolenie',
  title='Plot a nový stavebný zákon: kedy stačí ohlásenie (2026) | LIBES',
  desc='Treba na plot povolenie? Od 1. 4. 2025 platí nový stavebný zákon: plný plot do 1,6 m a priehľadný do 2 m je drobná stavba a stačí ho ohlásiť. Čo platí pre vyšší plot, hranicu so susedom a plot pri ceste.',
  h1='Plot a nový stavebný zákon', h1b='Kedy stačí ohlásenie.',
  lead='Od 1. apríla 2025 platí nový stavebný zákon č. 25/2025 Z. z. Pre ploty priniesol jasné výškové limity. Zhrnuli sme, čo to znamená pre bežný rodinný dom.',
  minutes=6, image='r093.webp', published='2026-10-31', modified='2026-10-31',
  body=f'''
<p class="art-note"><strong>Dôležité:</strong> Tento článok je praktické zhrnutie, nie právna rada. Konkrétne podmienky pre váš pozemok vždy overte na stavebnom úrade vo vašej obci.</p>

<h2>Drobná stavba: limity pre plot</h2>
<p>Nový zákon zaraďuje oplotenie medzi <strong>drobné stavby</strong>, ak nepresiahne tieto výšky (merané od priľahlého terénu):</p>
<ul>
<li><strong>plný, nepriehľadný plot</strong> (napríklad betónový) — najviac <strong>1,6 m</strong>,</li>
<li><strong>ľahký, priehľadný plot</strong> (napríklad 3D panel alebo pletivo) — najviac <strong>2 m</strong>.</li>
</ul>
<p>Na drobnú stavbu netreba stavebné povolenie, stačí ju <strong>ohlásiť stavebnému úradu</strong>. Ak plot limity prekročí, nejde už o drobnú stavbu a potrebuje <strong>rozhodnutie o stavebnom zámere</strong> — teda náročnejší proces s projektovou dokumentáciou.</p>

<h2>Čo to znamená v praxi</h2>
<div class="tbl-wrap"><table class="cmp">
<thead><tr><th>Plot</th><th>Výška</th><th>Postup</th></tr></thead>
<tbody>
<tr><td>Betónový (3 dosky)</td><td>1,5 m</td><td>drobná stavba → ohlásenie</td></tr>
<tr><td>Betónový (4 dosky)</td><td>2,0 m</td><td>nad 1,6 m → rozhodnutie o stavebnom zámere</td></tr>
<tr><td>3D panel</td><td>1,23 – 1,73 m</td><td>drobná stavba → ohlásenie</td></tr>
<tr><td>3D panel 2,03 m s podhrabom</td><td>nad 2 m</td><td>nad limitom → rozhodnutie o stavebnom zámere</td></tr>
</tbody></table></div>
<p>Pozor na výšku pri svahu a na podmurovke: meria sa od priľahlého terénu, takže na nižšej strane pozemku môže byť plot „vyšší“, než sa zdá.</p>

<h2>Ako prebieha ohlásenie</h2>
<ol>
<li><strong>Formulár</strong> ohlásenia drobnej stavby podáte na stavebný úrad (podľa § 63 zákona).</li>
<li>Priložíte <strong>jednoduchý situačný nákres</strong> s umiestnením plota, <strong>popis</strong> (materiál, výška, dĺžka) a doklad o <strong>vlastníctve pozemku</strong>; v niektorých prípadoch aj vyjadrenia dotknutých orgánov.</li>
<li>Úrad má na overenie <strong>30 dní</strong>. Ak v tejto lehote nekoná, zákon predpokladá, že ohlásenie overil.</li>
</ol>
<p>Kolaudácia sa pri drobnej stavbe nerobí. Na nákres netreba architekta — stačí zrozumiteľná situácia pozemku s vyznačeným plotom.</p>

<h2>Hranica so susedom</h2>
<ul>
<li>Plot aj jeho základy musia stáť <strong>na vašom pozemku</strong>. Starý plot nemusí stáť presne na hranici.</li>
<li>Pri nejasnej hranici sa oplatí <strong>vytýčenie geodetom</strong> — je výrazne lacnejšie než neskôr prekladať hotový plot.</li>
<li>So susedom sa dohodnite vopred, ideálne <strong>písomne</strong>, najmä ak treba vstúpiť na jeho pozemok alebo odstrániť spoločný starý plot.</li>
<li>Pri stavbe blízko hranice susedného pozemku úrad ohlásenie posudzuje dôkladnejšie.</li>
</ul>
{fig('r060.webp', 'Betónový plot postavený na hranici pozemku pri susednom dome', 'Plot na hranici pozemku — pred stavbou sa oplatí hranicu vytýčiť.')}

<h2>Plot pri ceste</h2>
<ul>
<li>Plot nesmie zhoršiť <strong>výhľad</strong> pri výjazde z pozemku ani na križovatke.</li>
<li>Bránky a brány by sa nemali otvárať do chodníka alebo cesty.</li>
<li>Pri rušnejšej ceste môže byť potrebné vyjadrenie <strong>správcu cesty</strong>; ďalšie podmienky môže určiť územný plán obce alebo ochranné pásma sietí.</li>
</ul>

<h2>Čo hrozí, ak plot neohlásite</h2>
<p>Stavebný úrad môže uložiť <strong>pokutu</strong> a nariadiť <strong>odstránenie stavby</strong> na náklady stavebníka. Dodatočné riešenie je administratívne oveľa náročnejšie než ohlásenie vopred — preto sa ohlásenie oplatí podať ešte pred začatím prác.</p>

<h2>Ako vám pomôžeme</h2>
<p>Pri obhliadke vám poradíme s výškou a typom plota a povieme presné údaje (materiál, výška, dĺžka), ktoré do ohlásenia uvediete.</p>
{cta('Navrhnite si plot v plánovači — pri výške nad limit vás plánovač upozorní.', '/#planovac', 'Otvoriť plánovač plota')}
<p class="art-src">Zdroj: zákon č. 25/2025 Z. z. (stavebný zákon), účinný od 1. 4. 2025, najmä § 2 ods. 4 (drobné stavby) a § 63 (ohlásenie). Znenie zákona nájdete na <a href="https://www.slov-lex.sk/" target="_blank" rel="noopener">slov-lex.sk</a>.</p>
''',
  faq=[('Treba na plot stavebné povolenie?', 'Plný plot do 1,6 m a priehľadný plot do 2 m sú podľa nového stavebného zákona drobné stavby — stačí ich ohlásiť stavebnému úradu. Vyšší plot potrebuje rozhodnutie o stavebnom zámere.'),
       ('Ako dlho trvá ohlásenie plota?', 'Stavebný úrad má na overenie ohlásenia 30 dní. Ak v lehote nekoná, ohlásenie sa považuje za overené.'),
       ('Môžem postaviť betónový plot vysoký 2 metre?', 'Áno, ale plný plot vyšší ako 1,6 m už nie je drobná stavba, takže nestačí ohlásenie — potrebuje rozhodnutie o stavebnom zámere.'),
       ('Potrebujem na plot súhlas suseda?', 'Plot musí stáť na vašom pozemku. Formálny súhlas suseda sa vo všeobecnosti nevyžaduje, no dohoda vopred predíde sporom a pri stavbe pri hranici ju úrad posudzuje dôkladnejšie.')],
  related=['ploty-betonove', 'ploty-3d'],
),
dict(
  slug='ako-prebieha-stavba-plota',
  title='Ako prebieha stavba betónového plota: postup krok za krokom | LIBES',
  desc='Ako prebieha stavba betónového plota od obhliadky po upratanie: hranica pozemku, ohlásenie, výkopy, betonáž stĺpikov, montáž dosiek a čo si pripraviť ako majiteľ.',
  h1='Ako prebieha stavba plota', h1b='Krok za krokom.',
  lead='Čo sa deje od prvého telefonátu po hotový plot — a čo si môžete pripraviť vy, aby všetko išlo rýchlo a bez prekvapení.',
  minutes=5, image='ba-after.webp', published='2026-10-31', modified='2026-10-31',
  body=f'''
<h2>1. Hranica pozemku a ohlásenie</h2>
<p>Ešte pred stavbou si overte, kde presne vedie hranica pozemku, a plot ohláste stavebnému úradu. Plný plot do 1,6 m a priehľadný do 2 m stačí ohlásiť — podrobne v článku <a href="/poradna/plot-a-stavebne-povolenie/">Plot a nový stavebný zákon</a>.</p>

<h2>2. Obhliadka a zameranie</h2>
<p>Prídeme na pozemok, zameriame dĺžku a terén a dohodneme výšku, dekor alebo farbu, umiestnenie bránok a brán. Obhliadka je zdarma a nezáväzná.</p>

<h2>3. Cenová ponuka</h2>
<p>Pošleme kalkuláciu, ktorá obsahuje materiál, dopravu aj prácu. Po odsúhlasení dohodneme termín.</p>

<h2>4. Výkopy a príprava</h2>
<p>Pre každý stĺpik sa vykope jama pre betónovú pätku. Pri dlhom plote je to veľa zeminy — koľko, si môžete spočítať v <a href="/sluzby/pomocne-prace/#nastroj">kalkulačke výkopu</a>.</p>
{fig('ba-before.webp', 'Osadené betónové stĺpiky plota a rozkopaný pozemok počas stavby', 'Osadené stĺpiky — pred montážou dosiek musí betón zatvrdnúť.')}

<h2>5. Osadenie a zabetónovanie stĺpikov</h2>
<p>Stĺpiky sa osadia presne do roviny a do správnych rozostupov (bežne 2 m) a zabetónujú. Betón potrebuje čas na zatvrdnutie, preto sa dosky montujú až vtedy, keď sú stĺpiky pevné. Pri mrazoch betónovanie pozastavíme.</p>

<h2>6. Montáž dosiek</h2>
<p>Dosky (bežne 50 cm vysoké) sa zasúvajú do drážok stĺpikov — tri dosky dajú výšku 1,5 m, štyri 2 m. Pri svahu sa polia stupňujú, aby plot kopíroval terén.</p>
{fig('ba-after.webp', 'Hotový betónový plot s kamenným dekorom na tom istom dvore', 'Ten istý dvor po montáži dosiek.')}

<h2>7. Bránky, brány a upratanie</h2>
<p>Doplníme vstupy podľa dohody a po sebe upraceme — odvezieme zvyšky a zarovnáme terén okolo plota. Preberáte hotový plot, nie stavenisko.</p>

<h2>Čo si pripraviť ako majiteľ</h2>
<ul>
<li><strong>Vytýčenú hranicu</strong> pozemku, ak si nie ste istí, kde vedie.</li>
<li><strong>Ohlásenie</strong> stavebnému úradu.</li>
<li><strong>Prístup</strong> pre auto s materiálom čo najbližšie k plotu — ak to nejde, materiál prenesieme (<a href="/sluzby/prenos-materialu/">prenos materiálu</a>).</li>
<li>Dohodu so <strong>susedom</strong>, ak sa bude odstraňovať spoločný starý plot.</li>
</ul>
{cta('Chcete vedieť, koľko polí, stĺpikov a dosiek bude mať váš plot?', '/#planovac', 'Navrhnúť plot v plánovači')}
''',
  faq=[('Dá sa plot stavať aj v zime?', 'Betónovanie vyžaduje teploty nad bodom mrazu, preto pri silných mrazoch práce pozastavíme. Inak staviame celý rok.'),
       ('Kto podáva ohlásenie plota?', 'Ohlásenie podáva stavebník, teda vlastník pozemku. Údaje o plote (materiál, výška, dĺžka) vám po obhliadke radi poskytneme.'),
       ('Musím byť pri stavbe doma?', 'Pri obhliadke a odovzdaní áno. Počas samotnej stavby stačí, ak máme prístup na pozemok — dohodneme vopred.')],
  related=['ploty-betonove', 'pomocne-prace'],
),
]
