# second round of v2 changes, applied on top of build_v2.py
ARR = '<svg class="arr" viewBox="0 0 16 16" fill="none" overflow="visible"><path d="M1.3 14.7L14.2 1.8M6.6 1.8H14.2V9.4" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# own manifest so the home-screen icon opens v2
rep('href="manifest.webmanifest?v=3"', 'href="v2/manifest.webmanifest"')

# route cards: move them from above the sheet to under the summary
i = s.index('<div id="fastWrap">'); j = s.index('</div></div>', i) + len('</div></div>')
s = s[:i] + s[j:]
cards = '''<div id="fastWrap"><div id="fast" class="hscroll">
        <button class="fa" data-toast="Домой: 2 ч 45 мин, пробки 9 баллов"><span class="fi"><span class="ic" data-ic="home"></span></span><span class="ft"><b>2 ч 45 мин</b>Домой</span></button>
        <button class="fa" data-toast="На работу: 45 мин"><span class="fi"><span class="ic" data-ic="brief"></span></span><span class="ft"><b>45 мин</b>На работу</span></button>
        <button class="fa" data-toast="Красный проспект, 8: маршрут строится"><span class="fi"><span class="ic" data-ic="clock"></span></span><span class="ft"><b>Красный пр., 8</b>Недавнее</span></button>
      </div></div>
      '''
i = s.index('<div id="xChipsWrap">'); s = s[:i] + cards + s[i:]

# title arrows
rep('<button class="s1" data-go="main" id="sumPicks">5+ подборок мест,</button>', '<button class="s1" data-go="main" id="sumPicks">5+ подборок мест' + ARR + ',</button>')
rep('<button class="s2" data-go="news" id="sumNews">2 новости района</button>', '<button class="s2" data-go="news" id="sumNews">2 новости района' + ARR + '</button>')
rep("$('#sumNews').textContent = n ? `${n} ${n===1?'новость':'новости'} района` : 'новостей нет';",
    "$('#sumNews').innerHTML = (n ? `${n} ${n===1?'новость':'новости'} района` : 'новостей нет') + ARR;")
rep("$('#sumPicks').textContent = n ? '5+ подборок мест,' : '5+ подборок мест';",
    "$('#sumPicks').innerHTML = '5+ подборок мест' + ARR + (n ? ',' : '');")
rep("const MW=412, MH=652;", "const ARR = '" + ARR + "';\nconst MW=412, MH=652;")

# chips above the sheet: Кофейни · Мои места · АЗС, one at a time
i = s.index('<button class="chip" data-layer="friends"'); j = s.index('</button>', i) + 9; s = s[:i] + s[j:]
i = s.index('<button class="chip" data-layer="places"'); j = s.index('</button>', i) + 9
ci0 = s.index('<svg class="chk"'); chk = s[ci0:s.index('</svg>', ci0)+6]
s = s[:j] + '<button class="chip" data-layer="fuel" aria-pressed="false"><span class="ci"><span class="fuel">⛽</span>' + chk + '</span>АЗС</button>' + s[j:]
rep('<button class="chip" data-layer="coffee" aria-pressed="true">', '<button class="chip" data-layer="coffee" aria-pressed="false">')
rep('<button class="chip" data-layer="places" aria-pressed="true">', '<button class="chip" data-layer="places" aria-pressed="false">')
rep("const layers = {friends:true, coffee:true, places:true};", "const layers = {friends:true, coffee:true, places:true, fuel:false};\nlet only = null;   // v2: one category at a time")
rep("  for (const m of markers){ if (!m.layer) continue; m.el.classList.toggle('off', (m.layer!=='picks' && !layers[m.layer]) || !!m.hidden); }\n  $$('.chip').forEach(c => c.setAttribute('aria-pressed', String(layers[c.dataset.layer])));",
    "  for (const m of markers){ if (!m.layer) continue; const vis = m.layer==='friends' ? layers.friends : only ? m.layer===only : m.layer!=='fuel'; m.el.classList.toggle('off', !vis || !!m.hidden); }\n  $$('.chip').forEach(c => c.setAttribute('aria-pressed', String(c.dataset.layer===only))); $('#filters').classList.toggle('picked', !!only);")
