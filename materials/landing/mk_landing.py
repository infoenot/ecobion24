import re, base64, os
D = os.path.dirname(os.path.abspath(__file__))
s = open(D + '/pres/deck.norm.html').read()
css = s[s.index('<style>') + 7:s.index('</style>')]
secs = re.findall(r'<section class="page[^"]*".*?</section>', s, re.S)

PHONE = '+7 921 950-38-60'
TEL = 'tel:+79219503860'

def form(fid, place, title, sub, extra=''):
    return f'''<form class="lform" id="{fid}" data-place="{place}">
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
out[0] = f'''<section class="page cover hero1">
  <div class="h1grid">
    <div class="ht">
      {h1}
      {lead}
    </div>
    {form('form-top', 'первый экран', 'Получите консультацию', 'Перезвоним, разберём ваш город и ответим на вопросы по станку.', '<input name="city" placeholder="Город">')}
    <div class="hpic"><img src="img/hero.jpg" alt="Лоджия: белые короба на стойках панорамного остекления"></div>
  </div>
</section>'''

mid = f'''<section class="page cover midform" id="form-mid-sec">
  <div class="hgrid">
    <div>
      <div class="top"><b>Посмотреть вживую</b></div>
      <h2>Приезжайте на объект в Москве — покажем станок и монтаж</h2>
      <p class="lead">Или созвонимся по видео: покажем, как гнётся короб, ответим про ваш город, сроки и комплект.</p>
    </div>
    {form('form-mid', 'середина', 'Запросить консультацию', 'Перезвоним и договоримся о встрече или видеозвонке.', '<select name="topic"><option>Хочу посмотреть станок вживую</option><option>Видеозвонок</option><option>Вопрос по комплекту и цене</option></select>')}
  </div>
</section>'''
end = f'''<section class="page cover midform" id="form-end-sec">
  <div class="hgrid">
    <div>
      <div class="top"><b>Заявка</b></div>
      <h2>Получите консультацию по станку и запуску в вашем городе</h2>
      <p class="lead">Вячеслав, продажи и запуск — звонок или MAX: <a href="{TEL}" class="ph">{PHONE}</a></p>
      <p class="lead small">Технические вопросы разбирает Сергей Попов — инженер-технолог, разработчик станка, в оконной отрасли с 1994 года.</p>
    </div>
    {form('form-bottom', 'низ', 'Получите консультацию', 'Оставьте телефон — перезвоним и ответим на вопросы.', '<input name="city" placeholder="Город"><textarea name="comment" rows="2" placeholder="Вопрос (необязательно)"></textarea>')}
  </div>
</section>'''

# middle form after section "10 · Монтаж" (index of section with id s10)
pos = next(i for i, x in enumerate(out) if 'id="s10"' in x) + 1
out.insert(pos, mid)
out.append(end)

body = '\n\n'.join(out)
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
const io=new IntersectionObserver(es=>{es.forEach(e=>e.isIntersecting?vis.add(e.target):vis.delete(e.target));fab.style.visibility=vis.size?'hidden':'visible'},{threshold:.1});
document.querySelectorAll('form.lform').forEach(f=>io.observe(f));
</script>'''
css = css.replace('@page{size:297mm 210mm;margin:0}', '')
html = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Станок «Оконщик 3000» — оборудование и технология бесшовных термокоробов</title>
<meta name="description" content="Станок для бесшовных термокоробов и 3D-откосов из ПВХ-сэндвича 10 мм. Комплект 450 000 ₽ без НДС, обучение и год поддержки. Без роялти и паушального взноса.">
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}{WEB}</style></head>
<body>
<header class="bar"><div class="in"><div class="logo">Оконщик <span>3000</span></div><div style="display:flex;align-items:center;gap:14px"><a class="tel" href="{TEL}">{PHONE}</a><a class="btn" href="#form-top">Консультация</a></div></div></header>
{body}
<footer><b>Оконщик 3000</b> · оборудование и технология бесшовных термокоробов<br>Исполнитель по договору — ООО «Меркурий-групп», ИНН 5916035699 · {PHONE}</footer>
<div class="fab"><a class="btn t" href="{TEL}">Позвонить</a><a class="btn" href="#form-bottom">Получить консультацию</a></div>
{JS}
</body></html>'''
open(D + '/landing/index.html', 'w').write(html)
one = re.sub(r'src="img/(\w+)\.jpg"', lambda m: 'src="data:image/jpeg;base64,' + base64.b64encode(open(D + '/landing/img/' + m.group(1) + '.jpg', 'rb').read()).decode() + '"', html)
open(D + '/landing/Оконщик_3000_лендинг_один_файл.html', 'w').write(one)
print('sections', len(out), 'size KB', round(len(one) / 1024))
