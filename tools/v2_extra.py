# second round of v2 changes, applied on top of build_v2.py
ARR = '<svg class="arr" viewBox="0 0 16 16" fill="none"><path d="M3 14L13 4M13 12V4H4" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

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
rep("  $('#sumDate2').style.opacity", "  fastWrap.style.height = (72*(1-p)) + 'px'; fastWrap.style.opacity = clamp(1 - p*2, 0, 1);\n  $('#sumDate2').style.opacity")

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
.arr{display:inline-block;width:.6em;height:.6em;margin-left:.14em;vertical-align:.06em}
.chip .fuel{position:absolute;left:5px;top:6px;font-size:27px;line-height:30px;transition:filter .2s,opacity .2s}
.chip[aria-pressed="false"]{color:var(--blue)}
.chip[aria-pressed="false"] .ci img{filter:none;opacity:1;transform:none}
#filters.picked .chip[aria-pressed="false"]{color:rgba(20,20,20,.55)}
#filters.picked .chip[aria-pressed="false"] .ci img,#filters.picked .chip[aria-pressed="false"] .fuel{filter:grayscale(1);opacity:.55}
#sumMore .s2::after{content:none!important}
'''
rep('@media (prefers-reduced-motion: reduce){', X2 + '\n@media (prefers-reduced-motion: reduce){')
