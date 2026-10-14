import re,sys
src='/home/claude/alexb-proto/index.html'; dst='/home/claude/alexb-proto/v2/index.html'
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:90]); s=s.replace(a,b)
def cut(a,b):
    global s
    i=s.index(a); j=s.index(b,i)+len(b); s=s[:i]+s[j:]

# base: v2 is served from /v2/ and from its own domain root; assets live at the site root
rep('<meta charset="utf-8">','<meta charset="utf-8">\n<base href="/">')
rep('<title>BingoBongo 2GIS</title>','<title>BingoBongo 2GIS · v2</title>')
rep('content="BingoBongo 2GIS">','content="BingoBongo v2">')

# drop the old "mini" search styles (v2 has its own bar)
cut('/* collapsing search: the pill shrinks','#searchWrap.mini #searchBtn .sbg{pointer-events:auto}')

# ---------- markup: greeting first, then service tiles; new bottom bar ----------
i=s.index('<div id="fastWrap">'); j=s.index('</div></div>',i)+len('</div></div>')
fast=s[i:j]; s=s[:i]+s[j:]
i=s.index('<div id="xChipsWrap">'); s=s[:i]+fast+'\n      '+s[i:]
rep('<button class="fa" data-toast="Домой: 2 ч 45 мин, пробки 9 баллов"><span class="ic" data-ic="home"></span>2 ч 45 мин</button>',
    '<button class="fa" data-toast="Домой: 2 ч 45 мин, пробки 9 баллов"><span class="ic" data-ic="home"></span><span class="ft"><i>Домой</i>2 ч 45 мин</span></button>')
rep('<button class="fa" data-toast="На работу: 45 мин"><span class="ic" data-ic="brief"></span>45 мин</button>',
    '<button class="fa" data-toast="На работу: 45 мин"><span class="ic" data-ic="brief"></span><span class="ft"><i>На работу</i>45 мин</span></button>')
rep('<button class="fa" data-toast="Красный проспект, 8: маршрут строится"><span class="ic" data-ic="clock"></span>Красный проспект, 8</button>',
    '<button class="fa" data-toast="Красный проспект, 8: маршрут строится"><span class="ic" data-ic="clock"></span><span class="ft"><i>Недавнее</i>Красный пр., 8</span></button>')
rep('<h2 id="sumTitle">Для вас на <span id="sumDate">7 октября</span><span class="colon">:</span></h2>',
    '<div id="sumDate2">7 октября</div><h2 id="sumTitle">Для вас сегодня<span class="colon">:</span></h2>')
rep('<button class="s2" data-go="news" id="sumNews">2 новости района</button>','<button class="s2" data-go="news" id="sumNews">2 новости района</button>')
rep('<button id="searchBtn" aria-label="Поиск места"><span class="sbg"></span><img src="img/search.png" alt=""><span class="sl">Поиск места</span></button>',
    '''<button class="bc" id="barFav" aria-label="Мои места"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 20.3C11.8 20.3 11.6 20.2 11.4 20.1C9.6 19.4 7.4 18.1 5.6 16.4C3.7 14.6 2.3 12.4 2.3 9.8C2.3 6.7 4.4 4.3 7.4 4C9.3 3.8 10.9 4.7 12 6.1C13.1 4.7 14.7 3.8 16.6 4C19.6 4.3 21.7 6.7 21.7 9.8C21.7 12.4 20.3 14.6 18.4 16.4C16.6 18.1 14.4 19.4 12.6 20.1C12.4 20.2 12.2 20.3 12 20.3Z" stroke="#141414" stroke-width="2"/></svg></button>
      <div id="pillBox"><svg id="comet" aria-hidden="true"><defs><filter id="cglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4.5"/></filter></defs><g id="cometGlow" filter="url(#cglow)"></g><g id="cometCore"></g></svg>
        <button id="searchBtn" aria-label="Поиск места"><span class="sbg"></span><span class="sl">Поиск места</span><img src="img/search.png" alt=""></button></div>
      <button class="bc" id="barHelp" aria-label="Помощник"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M21.5 11.9C21.5 17.1 17.2 21.5 12 21.5C10.9 21.5 9.96 21.3 9.29 21.1C9 21 8.81 20.96 8.64 20.89C7.27 21.48 6 21.64 5.06 21.65C4.3 21.66 3.6 21.55 3.28 21.46C2.97 21.38 2.72 21.16 2.59 20.87C2.46 20.58 2.47 20.25 2.61 19.97C2.92 19.36 3.21 18.83 3.4 18.45C3.61 18.05 3.73 17.79 3.8 17.58C3.86 17.39 3.87 17.28 3.85 17.18C3.84 17.07 3.79 16.9 3.64 16.6C2.85 15.04 2.5 13.29 2.5 11.92C2.5 6.71 6.76 2.5 12 2.5C17.24 2.5 21.5 6.71 21.5 11.92Z" stroke="#141414" stroke-width="2"/></svg></button>''')

