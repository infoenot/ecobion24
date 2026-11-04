import re, json, base64, os, shutil
D = os.path.dirname(os.path.abspath(__file__))
OUT = D + '/landing2'
os.makedirs(OUT + '/img', exist_ok=True)
for f in os.listdir(D + '/landing/img'):
    shutil.copy(D + '/landing/img/' + f, OUT + '/img/' + f)
SV = json.load(open(D + '/landing2_svg.json'))
PHONE = '+7 921 950-38-60'
TEL = 'tel:+79219503860'
ARR = '<i aria-hidden="true">→</i>'


def H2(txt, cls=''):
    # [слово] — акцент
    return f'<h2 class="h2 {cls}">' + re.sub(r'\[(.+?)\]', r'<em>\1</em>', txt) + '</h2>'


def lbl(n, t):
    return f'<span class="lbl">{n} · {t}</span>'


SHORT = {
 'Что вы покупаете': 'Что вы [покупаете]',
 'За что платит клиент': 'За что [платит клиент]',
 'Решение': '[Термокороб]',
 'Материал': 'Материал — [ПВХ‑сэндвич 10 мм]',
 'Как работает оборудование': '[4 операции] оборудования',
 'Комплект': 'Что входит [в комплект]',
 'Характеристики': '[Вес] оборудования',
 'Где делать короба': 'Где [делать короба]',
 'Монтаж': '[Монтаж] короба',
 'Изделия': 'Что ещё [делают]',
 'Подоконник': '[Подоконник]',
 'Отделка': '[Отделка]',
 'Галерея': '[Галерея]',
 'Обучение и поддержка': '[Обучение] и поддержка',
 'Гарантия и договор': '[Договор] и гарантия',
 'Экономика': '[Цены] и пример объекта',
 'Окупаемость': '[Окупаемость]',
 'Как начать': 'Как [начать]',
}


def head(n, t, h, lead='', dark=False):
    full = re.sub(r'[\[\]]', '', h)
    return f'''<div class="shead">
  <div class="shead-lbl">{lbl(n, t)}</div>
  <div class="shead-l">{H2(SHORT.get(t, h))}</div>
  <div class="shead-r"><p class="sfull">{full}</p>{f'<p class="lead">{lead}</p>' if lead else ''}</div>
</div>'''


def form(fid, place, title, sub, extra='', tone=''):
    return f'''<form class="lform {tone}" id="{fid}" data-place="{place}">
  <div class="fhead"><h3>{title}</h3><p>{sub}</p></div>
  <div class="frow">
    <input name="name" placeholder="Имя" autocomplete="name" required>
    <input name="phone" type="tel" placeholder="+7 (___) ___-__-__" autocomplete="tel" required>
    {extra}
    <button class="btn" type="submit"><span>Получить консультацию</span>{ARR}</button>
  </div>
  <div class="agree">Нажимая кнопку, вы соглашаетесь на обработку персональных данных для обратной связи.</div>
  <div class="ok"><b>Заявка отправлена</b>Перезвоним в ближайшее время. Или сразу: <a href="{TEL}">{PHONE}</a>, звонок или MAX.</div>
</form>'''


def rows(items):
    return '<div class="kv">' + ''.join(f'<div><span>{a}</span><b>{b}</b></div>' for a, b in items) + '</div>'


def ul(items):
    return '<ul class="ln">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


S = []

# ---------- HERO ----------
S.append(f'''<header class="hero" id="top">
  <img src="img/city_wide.jpg" alt="Новостройки с панорамным остеклением">
  <nav class="nav"><a class="logo" href="#top"><b></b>Оконщик 3000</a>
    <div class="links"><a href="#s02">Комплект</a><a href="#s06">Оборудование</a><a href="#s11">Изделия</a><a href="#s14">Экономика</a><a href="#s16">Как начать</a></div>
    <a class="ct" href="{TEL}">{PHONE}</a></nav>
  <div class="hero-t">
    <h1 class="up"><span>Начни свой бизнес на</span> <span><em>утеплении</em> холодного панорамного</span> <span>остекления изнутри</span></h1>
    <div class="hero-r">
      <p>Для мастеров, оконщиков, ремонтников и тех, кто устал работать на рынке с высокой конкуренцией и низкой доходностью.</p>
      <a class="btn" href="#form-top"><span>Получить консультацию</span>{ARR}</a>
    </div>
  </div>
</header>
<section class="fstrip">{form('form-top', 'первый экран', 'Обсудить запуск в вашем городе', 'Перезвоним, разберём город и ответим на вопросы по оборудованию.', '<input name="city" placeholder="Город">')}</section>
<section class="dark nums4" id="nums">
  <div><div class="num">150–500 <small>тыс. ₽</small></div><p>чек за один заказ</p></div>
  <div><div class="num">2–4 <small>дня</small></div><p>работа на объекте</p></div>
  <div><div class="num">100–200 <small>тыс. ₽</small></div><p>остаток после прямых расходов</p></div>
  <div><div class="num">3–4 <small>заказа</small></div><p>вместо 20 по 10–15 тыс. ₽</p></div>
</section>''')

