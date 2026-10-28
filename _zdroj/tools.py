"""Interaktívne nástroje pre podstránky LIBES.
Každý nástroj: HTML sekcia (ovládanie + výkres + výkaz) a JS.
Výsledok sa posiela do objednávky na hlavnej stránke cez ?sluzba=&popis=.
"""

TOOL_CSS = r'''
/* ===== nástroje na podstránkach ===== */
.tool-group[hidden]{display:none!important}
.steppers{display:grid;gap:8px}
.stp{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 12px;border:1px solid var(--line-d);border-radius:var(--r);background:rgba(234,229,216,.03)}
.stp span{font-size:.88rem;min-width:0}
.stp span small{display:block;font-family:var(--f-mono);font-size:.64rem;color:var(--stone-d);margin-top:1px}
.stp .ctl{display:flex;align-items:center;gap:6px;flex:none}
.stp button{width:32px;height:32px;border-radius:50%;border:1px solid var(--line-d);background:transparent;color:var(--bone);font:600 1rem var(--f-body);cursor:pointer;line-height:1}
.stp button:hover{border-color:var(--brass);color:var(--brass)}
.stp output{min-width:44px;text-align:center;font-family:var(--f-display);font-size:1.35rem;font-weight:600;font-variant-numeric:tabular-nums}
.tool-link{display:inline-flex;margin-top:22px;font-family:var(--f-mono);font-size:.78rem;letter-spacing:.04em;color:var(--brass-hi);text-decoration:none;border-bottom:1px solid rgba(198,155,91,.5);padding-bottom:3px}
.tool-link:hover{color:var(--bone);border-color:var(--bone)}
.level{display:inline-block;padding:3px 10px;border-radius:999px;font-family:var(--f-mono);font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;margin-top:6px}
'''

def rng(id, label, mn, mx, step, val, unit, marks):
    m = ''.join(f'<span>{x}</span>' for x in marks)
    return f'''<div><div class="ctrl-lab"><span id="{id}Lab">{label}</span><b id="{id}Out">{val}<small>{unit}</small></b></div>
<input class="rng" type="range" id="{id}" min="{mn}" max="{mx}" step="{step}" value="{val}" aria-label="{label}">
<div class="rng-scale">{m}</div></div>'''

def seg(id, label, opts, default):
    b = ''.join(f'<button type="button" data-v="{v}" aria-pressed="{str(v == default).lower()}">{t}</button>' for v, t in opts)
    return f'<div><div class="ctrl-lab" id="{id}Lab">{label}</div><div class="dseg" id="{id}">{b}</div></div>'

def stp(id, label, sub, val, step='1'):
    return f'<div class="stp"><span>{label}<small>{sub}</small></span><span class="ctl"><button type="button" data-t="{id}" data-d="-{step}" aria-label="Menej: {label}">−</button><output id="{id}">{val}</output><button type="button" data-t="{id}" data-d="{step}" aria-label="Viac: {label}">+</button></span></div>'

def section(eyebrow, h2, lead, controls, sheet_title, bom, note):
    boms = ''.join(f'<div><small id="{i}Lab">{l}</small><b id="{i}">–</b></div>' for l, i in bom)
    return f'''
<section class="band dark-2" id="nastroj">
  <div class="wrap">
    <div class="sec-head split"><div><span class="eyebrow"><i class="stripes"></i>{eyebrow}</span><h2 class="h-sec">{h2}</h2></div>
      <p class="lead">{lead}</p></div>
    <div class="plan-grid">
      <div class="plan-ctrl">{controls}</div>
      <div class="sheet">
        <div class="sheet-top"><span>LIBES s.r.o. · <b>{sheet_title}</b></span><span id="tTitle"></span><span>orientačne</span></div>
        <svg class="drawing" id="tSvg" viewBox="0 0 860 380" role="img" aria-label="{sheet_title}"></svg>
        <div class="bom">{boms}</div>
        <div class="sheet-foot"><p id="tNote">{note}</p>
          <a class="btn btn-ink btn-sm" href="../../index.html#objednavka" id="tSend">Poslať do objednávky <svg><use href="#i-arrow"/></svg></a></div>
      </div>
    </div>
  </div>
</section>'''