# ---------- styles (appended last so they win) ----------
V2CSS = r'''
/* ================= v2: calmer "Sber family" skin ================= */
:root{ --bg2:#F2F3F5; --green2:#1FB24A; }
#sheet{background:linear-gradient(180deg,#DCEAFF 0,#EAF1FB 150px,var(--bg2) 300px);box-shadow:0 -2px 18px rgba(0,0,0,.08)}
#sumDate2{font-size:14px;line-height:18px;color:rgba(20,20,20,.45);letter-spacing:-.1px;margin-bottom:6px;transition:opacity .2s}
#sumTitle{font-size:26px;line-height:30px;letter-spacing:-.5px}
#sumMore button{font-size:26px;line-height:30px;letter-spacing:-.5px}
#sumMore .s1{color:var(--green2)}
#sumMore .s2{color:#FF8A00}
#sumMore .s2::after{content:" ↗";font-weight:500}
#fastWrap{overflow:visible}
#fast{height:84px;padding:8px 16px 4px;gap:8px;overflow:visible}
.fa{width:calc((var(--cw,358px) - 16px)/3);height:84px;border-radius:20px;box-shadow:0 1px 2px rgba(0,0,0,.04);flex-direction:column;align-items:flex-start;justify-content:space-between;
  padding:12px 12px 11px;gap:0;font-size:15px;line-height:18px;letter-spacing:-.3px;background:#fff}
.fa .ic{opacity:1;color:#141414}
.fa .ft{display:flex;flex-direction:column;align-items:flex-start;white-space:nowrap;overflow:hidden;max-width:100%;text-overflow:ellipsis}
.fa .ft i{font-style:normal;font-weight:400;font-size:13px;line-height:16px;color:rgba(20,20,20,.5)}
.xc[aria-selected="true"]{background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.05)}
.nw{background:#fff}
.nw.y{background:#FFF5D1}
.nw-x{background:var(--bg2)}
.xh{font-size:20px;line-height:24px;letter-spacing:-.4px}
#fadeBottom{background:linear-gradient(180deg,rgba(242,243,245,0),rgba(242,243,245,.92) 55%,var(--bg2));height:110px}

/* bottom bar: heart · search pill · helper (like the reference apps) */
#searchWrap{left:16px;right:16px;width:auto;margin-left:0;height:56px;display:flex;gap:8px;align-items:center;bottom:calc(var(--sbtn,21px) + 4px)}
#wave{display:none}
.bc{flex:none;width:56px;height:56px;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 4px 14px rgba(0,0,0,.1),0 1px 3px rgba(0,0,0,.06);
  transition:transform .45s var(--spring),opacity .3s;transition-delay:var(--d,0s)}
.bc:active{transform:scale(.92)}
#barFav{--d:.08s}#barHelp{--d:.14s}
#pillBox{position:relative;flex:1;height:56px;min-width:0}
#searchBtn{position:absolute;inset:0;border-radius:28px}
#searchBtn .sbg{position:absolute;inset:0;border-radius:28px;background:#fff;box-shadow:0 4px 14px rgba(0,0,0,.1),0 1px 3px rgba(0,0,0,.06)}
#searchBtn .sl{position:absolute;left:20px;top:50%;margin-top:-10px;line-height:20px;font-weight:500;font-size:16px;letter-spacing:-.3px;color:rgba(20,20,20,.5);z-index:1}
#searchBtn img{position:absolute;right:14px;top:50%;margin-top:-13px;width:26px;height:26px;z-index:1}
#comet{position:absolute;left:-14px;top:-14px;width:calc(100% + 28px);height:84px;overflow:visible;pointer-events:none;z-index:2}
#searchWrap.mini .bc{transform:scale(.6);opacity:0;pointer-events:none;transition-delay:0s}
#searchWrap.mini #pillBox{flex:none;width:200px;margin:0 auto}
#pillBox{transition:width .45s var(--ease)}
#searchWrap.intro .bc{transform:scale(.4);opacity:0}

/* place card on the grey canvas */
#pop.place.expanded{background:var(--bg2)}
#pop.place.expanded .pc{background:var(--bg2)}
#pop.place.expanded .pc-box{background:#fff}
#pop.place.expanded .pc-tab.on{background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.05)}
#pop.place.expanded .pc-grab{background:linear-gradient(var(--bg2) 70%,rgba(242,243,245,0))}
.pc-box{border-radius:24px}
#pcBar.docked::before{background:#fff}
#search{background:var(--bg2)}
#sField{background:#fff}
'''
rep('@media (prefers-reduced-motion: reduce){','%s\n@media (prefers-reduced-motion: reduce){' % V2CSS)

# ---------- layout numbers for the taller header ----------
rep("  peekTop = Math.round(H - (234 + SAB));","  peekTop = Math.round(H - (366 + SAB));")
rep("  fastWrap.style.height = (50*(1-p)) + 'px'; fastWrap.style.marginTop = (20*(1-p)) + 'px'; fastWrap.style.opacity = clamp(1 - p*2, 0, 1);",
    "  fastWrap.style.height = (96*(1-p)) + 'px'; fastWrap.style.marginTop = (14*(1-p)) + 'px'; fastWrap.style.opacity = clamp(1 - p*2, 0, 1);\n  $('#sumDate2').style.opacity = clamp(1 - p*2.5, 0, 1); $('#sumDate2').style.height = (24*(1-p)) + 'px';")
