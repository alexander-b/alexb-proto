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
i=s.index('<div id="filters"'); s=s[:i]+fast+'\n        '+s[i:]
rep('<h2 id="sumTitle">Для вас на <span id="sumDate">7 октября</span><span class="colon">:</span></h2>',
    '<div id="sumDate2">7 октября</div><h2 id="sumTitle">Для вас сегодня<span class="colon">:</span></h2>')
rep('<button class="s2" data-go="news" id="sumNews">2 новости района</button>','<button class="s2" data-go="news" id="sumNews">2 новости района</button>')
rep('<button id="searchBtn" aria-label="Поиск места"><span class="sbg"></span><img src="img/search.png" alt=""><span class="sl">Поиск места</span></button>',
    '''<button class="bf bs" id="barFav" aria-label="Мои места"><span class="bsa"><img class="s1" src="img/ph_dark.jpg" alt=""><img class="s2" src="img/ph_teal.jpg" alt=""><img class="m" src="img/ph_bereza.jpg" alt=""></span><span class="bfn"><svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M19 5.16V18.24C19 19.47 19 20.08 18.78 20.44C17.18 22.94 13.01 17.24 12 16.31C10.98 17.24 6.82 22.94 5.22 20.44C5 20.08 5 19.47 5 18.24V5.16C5 4.4 5 4.02 5.13 3.73C5.24 3.48 5.42 3.27 5.64 3.14C5.89 3 6.22 3 6.87 3H17.13C17.78 3 18.11 3 18.36 3.14C18.58 3.27 18.76 3.48 18.87 3.73C19 4.02 19 4.4 19 5.16Z" fill="#141414"/></svg><b id="savedN">1</b></span></button>
      <div id="pillBox"><svg id="comet" aria-hidden="true"><defs><filter id="cglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4.5"/></filter></defs><g id="cometGlow" filter="url(#cglow)"></g><g id="cometCore"></g></svg>
        <button id="searchBtn" aria-label="Поиск места"><span class="sbg"></span><span class="sl">Поиск места</span><img src="img/search.png" alt=""></button></div>
      <button class="bf" id="barHelp" aria-label="Друзья рядом"><span class="bfa"><img class="s1" src="img/fr_kate.jpg" alt=""><img class="s2" src="img/fr_dima.jpg" alt=""><img class="m" src="img/fr_anya.jpg" alt=""></span><span class="bfn"><svg width="12" height="12" viewBox="0 0 24 24"><path d="M16 6C16 8.2 15.2 12 12 12S8 8.2 8 6a4 4 0 0 1 8 0Z" fill="#141414"/><path d="M4.2 19.2C4 19 4 18.9 4 18.7 4.2 16.1 6.3 14 9 14h6c2.7 0 4.8 2.1 5 4.7 0 .2 0 .3-.2.5-2.4 2.7-13.2 2.7-15.6 0Z" fill="#141414"/></svg>4</span></button>''')