# spoločné JS pomôcky (vkladajú sa pred každý nástroj)
COMMON_JS = r'''
var $=function(i){return document.getElementById(i)};
function pl(n,a,b,c){n=Math.abs(n);return n===1?a:(n>=2&&n<=4?b:c)}
function vol(v){return v<1?dec(v,2):dec(v,1)}
function fmt(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,' ')}
function dec(n,d){return (Math.round(n*Math.pow(10,d))/Math.pow(10,d)).toFixed(d).replace('.',',')}
var MONO='font-family="JetBrains Mono,monospace"';
function T(x,y,t,o){o=o||{};return '<text x="'+x+'" y="'+y+'" '+MONO+' font-size="'+(o.s||14)+'" fill="'+(o.c||'#2A2620')+'"'+(o.a?' text-anchor="'+o.a+'"':'')+(o.w?' font-weight="'+o.w+'"':'')+(o.r?' transform="rotate('+o.r+' '+x+' '+y+')"':'')+'>'+t+'</text>'}
function DIM(x1,y1,x2,y2,label,o){o=o||{};var c=o.c||'#2A2620',s='',v=x1===x2;
  s+='<path d="M'+x1+' '+y1+' L'+x2+' '+y2+'" stroke="'+c+'" stroke-width="1.2"/>';
  [[x1,y1],[x2,y2]].forEach(function(p){s+='<path d="M'+(p[0]-5)+' '+(p[1]+5)+' l10 -10" stroke="'+c+'" stroke-width="1.4"/>'});
  if(v){s+=T(x1-10,(y1+y2)/2,label,{a:'middle',r:-90,c:c})}else{s+=T((x1+x2)/2,y1-7,label,{a:'middle',c:c})}
  return s}
function PERSON(x,ground,s,label){ /* silueta 180 cm, s = px na cm */
  var p='M-21 26 L21 26 L25 95 L18 96 L15 52 L13 100 L13 178 L3 178 L0 108 L-3 178 L-13 178 L-13 100 L-15 52 L-18 96 L-25 95 Z';
  var g='<g transform="translate('+x+' '+(ground-180*s)+') scale('+s+')"><circle cx="0" cy="11" r="10.5" fill="#2A2620" fill-opacity=".55"/><path d="'+p+'" fill="#2A2620" fill-opacity=".55"/></g>';
  if(label!==false){g+='<path d="M'+(x+26*s+8)+' '+(ground-180*s)+' V'+ground+'" stroke="#7A5626" stroke-width="1" stroke-dasharray="3 3"/>'+T(x+26*s+14,ground-90*s,'180 cm',{c:'#7A5626',s:12})}
  return g}
function fillRng(el){el.style.setProperty('--fill',((el.value-el.min)/(el.max-el.min)*100)+'%')}
function bindSeg(id,cb){var g=$(id);g.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;g.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});cb(b.dataset.v)})}
function setSeg(id,v){$(id).querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.v===String(v)))})}
function bindRng(id,cb,unit,d){var el=$(id);function u(){fillRng(el);$(id+'Out').innerHTML=(d?dec(+el.value,d):el.value)+'<small>'+unit+'</small>';cb(+el.value)}el.addEventListener('input',u);u()}
function send(svc,txt){location.href='../../index.html?sluzba='+encodeURIComponent(svc)+'&popis='+encodeURIComponent(txt)+'#objednavka'}
var rsz;window.addEventListener('resize',function(){clearTimeout(rsz);rsz=setTimeout(function(){window.__draw&&window.__draw()},150)});
'''

TOOLS = {}

