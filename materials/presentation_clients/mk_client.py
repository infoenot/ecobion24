import re
s=open('pres/deck.norm.html').read()
head=s[:s.index('<section')]; tail=s[s.rindex('</section>')+10:]
secs=re.findall(r'<section class="page[^"]*".*?</section>',s,re.S); S={i+1:x for i,x in enumerate(secs)}
def R(x,a,b):
    assert a in x,(a[:70]); return x.replace(a,b,1)
BR='Тёплые окна в пол'
CSS='''<style>
.cvr{display:grid;grid-template-columns:1.05fr 1fr;gap:0;padding:0!important}
.cvr .l{padding:16mm 14mm 14mm 18mm;display:flex;flex-direction:column}
.cvr .r{position:relative;overflow:hidden}.cvr .r img{width:100%;height:100%;object-fit:cover;object-position:50% 70%}
.cvr h1{font-size:30pt;margin-top:22mm;line-height:1.1}
.cvr .sub{color:#BDBDBD;font-size:13pt;margin-top:4mm}
.cvr .chips{margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.cvr .chips div{border:1px solid rgba(255,255,255,.18);border-radius:2.5mm;padding:3mm 4mm;font-size:10.5pt}
.cvr .chips b{display:block;color:var(--or);font-size:15pt}
.pg8{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:62mm;gap:5mm 4mm;margin-top:3mm}
.pg8 figure{margin:0;display:flex;flex-direction:column;min-height:0}
.pg8 img{width:100%;flex:1;min-height:0;object-fit:cover;border-radius:2.5mm}
.pg8 figcaption{font-size:9pt;margin-top:1.8mm;color:var(--muted)}
.pg3{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;flex:1;min-height:0;margin-top:3mm}
.pg3 figure{margin:0;display:flex;flex-direction:column;min-height:0}.pg3 img{width:100%;flex:1;min-height:0;object-fit:cover;border-radius:3mm}
.pg3 figcaption{font-size:10pt;margin-top:2mm}
.two{display:grid;grid-template-columns:1fr 1.15fr;gap:8mm;flex:1;min-height:0}
.two .pimg{border-radius:3mm;overflow:hidden;min-height:0}.two .pimg img{width:100%;height:100%;object-fit:cover;object-position:55% 50%;display:block}
</style>'''
head=head.replace('</head>',CSS+'</head>')
cover='''<section class="page cover cvr">
  <div class="l">
    <div class="top"><b>Тёплые окна в пол</b><span>для собственников квартир</span></div>
    <h1><span style="display:block;white-space:nowrap">Утеплим холодные</span><span class="or" style="display:block;white-space:nowrap">панорамные окна,</span><span class="or" style="display:block;white-space:nowrap">балконы и лоджии</span><span style="display:block;white-space:nowrap">изнутри</span></h1>
    <div class="sub">в вашем жилом комплексе</div>
    <div class="chips"><div><b>Бесплатно</b>замер и расчёт</div><div><b>1–3 дня</b>установка</div><div><b>Без сверления</b>профиль окна целый</div><div><b>800+ RAL</b>и 200+ плёнок</div></div>
  </div>
  <div class="r"><img src="{{cover}}"></div>
</section>'''
p2=R(S[2],'<b>01 · Рынок</b>','<b>01 · Знакомая ситуация</b>')
p2=R(p2,'<h2>Владелец квартиры с панорамными окнами хочет, чтобы у окна было','<h2>Окна в пол — это красиво. Но у окна должно быть')
a=p2.index('<div class="facts f4">'); b=p2.index('<div class="foot">',a)
p2=p2[:a]+'<div class="facts f4"><div><div class="fv">бесплатно</div><div class="fl">замер и расчёт стоимости</div></div><div><div class="fv">1–3 дня</div><div class="fl">установка в квартире</div></div><div><div class="fv">без сверления</div><div class="fl">профиль окна не повреждаем</div></div><div><div class="fv">до 10 мм</div><div class="fl">максимум меньше становится проём</div></div></div>\n  '+p2[b:]
p2=p2.replace('<div class="k">Почему обычный ремонт не помогает</div>','<div class="k">Почему обычный ремонт не помогает</div>')
T=[('Проблема: слышно соседей','Тихо','Полые стойки проходят через этажи и передают звук. Пустоты заполняем, стойку закрываем.'),
('Проблема: профиль застройщика','Красиво','Короба белые, в цвет по RAL или под дерево. Царапины и следы стройки скрыты.'),
('Проблема: лоджия как склад','Уютно','Ровные поверхности без щелей и самодельных стыков. Лоджия становится частью квартиры.'),
('Проблема: холодные стойки','Тепло','Утеплитель и короб закрывают холодный металл. У окна можно поставить стол или кресло.'),
('Проблема: конденсат','Сухо','Металл закрываем бутиловой лентой или жидкой резиной. На этом слое конденсат не образуется.'),
('Проблема: метры пустуют','Больше площадь','Вместе с утеплением пола и потолка лоджия становится кабинетом или детским уголком.'),
('Проблема: квартира под сдачу','Дороже аренда','Аккуратные окна хорошо смотрятся на фото в объявлении.')]
cards=''.join(f'<div class="card col pay"><div class="k">{k}</div><div><h3>{h}</h3><p>{t}</p></div></div>' for k,h,t in T)
p4=f'''<section class="page">
  <div class="top"><b>02 · Что вы получите</b><span>{BR}</span></div>
  <h2>Один заказ решает семь задач</h2>
  <p class="lead" style="margin-bottom:4mm">Стойки несущие — их не меняют. Мы утепляем их изнутри квартиры и закрываем бесшовными коробами по размеру.</p>
  <div class="paygrid">{cards}
    <div class="ba"><div><img src="{{{{before}}}}"><span>До</span></div><div><img src="{{{{after}}}}"><span>После</span></div></div>
  </div>
  <div class="cta band">
    <div><h3 style="font-size:14pt">Выезд замерщика — бесплатно</h3><p class="muted">посмотрим окна и рассчитаем стоимость</p></div>
    <div class="ph">1–3 дня</div>
    <p class="muted small">установка в квартире</p>
  </div>
  <div class="foot"><span>x</span><span>0</span></div>
</section>'''
how=f'''<section class="page">
  <div class="top"><b>03 · Как мы это делаем</b><span>{BR}</span></div>
  <div class="two">
    <div style="display:flex;flex-direction:column">
      <h2>Короб делаем по замеру каждой стойки и ставим за 1–3 дня</h2>
      <p class="lead" style="margin-bottom:5mm">Стойку закрываем от влаги, утепляем и надеваем короб из ПВХ-панели 10 мм с утеплителем внутри. Остекление не меняем.</p>
      <div class="strows">
        <div class="card strow"><div class="k">01</div><div><h3>Бесплатный замер</h3><p class="small muted">Приезжаем, меряем каждую стойку, называем стоимость и срок.</p></div></div>
        <div class="card strow"><div class="k">02</div><div><h3>Выбор отделки</h3><p class="small muted">Белый, 800+ цветов RAL или 200+ плёнок под дерево — в тон вашему интерьеру.</p></div></div>
        <div class="card strow"><div class="k">03</div><div><h3>Изготовление</h3><p class="small muted">Гнём короба из цельной полосы: на внешнем ребре нет стыка.</p></div></div>
        <div class="card strow"><div class="k">04</div><div><h3>Установка за 1–3 дня</h3><p class="small muted">Сажаем короб на клей. Без сверления профиля, без шума и пыли.</p></div></div>
      </div>
    </div>
    <div class="pimg"><img src="{{{{n_portal}}}}"></div>
  </div>
  <div class="foot"><span>x</span><span>0</span></div>
</section>'''
prods=[('g02','Портал балконного блока и 3D-откосы под дуб'),('g06','Откосы входной двери под дуб'),('g11','Подоконник с боковинами вокруг радиатора'),('g12','Ниша под телевизор под орех'),('g17','Портал проёма без двери'),('g18','Реечная стена из П-профилей'),('g24','Фальшбалки под светлый дуб'),('g23','Рама для большого зеркала')]
figs=''.join(f'<figure><img src="{{{{{k}}}}}"><figcaption>{c}</figcaption></figure>' for k,c in prods)
pr=f'''<section class="page">
  <div class="top"><b>04 · Что ещё можно сделать</b><span>{BR}</span></div>
  <h2>Откосы, подоконники, порталы и рамы — в одном стиле с коробами</h2>
  <div class="pg8">{figs}</div>
  <div class="foot"><span>x</span><span>0</span></div>
</section>'''
fin=R(S[14],'<b>11 · Изделия</b>','<b>05 · Отделка</b>')
fin=fin.replace('Примеры готовых изделий в разной отделке — в галерее на следующих страницах.','Образцы покажем на замере.')
g1=f'''<section class="page">
  <div class="top"><b>06 · Как это выглядит</b><span>{BR}</span></div>
  <h2>Окна в пол становятся частью интерьера</h2>
  <div class="pg3"><figure><img src="{{{{n_erker}}}}"><figcaption>Эркер: белые короба на стойках</figcaption></figure><figure><img src="{{{{n_oak}}}}"><figcaption>Короба под светлый дуб</figcaption></figure><figure><img src="{{{{n_bedroom}}}}"><figcaption>Спальня: окна до пола, белые короба</figcaption></figure></div>
  <div class="foot"><span>x</span><span>0</span></div>
</section>'''
gl=[('g04','Лоджия: белые короба на стойках и ригелях'),('g03','Подоконник под дуб на ригеле'),('g01','Подоконник-столешница вдоль окна'),('g14','Графитовые короба на стойках'),('g05','Эркер: короба на стойках граней'),('g09','Лоджия: белые короба'),('g13','Откосы, порог и плинтус балконной двери'),('g19','Портал выхода на лоджию под дуб')]
figs=''.join(f'<figure><img src="{{{{{k}}}}}"><figcaption>{c}</figcaption></figure>' for k,c in gl)
g2=f'''<section class="page">
  <div class="top"><b>06 · Как это выглядит</b><span>{BR}</span></div>
  <h2>Белые, цветные и под дерево — под любой интерьер</h2>
  <div class="pg8">{figs}</div>
  <div class="foot"><span>x</span><span>0</span></div>
</section>'''
last=f'''<section class="page">
  <div class="top"><b>07 · Как заказать</b><span>{BR}</span></div>
  <h2>Замерщик приедет бесплатно</h2>
  <p class="lead" style="margin-bottom:6mm">Стоимость считаем на месте: она зависит от размеров остекления, количества стоек и отделки.</p>
  <div class="grid g3" style="gap:5mm">
    <div class="card col"><div class="k">01</div><h3>Позвоните или напишите</h3><p class="small muted">Расскажите, что хотите сделать: лоджия, балкон или окна в пол.</p></div>
    <div class="card col"><div class="k">02</div><h3>Замер в удобное время</h3><p class="small muted">Меряем каждую стойку, отвечаем на вопросы, называем стоимость и срок.</p></div>
    <div class="card col"><div class="k">03</div><h3>Договор и установка</h3><p class="small muted">Фиксируем стоимость и сроки в договоре. Установка за 1–3 дня.</p></div>
  </div>
  <div class="pg3" style="margin:6mm 0 6mm"><figure><img src="{{{{g08}}}}"></figure><figure><img src="{{{{n_bedroom}}}}"></figure><figure><img src="{{{{g07}}}}"></figure></div>
  <div class="cta band">
    <div><h3 style="font-size:16pt">Бесплатный замер и расчёт</h3><p class="muted">звонок или MAX</p></div>
    <div class="ph">+7 921 950-38-60</div>
    <p class="muted small">Нужна ли замена стеклопакетов, специалист скажет на замере.</p>
  </div>
  <div class="foot"><span>x</span><span>0</span></div>
</section>'''
pages=[cover,p2,p4,how,pr,fin,g1,g2,last]
out=[]
for n,pg in enumerate(pages,1):
    pg=pg.replace('<span>Оконщик 3000</span></div>','<span>'+BR+'</span></div>')
    pg=re.sub(r'<div class="foot"><span>[^<]*</span><span>\d+</span></div>',f'<div class="foot"><span>Тёплые окна в пол · для собственников</span><span>{n}</span></div>',pg)
    out.append(pg)
