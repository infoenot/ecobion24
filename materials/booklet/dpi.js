const path=require('path');const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const pg=await b.newPage();await pg.goto('file://'+path.join(process.argv[2],'booklet.html'),{waitUntil:'networkidle'});
const r=await pg.evaluate(()=>[...document.querySelectorAll('img')].map(i=>{const q=i.getBoundingClientRect();const W=i.naturalWidth,H=i.naturalHeight;const wi=q.width/96,hi=q.height/96;const s=Math.max(wi/W,hi/H);
const alt=(i.closest('figure')?.textContent||i.closest('.p')?.querySelector('h1,h2,.k')?.textContent||'').trim().slice(0,40);
return [alt,W+'x'+H,Math.round(q.width/96*25.4)+'x'+Math.round(q.height/96*25.4)+'mm',Math.round(1/s)+' dpi']}));
r.forEach(x=>console.log(x.join(' | ')));await b.close();})();