rep("const LNAME = {friends:'Друзья', coffee:'Кофейни', places:'Мои места'};", "const LNAME = {friends:'Друзья', coffee:'Кофейни', places:'Мои места', fuel:'АЗС'};")
rep("function toggleLayer(l){ layers[l] = !layers[l]; applyLayers(); toast(`${LNAME[l]}: ${layers[l]?'показаны на карте':'скрыты'}`); }",
    "function toggleLayer(l){ only = only===l ? null : l; applyLayers(); toast(only ? `Показываем: ${LNAME[l]}` : 'Показываем всё рядом'); }")
rep("if (layers[c.dataset.layer]) c.classList.add('pop')", "if (only===c.dataset.layer) c.classList.add('pop')")

# gas stations (emoji drawn into the pin)
rep("  {id:'bereza', layer:'picks', type:'gp'},", "  {id:'fuel1', layer:'fuel', type:'gp', x:330, y:420},\n  {id:'fuel2', layer:'fuel', type:'gp', x:70, y:470},\n  {id:'fuel3', layer:'fuel', type:'gp', x:250, y:150},\n  {id:'bereza', layer:'picks', type:'gp'},")
rep("const GALLERY = {", """const FUEL_ICON = (() => { try { const c = document.createElement('canvas'); c.width = c.height = 96; const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0,0,96,96); x.font = '60px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('⛽', 48, 54); return c.toDataURL(); } catch(e){ return 'img/em_cup.png'; } })();
for (const [id, name, addr] of [['fuel1','Лукойл','Садовническая наб., 7'],['fuel2','Газпромнефть','Котельническая наб., 1'],['fuel3','Роснефть','Яузский б-р, 2']])
  PLACES[id] = {name, kind:'АЗС', addr, hero:'img/cafe.jpg', logo:FUEL_ICON, contain:true, rating:'4.4', count:310, react:12, check:'АИ-95 · 62 ₽', hours:'круглосуточно', today:'Открыто круглосуточно', phone:'8 800 100-09-11', site:'2gis.ru', desc:'Кофе с собой, мойка и магазин у кассы', feats:[], cats:[]};
const GALLERY = {""")

# sheet height: summary + route cards visible
rep('peekTop = Math.round(H - (262 + SAB));', 'peekTop = Math.round(H - (334 + SAB));')
rep("  $('#sumDate2').style.opacity", "  fastWrap.style.height = (84*(1-p)) + 'px'; fastWrap.style.opacity = clamp(1 - p*2, 0, 1);\n  $('#sumDate2').style.opacity")

X2 = r'''
#filters{display:flex}
#btnLocate{bottom:72px}
#fastWrap{position:static;overflow:visible;flex:none}
#fast{height:72px;padding:14px 16px 4px;gap:8px;overflow-y:visible}
.fa{height:64px;border-radius:20px;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.04);padding:0 16px 0 12px;gap:10px;flex:none;width:auto;flex-direction:row;align-items:center;justify-content:flex-start}
.fa .fi{width:40px;height:40px;border-radius:50%;background:var(--bg2);display:grid;place-items:center;flex:none}
.fa .ic{opacity:1;color:#141414}
.fa .ft{display:flex;flex-direction:column;align-items:flex-start;font-weight:400;font-size:13px;line-height:17px;color:rgba(20,20,20,.5);letter-spacing:-.2px}
.fa .ft b{font-weight:600;font-size:16px;line-height:20px;color:#141414;letter-spacing:-.3px}
.arr{display:inline-block;width:.54em;height:.54em;margin-left:.14em;vertical-align:baseline;overflow:visible}
.chip .fuel{position:absolute;left:5px;top:6px;font-size:27px;line-height:30px;transition:filter .2s,opacity .2s}
.chip[aria-pressed="false"]{color:var(--blue)}
.chip[aria-pressed="false"] .ci img{filter:none;opacity:1;transform:none}
#filters.picked .chip[aria-pressed="false"]{color:rgba(20,20,20,.55)}
#filters.picked .chip[aria-pressed="false"] .ci img,#filters.picked .chip[aria-pressed="false"] .fuel{filter:grayscale(1);opacity:.55}
#sumMore .s2::after{content:none!important}
'''
rep('@media (prefers-reduced-motion: reduce){', X2 + '\n@media (prefers-reduced-motion: reduce){')

