const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
(async()=>{const d=process.argv[2],P=path.join(d,'../presentation');let h=fs.readFileSync(path.join(d,'booklet.tpl.html'),'utf8');
const img=(f)=>'data:image/jpeg;base64,'+fs.readFileSync(f).toString('base64');
for(const g of ['g04','g06','g17','n_erker','n_portal','n_bedroom','n_oak'])h=h.split(`{{${g}}}`).join(img(path.join(d,'hi',g+'.jpg')));h=h.replace('{{cover}}',img(path.join(d,'hi','cover.jpg')));h=h.replace('{{g03}}',img(P+'/gallery/g03.jpg')).replace('{{g04}}',img(path.join(d,'hi','g04.jpg'))).replace('{{g14}}',img(path.join(d,'hi','g14.jpg'))).replace('{{g11}}',img(P+'/gallery/g11.jpg')).replace('{{before}}',img(P+'/img/before.jpg')).replace('{{after}}',img(P+'/img/after.jpg'));
const S='fill="none" stroke="#D2622B" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"';
const I={i_t:`<svg viewBox="0 0 24 24" ${S}><path d="M12 3v11"/><circle cx="12" cy="17" r="3.5"/><path d="M15 6h3M15 9h3"/></svg>`,
i_q:`<svg viewBox="0 0 24 24" ${S}><path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M17 9l4 6M21 9l-4 6"/></svg>`,
i_d:`<svg viewBox="0 0 24 24" ${S}><path d="M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z"/></svg>`,
i_c:`<svg viewBox="0 0 24 24" ${S}><circle cx="12" cy="12" r="8"/><circle cx="9" cy="10" r="1.2"/><circle cx="14" cy="8.5" r="1.2"/><circle cx="15.5" cy="13" r="1.2"/></svg>`,
i_h:`<svg viewBox="0 0 24 24" ${S}><path d="M4 11l8-6 8 6v8H4z"/><path d="M10 19v-5h4v5"/></svg>`,
i_s:`<svg viewBox="0 0 24 24" ${S}><rect x="4" y="4" width="16" height="16" rx="1"/><path d="M4 12h7v8M14 4v6h6"/></svg>`,
i_r:`<svg viewBox="0 0 24 24" ${S}><path d="M14 4l6 6-9 9H5v-6z"/><circle cx="15" cy="9" r="1.2"/></svg>`};
for(const k in I)h=h.replace(`{{${k}}}`,I[k]);
h=h.replace('{{scheme}}',`<svg viewBox="0 0 100 100"><rect x="0" y="0" width="100" height="100" fill="none"/>
<rect x="6" y="40" width="22" height="20" fill="#CFE3EE"/><rect x="72" y="40" width="22" height="20" fill="#CFE3EE"/>
<rect x="38" y="30" width="24" height="40" fill="#8A919E"/><rect x="42" y="34" width="16" height="32" fill="#B5BBC6"/>
<rect x="35" y="27" width="30" height="46" fill="none" stroke="#1A1A1A" stroke-width="3"/>
<rect x="30" y="22" width="40" height="5" fill="#F2A65A"/><rect x="30" y="73" width="40" height="5" fill="#F2A65A"/><rect x="30" y="22" width="5" height="56" fill="#F2A65A"/><rect x="65" y="22" width="5" height="56" fill="#F2A65A"/>
<path d="M28,60 L28,18 L72,18 L72,60" fill="none" stroke="#202531" stroke-width="5.5" stroke-linejoin="miter"/>
<path d="M28,60 L28,18 L72,18 L72,60" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="miter"/>
<text x="50" y="94" font-size="7" text-anchor="middle" fill="#5B6270" font-family="Onest">разрез стойки, вид сверху</text></svg>`);
fs.writeFileSync(path.join(d,'booklet.html'),h);
const b=await chromium.launch();const pg=await b.newPage();await pg.goto('file://'+path.join(d,'booklet.html'),{waitUntil:'networkidle'});await pg.evaluate(()=>document.fonts.ready);
const over=await pg.evaluate(()=>[...document.querySelectorAll('.p')].map((p,i)=>{const r=p.getBoundingClientRect();let m=0;p.querySelectorAll('*').forEach(e=>{const q=e.getBoundingClientRect();if(q.bottom>m)m=q.bottom});return [i+1,Math.round(m-r.top),Math.round(r.height)]}));
console.log('fit',JSON.stringify(over),await pg.evaluate(()=>document.fonts.check('12px Onest')));
await pg.pdf({path:path.join(d,'Евробуклет_для_клиента.pdf'),width:'303mm',height:'216mm',printBackground:true});await b.close();})();