# ---------- 01 Рынок ----------
bad = ['Зимой алюминиевые стойки холодные, у окна некомфортно', 'На металле собирается конденсат', 'По полым профилям передаётся шум', 'Металл застройщика выбивается из интерьера']
why = ['Заменить фасад — дорого, часто нельзя без согласования', 'Второй ряд окон съедает площадь и вид', 'Подручные материалы — громоздко, видны стыки']
cell = lambda n, t: f'<div class="mk-c"><span class="mk-n">{n:02d}</span><p>{t}</p></div>'
S.append(f'''<section class="mk" id="s01">
  <div class="mk-top">
    <div class="mk-h">{lbl('01', 'Рынок')}{H2('Владелец квартиры с панорамными окнами хочет, чтобы у окна было [тепло, тихо, сухо и красиво]')}</div>
    <div class="ph"><img src="img/hero.jpg" alt="Лоджия: белые короба на стойках панорамного остекления" loading="lazy"><div class="c"><span class="cap up">Тёплое остекление без замены фасада</span></div></div>
  </div>
  <div class="mk-grid">
    <div class="mk-c hd"><h3 class="up">Что не так</h3></div>
    {''.join(cell(i + 1, t) for i, t in enumerate(bad))}
    <div class="mk-c hd g2"><h3 class="up">Почему обычный ремонт не помогает</h3></div>
    {''.join(cell(i + 1, t) for i, t in enumerate(why))}
    <div class="mk-c sol"><h3 class="up">Решение</h3><p>Утеплить стойки и закрыть бесшовными коробами по размеру, не меняя фасад.</p></div>
  </div>
</section>''')

# ---------- 02 Что вы покупаете ----------
S.append(f'''<section class="sec" id="s02">
  {head('02', 'Что вы покупаете', 'Вы покупаете [оборудование, технологию] и год поддержки', 'Это не франшиза: нет роялти и ежемесячных платежей. Комплект после оплаты — ваш.')}
  <div class="cards c4">
    <div><span class="k">01</span><h3 class="up">Оборудование</h3><p>Оборудование «Оконщик 3000», настольная пила, расходные материалы из расчёта на 5–6 месяцев работы.</p></div>
    <div><span class="k">02</span><h3 class="up">Технология</h3><p>Как делать изделия на оборудовании, как утеплять стойку перед установкой короба, как монтировать, красить и ламинировать.</p></div>
    <div><span class="k">03</span><h3 class="up">Обучение</h3><p>В Москве на нашей базе или удалённо: по видео и на консультациях с разработчиком.</p></div>
    <div class="dk"><span class="k">04</span><h3 class="up">Поддержка год</h3><p>Консультации по производству и продажам 12 месяцев с даты договора. Разбор вопросов по фото и видео с объекта.</p></div>
  </div>
  <div class="tiles t3">
    <div class="tile"><div class="num">Цена <small>по запросу</small></div><p>Назовём на консультации. Доставка транспортной компанией оплачивается отдельно.</p></div>
    <div class="tile"><div class="num">20 <small>рабочих дней</small></div><p>Срок изготовления и отгрузки комплекта по договору.</p></div>
    <div class="tile"><div class="num">24 <small>месяца</small></div><p>Гарантия на оборудование с момента получения и запуска.</p></div>
  </div>
</section>''')

# ---------- 03 За что платит клиент ----------
tasks = [('Холодные стойки', 'Тепло', 'Зимой алюминиевые стойки холодные. Утеплитель и короб закрывают холодный металл.'),
         ('Лоджия как склад', 'Уют', 'Ровные бесшовные поверхности без щелей и самодельных стыков. Лоджия становится частью квартиры.'),
         ('Слышно соседей', 'Тишина', 'Пустотелые стойки проходят через этажи и передают звук. Пустоты заполняют, стойку закрывают коробом.'),
         ('Конденсат', 'Сухость', 'Металл закрывают бутиловой лентой или жидкой резиной. На этом слое конденсат не образуется.'),
         ('Профиль застройщика', 'Дизайн', 'Короба красят по RAL или клеят плёнку. Царапины и следы стройки скрыты.'),
         ('Метры пустуют', 'Площадь', 'С утеплением пола и потолка лоджия становится кабинетом или детским уголком. Без второго ряда остекления.'),
         ('Квартира под сдачу', 'Аренда', 'Аккуратные окна видны на фото объявления. Аргумент для владельцев квартир под сдачу.')]
tcards = ''.join(f'<div><span class="k">Проблема: {p.lower()}</span><h3 class="up">{t}</h3><p>{x}</p></div>' for p, t, x in tasks)
S.append(f'''<section class="sec" id="s03">
  {head('03', 'За что платит клиент', 'Клиент платит не за пластик, а за [решение семи задач]', 'Холодная, шумная и некрасивая лоджия становится тёплой, тихой и красивой частью квартиры. Стойки несущие — их не меняют, а утепляют и закрывают коробом.')}
  <div class="ba">
    <div class="ph"><img src="img/before.jpg" alt="Лоджия до работ" loading="lazy"><span class="tag">До</span></div>
    <div class="ph"><img src="img/after.jpg" alt="Лоджия после работ" loading="lazy"><span class="tag ac">После</span></div>
  </div>
  <div class="cards c4 tasks">{tcards}
    <div class="acc-b"><span class="k">Все семь задач закрывает один заказ</span><div class="num">1–3 <small>дня</small></div><p>Утепление узла и бесшовный короб по замеру. Установка на объекте после замера; покраска по RAL добавляет несколько дней.</p></div>
  </div>
</section>''')

