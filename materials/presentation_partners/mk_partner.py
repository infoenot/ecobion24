import re
s=open('deck.norm.html').read()
head=s[:s.index('<section')]; tail=s[s.rindex('</section>')+10:]
secs=re.findall(r'<section class="page[^"]*".*?</section>',s,re.S)
S={i+1:x for i,x in enumerate(secs)}
def R(x,a,b):
    assert a in x,(a[:70]); return x.replace(a,b,1)
BR='Бесшовные термокороба'
cover='''<section class="page cover">
  <div class="top"><b>Бесшовные термокороба</b><span>Технология и изделия · для дизайнеров и прорабов</span></div>
  <h1><span style="display:block;white-space:nowrap">Утеплим холодные</span><span class="or" style="display:block;white-space:nowrap">панорамные окна, балконы</span><span style="display:block;white-space:nowrap"><span class="or">и лоджии</span> изнутри</span></h1>
  <p class="lead">Что предложить заказчику, у которого холодные алюминиевые стойки: как устроено решение, какие изделия и отделки есть, как это выглядит в интерьере и как проходит заказ.</p>
  <div class="toc">
    <div><span>01</span>Проблема заказчика</div>
    <div><span>02</span>Семь задач, которые решает один заказ</div>
    <div><span>03</span>Что такое термокороб и 3D-термооткос</div>
    <div><span>04</span>Как устроен узел на стойке</div>
    <div><span>05</span>Профили для окон, дверей и интерьера</div>
    <div><span>06</span>Подоконники</div>
    <div><span>07</span>Отделка: белый, RAL, плёнка</div>
    <div><span>08</span>Галерея</div>
    <div><span>09</span>Как проходит заказ</div>
  </div>
</section>'''
p2=R(S[2],'<b>01 · Рынок</b>','<b>01 · Проблема заказчика</b>')
a=p2.index('<div class="facts f4">'); b=p2.index('<div class="foot">',a)
p2=p2[:a]+'<div class="facts f4"><div><div class="fv">800+ RAL</div><div class="fl">и 200+ плёнок под интерьер</div></div><div><div class="fv">до 10 мм</div><div class="fl">на столько максимум уменьшается проём</div></div><div><div class="fv">1–3 дня</div><div class="fl">установка на объекте</div></div><div><div class="fv">без сверления</div><div class="fl">профиль окна не повреждают</div></div></div>\n  '+p2[b:]
p4=R(S[4],'<b>03 · За что платит клиент</b>','<b>02 · Что получает заказчик</b>')
p4=R(p4,'<h2>Клиент платит не за пластик, а за решение семи задач</h2>','<h2>Один заказ решает для заказчика семь задач</h2>')
p4,n=re.subn(r'<div class="ph">3–7 дней</div>\s*<p class="muted small">от замера до монтажа[^<]*</p>','<div class="ph">1–3 дня</div>\n    <p class="muted small">установка на объекте после бесплатного замера</p>',p4); assert n==1
p5=R(S[5],'<b>04 · Решение</b>','<b>03 · Решение</b>')
p11=R(S[11],'<b>10 · Монтаж</b>','<b>04 · Как устроен узел</b>')
p11=R(p11,'Ей учим на объектах и разбираем сложные узлы по фото.','Её подбирают на замере, после осмотра стоек и примыканий.')
p12=R(S[12],'<b>11 · Изделия</b>','<b>05 · Изделия</b>')
p12=R(p12,'<h2>Кроме утепления, на станке делают профили для окон, дверей и интерьера</h2>','<h2>Кроме утепления — профили для окон, дверей и интерьера в одном стиле</h2>')
p12,n=re.subn(r'<p class="lead" style="margin-bottom:5mm">Всё — из того же листа.*?</p>','<p class="lead" style="margin-bottom:5mm">Всё — из одного материала, ПВХ-сэндвича 10 мм, и в одной отделке с коробами. Ниже — схемы сечений.</p>',p12,flags=re.S); assert n==1
p13=R(S[13],'<b>11 · Изделия</b>','<b>06 · Подоконники</b>')
p14=R(S[14],'<b>11 · Изделия</b>','<b>07 · Отделка</b>')
gal=[]
for k in (15,16,17):
    g=R(S[k],'<b>11 · Изделия: галерея</b>','<b>08 · Галерея</b>')
    g=g.replace('Что можно сделать на станке','Что можно сделать'); assert 'станк' not in g; gal.append(g)
last=open('../partner_last.html').read()
pages=[cover,p2,p4,p5,p11,p12,p13,p14]+gal+[last]
out=[]
for n,pg in enumerate(pages,1):
    pg=pg.replace('<span>Оконщик 3000</span></div>','<span>'+BR+'</span></div>')
    pg=re.sub(r'<div class="foot"><span>[^<]*</span><span>\d+</span></div>',f'<div class="foot"><span>Бесшовные термокороба · технология и изделия</span><span>{n}</span></div>',pg)
    out.append(pg)
html=head+'\n\n'.join(out)+tail
html=re.sub(r'<title>[^<]*</title>','<title>Бесшовные термокороба</title>',html)
def ty(t):
    for _ in range(2): t=re.sub(r'(?<![\wА-яЁё])([А-яЁёA-Za-z]{1,2}) (?=\S)',lambda m:m.group(1)+'\u00a0',t)
    t=t.replace(' —','\u00a0—').replace(' –','\u00a0–')
    t=re.sub(r'(\d) (?=(₽|%|мм|см|м²|м|кг|В|дн|дней|дня|тыс|°C))',lambda m:m.group(1)+'\u00a0',t)
    t=re.sub(r'(\d)–(\d)',lambda m:m.group(1)+'–\u2060'+m.group(2),t)
    t=re.sub(r'\b(П|Г|W|3D|Z|U|L)-',lambda m:m.group(1)+'\u2011',t)
    return t
st=html.index('</style>')
body=re.sub(r'>([^<]+)<',lambda m:'>'+ty(m.group(1))+'<',html[st:])
full=html[:st]+body
PAL={'#F26B1D':'#1A9BFC','#202531':'#262626','#0A0E15':'#111111','#4E5766':'#555555','#E0E4EB':'#E3E3E3','#F0F1F5':'#F2F2F2','#C9CED8':'#CCCCCC','#B9C0CC':'#BDBDBD','#C3C9D3':'#C8C8C8','#5B6576':'#5E5E5E','#8A93A3':'#8F8F8F','rgba(32,37,49':'rgba(38,38,38'}
for a,b in PAL.items(): full=full.replace(a,b).replace(a.lower(),b)
open('partner.tpl.html','w').write(full)
low=body.lower(); print(len(pages),'станок' in low,'окупаем' in low,'цен' in low)