# ---------------------------------------------------------------- MURÁRSKE
TOOLS['murarske-prace'] = (section(
    'Kalkulačka steny', 'Koľko tvárnic<br>na vašu stenu?',
    'Zadajte rozmery steny a otvory. Stena sa vyskladá na výkrese a výkaz ukáže orientačný počet tvárnic s 5 % rezervou.',
    seg('wT', 'Typ muriva', [('por', 'Pórobetón'), ('teh', 'Tehla'), ('dt', 'Debniaca')], 'por') +
    rng('wL', 'Dĺžka steny', 1, 30, 0.5, 6, 'm', ['1 m', '10', '20', '30 m']) +
    rng('wH', 'Výška steny', 1, 3.5, 0.05, 2.6, 'm', ['1 m', '2', '3', '3,5 m']) +
    rng('wW', 'Počet okien', 0, 6, 1, 1, 'ks', ['0', '2', '4', '6']) +
    seg('wD', 'Dvere', [('0', 'žiadne'), ('1', '1'), ('2', '2'), ('3', '3')], '1'),
    'Pohľad na stenu',
    [('Čistá plocha', 'bArea'), ('Tvárnic', 'bBlocks'), ('Lepidlo', 'bMat'), ('Otvory', 'bOpen')],
    'Okno počítame 1,2 × 1,5 m, dvere 0,9 × 2,0 m. Presný počet podľa konkrétneho systému a projektu upresníme pri obhliadke.'),
r'''
var TY={por:{n:'pórobetón 50×25 cm',bw:.5,bh:.25,k:8,fill:'#E9E4D8',st:'#A39A8A',mat:['Lepidlo 25 kg','vrec',function(a){return Math.ceil(a*8.5/25)}]},
        teh:{n:'brúsená tehla 25×25 cm',bw:.25,bh:.25,k:16,fill:'#C98E6B',st:'#8A5B3F',mat:['Lepiaca pena','dóz',function(a){return Math.ceil(a/8)}]},
        dt:{n:'debniaca tvárnica 50×25 cm',bw:.5,bh:.25,k:8,fill:'#C2BDB2',st:'#7E786D',mat:['Betón na výplň','m³',function(a){return dec(a*.15,1)}]}};
var S={t:'por',L:6,H:2.6,w:1,d:1};
function layout(){var items=[],w=S.w,d=S.d;
  function need(){return w*1.2+d*.9+(w+d+1)*.4}
  while(w+d>0&&need()>S.L){if(w>0)w--;else d--}
  for(var i=0;i<d;i++)items.push('d');for(var j=0;j<w;j++)items.push('w');
  return {w:w,d:d,items:items}}
function draw(){var t=TY[S.t],lay=layout(),svg=$('tSvg');
  var x0=110,ground=318,maxW=window.innerWidth<640?620:690;
  var s=Math.min(maxW/S.L,230/S.H),W=S.L*s,H=S.H*s,top=ground-H,o='';
  o+='<defs><clipPath id="wc"><rect x="'+x0+'" y="'+top+'" width="'+W+'" height="'+H+'"/></clipPath></defs>';
  o+='<path d="M60 '+ground+' H820" stroke="#2A2620" stroke-width="2"/>';
  for(var gx=64;gx<820;gx+=14)o+='<path d="M'+gx+' '+(ground+1)+' l-10 10" stroke="#2A2620" stroke-opacity=".3"/>';
  o+='<g clip-path="url(#wc)">';
  var rows=Math.ceil(S.H/t.bh);
  for(var r=0;r<rows;r++){var y=ground-(r+1)*t.bh*s,off=(r%2)*t.bw/2*s;
    for(var x=x0-off;x<x0+W;x+=t.bw*s)o+='<rect x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+(t.bw*s).toFixed(1)+'" height="'+(t.bh*s).toFixed(1)+'" fill="'+t.fill+'" stroke="'+t.st+'" stroke-width=".8"/>'}
  o+='</g><rect x="'+x0+'" y="'+top+'" width="'+W+'" height="'+H+'" fill="none" stroke="#2A2620" stroke-width="1.6"/>';
  var n=lay.items.length;
  lay.items.forEach(function(k,i){var cx=x0+W*(i+1)/(n+1);
    if(k==='d'){var dw=.9*s,dh=Math.min(2,S.H-.1)*s;o+='<rect x="'+(cx-dw/2)+'" y="'+(ground-dh)+'" width="'+dw+'" height="'+dh+'" fill="#F4F1E9" stroke="#2A2620" stroke-width="1.4"/><circle cx="'+(cx+dw/2-6)+'" cy="'+(ground-dh/2)+'" r="2.5" fill="#2A2620"/>'}
    else{var ww=1.2*s,wh=Math.min(1.5,S.H-1.0)*s,wy=ground-Math.min(.9,S.H-1.5>0?.9:S.H*.3)*s-wh;
      if(wh>4)o+='<rect x="'+(cx-ww/2)+'" y="'+wy+'" width="'+ww+'" height="'+wh+'" fill="#DCE6EA" stroke="#2A2620" stroke-width="1.4"/><path d="M'+cx+' '+wy+' V'+(wy+wh)+' M'+(cx-ww/2)+' '+(wy+wh/2)+' H'+(cx+ww/2)+'" stroke="#2A2620" stroke-width="1"/>'}});
  o+=DIM(x0,ground+40,x0+W,ground+40,fmt(Math.round(S.L*1000)));
  o+=DIM(x0-40,top,x0-40,ground,fmt(Math.round(S.H*1000)));
  if(x0+W+110<850)o+=PERSON(x0+W+60,ground,s/100);
  svg.innerHTML=o;
  var area=S.L*S.H,open=lay.w*1.2*1.5+lay.d*.9*2,net=Math.max(0,area-open),ks=Math.ceil(net*t.k*1.05);
  $('tTitle').textContent=t.n;
  $('bArea').textContent=dec(net,1)+' m²';$('bBlocks').textContent=fmt(ks)+' ks';
  $('bMatLab').textContent=t.mat[0];var mv=t.mat[2](net);$('bMat').textContent=mv+' '+(t.mat[1]==='m³'?'m³':t.mat[1]==='vrec'?pl(+mv,'vrece','vrecia','vriec'):pl(+mv,'dóza','dózy','dóz'));
  $('tNote').textContent=(lay.w<S.w||lay.d<S.d)?('Na stenu dĺžky '+dec(S.L,1)+' m sa zmestí najviac '+lay.w+' '+pl(lay.w,'okno','okná','okien')+' a '+lay.d+' dvere — výpočet počíta s nimi. Zväčšite dĺžku steny alebo uberte otvory.'):'Okno počítame 1,2 × 1,5 m, dvere 0,9 × 2,0 m. Presný počet podľa konkrétneho systému a projektu upresníme pri obhliadke.';
  $('bOpen').textContent=lay.w+' + '+lay.d;
  $('bOpenLab').textContent='Okná + dvere';
  window.__res={t:t,lay:lay,net:net,ks:ks};
}
window.__draw=draw;
bindSeg('wT',function(v){S.t=v;draw()});
bindSeg('wD',function(v){S.d=+v;draw()});
bindRng('wL',function(v){S.L=v;draw()},'m',1);
bindRng('wH',function(v){S.H=v;draw()},'m',2);
bindRng('wW',function(v){S.w=v;draw()},'ks');
$('tSend').addEventListener('click',function(e){e.preventDefault();var r=window.__res;
  send('Murárske práce','Kalkulačka steny: '+r.t.n+', stena '+dec(S.L,1)+' × '+dec(S.H,2)+' m, '+r.lay.w+pl(r.lay.w,' okno',' okná',' okien')+', '+r.lay.d+' dvere, čistá plocha '+dec(r.net,1)+' m², cca '+r.ks+' ks tvárnic.')});
draw();
''')