# ---------- round 3: simpler ----------
# tab bar: plain round buttons — bookmark left, friends (icon library "person") right
i = s.index('<button class="bf bs" id="barFav"'); j = s.index('</button>', i) + 9
s = s[:i] + '<button class="bc" id="barFav" aria-label="Мои места"><span class="ic" data-ic="bm"></span></button>' + s[j:]
i = s.index('<button class="bf" id="barHelp"'); j = s.index('</button>', i) + 9
s = s[:i] + '<button class="bc" id="barHelp" aria-label="Друзья"><span class="ic" data-ic="person"></span></button>' + s[j:]
rep("setInterval(() => { const n = $('#savedN'); if (n && n.textContent != saved.size) n.textContent = saved.size; }, 500);", "")

# no grey date above the title
rep('<div id="sumDate2">7 октября</div>', '')
rep("  $('#sumDate2').style.opacity = clamp(1 - p*2.5, 0, 1); $('#sumDate2').style.height = (24*(1-p)) + 'px';", "")
rep('peekTop = Math.round(H - (334 + SAB));', 'peekTop = Math.round(H - (306 + SAB));')

# more single-choice filters: transport, pharmacy (emoji with a white outline)
EMO = {'bus':('🚌','Транспорт'), 'pharm':('💊','Аптеки')}
for k,(e,label) in EMO.items():
    i = s.index('<button class="chip" data-layer="fuel"'); j = s.index('</button>', i) + 9
    nxt = s[i:j].replace('data-layer="fuel"', 'data-layer="%s"' % k).replace('⛽', e).replace('АЗС</button>', label + '</button>')
    # append after the last chip
    last = s.index('</div>', s.index('<div id="filters"'))
    s = s[:last] + nxt + s[last:]
rep("const LNAME = {friends:'Друзья', coffee:'Кофейни', places:'Мои места', fuel:'АЗС'};",
    "const LNAME = {friends:'Друзья', coffee:'Кофейни', places:'Мои места', fuel:'АЗС', bus:'Транспорт', pharm:'Аптеки'};")
rep("m.layer!=='fuel'; m.el", "!['fuel','bus','pharm'].includes(m.layer); m.el")
rep("  {id:'bereza', layer:'picks', type:'gp'},", "  {id:'bus1', layer:'bus', type:'gp', x:150, y:470},\n  {id:'bus2', layer:'bus', type:'gp', x:300, y:250},\n  {id:'bus3', layer:'bus', type:'gp', x:110, y:200},\n  {id:'ph1', layer:'pharm', type:'gp', x:230, y:420},\n  {id:'ph2', layer:'pharm', type:'gp', x:60, y:400},\n  {id:'bereza', layer:'picks', type:'gp'},")
rep("const FUEL_ICON = (() => { try {", "const emoIcon = e => { try { const c = document.createElement('canvas'); c.width = c.height = 96; const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0,0,96,96); x.font = '60px \"Apple Color Emoji\",\"Segoe UI Emoji\",\"Noto Color Emoji\",sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(e, 48, 54); return c.toDataURL(); } catch(_){ return 'img/em_cup.png'; } };\nconst FUEL_ICON = (() => { try {")
rep("const GALLERY = {", """for (const [id, name, kind, addr, e, desc] of [
  ['bus1','Остановка «Устьинский мост»','Остановка','Устьинская наб.','🚌','Автобусы м5, 158 и трамвай А'],
  ['bus2','Китай-город','Метро','Славянская пл.','🚇','Пересадка на 6 и 7 линии'],
  ['bus3','Остановка «Солянка»','Остановка','ул. Солянка','🚌','Автобусы м27 и 158'],
  ['ph1','Аптека Горздрав','Аптека','Солянка, 1/2','💊','Работает до 23:00, есть доставка'],
  ['ph2','Ригла','Аптека','Яузский б-р, 9','💊','Заказ с самовывозом за 30 минут']])
  PLACES[id] = {name, kind, addr, hero:'img/cafe.jpg', logo:emoIcon(e), contain:true, rating:'4.5', count:120, react:8, check:'—', hours:'до 23:00', today:'Сегодня 8:00–23:00', phone:'8 800 000-00-00', site:'2gis.ru', desc, feats:[], cats:[]};
const GALLERY = {""")