# ---------- 04 Решение ----------
S.append(f'''<section class="sec" id="s04">
  {head('04', 'Решение', 'Термокороб — [цельногнутый короб] из ПВХ-сэндвича с утеплителем внутри', 'Короб делают по замеру конкретной стойки и клеят поверх утеплённого профиля. Стыка на внешнем ребре нет: изделие согнуто из одной полосы.')}
  <div class="split">
    <div class="blk-t big"><span class="k">01</span><h3 class="up">Термокороб на стойки и ригели</h3>{ul(['П-образный — на вертикальную стойку, Г-образный — на ригель и примыкания.', 'От пола до потолка одной деталью, без набора планок.', 'Монтаж на клей, без сверления профиля.', 'Световой проём уменьшается максимум на 10 мм: короб закрывает только стойку.'])}</div>
    <div class="blk-t big"><span class="k">02</span><h3 class="up">3D-термооткос на окна и двери</h3>{ul(['Откос загнут до стены. Ширина полок любая, например 90 мм спереди и 30 мм сбоку.', 'Обычный F-профиль даёт фиксированные 50–60 мм.', 'Детали режут под 90°, без стыков на 45°.', 'Подходит для ПВХ, алюминиевых и деревянных окон, входных и межкомнатных дверей.'])}</div>
  </div>
  <div class="tiles t3">
    <div class="tile"><div class="num">10 <small>мм</small></div><p>сэндвич-панель с утеплителем внутри</p></div>
    <div class="tile"><div class="num sm">без сверления</div><p>короб сажают на клей поверх утеплённой стойки</p></div>
    <div class="tile"><div class="num">до 10 <small>мм</small></div><p>на столько максимум уменьшается световой проём</p></div>
  </div>
  <p class="note">Утепление стоек не превращает любое холодное остекление в тёплое. Нужна ли замена стёкол или стеклопакетов, решает инженер на объекте.</p>
</section>''')

# ---------- 05 Материал ----------
S.append(f'''<section class="sec" id="s05">
  {head('05', 'Материал', 'Сырьё одно — [ПВХ-сэндвич 10 мм], его продают в каждом областном городе', 'Сэндвич — два листа пластика, между ними экструдированный пенополистирол (XPS). Из этого же материала делают заполнение балконных дверей ПВХ.')}
  <div class="split">
    {rows([('Толщина панели', '10 мм'), ('Лицевой пластик', 'не тоньше 0,7 мм, лучше 0,8–1 мм'), ('Утеплитель внутри', 'XPS, около 10 мм'), ('Формат листа', '1500×3000 или 2000×3000 мм'), ('Цвет', 'белый, как у пластикового окна'), ('Цена листа', '2 650–3 000 ₽ (1500×3000, 2026 г.)'), ('Поставщик', 'Т.Б.М. — филиалы по всей России')])}
    <div class="blk g2">
      <div class="cb g"><span class="up">Сколько выходит с листа</span><p>При развёртке 300 мм — 15 погонных метров откоса. Материал на 1 метр изделия — 150–300 ₽ в зависимости от развёртки.</p></div>
      <div class="cb"><span class="up">Продажная цена изделий</span><p>От 1 250 ₽ за погонный метр без монтажа. С монтажом — от 2 000 ₽.</p></div>
      <div class="cb w"><span class="up">Что не подходит</span><p>Сэндвич с пластиком 0,4 мм. Он не держит прямую линию и плохо ведёт себя при нагреве на сгибе.</p></div>
    </div>
  </div>
</section>''')

# ---------- 06 Оборудование ----------
S.append(f'''<section class="sec dark" id="s06">
  {head('06', 'Как работает оборудование', 'Оборудование делает изделие за 4 операции: [раскрой, паз, нагрев, сгиб]', 'Оборудование нагревает лист по линии сгиба и сгибает его под 90°. Получается цельное П- или Г-образное изделие.')}
  <div class="steps s4">
    <div><div class="num">01</div><h3 class="up">Раскрой</h3><p>Нарезка заготовки с точностью до 0,5 мм.</p></div>
    <div><div class="num">02</div><h3 class="up">Выборка паза</h3><p>Выборка паза под будущий сгиб.</p></div>
    <div><div class="num">03</div><h3 class="up">Нагрев</h3><p>Оборудование прогревает пластик по линии паза.</p></div>
    <div><div class="num">04</div><h3 class="up">Сгиб</h3><p>Заготовку сгибают под 90°. Для П-короба — два сгиба, для Г-короба — один.</p></div>
  </div>
  <div class="split">
    <div class="cb"><span class="up">Точность</span><p>Изделие делают по замеру, нарезка с точностью до 0,5 мм.</p></div>
    <div class="cb g2c"><span class="up">Чего оборудование не делает</span><p>Оконные рамы и стекло, не гнёт алюминиевые стойки. Гнёт листовой пластик и сэндвич толщиной до 10 мм. Сэндвич 24, 32, 40 и 50 мм не гнёт.</p></div>
  </div>
</section>''')