# ---------------------------------------------------------------- POMOCNÉ (výkop)
TOOLS['pomocne-prace'] = (section(
    'Kalkulačka výkopu', 'Koľko zeminy<br>vykopeme?',
    'Vyberte typ výkopu a rozmery. Rez ukáže hĺbku v porovnaní s postavou a výkaz spočíta objem, hmotnosť aj počet kontajnerov.',
    seg('kT', 'Typ výkopu', [('pas', 'Základový pás'), ('pat', 'Pätky'), ('ryha', 'Ryha')], 'pas') +
    '<div class="tool-group" id="gLin">' +
    rng('kL', 'Dĺžka', 1, 100, 1, 24, 'm', ['1 m', '30', '60', '100 m']) +
    '<div style="height:22px"></div>' +
    rng('kW', 'Šírka', 0.2, 1.2, 0.05, 0.5, 'm', ['0,2', '0,5', '0,8', '1,2 m']) +
    '</div><div class="tool-group" id="gPat" hidden>' +
    rng('kN', 'Počet pätiek', 1, 60, 1, 12, 'ks', ['1', '20', '40', '60']) +
    '<div style="height:22px"></div>' +
    rng('kA', 'Rozmer pätky', 0.25, 0.8, 0.05, 0.4, 'm', ['0,25', '0,4', '0,6', '0,8 m']) +
    '</div>' +
    rng('kD', 'Hĺbka', 0.3, 2.0, 0.05, 0.8, 'm', ['0,3', '0,8', '1,4', '2 m']),
    'Rez výkopom',
    [('Objem výkopu', 'bV'), ('Po vykopaní', 'bLoose'), ('Hmotnosť', 'bMass'), ('Kontajnery 5 m³', 'bCont')],
    'Rastlá zemina cca 1,8 t/m³, po vykopaní nakyprí asi o 25 %. Skutočné hodnoty závisia od druhu pôdy.'),
r'''
var S={t:'pas',L:24,W:.5,N:12,A:.4,D:.8};
var NAMES={pas:'základový pás',pat:'pätky',ryha:'ryha'};
function draw(){var svg=$('tSvg'),o='';
  var w=S.t==='pat'?S.A:S.W, s=Math.min(300/(1.8+S.D),150), ground=40+1.8*s, cx=260;
  o+='<defs><pattern id="soil" patternUnits="userSpaceOnUse" width="12" height="12"><rect width="12" height="12" fill="#D9CBB2"/><path d="M0 12 L12 0" stroke="#A58E68" stroke-width="1"/></pattern></defs>';
  o+='<rect x="40" y="'+ground+'" width="780" height="'+(380-ground)+'" fill="url(#soil)"/>';
  o+='<rect x="'+(cx-w*s/2)+'" y="'+ground+'" width="'+(w*s)+'" height="'+(S.D*s)+'" fill="#F4F1E9" stroke="#2A2620" stroke-width="1.6"/>';
  o+='<path d="M40 '+ground+' H820" stroke="#2A2620" stroke-width="2"/>';
  var area=w*S.D*1.25,b=Math.sqrt(6*area)*s,h=b/3,mx=cx+w*s/2+30;
  o+='<path d="M'+mx+' '+ground+' L'+(mx+b/2)+' '+(ground-h)+' L'+(mx+b)+' '+ground+' Z" fill="url(#soil)" stroke="#2A2620" stroke-width="1.2"/>';
  o+=T(mx+b/2,ground-h-10,'vykopaná zemina',{a:'middle',s:12,c:'#6B5A3C'});
  o+=DIM(cx-w*s/2,ground-16,cx+w*s/2,ground-16,fmt(Math.round(w*1000)));
  o+=DIM(cx-w*s/2-26,ground,cx-w*s/2-26,ground+S.D*s,fmt(Math.round(S.D*1000)));
  o+=PERSON(Math.min(mx+b+90,720),ground,s/100);
  var V=S.t==='pat'?S.N*S.A*S.A*S.D:S.L*S.W*S.D, loose=V*1.25, mass=V*1.8, cont=Math.ceil(loose/5);
  o+=T(60,30,S.t==='pat'?('rez jednou pätkou · × '+S.N+' ks'):('rez · dĺžka '+S.L+' m'),{s:13,c:'#6B6457'});
  svg.innerHTML=o;
  $('tTitle').textContent=NAMES[S.t]+' · hĺbka '+dec(S.D,2)+' m';
  $('bV').textContent=dec(V,2)+' m³';$('bLoose').textContent=vol(loose)+' m³';$('bMass').textContent=vol(mass)+' t';$('bCont').textContent=cont;
  window.__res={V:V,loose:loose,mass:mass,cont:cont,w:w};
}
window.__draw=draw;
bindSeg('kT',function(v){S.t=v;$('gLin').hidden=v==='pat';$('gPat').hidden=v!=='pat';
  if(v==='pat'){$('kD').value=1;$('kD').dispatchEvent(new Event('input'))}else if(v==='ryha'){$('kW').value=.4;$('kW').dispatchEvent(new Event('input'));$('kD').value=1;$('kD').dispatchEvent(new Event('input'))}
  draw()});
bindRng('kL',function(v){S.L=v;draw()},'m');
bindRng('kW',function(v){S.W=v;draw()},'m',2);
bindRng('kN',function(v){S.N=v;draw()},'ks');
bindRng('kA',function(v){S.A=v;draw()},'m',2);
bindRng('kD',function(v){S.D=v;draw()},'m',2);
$('tSend').addEventListener('click',function(e){e.preventDefault();var r=window.__res;
  var dim=S.t==='pat'?(S.N+' pätiek '+dec(S.A,2)+' × '+dec(S.A,2)+' m'):('dĺžka '+S.L+' m, šírka '+dec(S.W,2)+' m');
  send('Pomocné práce','Kalkulačka výkopu: '+NAMES[S.t]+', '+dim+', hĺbka '+dec(S.D,2)+' m, objem cca '+dec(r.V,2)+' m³ ('+dec(r.mass,1)+' t zeminy).')});
draw();
''')