X3 = r'''
/* white sheet */
#sheet{background:#fff}
.fa{background:var(--bg2);box-shadow:none}
.fa .fi{background:#fff}
.nw{background:var(--card)}
.xc[aria-selected="true"]{background:rgba(5,5,5,.05);box-shadow:none}
#fadeBottom{background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.92) 55%,#fff)}
#pop.place.expanded,#pop.place.expanded .pc{background:#fff}
#pop.place.expanded .pc-box{background:var(--card)}
#pop.place.expanded .pc-tab.on{background:var(--beige);box-shadow:none}
#pop.place.expanded .pc-grab{background:linear-gradient(#fff 70%,rgba(255,255,255,0))}
.bc .ic{color:#141414}
/* emoji chips get the same white outline as the cup/heart assets */
.chip .fuel{filter:drop-shadow(1.6px 0 0 #fff) drop-shadow(-1.6px 0 0 #fff) drop-shadow(0 1.6px 0 #fff) drop-shadow(0 -1.6px 0 #fff) drop-shadow(0 1px 2px rgba(0,0,0,.18))}
#filters.picked .chip[aria-pressed="false"] .fuel{filter:grayscale(1) drop-shadow(1.6px 0 0 #fff) drop-shadow(-1.6px 0 0 #fff) drop-shadow(0 1.6px 0 #fff) drop-shadow(0 -1.6px 0 #fff);opacity:.55}
'''
rep('@media (prefers-reduced-motion: reduce){', X3 + '\n@media (prefers-reduced-motion: reduce){')

# ---------- round 4 ----------
BM_FILL = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M19 5.16V18.24C19 19.47 19 20.08 18.78 20.44C17.18 22.94 13.01 17.24 12 16.31C10.98 17.24 6.82 22.94 5.22 20.44C5 20.08 5 19.47 5 18.24V5.16C5 4.4 5 4.02 5.13 3.73C5.24 3.48 5.42 3.27 5.64 3.14C5.89 3 6.22 3 6.87 3H17.13C17.78 3 18.11 3 18.36 3.14C18.58 3.27 18.76 3.48 18.87 3.73C19 4.02 19 4.4 19 5.16Z" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
rep('<button class="bc" id="barFav" aria-label="Мои места"><span class="ic" data-ic="bm"></span></button>',
    '<button class="bc" id="barFav" aria-label="Мои места"><span class="ic">' + BM_FILL + '</span><span class="bcn" id="savedN">1</span></button>')
rep('<button class="bc" id="barHelp" aria-label="Друзья"><span class="ic" data-ic="person"></span></button>',
    '<button class="bc" id="barHelp" aria-label="Друзья"><span class="ic" data-ic="person"></span><span class="bcn">4</span></button>')
rep("$('#barFav').addEventListener('click', () => { touch(); toast(`Мои места: ${saved.size} сохранено`); });",
    "$('#barFav').addEventListener('click', () => { touch(); toast(`Мои места: ${saved.size} сохранено`); });\nsetInterval(() => { const n = $('#savedN'); if (n && n.textContent != saved.size) n.textContent = saved.size; }, 400);")

# only me on the map; everything else comes from the filters; friends hidden for now
rep("const layers = {friends:true, coffee:true, places:true, fuel:false};", "const layers = {friends:false, coffee:true, places:true, fuel:false};")
rep("const vis = m.layer==='friends' ? layers.friends : only ? m.layer===only : !['fuel','bus','pharm'].includes(m.layer);",
    "const vis = m.id===selId || (m.layer==='friends' ? layers.friends : only ? (m.layer===only || (only==='places' && m.layer==='picks')) : false);")
rep("function selectPin(id){\n  selId = id;", "function selectPin(id){\n  selId = id; applyLayers();")