# ---------- 07 Комплект + 08 Характеристики ----------
S.append(f'''<section class="sec" id="s07">
  {head('07', 'Комплект', 'Что входит в комплект — [по спецификации договора]', 'Состав комплекта, цену и сроки фиксируем в договоре до оплаты.')}
  <div class="tbl spec">
    <div class="th"><span>Позиция</span><span>Что это</span><span>Кол-во</span></div>
    <div><b>Оборудование «Оконщик 3000»</b><span>стол 600 × 900 × 3200 мм на стальных регулируемых опорах с рабочими модулями: раскрой, паз, нагрев, сгиб</span><span>1 шт.</span></div>
    <div><b>Настольная пила</b><span>«Декстер», 210 мм</span><span>1 шт.</span></div>
    <div><b>Расходные материалы</b><span>из расчёта на 5–6 месяцев работы</span><span>1 набор</span></div>
  </div>
</section>
<section class="sec" id="s08">
  {head('08', 'Характеристики', 'Оборудование весит 53 кг, работает от розетки и перевозится [на багажнике легковой машины]')}
  <div class="tiles t4">
    <div class="tile"><div class="num">53 <small>кг</small></div><p>Длина 3,2 м, опоры снимаются. Двое грузят его на багажник легковой машины.</p></div>
    <div class="tile"><div class="num">220 <small>В</small></div><p>Работает от обычной сети.</p></div>
    <div class="tile"><div class="num">3×4 <small>м</small></div><p>Ориентир рабочей зоны с учётом листа и проходов.</p></div>
    <div class="tile"><div class="num">100 <small>м за смену</small></div><p>Выработка одного мастера за смену 6–7 часов.</p></div>
  </div>
  <p class="note">Оборудование работает без шума и пыли. Расходные части меняются по износу.</p>
</section>''')

# ---------- 09 Где делать ----------
S.append(f'''<section class="sec" id="s09">
  {head('09', 'Где делать короба', 'Короба делают в цехе или гараже, [реже — прямо на объекте]', 'Обычно оборудование стоит в цехе или гараже, на объект везут готовые короба. Реже оборудование привозят на объект и делают короба на месте.')}
  <div class="cards c3">
    <div><span class="k">01</span><h3 class="up">В цехе</h3><p>Тёплое помещение от 12–14 м². Делаете изделия для своих заказов и на продажу другим мастерам.</p></div>
    <div><span class="k">02</span><h3 class="up">В гараже</h3><p>Тёплый гараж подходит для старта: оборудование работает от 220 В, без шума и пыли.</p></div>
    <div><span class="k">03 · реже</span><h3 class="up">На объекте</h3><p>Оборудование привозят на объект: замер, изготовление и монтаж в одном месте.</p></div>
  </div>
  <div class="split">
    <div class="ph tall"><img src="img/work.jpg" alt="Установка короба на утеплённую стойку" loading="lazy"><div class="c"><span class="cap up">Установка короба на утеплённую стойку</span></div></div>
    <div class="days dark">
      <h3 class="up">Сколько занимает заказ на белых коробах</h3>
      <div><span class="num">День 1</span><b>замер и заказ</b></div>
      <div><span class="num">День 2</span><b>изготовление</b></div>
      <div><span class="num">День 3</span><b>монтаж</b></div>
      <p>Покраска по RAL у партнёра добавляет несколько дней.</p>
    </div>
  </div>
</section>''')

# ---------- 10 Монтаж ----------
mnt = [('Гидроизоляция', 'Металл стойки закрывают бутиловой лентой или жидкой резиной. На этом слое конденсат не образуется.'),
       ('Утепление', 'На вертикальные и горизонтальные профили клеят пеноплекс.'),
       ('Заполнение и герметизация', 'Пустоты заполняют пеной, примыкания проходят герметиком. Между стеклопакетом и коробом прокладывают резину.'),
       ('Замер', 'Снимают точный размер стойки.'),
       ('Установка', 'Чистовой короб сажают на клей или герметик, который не растворяет пенополистирол. Крепёж в профиль не нужен.')]
acc = ''.join(f'<details{" open" if i == 0 else ""}><summary><span class="n">0{i+1}</span><span class="t">{t}</span><span class="pm"></span></summary><p>{x}</p></details>' for i, (t, x) in enumerate(mnt))
S.append(f'''<section class="sec" id="s10">
  {head('10', 'Монтаж', 'Перед установкой короба стойку [изолируют и утепляют]', 'Короб — финишный слой. Тепло даёт весь узел: изоляция металла, утеплитель и герметичные примыкания.')}
  <div class="split msplit">
    <div class="ph tall"><img src="img/tape.jpg" alt="Стойки и ригели в изоляции перед установкой коробов" loading="lazy"><div class="c"><span class="cap up">Стойки и ригели в изоляции перед установкой коробов</span></div></div>
    <div class="acc">{acc}<p class="note in">Для каждой профильной системы — своя последовательность. Ей учим на объектах и разбираем сложные узлы по фото.</p></div>
  </div>
</section>''')

