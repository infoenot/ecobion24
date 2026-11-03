import re, base64, os
D = os.path.dirname(os.path.abspath(__file__))
s = open(D + '/pres/deck.norm.html').read()
css = s[s.index('<style>') + 7:s.index('</style>')]
secs = re.findall(r'<section class="page[^"]*".*?</section>', s, re.S)

# ---- цена станка только по запросу (03.11) ----
def NP(a, b, cnt=1):
    global s
    assert s.count(a) >= 1, a[:60]; s = s.replace(a, b)
NP('<div class="card fill"><div class="num">450 000 <small>₽</small></div><p class="muted">Цена комплекта, без НДС. Доставка транспортной компанией оплачивается отдельно.</p></div>',
   '<div class="card fill"><div class="num">Цена <small>по запросу</small></div><p class="muted">Назовём на консультации. Доставка транспортной компанией оплачивается отдельно.</p></div>')
NP('<div class="fv">450 000 ₽</div><div class="fl">цена комплекта без НДС</div>','<div class="fv">по запросу</div><div class="fl">цена комплекта — на консультации</div>')
NP('<div>Цена</div><div>450 000 ₽ без НДС</div>','<div>Цена</div><div>по запросу, фиксируется в договоре</div>')
NP('Платите один раз — <b class="or">450 000 ₽</b>.','Платите один раз — без роялти и ежемесячных платежей.')
s = re.sub(r'<div class="pb">.*?<span>окупились</span></div>\s*</div>', '', s, count=1, flags=re.S)
s = re.sub(r'\s*<tr><td><b>Объектов до окупаемости</b></td>.*?</tr>', '', s, count=1, flags=re.S)
assert '<div class="pb-axis"' not in s and 'Объектов до окупаемости' not in s
secs = re.findall(r'<section class="page[^"]*".*?</section>', s, re.S)

PHONE = '+7 921 950-38-60'
TEL = 'tel:+79219503860'

def form(fid, place, title, sub, extra='', panel=False):
    return f'''<form class="lform{' u-panel' if panel else ''}" id="{fid}" data-place="{place}">
  <div class="fields">
    <h3>{title}</h3><p>{sub}</p>
    <input name="name" placeholder="Имя" autocomplete="name" required>
    <input name="phone" type="tel" placeholder="+7 (___) ___-__-__" autocomplete="tel" required>
    {extra}
    <button class="btn" type="submit">Получить консультацию</button>
    <div class="agree">Нажимая кнопку, вы соглашаетесь на обработку персональных данных для обратной связи.</div>
  </div>
  <div class="ok"><b>Заявка отправлена</b>Перезвоним в ближайшее время. Или сразу: <a href="{TEL}">{PHONE}</a>, звонок или MAX.</div>
</form>'''

out = []
ids = {}
for i, x in enumerate(secs, 1):
    x = re.sub(r'\s*<div class="foot">.*?</div>\s*</section>', '\n</section>', x, flags=re.S)
    m = re.search(r'<div class="top"><b>(\d\d) ·', x)
    if m and m.group(1) not in ids:
        ids[m.group(1)] = f's{m.group(1)}'
        x = x.replace('<section class="page', f'<section id="s{m.group(1)}" class="page', 1)
    out.append(x)

