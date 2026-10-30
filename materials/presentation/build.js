const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
(async()=>{const d=process.argv[2];let h=fs.readFileSync(path.join(d,'deck.tpl.html'),'utf8');
for(const n of ['before','after','work','tape','city']){h=h.split(`{{${n}}}`).join('data:image/jpeg;base64,'+fs.readFileSync(path.join(d,'img',n+'.jpg')).toString('base64'));}
fs.writeFileSync(path.join(d,'deck.html'),h);
const b=await chromium.launch();const pg=await b.newPage();await pg.goto('file://'+path.join(d,'deck.html'),{waitUntil:'networkidle'});
await pg.evaluate(()=>document.fonts.ready);
const over=await pg.evaluate(()=>[...document.querySelectorAll('.page')].map((p,i)=>{const r=p.getBoundingClientRect();let m=0;p.querySelectorAll('*').forEach(e=>{if(e.closest('.foot'))return;const q=e.getBoundingClientRect();if(q.bottom-r.top>m)m=q.bottom-r.top});return [i+1,Math.round(m),Math.round(r.height)]}).filter(x=>x[1]>x[2]-60));
console.log('overflow',JSON.stringify(over),'font',await pg.evaluate(()=>document.fonts.check('12px Onest')));
await pg.pdf({path:path.join(d,'Оконщик_3000_оборудование_и_технология.pdf'),width:'297mm',height:'210mm',printBackground:true});await b.close();})();