# ---------- MID FORM ----------
S.append(f'''<section class="midf dark" id="form-mid-sec">
  <div class="midf-t"><span class="lbl">Посмотреть вживую</span>{H2('Приезжайте [на объект]')}<p class="sfull">Приезжайте на объект в Москве — покажем оборудование и монтаж.</p><p class="lead">Или созвонимся по видео: покажем, как гнётся короб, ответим про ваш город, сроки и комплект.</p></div>
  {form('form-mid', 'середина', 'Запросить консультацию', 'Перезвоним и договоримся о встрече или видеозвонке.', '<select name="topic"><option>Узнать цену комплекта</option><option>Хочу посмотреть оборудование вживую</option><option>Видеозвонок</option></select>', 'v dk')}
</section>''')

# ---------- 11 Изделия ----------
prods = ''.join(f'<div><div class="svgw">{svg}</div><h3 class="up">{t}</h3><p>{x}</p></div>' for svg, t, x in SV['prods'])
sills = SV['sills']
sill2 = sills[1][1].replace('id="ht"', 'id="ht2"').replace('url(#ht)', 'url(#ht2)')
sill_txt = ['Плиту кладут на стену под окном. Сэндвич П-профилем надевают на плиту: сверху, по торцу и снизу. Толщина по фронту — 50 мм.',
            'На стену кладут пеноплекс — он утепляет и держит форму. Сверху сэндвич с загибом вниз: свес за стену 50–150 мм, торец закрыт загибом к стене.']
S.append(f'''<section class="sec" id="s11">
  {head('11', 'Изделия', 'Кроме утепления, на оборудовании делают [профили для окон, дверей] и интерьера', 'Всё — из того же листа сэндвича 10 мм и теми же 4 операциями: раскрой, паз, нагрев, сгиб. Ниже — схемы сечений.')}
  <div class="cards c4 prods">{prods}</div>
</section>
<section class="sec" id="s11b">
  {head('11', 'Подоконник', 'Подоконник из сэндвича делают [двумя способами]', 'Сэндвич — финишная поверхность. Жёсткость и форму даёт основа: плита или пеноплекс. Схемы — в разрезе.')}
  <div class="split sills">
    <div><span class="k">Вариант 1</span><h3 class="up">{sills[0][0]}</h3><div class="svgw">{sills[0][1]}</div><p>{sill_txt[0]}</p></div>
    <div><span class="k">Вариант 2</span><h3 class="up">{sills[1][0]}</h3><div class="svgw">{sill2}</div><p>{sill_txt[1]}</p></div>
  </div>
</section>''')

# ---------- Отделка ----------
def sw(bg, name, border=False):
    return f'<div class="sw"><i style="background:{bg};{"box-shadow:inset 0 0 0 1px #E3E3E3;" if border else ""}"></i><span>{name}</span></div>'
oak = lambda a, b, c: f'repeating-linear-gradient(92deg,{a} 0 3px,{b} 3px 7px,{a} 7px 9px,{c} 9px 14px)'
S.append(f'''<section class="sec" id="s11c">
  {head('11', 'Отделка', 'Любое изделие делают в одном из [трёх вариантов отделки]', 'Цвет подбирают под интерьер: короб, откос и подоконник можно сделать в тон стенам, полу или мебели.')}
  <div class="cards c3 fin">
    <div><span class="k">01</span><h3 class="up">Белый</h3><p>Базовый цвет сэндвича, как у пластикового окна. Без дополнительной отделки, самый быстрый вариант.</p><div class="sws">{sw('#FFFFFF', 'белый матовый', True)}</div></div>
    <div><span class="k">02</span><h3 class="up">Покраска по RAL</h3><p>800+ вариантов цвета по шкале RAL. Красят в покрасочной камере партнёра. Добавляет несколько дней к сроку.</p><div class="sws">{sw('#383E42', 'графит RAL 7016')}{sw('#16181B', 'чёрный матовый')}{sw('#59473A', 'коричневый')}{sw('#9DA3A6', 'серый')}</div></div>
    <div><span class="k">03</span><h3 class="up">Ламинация плёнкой</h3><p>200+ вариантов плёнки: под дерево, однотонные, детские с рисунком.</p><div class="sws">{sw(oak('#D9C3A0', '#CDB48D', '#E3D0B1'), 'светлый дуб')}{sw(oak('#C08A4E', '#B37C42', '#CC9960'), 'золотой дуб')}{sw(oak('#6E4B33', '#5F402B', '#7B563C'), 'орех')}{sw(oak('#B9B2A3', '#ACA493', '#C6C0B3'), 'ясень')}</div></div>
  </div>
</section>''')

# ---------- Галерея ----------
s = open(D + '/pres/deck.norm.html').read()
gal = re.findall(r'<img[^>]*src="\{\{(g\d\d)\}\}"[^>]*>\s*(?:<[^>]+>\s*)*?([^<]+?)\s*<', s)
figs = []
for k, (g, cap) in enumerate(gal):
    src = f'src="img/{g}.jpg" loading="lazy"' if k < 8 else f'data-src="img/{g}.jpg"'
    figs.append(f'<figure class="gal"><img {src} alt="{cap}"><figcaption>{cap}</figcaption></figure>')