# cover -> hero with form, toc as links
cov = out[0]
h1 = re.search(r'<h1>.*?</h1>', cov, re.S).group(0)
lead = re.search(r'<p class="lead">.*?</p>', cov, re.S).group(0)
toc = re.findall(r'<div><span>(\d\d)</span>(.*?)</div>', cov)
links = ''.join(f'<a href="#s{n}"><span>{n}</span>{t}</a>' for n, t in toc)
out[0] = f'''<section class="u-hero">
  <div class="u-wrap u-hgrid">
    <div class="u-htxt">
      <span class="u-chip">Без роялти и паушального взноса</span>
      <h1><span class="ln">Начни свой бизнес</span> <span class="ln">на утеплении панорамных</span> <span class="ln">окон, балконов</span> <span class="ln">и лоджий изнутри</span></h1>
      <p class="u-lead">Для мастеров, оконщиков, ремонтников и тех, кто устал работать на рынке с высокой конкуренцией и низкой доходностью.</p>
      <div class="u-btns"><a class="u-btn" href="#form-top">Получить консультацию</a><a class="u-btn u-out" href="{TEL}">{PHONE}</a></div>
    </div>
    <div class="u-hpic"><img src="img/hero.jpg" alt="Лоджия: белые короба на стойках панорамного остекления">
      <div class="u-fl u-fl1"><b>0 ₽</b>роялти и паушальный взнос</div>
      <div class="u-fl u-fl2"><b>20 рабочих дней</b>изготовление по договору</div>
      <div class="u-fl u-fl3"><b>24 месяца</b>гарантия на станок</div>
      <span class="u-ill">иллюстрация</span>
    </div>
  </div>
  <div class="u-wrap">{form('form-top', 'первый экран', 'Обсудить запуск в вашем городе', 'Перезвоним, разберём город и ответим на вопросы по станку.', '<input name="city" placeholder="Город">', panel=True)}</div>
</section>
<div class="u-trust"><div class="u-wrap"><span>оборудование в собственность</span><i>+</i><span>без роялти</span><i>+</i><span>обучение в Москве или удалённо</span><i>+</i><span>12 месяцев поддержки</span><i>+</i><span>гарантия 24 месяца</span></div></div>'''

mid = f'''<section data-t="u-tdark" class="page cover midform" id="form-mid-sec">
  <div class="hgrid">
    <div>
      <div class="top"><b>Посмотреть вживую</b></div>
      <h2>Приезжайте на объект в Москве — покажем станок и монтаж</h2>
      <p class="lead">Или созвонимся по видео: покажем, как гнётся короб, ответим про ваш город, сроки и комплект.</p>
    </div>
    {form('form-mid', 'середина', 'Запросить консультацию', 'Перезвоним и договоримся о встрече или видеозвонке.', '<select name="topic"><option>Узнать цену комплекта</option><option>Хочу посмотреть станок вживую</option><option>Видеозвонок</option></select>')}
  </div>
</section>'''
end = f'''<section class="u-finalsec" id="form-end-sec"><div class="u-wrap">
  <div class="u-final">
    <div>
      <h2>Обсудим запуск в вашем городе</h2>
      <p class="u-lead">Вячеслав, продажи и запуск — звонок или MAX. Технические вопросы разбирает Сергей Попов — инженер-технолог, разработчик станка, в оконной отрасли с 1994 года.</p>
      <div class="u-btns"><a class="u-btn u-white" href="{TEL}">{PHONE}</a></div>
    </div>
    {form('form-bottom', 'низ', 'Получить консультацию', 'Оставьте телефон — перезвоним и ответим на вопросы.', '<input name="city" placeholder="Город"><textarea name="comment" rows="2" placeholder="Вопрос (необязательно)"></textarea>')}
  </div>
</div></section>'''

# middle form after section "10 · Монтаж" (index of section with id s10)
pos = next(i for i, x in enumerate(out) if 'id="s10"' in x) + 1
for i in range(1, len(out)):
    tone = 'u-tbg' if i % 2 else 'u-twh'
    if 'id="s16"' in out[i]: tone = 'u-tdark'
    out[i] = out[i].replace('<section ', f'<section data-t="{tone}" ', 1)
out.insert(pos, mid)
out.append(end)

body = '\n\n'.join(out)
body = re.sub(r'<div class="top"><b>(?:\d\d · )?([^<]*)</b><span>[^<]*</span></div>', lambda m: '<span class="u-eye">'+m.group(1)+'</span>', body)
body = re.sub(r'\{\{(\w+)\}\}', lambda m: f'img/{m.group(1)}.jpg', body)

