# Лендинг «Оконщик 3000» — продажа оборудования

Лендинг = основная презентация `materials/presentation/deck.tpl.html`, переверстанная под сайт: все 22 раздела, те же тексты, фото и схемы.
Пересобрать после правок презентации: `python3 mk_landing.py` (берёт `pres/deck.norm.html`, картинки из `landing/img`).

- `index.html` + `img/` — для хостинга. `Оконщик_3000_лендинг_один_файл.html` — всё в одном файле (2,8 МБ).
- Формы: первый экран, середина (после «Монтаж»), низ. На телефоне — плавающие «Позвонить» / «Получить консультацию».
## Как получать заявки в таблицу «Заявки»

Сейчас `FORM_ENDPOINT = ''` — форма показывает «Заявка отправлена», но никуда не шлёт. Подключить:

1. Таблица «Заявки» → Расширения → Apps Script → вставить код ниже → Сохранить.
2. «Развернуть» → «Новое развёртывание» → тип «Веб-приложение», доступ «Все» → скопировать URL.
3. В `index.html` вписать URL в `const FORM_ENDPOINT = '...'`.

```js
function doPost(e){
  const d=JSON.parse(e.postData.contents);
  const sh=SpreadsheetApp.getActive().getSheetByName('Заявки');
  const date=Utilities.formatDate(new Date(),'Europe/Moscow','d MMM');
  sh.appendRow([date,d.name||'',"'"+(d.phone||''),d.city||'','Лендинг','новая','','','',
    'Заявка с лендинга ('+(d.place||'')+'). '+(d.topic||'')+' '+(d.comment||''),'','Лендинг']);
  return ContentService.createTextOutput('ok');
}
```