# three sheet heights: mini (just the grabber above the tab bar) → peek → full
rep("let sheetState = 'peek';", "let sheetState = 'peek', miniTop = 700;")
rep("  peekTop = Math.round(H - (306 + SAB));", "  peekTop = Math.round(H - (306 + SAB));\n  miniTop = Math.round(H - (Math.max(21, SAB-13) + 4 + 56 + 34));")
rep("  setSheet(state==='full' ? fullTop : peekTop, true);", "  setSheet(state==='full' ? fullTop : state==='mini' ? miniTop : peekTop, true);\n  if (!live) fitMap();")
rep("  if (y > peekTop) y = peekTop + Math.min(30, (y-peekTop)*0.3);", "  if (y > miniTop) y = miniTop + Math.min(30, (y-miniTop)*0.3);")
rep("  snapSheet(v < -0.35 ? 'full' : v > 0.35 ? 'peek' : (sheetTop < (fullTop+peekTop)/2 ? 'full' : 'peek'));",
    """  // always pass through the middle height: full ⇄ peek ⇄ mini
  const from = d.top0 <= fullTop + 30 ? 'full' : d.top0 >= miniTop - 30 ? 'mini' : 'peek';
  let to;
  if (Math.abs(v) > .35){
    if (v < 0) to = from==='mini' ? 'peek' : 'full';
    else to = from==='full' ? 'peek' : 'mini';
  } else {
    const opts = [['full', fullTop], ['peek', peekTop], ['mini', miniTop]];
    to = opts.reduce((a, b) => Math.abs(b[1]-sheetTop) < Math.abs(a[1]-sheetTop) ? b : a)[0];
    if (from==='full' && to==='mini') to = 'peek';
    if (from==='mini' && to==='full') to = 'peek';
  }
  snapSheet(to);""")
rep("  morph(y);\n}", "  morph(y);\n  const q = clamp((y - peekTop)/Math.max(1, miniTop - peekTop), 0, 1);   // fade the summary away toward mini\n  sumEl.style.opacity = 1 - q; fastWrap.style.opacity = sheetP > 0 ? fastWrap.style.opacity : String(1 - q);\n}")
rep("$('#sheetGrab').addEventListener('click', () => snapSheet(sheetState==='full'?'peek':'full'));",
    "$('#sheetGrab').addEventListener('click', () => snapSheet(sheetState==='full' ? 'peek' : sheetState==='mini' ? 'peek' : 'full'));")
rep("function coverBottom(){ return peekTop + 40; }", "function coverBottom(){ return (sheetState==='mini' ? miniTop : peekTop) + 40; }")

X4 = r'''
/* chips: black labels, lighter icons, more air on the left */
.chip{color:#141414;padding-left:9px;gap:4px}
.chip[aria-pressed="false"]{color:#141414}
#filters.picked .chip[aria-pressed="false"]{color:rgba(20,20,20,.45)}
.chip .ci{width:42px;height:42px;margin:0 1px 0 -3px}
.chip .ci img{width:42px;height:42px}
.chip .fuel{left:7px;top:8px;font-size:22px;line-height:26px}
.chip .chk{left:18px;top:20px;transform:scale(.85)}
.chip[aria-pressed="false"] .chk{transform:scale(.3)}
/* tab bar counters */
.bc{position:absolute;top:0}
.bcn{position:absolute;left:50%;bottom:-7px;transform:translateX(-50%);min-width:18px;height:18px;padding:0 6px;box-sizing:border-box;border-radius:9px;background:#fff;
  font-weight:600;font-size:11px;line-height:18px;color:#141414;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.14)}
/* smoother collapse into the small search */
#searchWrap{display:block}
#barFav{left:0}#barHelp{right:0}
#pillBox{position:absolute;top:0;bottom:0;left:64px;right:64px;width:auto;flex:none;margin:0;transition:left .55s cubic-bezier(.32,.72,0,1),right .55s cubic-bezier(.32,.72,0,1)}
#searchBtn .sl{transition:opacity .3s,transform .5s cubic-bezier(.32,.72,0,1)}
.bc{transition:transform .5s cubic-bezier(.32,.72,0,1),opacity .35s}
#searchWrap.mini #pillBox{left:calc(50% - 96px);right:calc(50% - 96px);width:auto;flex:none;margin:0}
#searchWrap.mini #barFav{transform:translateX(24px) scale(.5);opacity:0;pointer-events:none}
#searchWrap.mini #barHelp{transform:translateX(-24px) scale(.5);opacity:0;pointer-events:none}
'''
rep('@media (prefers-reduced-motion: reduce){', X4 + '\n@media (prefers-reduced-motion: reduce){')