def ty(t):
    for _ in range(2):
        t = re.sub(r'(?<![\wА-яЁё])([А-яЁёA-Za-z]{1,2}) (?=\S)', lambda m: m.group(1) + ' ', t)
    t = t.replace(' —', ' —').replace(' –', ' –')
    t = re.sub(r'(\d) (?=(₽|%|мм|см|м²|м|кг|В|дн|дней|дня|тыс|°C|раб|месяц|шт))', lambda m: m.group(1) + ' ', t)
    t = re.sub(r'(\d)–(\d)', lambda m: m.group(1) + '–⁠' + m.group(2), t)
    t = re.sub(r'\b(П|Г|W|3D|Z|U|L)-', lambda m: m.group(1) + '‑', t)
    return t
body = re.sub(r'>([^<]+)<', lambda m: '>' + ty(m.group(1)) + '<', body)

WEB = '''
html{scroll-behavior:smooth}
body{font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}
.page{width:100%;height:auto;min-height:0;padding:72px max(20px,calc((100% - 1160px)/2));overflow:visible;page-break-after:auto;display:flex;flex-direction:column}
.page:nth-of-type(even):not(.cover){background:#F6F6F6}
.page:nth-of-type(even):not(.cover) .card:not(.fill){background:#fff}
.top{margin-bottom:14px;font-size:12px;letter-spacing:.12em;text-transform:uppercase}
.top span{display:none}
h1{font-size:46px;max-width:none}h2{font-size:34px;max-width:920px;margin-bottom:12px}
.lead{font-size:18px;max-width:780px;margin-bottom:26px}
h3{font-size:17px}.small{font-size:14px}.k{font-size:13px}
body table{font-size:15px}td,th{padding:10px 12px}
.cap,.gal figcaption{font-size:13px;height:auto}
.grid{gap:16px}.card{border-radius:14px;padding:20px}
.num{font-size:34px}.num small{font-size:15px}
li{padding-left:18px;margin-top:6px}li:before{top:9px;width:7px;height:7px}
ul.tight li{font-size:15px}
.phwrap{height:auto;aspect-ratio:3/4}.imgcol .phwrap{flex:none;aspect-ratio:3/4}
img.ph{border-radius:14px}
.hero{flex:none;aspect-ratio:16/10;margin:18px 0}.hero img{border-radius:14px}
.mk{grid-template-rows:auto;margin-bottom:0}.mkcol{grid-auto-rows:auto}
.paygrid{grid-auto-rows:auto;margin-bottom:0}.ba div{aspect-ratio:3/4}
.galgrid{grid-auto-rows:auto;gap:18px 14px}.gal img{flex:none;aspect-ratio:4/3;border-radius:12px}
.strows{grid-auto-rows:auto;flex:none;gap:10px}.strow{padding:12px 16px;grid-template-columns:36px 1fr}
.facts,.facts.f4{margin:24px 0 0!important;padding:26px;gap:22px;border-radius:14px}.facts .fv{font-size:26px}.facts.f4 .fv{font-size:22px}.facts .fl{font-size:14px}
.cta{border-radius:14px}.cta.band{margin:26px 0 0;padding:24px}.cta.band .ph{font-size:26px}
.eq2{grid-auto-rows:auto}.eq .card{padding-bottom:20px}
svg.sec{height:110px}.bigsec{height:260px}
.note{margin-top:22px;font-size:14px}.days{gap:12px}.days b{font-size:16px}.days span{font-size:14px}
.sw{font-size:14px}.sw .chip{width:40px;height:40px}
.pb-lbl{font-size:14px}.pb-lbl span{font-size:13px}.pb-seg,.pb-bar{font-size:14px}
table.cmp td,table.cmp th{font-size:14px;padding:8px}
.cover h1{font-size:50px;margin-top:10px}.cover .lead{font-size:19px}
.hgrid{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
.hero1{padding-top:80px;padding-bottom:80px}
.h1grid{grid-template-areas:'t f';align-items:center}.h1grid .ht{grid-area:t}.h1grid .lform{grid-area:f;align-self:center}.h1grid .toc{grid-area:n;margin-top:0}
.toc{columns:2;column-gap:28px;margin-top:28px;font-size:15px}
.toc a{display:flex;gap:12px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.14);color:#fff;text-decoration:none;break-inside:avoid}
.toc a:hover{color:var(--or)}.toc a span{color:#9E9E9E;width:24px}
.midform h2{color:#fff}.midform .lead{color:#BDBDBD}.midform .ph{color:var(--or);font-weight:700;text-decoration:none;white-space:nowrap}
.lform{background:#fff;color:var(--ink);border-radius:16px;padding:22px;box-shadow:0 14px 40px rgba(0,0,0,.25)}
.lform h3{font-size:21px;color:var(--ink)}.lform p{font-size:14px;color:var(--muted);margin:4px 0 14px}
.lform input,.lform select,.lform textarea{width:100%;border:1.5px solid var(--line);border-radius:10px;padding:13px 14px;font:16px Onest,sans-serif;margin-bottom:10px;background:#fff;color:var(--ink)}
.lform input:focus,.lform select:focus,.lform textarea:focus{outline:none;border-color:var(--or)}
.btn{display:inline-flex;align-items:center;justify-content:center;background:var(--or);color:#fff;border:0;border-radius:12px;padding:15px 22px;font:600 16px Onest,sans-serif;cursor:pointer;text-decoration:none}
.btn:hover{filter:brightness(.93)}.lform .btn{width:100%}
.agree{font-size:12px;color:var(--muted);margin-top:10px}
.ok{display:none;text-align:center;padding:18px 0;font-size:15px}.ok b{display:block;font-size:20px;margin-bottom:6px}
.lform.sent .fields{display:none}.lform.sent .ok{display:block}
header.bar{position:sticky;top:0;z-index:20;background:rgba(22,22,22,.96);backdrop-filter:blur(6px);color:#fff}
header.bar .in{display:flex;align-items:center;justify-content:space-between;height:58px;padding:0 max(20px,calc((100% - 1160px)/2));gap:12px}
header.bar .logo{font-weight:700}header.bar .logo span{color:var(--or)}
header.bar .tel{color:#fff;font-weight:600;text-decoration:none;white-space:nowrap}
header.bar .btn{padding:9px 14px;font-size:14px;border-radius:10px}
.fab{display:none}
footer{background:#0E0E0E;color:#9A9A9A;font-size:13px;padding:28px max(20px,calc((100% - 1160px)/2))}footer b{color:#fff}
@media(max-width:860px){
  .page{padding:48px 16px}
  h1{font-size:32px}.cover h1{font-size:34px}h2{font-size:25px}.lead{font-size:16px;margin-bottom:20px}
  .hgrid,.g2,.g3,.g-img,.g-img2,.mk,.flow,.kv,.cta.band,.days{grid-template-columns:1fr!important}
  .hgrid{gap:28px}
  .h1grid{grid-template-areas:'t' 'f'}
  .grid[style*="grid-template-columns"]{grid-template-columns:1fr!important}
  .grid>*,.paygrid>*,.galgrid>*,.facts>*{min-width:0}
  td.r,th.r{white-space:normal}
  .g4,.paygrid,.galgrid,.facts,.facts.f4,.sws{grid-template-columns:1fr 1fr!important}
  .facts{padding:18px;gap:16px}.facts .fv,.facts.f4 .fv{font-size:19px}
  .toc{columns:1}
  .pb-row{grid-template-columns:1fr}.pb-axis,.pb-line{display:none}
  body table{font-size:14px}td,th{padding:8px 6px}
  .kv div:nth-child(odd){padding-bottom:0;border-bottom:0;font-size:13px}
  .hero{aspect-ratio:4/3}.phwrap,.imgcol .phwrap{aspect-ratio:4/3}
  header.bar .tel{display:none}
  .fab{position:fixed;left:16px;right:16px;bottom:14px;z-index:30;display:flex;gap:8px}
  .fab .btn{flex:1;box-shadow:0 8px 20px rgba(0,0,0,.25)}.fab .btn.t{flex:0 0 auto;background:#fff;color:var(--ink)}
  footer{padding-bottom:90px}
  .ba{grid-column:1/-1}
}

/* frontend-design pass */
.page .top{display:none}
.hero1{padding:0!important;min-height:calc(100vh - 58px)}
.h1grid{display:grid;align-items:stretch;grid-template-columns:minmax(0,1fr) minmax(0,1fr);grid-template-areas:'t p' 'f p';min-height:calc(100vh - 58px)}
.h1grid .ht{grid-area:t;padding:72px 48px 28px max(20px,calc((100vw - 1160px)/2));align-self:end}
.h1grid .lform{grid-area:f;margin:0 48px 72px max(20px,calc((100vw - 1160px)/2));align-self:start;max-width:460px}
.hpic{grid-area:p;position:relative;min-height:520px;align-self:stretch;height:100%}.hpic img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%}
.cover h1{font-size:54px;line-height:1.04;letter-spacing:-.025em;margin-top:0;max-width:640px}
.cover .lead{font-size:19px;max-width:560px;margin:20px 0 0}
h2{font-size:40px;line-height:1.08;letter-spacing:-.02em;max-width:880px;margin-bottom:16px}
.lead{max-width:680px}
.page{padding-top:96px;padding-bottom:96px}
.midform{padding-top:80px;padding-bottom:80px}
.lform{box-shadow:none;border-radius:18px}
.cover .lform{box-shadow:0 20px 60px rgba(0,0,0,.35)}

@media(max-width:860px){
  .hero1{min-height:0}
  .h1grid{grid-template-columns:1fr;grid-template-areas:'t' 'f' 'p';min-height:0}
  .h1grid .ht{padding:40px 16px 22px}
  .h1grid .lform{margin:0 16px 28px;max-width:none}
  .hpic{min-height:0;aspect-ratio:4/5}
  .cover h1{font-size:36px}.cover .lead{font-size:16px}
  h2{font-size:27px}
  .page{padding-top:56px;padding-bottom:56px}
}

/* ===== Утеплит DS 3.0 ===== */
:root{--u-bg:#F2F2F2;--u-card:#FFFFFF;--u-peach:#E3E3E3;--u-forest:#161616;--u-forest-2:#2E2E2E;--u-ink:#0E0E0E;--u-muted:#555555;--u-on-forest:#FFFFFF;--u-on-forest-muted:#BDBDBD;--u-action:#1A9BFC;--u-action-hover:#0B84E0;--u-sun:#1A9BFC;--u-line:#E3E3E3;--u-line-dark:#2E2E2E;--u-focus:#8F8F8F;
--u-fs-display:clamp(34px,4.2vw,52px);--u-fs-h2:clamp(30px,4vw,46px);--u-r-field:14px;--u-r-card:20px;--u-r-big:28px;--u-shadow-soft:0 1px 2px rgba(14,14,14,.04),0 10px 30px rgba(14,14,14,.06);--u-shadow-float:0 8px 24px rgba(14,14,14,.12);--u-gutter:16px;--u-section:64px;--u-inset:20px;
--or:var(--u-action);--dark:var(--u-forest);--accent:var(--u-forest);--ink:var(--u-ink);--muted:var(--u-muted);--line:var(--u-line)}
@media(min-width:768px){:root{--u-gutter:32px;--u-inset:24px}}@media(min-width:1024px){:root{--u-section:96px}}
body{background:var(--u-bg);color:var(--u-ink);font-size:15px}
.u-wrap{max-width:1200px;margin:0 auto;padding:0 var(--u-gutter)}
.page{padding:var(--u-section) max(var(--u-gutter),calc((100% - 1200px)/2 + var(--u-gutter)))!important;background:var(--u-bg)}
.page[data-t=u-twh]{background:#fff}
.page:nth-of-type(even):not(.cover){background:inherit}
.page[data-t=u-twh]{background:#fff!important}.page[data-t=u-tbg]{background:var(--u-bg)!important}
.page[data-t=u-tdark]{background:var(--u-forest)!important;color:#fff}
.page[data-t=u-tdark] h2,.page[data-t=u-tdark] h3{color:#fff}.page[data-t=u-tdark] .lead,.page[data-t=u-tdark] .muted{color:var(--u-on-forest-muted)}
.page[data-t=u-tdark] .card{background:transparent!important;border:1px solid var(--u-line-dark);color:#fff}.page[data-t=u-tdark] .card .k{color:var(--u-sun);font-size:28px;font-weight:600}
.u-eye{display:inline-block;align-self:flex-start;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:var(--u-peach);color:var(--u-ink);border-radius:999px;padding:6px 12px;margin-bottom:16px}
.page[data-t=u-tdark] .u-eye{background:var(--u-forest-2);color:#fff}
h2{font-size:var(--u-fs-h2);font-weight:600;line-height:1.08;letter-spacing:-.03em;max-width:24ch;margin-bottom:16px}
.lead{font-size:17px;line-height:1.6;max-width:56ch;margin-bottom:40px}
h3{font-weight:600;letter-spacing:-.01em}
/* cards: white on gray with soft shadow; on white — line, no shadow */
.card{border-radius:var(--u-r-card);padding:var(--u-inset)}
.page[data-t=u-tbg] .card:not(.fill){background:#fff;border-color:transparent;box-shadow:var(--u-shadow-soft)}
.page[data-t=u-twh] .card:not(.fill){background:#fff;border:1px solid var(--u-line);box-shadow:none}
.card.fill,.facts,.cta,.days div{background:var(--u-forest)!important;border-radius:var(--u-r-card)}
.facts .fv,.cta.band .ph,.days b,.card.fill .num{color:var(--u-sun)}
img.ph,.hero img,.ba img{border-radius:var(--u-r-big)}.gal img{border-radius:var(--u-r-card)}
li:before{background:var(--u-forest)}
.k{color:var(--u-action)}
/* buttons */
.u-btn,.lform .btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:52px;padding:0 24px;border-radius:999px;background:var(--u-action);color:#fff;font:600 15px Onest,system-ui,sans-serif;text-decoration:none;border:0;cursor:pointer;transition:background .15s,transform .12s;white-space:nowrap}
.u-btn:hover,.lform .btn:hover{background:var(--u-action-hover);filter:none}.u-btn:active,.lform .btn:active{transform:scale(.98)}
.u-btn.u-out{background:transparent;color:var(--u-ink);box-shadow:inset 0 0 0 1.5px var(--u-ink)}.u-btn.u-out:hover{background:var(--u-ink);color:#fff}
.u-btn.u-white{background:#fff;color:var(--u-ink)}.u-btn.u-white:hover{background:#E3E3E3}
.u-btn.u-sm{height:44px;padding:0 18px;font-size:14px}
:focus-visible{outline:3px solid var(--u-focus);outline-offset:3px}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
/* header */
header.bar{background:rgba(242,242,242,.92);color:var(--u-ink);backdrop-filter:blur(8px);border-bottom:1px solid var(--u-line)}
header.bar .in{height:60px;max-width:1200px;margin:0 auto;padding:0 var(--u-gutter)}
@media(min-width:768px){header.bar .in{height:72px}}
header.bar .logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:17px}header.bar .logo i{width:28px;height:28px;border-radius:8px;background:var(--u-forest);display:block}
header.bar .tel{color:var(--u-ink)}
/* hero */
.u-hero{background:var(--u-bg);padding:40px 0 var(--u-section)}
.u-hgrid{display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:center}
.u-chip{display:inline-block;background:#fff;border:1px solid var(--u-line);border-radius:999px;padding:6px 14px;font-size:13px;font-weight:500;margin-bottom:20px}
.u-hero h1{font-size:var(--u-fs-display);font-weight:600;line-height:1.02;letter-spacing:-.035em;color:var(--u-ink);max-width:none;text-wrap:balance}
@media(min-width:1200px){.u-hero h1 .ln{display:block;white-space:nowrap}}
.u-lead{font-size:17px;line-height:1.6;color:var(--u-muted);max-width:52ch;margin-top:20px}
.u-btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:32px}
.u-hpic{position:relative;border-radius:var(--u-r-big);aspect-ratio:4/5;max-height:680px}
.u-hpic img{width:100%;height:100%;object-fit:cover;object-position:50% 60%;border-radius:var(--u-r-big);display:block}
.u-fl{position:absolute;background:#fff;border-radius:var(--u-r-field);padding:12px 16px;box-shadow:var(--u-shadow-float);font-size:13px;color:var(--u-muted);line-height:1.3}
.u-fl b{display:block;color:var(--u-ink);font-size:17px;font-weight:600}
.u-fl1{left:-12px;top:12%;background:var(--u-action);color:#E3F2FF}.u-fl1 b{color:#fff;font-size:20px}
.u-fl2{right:-12px;top:46%}
.u-fl3{left:-12px;bottom:10%;background:var(--u-forest);color:var(--u-on-forest-muted)}.u-fl3 b{color:#fff}
.u-ill{position:absolute;right:14px;bottom:12px;font-size:11px;color:#fff;background:rgba(14,14,14,.45);padding:2px 8px;border-radius:999px}
/* form panel (DS «панель проверки города») */
.lform{border-radius:var(--u-r-big);box-shadow:var(--u-shadow-soft)!important;padding:24px}
.lform input,.lform select,.lform textarea{height:48px;border-radius:var(--u-r-field);border:1px solid var(--u-line);background:var(--u-bg);font-size:16px}
.lform textarea{height:auto}
.u-panel{margin-top:40px}
.u-panel .fields{display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr auto;gap:12px;align-items:center}
.u-panel h3{grid-column:1/-1;margin:0}.u-panel p{grid-column:1/-1;margin:-6px 0 4px}
.u-panel input{margin:0}.u-panel .btn{width:auto;margin:0}.u-panel .agree{grid-column:1/-1;margin-top:0}
.u-panel .fields>h3+p+input{grid-column:1}
/* trust ribbon */
.u-trust{background:var(--u-forest);color:#fff;font-weight:600;font-size:14px}
.u-trust .u-wrap{display:flex;gap:14px;align-items:center;padding-top:18px;padding-bottom:18px;overflow-x:auto;white-space:nowrap;scrollbar-width:none}
.u-trust i{color:var(--u-sun);font-style:normal}
/* mid form & final */
.midform .lform{box-shadow:none!important}
.u-finalsec{background:var(--u-bg);padding:var(--u-section) 0}
.u-final{background:var(--u-forest);color:#fff;border-radius:var(--u-r-big);padding:48px;display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.u-final h2{color:#fff}.u-final .u-lead{color:var(--u-on-forest-muted)}
footer{background:var(--u-bg);color:var(--u-muted);border-top:1px solid var(--u-line)}footer b{color:var(--u-ink)}
.fab .u-btn{flex:1;box-shadow:var(--u-shadow-float)}
.fab{transition:opacity .15s}.fab.off{opacity:0;pointer-events:none}
.grid>*,.paygrid>*,.mk>*{min-width:0}
@media(max-width:1180px){.mk{grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important}.paygrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:959px){.u-hgrid,.u-final{grid-template-columns:1fr}.u-hpic{aspect-ratio:4/5;max-height:none}.u-final{padding:28px 20px;gap:28px}}
@media(max-width:860px){
  .u-panel .fields{grid-template-columns:1fr}.u-panel .btn{width:100%}
  .u-btns .u-btn{width:100%}
  .u-fl1,.u-fl3{left:8px}.u-fl2{right:8px}
  .page{padding:var(--u-section) var(--u-gutter)!important}
  .lead{margin-bottom:32px}
  table.cmp td,table.cmp th{font-size:12.5px;padding:6px 4px;word-break:break-word;hyphens:auto}
}
'''
JS = '''<script>
// Адрес для заявок: веб-приложение Google Apps Script (см. README) — заявки попадут в таблицу «Заявки».
const FORM_ENDPOINT='';
document.querySelectorAll('input[type=tel]').forEach(i=>i.addEventListener('input',()=>{let d=i.value.replace(/\\D/g,'');if(d.startsWith('8'))d='7'+d.slice(1);if(!d.startsWith('7'))d='7'+d;d=d.slice(0,11);let s='+7';if(d.length>1)s+=' ('+d.slice(1,4);if(d.length>=4)s+=') '+d.slice(4,7);if(d.length>=7)s+='-'+d.slice(7,9);if(d.length>=9)s+='-'+d.slice(9,11);i.value=s;}));
document.querySelectorAll('form.lform').forEach(f=>f.addEventListener('submit',async e=>{e.preventDefault();
 const data=Object.fromEntries(new FormData(f));data.place=f.dataset.place;data.page=location.href;data.ts=new Date().toISOString();
 if((data.phone||'').replace(/\\D/g,'').length<11){f.querySelector('input[type=tel]').focus();return}
 const b=f.querySelector('button');b.disabled=true;b.textContent='Отправляем…';
 try{if(FORM_ENDPOINT)await fetch(FORM_ENDPOINT,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify(data)})}catch(err){}
 f.classList.add('sent');}));
const fab=document.querySelector('.fab'),vis=new Set();
const io=new IntersectionObserver(es=>{es.forEach(e=>e.isIntersecting?vis.add(e.target):vis.delete(e.target));upd()},{threshold:.1});
document.querySelectorAll('form.lform').forEach(f=>io.observe(f));
const hero=document.querySelector('.u-hero');function upd(){fab.classList.toggle('off',vis.size>0||hero.getBoundingClientRect().bottom>0)}
addEventListener('scroll',upd,{passive:true});upd();
</script>'''
css = css.replace('@page{size:297mm 210mm;margin:0}', '')
html = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Оконщик 3000 — свой бизнес на утеплении панорамных окон, балконов и лоджий</title>
<meta name="description" content="Станок для бесшовных термокоробов и 3D-откосов из ПВХ-сэндвича 10 мм. Комплект, обучение и год поддержки. Без роялти и паушального взноса.">
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}{WEB}</style></head>
<body>
<header class="bar"><div class="in"><div class="logo"><i></i>Оконщик 3000</div><div style="display:flex;align-items:center;gap:14px"><a class="tel" href="{TEL}">{PHONE}</a><a class="u-btn u-sm" href="#form-top">Консультация</a></div></div></header>
{body}
<footer><b>Оконщик 3000</b> · оборудование и технология бесшовных термокоробов<br>Исполнитель по договору — ООО «Меркурий-групп», ИНН 5916035699 · {PHONE}</footer>
<div class="fab"><a class="u-btn" href="#form-bottom">Получить консультацию</a></div>
{JS}
</body></html>'''
open(D + '/landing/index.html', 'w').write(html)
one = re.sub(r'src="img/(\w+)\.jpg"', lambda m: 'src="data:image/jpeg;base64,' + base64.b64encode(open(D + '/landing/img/' + m.group(1) + '.jpg', 'rb').read()).decode() + '"', html)
open(D + '/landing/Оконщик_3000_лендинг_один_файл.html', 'w').write(one)
print('sections', len(out), 'size KB', round(len(one) / 1024))