assert len(figs) == 24, len(figs)
S.append(f'''<section class="sec" id="s11d">
  {head('11', 'Галерея', 'Что можно сделать [на оборудовании]')}
  <div class="galgrid" id="gal">{''.join(figs)}</div>
  <button type="button" class="more-btn" id="galbtn">Показать ещё 16 фото</button>
</section>''')

# ---------- 12 Обучение ----------
S.append(f'''<section class="sec red" id="s12">
  {head('12', 'Обучение и поддержка', 'Учим работе на оборудовании, монтажу и расчёту заказа, затем [год отвечаем на вопросы]')}
  <div class="cards c3">
    <div><span class="k">01</span><h3 class="up">Чему учим</h3>{ul(['Раскрой, выборка паза, нагрев и сгиб сэндвича', 'Замер, утепление узла, монтаж короба', 'Покраска и ламинация изделий', 'Расчёт заказа, расхода материала и цены для клиента'])}</div>
    <div><span class="k">02</span><h3 class="up">Как учим</h3>{ul(['На нашей базе в Москве или удалённо', 'Учебные видео — пока изготавливается комплект', 'По желанию — стажировка на действующих объектах в Москве', 'Выезд специалиста к вам в цену не входит'])}</div>
    <div><span class="k">03</span><h3 class="up">После обучения</h3>{ul(['12 месяцев консультаций по производству и продажам', 'Разбор сложных узлов по фото и видео с объекта', 'Ведём до сдачи первых 1–2 квартир', 'Контакты поставщиков сэндвича и плёнки'])}</div>
  </div>
  <div class="band">
    <div><h3 class="up">Поддержка по договору</h3><p>консультации по производству и продажам с даты подписания</p></div>
    <div class="num">12 <small>месяцев</small></div>
  </div>
  <p class="note">Отдельная тема обучения — как увеличить толщину стеклопакета без альпинистов.</p>
</section>''')

# ---------- 13 Договор ----------
S.append(f'''<section class="sec" id="s13">
  {head('13', 'Гарантия и договор', 'Договор с ООО «Меркурий-групп»: [срок, гарантия и ответственность] прописаны')}
  <div class="split">
    {rows([('Исполнитель', 'ООО «Меркурий-групп», ИНН 5916035699, Москва'), ('Покупатель', 'физлицо, ИП или ООО'), ('Цена', 'по запросу, фиксируется в договоре'), ('Способы оплаты', 'по счёту, QR-код онлайн-кассы, банковская карта, наличные с кассовым чеком'), ('Порядок оплаты', 'часть при заказе, остаток до 100% — перед отправкой; рассрочки нет'), ('Изготовление', '20 рабочих дней'), ('Доставка', 'ТК «Деловые линии» в ваш город, оплачивается отдельно'), ('Просрочка отгрузки', 'пени 0,5% в день')])}
    <div class="gar dark">
      <div class="num">24 <small>месяца</small></div><h3 class="up">Гарантия</h3>
      {ul(['Срок — с момента получения и запуска оборудования.', 'Дефект по вине производителя устраняем за 14 календарных дней своими силами и за свой счёт.', 'Гарантия не распространяется на расходные части.', 'Механические повреждения и комплектацию проверяйте при получении.'])}
    </div>
  </div>
</section>''')

# ---------- 14 Экономика ----------
S.append(f'''<section class="sec" id="s14">
  {head('14', 'Экономика', 'Цены на изделия и [пример одного объекта] в Москве', 'Цены по Москве. В вашем городе цены и спрос другие — считаем на созвоне.')}
  <div class="split">
    <div class="tbl two pr">
      <div class="th"><span>Изделие</span><span>Цена за пог. м</span></div>
      <div><b>Опт оконщикам: по их размерам, без замера и монтажа</b><span class="big">1 250 ₽</span></div>
      <div><b>3D-термооткос с монтажом</b><span class="big">от 2 000 ₽</span></div>
      <div><b>Термокороб под ключ, белый</b><span class="big">2 000–2 500 ₽</span></div>
      <div><b>Термокороб с покраской или ламинацией</b><span class="big">до 5 000 ₽</span></div>
      <div><b>Материал на 1 пог. м</b><span class="big">150–300 ₽</span></div>
    </div>
    <div class="obj dark">
      <span class="k">Объект в Москве, июль 2026</span>
      <h3 class="up">120 пог. м коробов в цвете RAL 9016 и ламинация 6 створок по месту</h3>
      <div class="ol"><span>Договор с клиентом</span><b>593 000 ₽</b></div>
      <div class="ol"><span>Материалы и покраска</span><b>69 000 ₽</b></div>
      <div class="ol"><span>Зарплата изготовления и монтажа</span><b>60 000 ₽</b></div>
      <div class="ol tot"><span>Остаток до налогов</span><b>464 000 ₽</b></div>
      <div class="ol"><span>Срок</span><b>7 рабочих дней</b></div>
    </div>
  </div>
  <p class="note">Это крупный объект, не средний заказ. Остаток 464 000 ₽ — до налогов и прочих расходов. Сколько заказов вы возьмёте, зависит от ваших продаж. Поток заявок и доход не гарантируем.</p>
</section>''')