# ---------- round 5 ----------
rep('<span class="bcn" id="savedN">1</span>', '')
rep('<span class="bcn">4</span>', '')
rep("setInterval(() => { const n = $('#savedN'); if (n && n.textContent != saved.size) n.textContent = saved.size; }, 400);", "")
# collapsed sheet keeps a grey hint of what's inside
rep('<div class="grab" id="sheetGrab"></div>', '<div class="grab" id="sheetGrab"></div><div id="miniCap">Для вас сегодня</div>')
rep("  miniTop = Math.round(H - (Math.max(21, SAB-13) + 4 + 56 + 34));", "  miniTop = Math.round(H - (Math.max(21, SAB-13) + 4 + 56 + 52));")
rep("  sumEl.style.opacity = 1 - q;", "  sumEl.style.opacity = 1 - q; $('#miniCap').style.opacity = clamp(q*1.6 - .6, 0, 1);")
X5 = r'''
#miniCap{position:absolute;left:0;right:0;top:18px;text-align:center;font-weight:600;font-size:14px;line-height:18px;letter-spacing:-.2px;color:rgba(20,20,20,.45);opacity:0;pointer-events:none}
#search{background:#fff}
#sField{background:#fff}
/* chip spark sits above the chip, quicker */
.xc{isolation:isolate}
.xc::before,.xc::after{z-index:3}
.xc.pop::before,.xc.pop::after{animation:spark1 .7s cubic-bezier(.3,.1,.3,1) forwards}
.xc.pop{animation:xcPop .32s var(--spring)}
@keyframes spark1{0%{--ang:-40deg;opacity:1}85%{opacity:1}100%{--ang:340deg;opacity:0}}
'''
rep('@media (prefers-reduced-motion: reduce){', X5 + '\n@media (prefers-reduced-motion: reduce){')
rep("$('#xChips').addEventListener('click', e => { const c = e.target.closest('.xc'); if (!c) return; touch(); chipPop(c); if (c.dataset.cat!==cat) setCat(c.dataset.cat, true); });",
    "$('#xChips').addEventListener('click', e => { const c = e.target.closest('.xc'); if (!c) return; touch(); chipPop(c); if (c.dataset.cat!==cat) setTimeout(() => setCat(c.dataset.cat, true), 60); });   // a real tap only, never while swiping the row")
rep(".xc::before,.xc::after{z-index:3}", ".xc::before,.xc::after{z-index:3}\n.xc::before{inset:0;padding:2.5px;border-radius:25px}\n.xc::after{inset:-3px;padding:5px;border-radius:28px;filter:blur(3px)}")

# own home-screen icon: black pin on lime
rep('href="app-icon-180.png"', 'href="v2/app-icon-180.png"')
rep('href="app-icon-192.png"', 'href="v2/app-icon-192.png"')

# friends tab: the 2GIS "Friends" glyph (two eyes + smile) instead of the person icon
FRIENDS_SVG = '<svg width="25" height="24" viewBox="0 0 25 24" fill="none"><path d="M4.47559 16.7236C5.72884 20.3695 8.58714 22.0319 11.5264 22.0879C14.5026 22.1445 17.5708 20.5519 19.1621 17.5967L20.6582 18.4033C18.7495 21.9477 15.0733 23.8554 11.4932 23.7871C8.16448 23.7235 4.92752 21.9498 3.26562 18.2744C2.78278 18.5802 2.31491 18.8677 1.92188 19.1035C1.60601 19.293 1.33742 19.4517 1.14746 19.5625C1.05245 19.6179 0.97667 19.6615 0.924805 19.6914L0.845703 19.7373L0 18.2617C0.00799708 18.258 0.0503823 18.2331 0.0751953 18.2188C0.124849 18.1901 0.197667 18.1476 0.290039 18.0938C0.475011 17.9858 0.738 17.8318 1.04688 17.6465C1.66635 17.2748 2.46614 16.7823 3.2002 16.293L4.11719 15.6816L4.47559 16.7236ZM12.7783 2C14.3819 2.00025 15.54 3.5352 15.0996 5.07715L12.9551 12.583C12.3773 14.6051 10.5288 15.9997 8.42578 16C6.72252 15.9997 5.5121 14.3404 6.0332 12.7188L7.34961 8.62207L10.9727 5H8.52051C9.16313 3.20684 10.8628 2.00022 12.7783 2ZM21.7783 2C23.3819 2.00025 24.54 3.5352 24.0996 5.07715L21.9551 12.583C21.3773 14.6051 19.5288 15.9997 17.4258 16C15.7225 15.9997 14.5121 14.3404 15.0332 12.7188L16.3252 8.69629L20.0225 5H17.5205C18.1631 3.20684 19.8628 2.00022 21.7783 2Z" fill="currentColor"/></svg>'
rep('<button class="bc" id="barHelp" aria-label="Друзья"><span class="ic" data-ic="person"></span>', '<button class="bc" id="barHelp" aria-label="Друзья"><span class="ic">' + FRIENDS_SVG + '</span>')
rep(".xc::after{inset:-3px;padding:5px;border-radius:28px;filter:blur(3px)}", ".xc::after{inset:-4px;padding:6px;border-radius:29px;filter:blur(6px)}\n.xc.pop::before{filter:blur(.8px)}")