html=head+'\n\n'.join(out)+tail
html=re.sub(r'<title>[^<]*</title>','<title>Тёплые окна в пол</title>',html)
def ty(t):
    for _ in range(2): t=re.sub(r'(?<![\wА-яЁё])([А-яЁёA-Za-z]{1,2}) (?=\S)',lambda m:m.group(1)+' ',t)
    t=t.replace(' —',' —').replace(' –',' –')
    t=re.sub(r'(\d) (?=(₽|%|мм|см|м²|м|кг|В|дн|дней|дня|тыс|°C))',lambda m:m.group(1)+' ',t)
    t=re.sub(r'(\d)–(\d)',lambda m:m.group(1)+'–⁠'+m.group(2),t)
    t=re.sub(r'\b(П|Г|W|3D|Z|U|L)-',lambda m:m.group(1)+'‑',t)
    return t
st=html.index('</style>')
full=html[:st]+re.sub(r'>([^<]+)<',lambda m:'>'+ty(m.group(1))+'<',html[st:])
PAL={'#F26B1D':'#D2622B','#202531':'#2B2725','#0A0E15':'#1C1917','#4E5766':'#6B635C','#E0E4EB':'#E6DDD2','#F0F1F5':'#F6F0E7','#C9CED8':'#D8CFC4','#B9C0CC':'#C9BFB3','#C3C9D3':'#D1C7BB','#5B6576':'#6B635C','#8A93A3':'#9A8F80','rgba(32,37,49':'rgba(43,39,37'}
for a,b in PAL.items(): full=full.replace(a,b).replace(a.lower(),b)
open('pres/client.tpl.html','w').write(full)
low=full.lower(); print(len(pages),'станок' in low,'окупаем' in low,'10…+16' in full)