# ---------- 15 Окупаемость ----------
S.append(f'''<section class="sec" id="s15">
  {head('15', 'Окупаемость', 'При средней смете 200 тыс. ₽ комплект окупается [за 2–3 объекта]', 'Расчёт по структуре затрат реального объекта в Москве: материалы — около 12% сметы, зарплата изготовления и монтажа — около 10%.')}
  <div class="pay">
    <div class="pay-big"><span class="pay-n">3</span><div><h3 class="up">объекта — и комплект окупился</h3><p>При средней смете 200 тыс. ₽</p></div></div>
    <div class="pay-s"><h3 class="up">Монтируете сами</h3><div><div class="num">175 <small>тыс. ₽</small></div><p>с объекта</p></div></div>
    <div class="pay-s"><h3 class="up">С наёмным мастером</h3><div><div class="num">155 <small>тыс. ₽</small></div><p>с объекта</p></div></div>
  </div>
  <div class="cap15 ftcap"><h3 class="up">Чем покупка отличается от франшизы</h3></div>
  <div class="ft"><div class="ft-h"><span></span><span>Паушальный взнос</span><span>Роялти</span><span>Ежемесячные платежи</span><span>Что остаётся у вас</span></div><div class="ft-r"><span class="ft-l">Франшиза</span><span>есть</span><span>% с выручки каждый месяц</span><span>есть</span><span>право работать под чужим брендом по договору</span></div><div class="ft-r own"><span class="ft-l">Оконщик 3000</span><span><span class="yes">нет</span></span><span><span class="yes">нет</span></span><span><span class="yes">нет</span></span><span><b>оборудование в собственности и технология</b></span></div></div>
    <div class="tbl three fr t15 mob">
      <div class="cap15"><h3 class="up">Чем покупка отличается от франшизы</h3></div>
      <div class="th"><span></span><span>Франшиза</span><span>Оконщик 3000</span></div>
      <div><b>Паушальный взнос</b><span>есть</span><span class="yes">нет</span></div>
      <div><b>Роялти</b><span>% с выручки каждый месяц</span><span class="yes">нет</span></div>
      <div><b>Ежемесячные платежи</b><span>есть</span><span class="yes">нет</span></div>
      <div><b>Что остаётся у вас</b><span>право работать под чужим брендом по договору</span><span class="yes">оборудование в собственности и технология</span></div>
    </div>
  <p class="note">За комплект платите один раз.</p>
</section>''')

# ---------- 16 Как начать ----------
st = [('Созвон', 'Разбираем ваш город, опыт и формат: опт, монтаж под ключ или оба.'), ('Договор и оплата', 'Отправляем договор и счёт, фиксируем состав комплекта и сроки.'),
      ('Изготовление', '20 рабочих дней. В это время вы смотрите учебные видео.'), ('Обучение', 'В Москве на нашей базе или удалённо.'),
      ('Доставка', '«Деловые линии» привозят комплект, вы запускаете оборудование.'), ('Первый объект', 'Вместе подбираем дом в вашем городе и ведём до сдачи первых квартир.')]
S.append(f'''<section class="sec dark" id="s16">
  {head('16', 'Как начать', 'От созвона до первого объекта — [6 шагов]')}
  <div class="steps s3">{''.join(f'<div><div class="num">0{i+1}</div><h3 class="up">{t}</h3><p>{x}</p></div>' for i, (t, x) in enumerate(st))}</div>
</section>''')

# ---------- FINAL ----------
S.append(f'''<section class="final" id="form-end-sec">
  <div class="final-t">
    <span class="lbl">Вопросы по комплекту и запуску</span>
    {H2('Обсудим запуск [в вашем городе]')}
    <a class="bigtel" href="{TEL}">{PHONE}</a>
    <p>Вячеслав, продажи и запуск · звонок или MAX</p>
    <p class="muted">Технические вопросы разбирает Сергей Попов — инженер-технолог, разработчик оборудования, в оконной отрасли с 1994 года.</p>
  </div>
  {form('form-bottom', 'низ', 'Получить консультацию', 'Оставьте телефон — перезвоним и ответим на вопросы.', '<input name="city" placeholder="Город"><textarea name="comment" rows="2" placeholder="Вопрос (необязательно)"></textarea>', 'v ac')}
</section>
<footer><b>Оконщик 3000</b> · оборудование и технология бесшовных термокоробов<br>Исполнитель по договору — ООО «Меркурий-групп», ИНН 5916035699 · <a href="{TEL}">{PHONE}</a></footer>
<div class="fab"><a class="btn" href="#form-bottom"><span>Получить консультацию</span>{ARR}</a></div>''')

body = '\n'.join(S)