# ---------- round 6 ----------
X6 = r'''
/* badges line up with the title text, a little more air inside */
.pills{left:0}
.soc{transform:translateX(4px)}
.soc .pills{left:-4px}
.pc-hero .pills{left:0}
.soc{transform:translateX(4px)}
.soc .pills{left:-4px}
.pill{padding:0 14px}
.pill.rt{padding:0 11px}
/* full place card: soft fade under the action bar (like under search), same bottom gap as search */
#pcBar.docked{padding-bottom:calc(var(--sbtn,21px) + 4px);transition:transform .42s var(--ease),padding .3s var(--ease)}
#pcBar.docked::before{top:-44px;border-radius:0;box-shadow:none;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,.92) 45%,#fff)}
#pcBar.docked .pb:not(.go){background:#fff;box-shadow:0 0 0 .5px rgba(137,137,137,.25),0 2px 8px rgba(0,0,0,.1)}
'''
rep('@media (prefers-reduced-motion: reduce){', X6 + '\n@media (prefers-reduced-motion: reduce){')
rep('@media (prefers-reduced-motion: reduce){', '.nw-x,.nw.y .nw-x{background:rgba(0,0,0,.06);color:#141414}\n.nw-x .ic{opacity:.55}\n@media (prefers-reduced-motion: reduce){')

# chips: a small version of the search comet runs around the chip (same 0.7s dynamic)
rep('@media (prefers-reduced-motion: reduce){', '''.xc.pop::before,.xc.pop::after{animation:none;opacity:0}
.xc .ccomet{position:absolute;left:-8px;top:-8px;overflow:visible;pointer-events:none;z-index:4}
@media (prefers-reduced-motion: reduce){''')
rep("function chipPop(el){", r"""function chipComet(el){
  el.querySelectorAll('.ccomet').forEach(n => n.remove());
  const w = el.offsetWidth, h = el.offsetHeight, o = 8, r = h/2, NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'ccomet');
  svg.setAttribute('width', w + 2*o); svg.setAttribute('height', h + 2*o); svg.setAttribute('viewBox', `0 0 ${w + 2*o} ${h + 2*o}`);
  const fid = 'cg' + Math.random().toString(36).slice(2, 7);
  svg.innerHTML = `<defs><filter id="${fid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.6"/></filter></defs><g filter="url(#${fid})"></g><g></g>`;
  const d = `M${o},${o + r} A${r},${r} 0 0 1 ${o + r},${o} H${o + w - r} A${r},${r} 0 0 1 ${o + w},${o + r} A${r},${r} 0 0 1 ${o + w - r},${o + h} H${o + r} A${r},${r} 0 0 1 ${o},${o + r}Z`;
  const [gGlow, gCore] = svg.querySelectorAll('g'), N = 18, core = [], glow = [];
  for (let k = 0; k < N; k++) for (const [g, arr] of [[gGlow, glow], [gCore, core]]){ const p = document.createElementNS(NS, 'path'); p.setAttribute('d', d); p.setAttribute('fill', 'none'); p.setAttribute('stroke-linecap', 'round'); g.appendChild(p); arr.push(p); }
  el.appendChild(svg);
  const L = core[0].getTotalLength(), tail = L * .5, seg = tail / N, A = hex('#33D60A'), B = hex('#FFEE33'), t0 = performance.now(), DUR = 700;
  const step = now => {
    const t = clamp((now - t0) / DUR, 0, 1), env = Math.sin(Math.PI * clamp(t / .96, 0, 1)), head = L * (.05 + 1.05 * (1 - Math.pow(1 - t, 2.2)));
    for (let k = 0; k < N; k++){
      const f = k / (N - 1), col = 'rgb(' + A.map((v, i) => Math.round(lerp(v, B[i], Math.pow(f, .8)))).join(',') + ')';
      const wc = lerp(3.4, 1, f), a = env * Math.pow(1 - f, 1.3), off = (-(((head - k*seg) % L) + L) % L).toFixed(2), dash = `${(seg*1.3).toFixed(2)} ${L}`;
      for (const [p, wk, ak] of [[core[k], wc, a], [glow[k], wc*2.6 + 2, a*.85]]){
        p.setAttribute('stroke', col); p.setAttribute('stroke-width', wk.toFixed(2)); p.setAttribute('stroke-dasharray', dash); p.setAttribute('stroke-dashoffset', off); p.setAttribute('opacity', ak.toFixed(3));
      }
    }
    if (t < 1) requestAnimationFrame(step); else svg.remove();
  };
  requestAnimationFrame(step);
}
function chipPop(el){
  if (el.classList.contains('xc') && !reduced) chipComet(el);""")