# ---------- styles (appended last so they win) ----------
V2CSS = r'''
/* ================= v2: calmer "Sber family" skin ================= */
:root{ --bg2:#F2F3F5; --green2:#30C800; }
#sheet{background:var(--bg2);box-shadow:0 -2px 18px rgba(0,0,0,.08)}
#sumDate2{font-size:14px;line-height:18px;color:rgba(20,20,20,.45);letter-spacing:-.1px;margin-bottom:6px;transition:opacity .2s}
#sumTitle{font-size:26px;line-height:30px;letter-spacing:-.5px}
#sumMore button{font-size:26px;line-height:30px;letter-spacing:-.5px}
#sumMore .s1{color:var(--green2)}
#sumMore .s2{color:#FF8A00}
#sumMore .s2::after{content:" ↗";font-weight:500}
#fastWrap{position:absolute;left:0;right:0;bottom:10px;overflow:visible}
#fast{height:40px;padding:4px 12px 6px;overflow-y:visible}
.fa{background:#fff}
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
/* no layer chips above the sheet in v2 */
#filters{display:none}
#btnLocate{bottom:66px}
/* friends bubble in the bar */
.bf{flex:none;width:66px;height:58px;position:relative;transition:transform .45s var(--spring),opacity .3s;transition-delay:.14s}
.bf:active{transform:scale(.94)}
.bfa img{position:absolute;border-radius:50%;object-fit:cover;box-shadow:0 0 0 1.5px #C5F92B,0 2px 6px rgba(0,0,0,.15)}
.bfa .s1{left:0;top:4px;width:24px;height:24px}.bfa .s2{right:0;top:4px;width:24px;height:24px}
.bfa .m{left:17px;top:0;width:32px;height:32px;box-shadow:0 0 0 1.6px #C5F92B,0 2px 8px rgba(0,0,0,.18)}
.bfn{position:absolute;left:11px;top:28px;height:28px;padding:0 9px 0 8px;border-radius:20px;background:#fff;display:flex;align-items:center;gap:3px;
  font-weight:600;font-size:13px;color:#141414;box-shadow:0 2px 8px rgba(0,0,0,.1)}
#searchWrap.mini .bf{transform:scale(.6);opacity:0;pointer-events:none;transition-delay:0s}
#searchWrap.intro .bf{transform:scale(.4);opacity:0}
.bsa img{position:absolute;object-fit:cover;box-shadow:0 0 0 1.5px #C5F92B,0 2px 6px rgba(0,0,0,.18)}
.bsa .s1{left:3px;top:6px;width:22px;height:22px;border-radius:7px;transform:rotate(-14deg)}
.bsa .s2{right:3px;top:6px;width:22px;height:22px;border-radius:7px;transform:rotate(14deg)}
.bsa .m{left:17px;top:0;width:32px;height:32px;border-radius:10px;box-shadow:0 0 0 1.6px #C5F92B,0 2px 8px rgba(0,0,0,.2)}
.bfn b{font-weight:600}
#barFav{transition-delay:.08s}
/* chip pick: a glowing spark runs once around the chip */
@property --ang{syntax:'<angle>';inherits:false;initial-value:0deg}
.xc::before{inset:-2px;border-radius:27px;box-shadow:none;padding:2px;opacity:0;
  background:conic-gradient(from var(--ang),rgba(54,219,1,0) 0deg,rgba(255,238,51,0) 250deg,#FFEE33 300deg,#36DB01 352deg,rgba(54,219,1,0) 360deg);
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask:linear-gradient(#000 0 0) content-box exclude,linear-gradient(#000 0 0)}
.xc::after{inset:-4px;border-radius:29px;box-shadow:none;opacity:0;filter:blur(5px);
  background:conic-gradient(from var(--ang),rgba(54,219,1,0) 0deg,rgba(255,238,51,0) 270deg,rgba(255,238,51,.7) 310deg,rgba(54,219,1,.9) 352deg,rgba(54,219,1,0) 360deg);
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask:linear-gradient(#000 0 0) content-box exclude,linear-gradient(#000 0 0);padding:6px}
.xc.pop::before,.xc.pop::after{animation:spark1 1.1s cubic-bezier(.45,.05,.35,1) forwards}
@keyframes spark1{0%{--ang:-60deg;opacity:0}12%{opacity:1}80%{opacity:1}100%{--ang:340deg;opacity:0}}
.xc .spark{display:none}

#sField{background:#fff}
'''
rep('@media (prefers-reduced-motion: reduce){','%s\n@media (prefers-reduced-motion: reduce){' % V2CSS)

# ---------- layout numbers for the taller header ----------
rep("  peekTop = Math.round(H - (234 + SAB));","  peekTop = Math.round(H - (262 + SAB));")
rep("  fastWrap.style.height = (50*(1-p)) + 'px'; fastWrap.style.marginTop = (20*(1-p)) + 'px'; fastWrap.style.opacity = clamp(1 - p*2, 0, 1);",
    "  $('#sumDate2').style.opacity = clamp(1 - p*2.5, 0, 1); $('#sumDate2').style.height = (24*(1-p)) + 'px';")
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
setInterval(() => { const n = $('#savedN'); if (n && n.textContent != saved.size) n.textContent = saved.size; }, 500);
$('#barHelp').addEventListener('click', () => { touch(); toast('4 друга рядом: Аня, Дима, Лена, Катя'); });
'''+s[j:]
exec(open('/home/claude/alexb-proto/tools/v2_extra.py',encoding='utf-8').read())
open(dst,'w',encoding='utf-8').write(s)
print('ok', len(s))