rep("  t.style.height = lerp(32, 18, c) + 'px';","  t.style.height = lerp(30, 18, c) + 'px';")
rep("  sumMore.style.height = (64*(1 - p)) + 'px';","  sumMore.style.height = (60*(1 - p)) + 'px';")
rep("  sumEl.style.marginTop = lerp(lerp(18, 28, p), 0, c) + 'px';","  sumEl.style.marginTop = lerp(lerp(20, 26, p), 0, c) + 'px';")

# ---------- search animation: a glowing comet line flies around the pill ----------
i=s.index("function playWave(entrance){"); j=s.index("let waveTimer=null;")
s=s[:i]+r'''const cometCore = $('#cometCore'), cometGlow = $('#cometGlow'), cometSvg = $('#comet');
const N_SEG = 26, segCore = [], segGlow = [];
for (let k = 0; k < N_SEG; k++){
  for (const [g, arr] of [[cometGlow, segGlow], [cometCore, segCore]]){
    const p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('fill','none'); p.setAttribute('stroke-linecap','round'); g.appendChild(p); arr.push(p);
  }
}
const cA = hex('#33D60A'), cB = hex('#FFEE33');   // head green → tail yellow
function cometPath(){
  const box = $('#pillBox'), w = box.offsetWidth, h = box.offsetHeight, o = 14, r = h/2 + 2, x0 = o - 2, y0 = o - 2, W2 = w + 4, H2 = h + 4;
  cometSvg.setAttribute('viewBox', `0 0 ${w + 2*o} ${h + 2*o}`);
  // start on the left end, run clockwise along the top
  return `M${x0},${y0 + r} A${r},${r} 0 0 1 ${x0 + r},${y0} H${x0 + W2 - r} A${r},${r} 0 0 1 ${x0 + W2},${y0 + r} A${r},${r} 0 0 1 ${x0 + W2 - r},${y0 + H2} H${x0 + r} A${r},${r} 0 0 1 ${x0},${y0 + r}Z`;
}
function playWave(entrance){
  cancelAnimationFrame(waveRAF);
  if (sw.classList.contains('mini')){ sBtn.style.opacity = 1; sBtn.style.transform = ''; return; }
  lastWave = performance.now();
  if (entrance){ sw.classList.add('intro'); requestAnimationFrame(() => requestAnimationFrame(() => sw.classList.remove('intro'))); }
  if (reduced){ sBtn.style.transform=''; sBtn.style.opacity=1; return; }
  const d = cometPath(); for (const p of [...segCore, ...segGlow]) p.setAttribute('d', d);
  const L = segCore[0].getTotalLength(), tail = L * .55, seg = tail / N_SEG;
  const DUR = 1900, t0 = performance.now();
  const step = now => {
    const t = clamp((now - t0)/DUR, 0, 1);
    if (entrance){ const k = clamp(t/0.28,0,1); sBtn.style.opacity = clamp(t/0.06,0,1); sBtn.style.transform = `scale(${lerp(.9, 1, easeOutBack(k))})`; }
    else sBtn.style.transform = `scale(${1 + 0.02*Math.sin(Math.PI*clamp(t/0.3,0,1))})`;
    const env = Math.sin(Math.PI * clamp((t - .04)/.92, 0, 1));         // fades in, flies, fades out
    const head = L * (.02 + 1.08 * ease(t));                           // a bit more than one lap
    for (let k = 0; k < N_SEG; k++){
      const f = k / (N_SEG - 1), pos = head - k*seg, col = 'rgb(' + cA.map((v,ix) => Math.round(lerp(v, cB[ix], Math.pow(f,.8)))).join(',') + ')';
      const wCore = lerp(6, 1.6, f), a = env * Math.pow(1 - f, 1.3);
      for (const [p, wk, ak] of [[segCore[k], wCore, a], [segGlow[k], wCore*2.8 + 3, a*.85]]){
        p.setAttribute('stroke', col); p.setAttribute('stroke-width', wk.toFixed(2));
        p.setAttribute('stroke-dasharray', `${(seg*1.25).toFixed(2)} ${L}`); p.setAttribute('stroke-dashoffset', (-((pos % L) + L) % L).toFixed(2));
        p.setAttribute('opacity', ak.toFixed(3));
      }
    }
    if (t < 1) waveRAF = requestAnimationFrame(step);
    else { waveRAF = null; sBtn.style.transform=''; for (const p of [...segCore, ...segGlow]) p.setAttribute('opacity', 0); }
  };
  waveRAF = requestAnimationFrame(step);
}
$('#barFav').addEventListener('click', () => { touch(); toast(`Мои места: ${saved.size} сохранено`); });
$('#barHelp').addEventListener('click', () => { touch(); toast('Помощник: скоро'); });
'''+s[j:]
open(dst,'w',encoding='utf-8').write(s)
print('ok', len(s))