def ty(t):
    for _ in range(2):
        t = re.sub(r'(?<![\wА-яЁё])([А-яЁёA-Za-z]{1,2}) (?=\S)', lambda m: m.group(1) + ' ', t)
    t = t.replace(' —', ' —').replace(' –', ' –')
    t = re.sub(r'(\d) (?=(₽|%|мм|см|м²|м|кг|В|дн|дней|дня|тыс|°C|раб|месяц|шт|пог|створ|заказ|объект|плён|мес|квартир))', lambda m: m.group(1) + ' ', t)
    t = re.sub(r'(\d) (?=\d{3})', lambda m: m.group(1) + ' ', t)
    t = re.sub(r'(\d)–(\d)', lambda m: m.group(1) + '–⁠' + m.group(2), t)
    t = re.sub(r'\b(П|Г|F|3D)-', lambda m: m.group(1) + '‑', t)
    t = re.sub(r'(?<![\d\w])(\d{1,2}) (?=[А-яЁё])', lambda m: m.group(1) + '\u00a0', t)
    t = re.sub(r'(?<=[А-яЁёA-Za-z])-(?=[А-яЁёA-Za-z])', '\u2011', t)
    return t


body = re.sub(r'>([^<]+)<', lambda m: '>' + ty(m.group(1)) + '<', body)
# склейка последних двух слов в абзацах — без висячих строк
body = re.sub(r'(?<![\wА-яЁё])([А-яЁёA-Za-z]{1,2}) (<em>)', lambda m: m.group(1) + '\u00a0' + m.group(2), body)
def glue(m):
    a, b = m.group(1), m.group(2)
    return (' ' + a + '\u00a0' + b if len(a) + len(b) <= 20 else m.group(0)[:-len(m.group(3))]) + m.group(3)
body = re.sub(r' ([^\s<>]+) ([^\s<>]+)(</(?:p|li|figcaption|b)>)', glue, body)
body = re.sub(r'(alt|placeholder)="([^"]*)"', lambda m: m.group(1) + '="' + m.group(2).replace('⁠', '') + '"', body)

CSS = open(D + '/landing2.css').read()
JS = '''<script>
// Адрес для заявок: веб-приложение Google Apps Script (см. README) — заявки попадут в таблицу «Заявки».
const FORM_ENDPOINT='';
document.querySelectorAll('input[type=tel]').forEach(i=>i.addEventListener('input',()=>{let d=i.value.replace(/\\D/g,'');if(d.startsWith('8'))d='7'+d.slice(1);if(!d.startsWith('7'))d='7'+d;d=d.slice(0,11);let s='+7';if(d.length>1)s+=' ('+d.slice(1,4);if(d.length>=4)s+=') '+d.slice(4,7);if(d.length>=7)s+='-'+d.slice(7,9);if(d.length>=9)s+='-'+d.slice(9,11);i.value=s;}));
document.querySelectorAll('form.lform').forEach(f=>f.addEventListener('submit',async e=>{e.preventDefault();
 const data=Object.fromEntries(new FormData(f));data.place=f.dataset.place;data.page=location.href;data.ts=new Date().toISOString();
 if((data.phone||'').replace(/\\D/g,'').length<11){f.querySelector('input[type=tel]').focus();return}
 const b=f.querySelector('button');b.disabled=true;b.querySelector('span').textContent='Отправляем…';
 try{if(FORM_ENDPOINT)await fetch(FORM_ENDPOINT,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify(data)})}catch(err){}
 f.classList.add('sent');}));
const fab=document.querySelector('.fab'),vis=new Set();
const io=new IntersectionObserver(es=>{es.forEach(e=>e.isIntersecting?vis.add(e.target):vis.delete(e.target));upd()},{threshold:.1});
document.querySelectorAll('form.lform').forEach(f=>io.observe(f));
const hero=document.querySelector('.hero');function upd(){fab.classList.toggle('off',vis.size>0||hero.getBoundingClientRect().bottom>0)}
addEventListener('scroll',upd,{passive:true});upd();
const gb=document.getElementById('galbtn'),g=document.getElementById('gal');
const hid=()=>[...g.children].filter(f=>getComputedStyle(f).display==='none').length;
const lab=()=>{const n=hid();gb.textContent=n?'Показать ещё '+n+' фото':'Свернуть'};lab();addEventListener('resize',()=>{if(!g.classList.contains('open'))lab()});
gb.addEventListener('click',()=>{if(g.classList.toggle('open')){g.querySelectorAll('img[data-src]').forEach(i=>{i.src=i.dataset.src;i.removeAttribute('data-src')});gb.textContent='Свернуть'}else{lab();g.scrollIntoView({behavior:'smooth',block:'start'})}});
document.querySelectorAll('.acc details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)document.querySelectorAll('.acc details').forEach(o=>{if(o!==d)o.open=false})}));
</script>'''
html = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Оконщик 3000 — свой бизнес на утеплении холодного панорамного остекления</title>
<meta name="description" content="Оборудование для бесшовных термокоробов и 3D-откосов из ПВХ-сэндвича 10 мм. Комплект, обучение и год поддержки. Без роялти и паушального взноса.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>
{body}
{JS}
</body></html>'''
open(OUT + '/index.html', 'w').write(html)
one = re.sub(r'(src|data-src)="img/(\w+)\.jpg"', lambda m: m.group(1) + '="data:image/jpeg;base64,' + base64.b64encode(open(OUT + '/img/' + m.group(2) + '.jpg', 'rb').read()).decode() + '"', html)
open(OUT + '/Оконщик_3000_лендинг_DS41.html', 'w').write(one)
print('ok', round(len(one) / 1024), 'KB')
