const express=require('express'),multer=require('multer'),helmet=require('helmet'),compression=require('compression'),rateLimit=require('express-rate-limit');
const {execFile}=require('child_process'),fs=require('fs/promises'),os=require('os'),path=require('path');
const MAX=(+process.env.MAX_MB||50)*1048576,CONC=+process.env.CONCURRENCY||2,MAXQ=+process.env.MAX_QUEUE||30;
const app=express();app.set('trust proxy',1);
app.use(helmet({contentSecurityPolicy:false}),compression());
app.use('/api',rateLimit({windowMs:60000,limit:+process.env.RATE||20,message:{error:'rate'}}));
const up=multer({dest:os.tmpdir(),limits:{fileSize:MAX,files:1}});

// طابور: عدد محدود من التحويلات يشتغل بنفس الوقت عشان السيرفر ما يتعلق
let active=0;const q=[];
const run=fn=>new Promise((ok,no)=>{q.push({fn,ok,no});pump()});
function pump(){while(active<CONC&&q.length){const j=q.shift();active++;j.fn().then(j.ok,j.no).finally(()=>{active--;pump()})}}

const sh=(c,a,t=120000)=>new Promise((ok,no)=>execFile(c,a,{timeout:t,killSignal:'SIGKILL',env:{...process.env,HOME:'/tmp'}},e=>e?no(e):ok()));
const lo=(d,a)=>sh('soffice',['-env:UserInstallation=file://'+d+'/profile','--headless','--norestore','--nologo',...a,'--outdir',d]);
const swap=(p,e)=>p.replace(/\.[^.]+$/,'.'+e);
const tools={
 'to-pdf':{ext:/^(docx?|odt|rtf|pptx?|odp|xlsx?|ods|csv)$/,run:async(i,d)=>{await lo(d,['--convert-to','pdf',i]);return swap(i,'pdf')}},
 'pdf-to-word':{ext:/^pdf$/,run:async(i,d)=>{await lo(d,['--infilter=writer_pdf_import','--convert-to','docx:MS Word 2007 XML',i]);return swap(i,'docx')}},
 'compress':{ext:/^pdf$/,run:async(i,d)=>{const o=d+'/out.pdf';await sh('gs',['-sDEVICE=pdfwrite','-dPDFSETTINGS=/ebook','-dNOPAUSE','-dBATCH','-dQUIET','-sOutputFile='+o,i]);return o}},
 'ocr':{ext:/^pdf$/,run:async(i,d)=>{const o=d+'/out.pdf';await sh('ocrmypdf',['-l','ara+eng','--skip-text','--optimize','1',i,o],300000);return o}}
};
const head=async p=>{const h=await fs.open(p);const b=Buffer.alloc(5);await h.read(b,0,5,0);await h.close();return b.toString()};

app.post('/api/:tool',up.single('file'),async(req,res)=>{
 const t=tools[req.params.tool],f=req.file;
 if(!t||!f){if(f)fs.rm(f.path,{force:true});return res.status(400).json({error:'bad'})}
 const e=path.extname(f.originalname).slice(1).toLowerCase(),dir=await fs.mkdtemp(path.join(os.tmpdir(),'job-'));
 let dl=false;
 try{
  if(!t.ext.test(e))return res.status(415).json({error:'type'});
  if(e==='pdf'&&!(await head(f.path)).startsWith('%PDF'))return res.status(415).json({error:'type'});
  if(q.length>=MAXQ)return res.status(503).json({error:'busy'});
  const inp=path.join(dir,'in.'+e);await fs.rename(f.path,inp);
  const out=await run(()=>t.run(inp,dir));
  dl=true;res.download(out,'result'+path.extname(out),()=>fs.rm(dir,{recursive:true,force:true}).catch(()=>{}));
 }catch(err){console.error(req.params.tool,err.message);if(!res.headersSent)res.status(500).json({error:'failed'})}
 finally{fs.rm(f.path,{force:true}).catch(()=>{});if(!dl)fs.rm(dir,{recursive:true,force:true}).catch(()=>{})}
});
app.use((err,req,res,next)=>res.status(err.code==='LIMIT_FILE_SIZE'?413:400).json({error:err.code||'error'}));
app.get('/health',(_,r)=>r.send('ok'));
const D=process.env.DOMAIN,PUB=(process.env.ADSENSE_PUB||'').trim();
app.get('/ads.txt',(_,r)=>PUB?r.type('text/plain').send('google.com, '+PUB.replace(/^ca-/,'')+', DIRECT, f08c47fec0942fa0\n'):r.sendStatus(404));
app.get('/robots.txt',(_,r)=>r.type('text/plain').send('User-agent: *\nAllow: /\n'+(D?'Sitemap: https://'+D+'/sitemap.xml\n':'')));
app.get('/sitemap.xml',(_,r)=>r.type('xml').send('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+['','about','contact','privacy','terms','cookies','pdf-to-word','word-to-pdf','image-to-pdf','jpg-to-pdf','excel-to-pdf','pdf-to-image','pdf-to-jpg','merge-pdf','pdf-to-text','image-to-text'].map(p=>'<url><loc>https://'+D+'/'+p+'</loc></url>').join('')+'</urlset>'));
app.use(express.static(path.join(__dirname,'public'),{maxAge:'1d',extensions:['html']}));

// تنظيف أي مجلدات عالقة أقدم من ساعة
setInterval(async()=>{try{for(const n of await fs.readdir(os.tmpdir())){if(!/^job-/.test(n))continue;const p=path.join(os.tmpdir(),n);if(Date.now()-(await fs.stat(p)).mtimeMs>36e5)await fs.rm(p,{recursive:true,force:true})}}catch{}},6e5).unref();
app.listen(3000,()=>console.log('up :3000'));