# ---------------------------------------------------------------- PRENOS (váha)
TOOLS['prenos-materialu'] = (section(
    'Koľko to váži?', 'Spočítajte si<br>svoj materiál.',
    'Pridajte materiál a zadajte, kam ho treba dostať. Výkaz spočíta hmotnosť, počet nosení a ukáže, aký náročný bude prenos.',
    '<div><div class="ctrl-lab">Materiál</div><div class="steppers">' +
    stp('mPal', 'Paleta tvárnic', 'cca 1 000 kg', 0) +
    stp('mDos', 'Plotová doska 200 × 50', 'cca 50 kg', 40) +
    stp('mStl', 'Betónový stĺpik', 'cca 60 kg', 21) +
    stp('mVre', 'Vrece cementu / lepidla', '25 kg', 10) +
    stp('mPie', 'Piesok / štrk', 'm³ · cca 1 600 kg', 0, '0.5') +
    '</div></div>' +
    rng('mDist', 'Vzdialenosť od auta', 0, 100, 5, 15, 'm', ['0', '30', '60', '100 m']) +
    seg('mFl', 'Kam', [('0', 'Prízemie'), ('1', '1. posch.'), ('2', '2. posch.'), ('3', '3. posch.')], '0') +
    seg('mTer', 'Cesta', [('1', 'Rovina'), ('1.4', 'Svah / schody'), ('1.7', 'Úzky prechod')], '1'),
    'Prenos materiálu',
    [('Hmotnosť', 'bKg'), ('Nosení do 25 kg', 'bCarry'), ('Vzdialenosť', 'bDist'), ('Náročnosť', 'bLvl')],
    'Hmotnosti sú orientačné, líšia sa podľa výrobcu. Postup pri ťažkých kusoch dohodneme vopred.'),
r'''
var W={mPal:1000,mDos:50,mStl:60,mVre:25,mPie:1600};
var S={dist:15,fl:0,ter:1};
var LV=[[1.5,'Ľahká','#5E8C61'],[4,'Stredná','#B88A2E'],[8,'Náročná','#B5652E'],[1e9,'Veľmi náročná','#A23C28']];
function val(id){return parseFloat($(id).textContent.replace(',','.'))}
function draw(){var svg=$('tSvg'),o='',kg=0;Object.keys(W).forEach(function(k){kg+=val(k)*W[k]});
  var score=kg/1000*(1+S.dist/30)*(1+S.fl*.6)*S.ter, lv=LV.filter(function(l){return score<l[0]})[0];
  var ground=300;
  o+='<path d="M30 '+ground+' H830" stroke="#2A2620" stroke-width="2"/>';
  // auto
  o+='<g transform="translate(40 '+(ground-70)+')"><rect x="0" y="10" width="92" height="46" rx="4" fill="#E3DED2" stroke="#2A2620" stroke-width="1.4"/><path d="M92 22 H118 L134 40 V56 H92 Z" fill="#E3DED2" stroke="#2A2620" stroke-width="1.4"/><path d="M100 26 H116 L126 38 H100 Z" fill="#DCE6EA" stroke="#2A2620"/><circle cx="26" cy="60" r="10" fill="#2A2620"/><circle cx="110" cy="60" r="10" fill="#2A2620"/>'+
     '<rect x="10" y="0" width="30" height="12" fill="#C69B5B" stroke="#2A2620"/><rect x="44" y="0" width="30" height="12" fill="#C69B5B" stroke="#2A2620"/></g>';
  // dom
  var hx=600,fh=48,floors=4;
  for(var f=0;f<floors;f++){var y=ground-(f+1)*fh,on=f===S.fl;
    o+='<rect x="'+hx+'" y="'+y+'" width="180" height="'+fh+'" fill="'+(on?'#E9C48C':'#EDE8DD')+'" stroke="#2A2620" stroke-width="1.4"/>';
    o+='<rect x="'+(hx+20)+'" y="'+(y+12)+'" width="26" height="22" fill="#DCE6EA" stroke="#2A2620"/><rect x="'+(hx+134)+'" y="'+(y+12)+'" width="26" height="22" fill="#DCE6EA" stroke="#2A2620"/>';
    o+=T(hx+90,y+30,f===0?'prízemie':f+'. posch.',{a:'middle',s:12,c:on?'#1B1408':'#6B6457',w:on?600:400})}
  o+='<path d="M'+(hx-12)+' '+(ground-floors*fh)+' L'+(hx+90)+' '+(ground-floors*fh-46)+' L'+(hx+192)+' '+(ground-floors*fh)+' Z" fill="#B5652E" stroke="#2A2620" stroke-width="1.4"/>';
  // cesta
  var px0=190,px1=hx-14,py=ground-6;
  if(S.ter>1.5){o+='<rect x="'+((px0+px1)/2-50)+'" y="'+(ground-90)+'" width="34" height="90" fill="#CFC9BC" stroke="#2A2620"/><rect x="'+((px0+px1)/2+16)+'" y="'+(ground-90)+'" width="34" height="90" fill="#CFC9BC" stroke="#2A2620"/>'+T((px0+px1)/2,ground-100,'úzky prechod',{a:'middle',s:12,c:'#6B6457'})}
  if(S.ter>1.2&&S.ter<1.5){var sx=(px0+px1)/2-60,st='';for(var i=0;i<6;i++){st+=(i?' L':'M')+(sx+i*20)+' '+(ground-i*10)+' L'+(sx+i*20+20)+' '+(ground-i*10)}o+='<path d="'+st+' L'+(sx+120)+' '+ground+'" fill="#CFC9BC" stroke="#2A2620"/>'+T(sx+60,ground-72,'svah / schody',{a:'middle',s:12,c:'#6B6457'})}
  o+='<path d="M'+px0+' '+py+' H'+px1+'" stroke="#7A5626" stroke-width="2" stroke-dasharray="7 6"/><path d="M'+(px1-10)+' '+(py-6)+' L'+px1+' '+py+' L'+(px1-10)+' '+(py+6)+'" stroke="#7A5626" stroke-width="2" fill="none"/>';
  o+=T((px0+px1)/2,py-12,S.dist+' m',{a:'middle',c:'#7A5626',w:600,s:15});
  if(S.fl>0)o+='<path d="M'+(hx-6)+' '+(ground-4)+' V'+(ground-S.fl*fh-fh/2)+'" stroke="#7A5626" stroke-width="2" stroke-dasharray="5 5"/>';
  // ukazovateľ náročnosti
  var gx=40,gy=340,gw=300;
  LV.forEach(function(l,i){o+='<rect x="'+(gx+i*gw/4)+'" y="'+gy+'" width="'+(gw/4-4)+'" height="10" rx="2" fill="'+l[2]+'" fill-opacity="'+(l===lv?1:.25)+'"/>'});
  o+=T(gx,gy-8,'náročnosť prenosu',{s:12,c:'#6B6457'});
  o+=T(40,52,fmt(Math.round(kg))+' kg',{s:26,w:600});o+=T(40,74,'celková hmotnosť',{s:12,c:'#6B6457'});o+=T(gx+gw+14,gy+10,lv[1],{s:13,w:600,c:lv[2]});
  svg.innerHTML=o;
  $('tTitle').textContent=(S.fl?S.fl+'. poschodie':'prízemie')+' · '+S.dist+' m';
  $('bKg').textContent=kg>=1000?dec(kg/1000,2)+' t':fmt(Math.round(kg))+' kg';
  $('bCarry').textContent=fmt(Math.ceil(kg/25));
  $('bDist').textContent=S.dist+' m';
  $('bLvl').innerHTML='<span style="color:'+lv[2]+'">'+lv[1]+'</span>';
  window.__res={kg:kg,lv:lv[1]};
}
window.__draw=draw;
document.querySelectorAll('.stp button').forEach(function(b){b.addEventListener('click',function(){
  var o=$(b.dataset.t),v=Math.max(0,Math.round((val(b.dataset.t)+parseFloat(b.dataset.d))*10)/10);o.textContent=String(v).replace('.',',');draw()})});
bindRng('mDist',function(v){S.dist=v;draw()},'m');
bindSeg('mFl',function(v){S.fl=+v;draw()});
bindSeg('mTer',function(v){S.ter=+v;draw()});
$('tSend').addEventListener('click',function(e){e.preventDefault();var r=window.__res,parts=[];
  [['mPal','paleta tvárnic'],['mDos','plotové dosky'],['mStl','stĺpiky'],['mVre','vrecia 25 kg'],['mPie','m³ piesku/štrku']].forEach(function(x){var v=val(x[0]);if(v>0)parts.push(String(v).replace('.',',')+'× '+x[1])});
  send('Prenos materiálu','Prenos materiálu: '+(parts.join(', ')||'materiál upresním')+'; cca '+fmt(Math.round(r.kg))+' kg, vzdialenosť '+S.dist+' m, '+(S.fl?S.fl+'. poschodie':'prízemie')+', náročnosť: '+r.lv+'.')});
draw();
''')