# ---------- round 7 ----------
# peek height from the content itself, so the gap above the search bar is the same in Safari and on the home screen
rep('  peekTop = Math.round(H - (306 + SAB));', '  { const barTop = H - (Math.max(21, SAB-13) + 4 + 56); peekTop = Math.round(barTop - 20 - (16 + 20 + 30 + 60 + 84)); }')
rep('@media (prefers-reduced-motion: reduce){', '#pcBar.docked .pb:not(.go){background:var(--beige);box-shadow:none}\n@media (prefers-reduced-motion: reduce){')
rep('@media (prefers-reduced-motion: reduce){', '#fast{height:84px;padding:20px 16px 0}\n.pb{box-shadow:0 2px 10px rgba(0,0,0,.1)}\n#pcBar.docked .pb:not(.go){box-shadow:none}\n@media (prefers-reduced-motion: reduce){')
rep('@media (prefers-reduced-motion: reduce){', '#pcBar.docked .pb:not(.go){background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.1)}\n@media (prefers-reduced-motion: reduce){')

# ---------- perf: lighter for screen recording ----------
# friends are hidden in v2, so the moving-friend loop doesn't need to run every frame
rep("requestAnimationFrame(lenaLoop);\nconst LIVE_MAP", "const LIVE_MAP") if "requestAnimationFrame(lenaLoop);\nconst LIVE_MAP" in s else None
i = s.rfind("requestAnimationFrame(lenaLoop);"); s = s[:i] + "/* lenaLoop off in v2 */" + s[i+len("requestAnimationFrame(lenaLoop);"):]
# don't reposition hidden or merged pins on every map frame
rep("function placeMarker(m){\n", "function placeMarker(m){\n  if (m.el.classList.contains('off') || m.el.classList.contains('merged')) return;\n")
rep("  cluster();\n}\nlet selId", "  renderMap(); cluster();\n}\nlet selId") if "  cluster();\n}\nlet selId" in s else None
# explore cards don't animate while the sheet is down (they're invisible anyway)
rep("  explore.style.pointerEvents = p > .5 ? '' : 'none';", "  explore.style.pointerEvents = p > .5 ? '' : 'none'; explore.classList.toggle('still', p < .5);")
X7 = r'''
.still *,.still *::before,.still *::after{animation-play-state:paused!important}
.me .blur{filter:none;background:radial-gradient(circle,rgba(25,156,255,.75) 0,rgba(25,156,255,0) 70%);left:5px;top:9px;width:80px;height:80px}
#sheet.faded #sheetScroll{-webkit-mask-image:none;mask-image:none}
.mk{contain:layout style}
'''
rep('@media (prefers-reduced-motion: reduce){', X7 + '\n@media (prefers-reduced-motion: reduce){')
rep("    else a.m.el.classList.remove('merged');\n    for (const b of grp){", "    else a.m.el.classList.remove('merged');\n    placeMarker(a.m);\n    for (const b of grp){")
