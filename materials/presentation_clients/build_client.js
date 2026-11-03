const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
(async()=>{const d=process.argv[2],B=path.join(d,'../booklet/hi');let h=fs.readFileSync(path.join(d,'client.tpl.html'),'utf8');
h=h.replace(/\{\{(\w+)\}\}/g,(m,n)=>{let f=[path.join(B,n+'.jpg'),path.join(d,'img',n+'.jpg'),path.join(d,'gallery',n+'.jpg')].find(p=>fs.existsSync(p));if(!f)throw new Error('no img '+n);return 'data:image/jpeg;base64,'+fs.readFileSync(f).toString('base64')});
fs.writeFileSync(path.join(d,'client.html'),h);
const b=await chromium.launch();const pg=await b.newPage();await pg.goto('file://'+path.join(d,'client.html'),{waitUntil:'networkidle'});await pg.evaluate(()=>document.fonts.ready);
const over=await pg.evaluate(()=>[...document.querySelectorAll('.page')].map((p,i)=>{const r=p.getBoundingClientRect();let m=0;p.querySelectorAll('*').forEach(e=>{if(e.closest('.foot'))return;const q=e.getBoundingClientRect();if(q.bottom-r.top>m)m=q.bottom-r.top});return [i+1,Math.round(m),Math.round(r.height)]}).filter(x=>x[1]>x[2]-40));
console.log('overflow',JSON.stringify(over));
await pg.pdf({path:path.join(d,'Тёплые_окна_в_пол_для_собственников.pdf'),width:'297mm',height:'210mm',printBackground:true});await b.close();})();
