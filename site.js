(()=>{
const S=Object.assign({name:'حوّل ملفك',owner:'',email:'',phone:'',city:'',hours:''},window.SITE||{});
if(!S.email)S.email='support@'+location.hostname.replace(/^www\./,'');
window.SITE=S;
document.querySelectorAll('[data-s]').forEach(e=>{const v=S[e.dataset.s];
 if(v){e.textContent=v;if(e.tagName==='A'){e.href=({email:'mailto:',phone:'tel:'}[e.dataset.s]||'')+v}}
 else(e.closest('[data-row]')||e).remove()});
document.querySelectorAll('[data-api]').forEach(e=>{if((e.dataset.api==='on')!==(S.api!==false))e.remove()});
const st=document.createElement('style');
st.textContent='.sf{max-width:760px;margin:30px auto 0;padding:18px 16px 28px;border-top:1px solid #8884;font:14px/1.9 Tajawal,Tahoma,sans-serif;text-align:center;color:#888}.sf nav{display:flex;flex-wrap:wrap;justify-content:center;gap:0 4px}.sf a{color:inherit;margin:0 6px;white-space:nowrap}.ck{position:fixed;inset:auto 12px calc(12px + env(safe-area-inset-bottom,0px)) 12px;max-width:560px;margin:auto;background:#1d1b3a;color:#fff;border-radius:14px;padding:12px 14px;font:14px/1.7 Tajawal,Tahoma,sans-serif;z-index:99;box-shadow:0 6px 24px #0006}.ck button{font:inherit;border:0;border-radius:9px;padding:4px 14px;margin:6px 0 0 8px;cursor:pointer}.ck .y{background:#8f78ff;color:#fff}.ck a{color:#ffc2d6}';
document.head.appendChild(st);
const f=document.createElement('footer');f.className='sf';
f.innerHTML='<nav><a href="./">الرئيسية</a><a href="about">عن الموقع</a><a href="contact">اتصل بنا</a><a href="privacy">سياسة الخصوصية</a><a href="terms">شروط الاستخدام</a><a href="cookies">الكوكيز</a></nav><div>© '+new Date().getFullYear()+' '+S.name+'</div>';
document.body.appendChild(f);
let c;try{c=localStorage.getItem('ck')}catch(e){}
if(!c){const b=document.createElement('div');b.className='ck';b.setAttribute('role','dialog');
 b.innerHTML='نستخدم ملفات الكوكيز لتشغيل الموقع وعرض الإعلانات. <a href="cookies">التفاصيل</a><br><button class="y">موافق</button><button>رفض غير الضرورية</button>';
 b.onclick=e=>{if(e.target.tagName!=='BUTTON')return;try{localStorage.setItem('ck',e.target.className==='y'?'1':'0')}catch(_){}b.remove()};
 document.body.appendChild(b)}
})();