# ---------------------------------------------------------------- UPRATOVACIE (kontajner)
TOOLS['upratovacie-prace'] = (section(
    'Kontajnerový merač', 'Aký veľký kontajner<br>budete potrebovať?',
    'Vyberte typ práce a plochu. Odhadneme objem sutiny, hmotnosť a odporučíme veľkosť kontajnera.',
    seg('cT', 'Typ práce', [('kup', 'Kúpeľňa'), ('pri', 'Priečka'), ('pod', 'Podlahy'), ('stav', 'Po stavbe'), ('poz', 'Pozemok')], 'kup') +
    rng('cA', 'Podlahová plocha', 1, 300, 1, 6, 'm²', ['1', '100', '200', '300 m²']),
    'Odhad sutiny',
    [('Objem sutiny', 'bVol'), ('Hmotnosť', 'bT'), ('Kontajner', 'bBox'), ('Naplnenie', 'bFill')],
    'Odhad podľa bežných hodnôt pre daný typ práce. Skutočný objem závisí od materiálov — upresníme pri obhliadke.'),
r'''
var C={kup:{n:'rekonštrukcia kúpeľne',k:.45,lab:'Podlahová plocha',def:6},pri:{n:'búranie priečky',k:.15,lab:'Plocha steny',def:12},
       pod:{n:'výmena podláh',k:.08,lab:'Plocha podláh',def:40},stav:{n:'zvyšky po stavbe',k:.03,lab:'Podlahová plocha domu',def:120},
       poz:{n:'vypratanie pozemku',k:.05,lab:'Plocha pozemku',def:200}};
var SIZES=[3,5,7,10];
var S={t:'kup',a:6};
function box(x,yb,w,h,fillPct,label,on){var o='',sk=w*.16;
  var path='M'+x+' '+(yb-h)+' L'+(x+w)+' '+(yb-h)+' L'+(x+w-sk)+' '+yb+' L'+(x+sk)+' '+yb+' Z';
  o+='<defs><clipPath id="cb'+label+'"><path d="'+path+'"/></clipPath></defs>';
  o+='<path d="'+path+'" fill="'+(on?'#F4F1E9':'#ECE7DC')+'"/>';
  if(fillPct>0){var fh=h*Math.min(fillPct,1),fy=yb-fh,bump='';for(var i=0;i<=8;i++){bump+=' L'+(x+i*w/8)+' '+(fy+(i%2?-4:3))}
    o+='<path clip-path="url(#cb'+label+')" d="M'+x+' '+yb+bump+' L'+(x+w)+' '+yb+' Z" fill="#9C8B70"/>';
    for(var j=0;j<14;j++){var rx=x+sk+((j*53)%Math.max(1,(w-2*sk-14))),ry=yb-6-((j*37)%Math.max(1,fh-10));o+='<rect clip-path="url(#cb'+label+')" x="'+rx+'" y="'+ry+'" width="'+(8+j%3*4)+'" height="'+(5+j%2*3)+'" fill="#B8A88C" stroke="#7E6E55" stroke-width=".6"/>'}}
  o+='<path d="'+path+'" fill="none" stroke="'+(on?'#2A2620':'#9C9384')+'" stroke-width="'+(on?2:1.2)+'"/>';
  return o}
function draw(){var c=C[S.t],svg=$('tSvg'),o='';
  var V=S.a*c.k, t=V*1.3, n=1, size=SIZES.filter(function(z){return z>=V})[0];
  if(!size){size=7;n=Math.ceil(V/7)}
  var fill=V/(size*n);
  var ground=300;
  o+='<path d="M30 '+ground+' H830" stroke="#2A2620" stroke-width="2"/>';
  var DIMS={3:[2.8,1.0],5:[3.2,1.2],7:[3.6,1.4],10:[4.0,1.6]},PX=120,bw=DIMS[size][0]*PX,bh=DIMS[size][1]*PX,bx=50;
  o+=box(bx,ground-14,bw,bh,fill,'main',true);
  o+='<circle cx="'+(bx+bw*.25)+'" cy="'+(ground-7)+'" r="7" fill="#2A2620"/><circle cx="'+(bx+bw*.75)+'" cy="'+(ground-7)+'" r="7" fill="#2A2620"/>';
  o+=T(bx+bw/2,ground-14-bh-16,(n>1?n+' × ':'')+size+' m³',{a:'middle',s:22,w:600});
  o+=DIM(bx+bw+22,ground-14-bh,bx+bw+22,ground-14,Math.round(Math.min(fill,1)*100)+' %',{c:'#7A5626'});
  o+=PERSON(bx+bw+70,ground,PX/100);
  // rad veľkostí
  var rx=660;o+=T(rx,40,'veľkosti kontajnerov',{s:12,c:'#6B6457'});
  SIZES.forEach(function(z,i){var w=DIMS[z][0]*24,h=DIMS[z][1]*24,x=rx+(i%2)*98,yb=96+Math.floor(i/2)*78;
    o+=box(x,yb,w,h,0,'s'+z,z===size);o+=T(x+w/2,yb+18,z+' m³',{a:'middle',s:12,c:z===size?'#1B1408':'#9C9384',w:z===size?600:400})});
  svg.innerHTML=o;
  $('tTitle').textContent=c.n+' · '+S.a+' m²';
  $('bVol').textContent=vol(V)+' m³';$('bT').textContent=vol(t)+' t';
  $('bBox').textContent=(n>1?n+' × ':'')+size+' m³';$('bFill').textContent=Math.round(Math.min(fill,1)*100)+' %';
  window.__res={c:c,V:V,t:t,size:size,n:n};
}
window.__draw=draw;
bindSeg('cT',function(v){S.t=v;$('cALab')&&($('cALab').textContent=C[v].lab);var el=$('cA');el.value=C[v].def;el.dispatchEvent(new Event('input'))});
bindRng('cA',function(v){S.a=v;draw()},'m²');
$('tSend').addEventListener('click',function(e){e.preventDefault();var r=window.__res;
  send('Upratovacie práce','Kontajnerový merač: '+r.c.n+', '+S.a+' m², odhad sutiny cca '+dec(r.V,1)+' m³ ('+dec(r.t,1)+' t), kontajner '+(r.n>1?r.n+' × ':'')+r.size+' m³.')});
draw();
''')
