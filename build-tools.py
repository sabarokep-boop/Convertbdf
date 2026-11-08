# يولّد صفحة مستقلة لكل أداة من public/index.html (شغّله قبل set-domain.sh)
import re,json,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'public'))
idx=open('index.html',encoding='utf-8').read()
L={'pdf':'PDF','word':'Word (docx)','img':'الصور','excel':'Excel أو CSV'}
T=[
('pdf-to-word','تحويل PDF إلى وورد Word','تحويل PDF إلى وورد','pdf','.pdf','حوّل ملف PDF إلى مستند وورد (Word) قابل للتعديل بضغطة زر، مجانًا وبدون تسجيل. المعالجة تتم داخل متصفحك ولا يُرفع ملفك لأي سيرفر.',
 [('هل يحافظ التحويل على التنسيق والصور؟','تستخرج الأداة النص وتضعه في ملف وورد قابل للتعديل، وقد لا تحافظ على الجداول والصور والتنسيق المعقد. تناسب ملفات النصوص أكثر.'),('هل تدعم ملفات PDF الممسوحة ضوئيًا؟','لا، فالملف الممسوح صور وليس نصًا، فلا يوجد نص تستخرجه الأداة.')],'تحويل pdf الى وورد, تحويل pdf الى word, pdf to word بالعربي'),
('word-to-pdf','تحويل وورد Word إلى PDF','تحويل وورد إلى PDF','word','.docx','حوّل ملف وورد (docx) إلى PDF بضغطة زر، مجانًا وبدون تسجيل، ويدعم النصوص العربية من اليمين لليسار. ملفك لا يغادر جهازك.',
 [('ما صيغ وورد المدعومة؟','صيغة DOCX. إذا كان ملفك بصيغة DOC القديمة فافتحه واحفظه بصيغة DOCX ثم ارفعه.'),('هل يبقى التنسيق كما هو؟','يحافظ على النص والصور والجداول الأساسية، وقد يختلف شكل التنسيقات المعقدة قليلًا عن الأصل.')],'تحويل وورد الى pdf, تحويل word الى pdf, docx to pdf'),
('image-to-pdf','تحويل الصور إلى PDF','تحويل الصور إلى PDF','img','image/*','حوّل صورة أو عدة صور إلى ملف PDF واحد بضغطة زر، مجانًا وبدون تسجيل. الصور لا تُرفع لأي سيرفر.',
 [('هل أقدر أجمع أكثر من صورة في ملف واحد؟','نعم، ارفع كل الصور معًا وتُرتَّب في الملف بترتيب رفعها، كل صورة في صفحة.'),('هل تتغير جودة الصور؟','تبقى الصور بجودة عالية ويُضبط حجم كل صورة لتناسب صفحة A4 مع الحفاظ على نسبتها.')],'تحويل صور الى pdf, تحويل صورة الى pdf, image to pdf'),
('jpg-to-pdf','تحويل JPG إلى PDF','تحويل JPG إلى PDF','img','image/*','حوّل صور JPG و PNG إلى PDF بضغطة زر، صورة واحدة أو عدة صور بملف واحد، مجانًا وبدون تسجيل.',
 [('هل يدعم صور الآيفون؟','صور JPG و PNG مدعومة. صيغة HEIC من الآيفون قد لا تُدعم، فحوّلها إلى JPG أولًا.'),('هل الأداة مجانية؟','نعم، مجانية وبدون تسجيل ولا علامة مائية.')],'تحويل jpg الى pdf, تحويل png الى pdf, jpg to pdf'),
('excel-to-pdf','تحويل إكسل Excel إلى PDF','تحويل إكسل إلى PDF','excel','.xlsx,.xls,.csv','حوّل ملف إكسل (Excel) أو CSV إلى PDF بضغطة زر، مجانًا وبدون تسجيل. ملفك يُعالج داخل متصفحك.',
 [('ما الصيغ المدعومة؟','XLSX و XLS و CSV. تظهر أوراق العمل بالتسلسل في ملف PDF واحد.'),('ماذا عن الجداول الكبيرة؟','الجداول العريضة جدًا قد تتقطع على عدة صفحات، ويُفضّل ضبط الجدول قبل التحويل.')],'تحويل اكسل الى pdf, تحويل excel الى pdf, xlsx to pdf'),
('pdf-to-image','تحويل PDF إلى صور','تحويل PDF إلى صور','pdf','.pdf','حوّل كل صفحة من ملف PDF إلى صورة JPG عالية الجودة بضغطة زر، مجانًا وبدون تسجيل وبدون رفع الملف.',
 [('كم صورة أحصل عليها؟','صورة JPG لكل صفحة من ملف PDF، وتنزّلها واحدة واحدة.'),('هل هناك حد لعدد الصفحات؟','لا يوجد حد ثابت، لكن الملفات الكبيرة تأخذ وقتًا أطول لأن المعالجة على جهازك.')],'تحويل pdf الى صور, تحويل pdf الى صورة, pdf to image'),
('pdf-to-jpg','تحويل PDF إلى JPG','تحويل PDF إلى صور JPG','pdf','.pdf','استخرج صفحات PDF كصور JPG بضغطة زر، مجانًا وبدون تسجيل، وبدقة مناسبة للطباعة والمشاركة.',
 [('ما دقة الصور الناتجة؟','تُنتَج الصور بدقة مضاعفة عن العرض العادي لتكون واضحة عند التكبير.'),('هل ملفي آمن؟','نعم، التحويل يتم داخل متصفحك ولا يُرفع الملف لأي سيرفر.')],'تحويل pdf الى jpg, pdf to jpg, تحويل pdf الى صورة jpg'),
('image-to-text','استخراج النص من صورة','استخراج النص من صورة','img','image/*','استخرج النص من أي صورة (OCR) يدعم العربية والإنجليزية، وانسخه أو نزّله كملف نصي، مجانًا وبدون تسجيل. الصورة لا تُرفع لأي سيرفر.',
 [('هل يدعم النص العربي؟','نعم، يقرأ العربية والإنجليزية. تعتمد الدقة على وضوح الصورة وجودتها، والخط اليدوي لا يُقرأ جيدًا.'),('لماذا يتأخر أول تحويل؟','في أول مرة يحمّل المتصفح محرك قراءة النص وبيانات اللغة (بضعة ميغابايت)، ثم تصير المرات التالية أسرع.')],'استخراج النص من صورة, تحويل صورة الى نص, صورة الى نص, image to text, ocr عربي'),
('merge-pdf','دمج ملفات PDF','دمج ملفات PDF','pdf','.pdf','ادمج عدة ملفات PDF في ملف واحد بضغطة زر، مجانًا وبدون تسجيل وبدون رفع ملفاتك لأي سيرفر.',
 [('كم ملف أقدر أدمج؟','ملفين أو أكثر. تُدمج بترتيب رفعها، ولتغيير الترتيب احذف الملفات وارفعها بالترتيب المطلوب.'),('هل أقدر أدمج ملفات محمية بكلمة سر؟','لا، فك الحماية عن الملف أولًا ثم ارفعه.')],'دمج ملفات pdf, دمج pdf, merge pdf'),
('pdf-to-text','استخراج النص من PDF','استخراج النص من PDF','pdf','.pdf','استخرج النص من ملف PDF واحفظه كملف نصي TXT بضغطة زر، مجانًا وبدون تسجيل.',
 [('هل يدعم الملفات الممسوحة ضوئيًا؟','لا، الأداة تستخرج النص الموجود فعلًا داخل الملف، والملف الممسوح صور لا نص فيه.'),('هل يظهر النص العربي سليمًا؟','في أغلب الملفات نعم، لكن قد يختلف ترتيب الكلمات العربية في بعض الملفات حسب طريقة إنشائها.')],'استخراج النص من pdf, تحويل pdf الى نص, pdf to text'),
]
# --- patch index: tools grid, css, expected-type check
grid='<div class="tools">\n'+''.join('<a href="/%s" data-cmd="%s" data-from="%s" data-acc="%s" data-l="%s"><b>%s</b></a>\n'%(t[0],t[2],t[3],t[4],L[t[3]],t[1]) for t in T)+'</div>\n'
idx,n=re.subn(r'<div class="tools">.*?</div>\n(?=<section class="seo">)',lambda m:grid,idx,count=1,flags=re.S);assert n==1
css='.tools a{display:block;text-decoration:none;color:inherit;border:1px solid var(--bd);background:var(--card);border-radius:14px;padding:10px 12px;font-size:.92rem}.tools a:hover{border-color:var(--pri)}\n.seo ol{padding:0 22px;color:var(--mut)}\n</style>'
if '.tools a{' not in idx: idx=idx.replace('</style>',css,1)
chk="async function run(){\n if(window.EXPECT&&files.some(f=>kind(f)!==window.EXPECT))return say('هذه الأداة تقبل ملفات '+window.EXPECT_L+' فقط. لباقي التحويلات ارجع للصفحة الرئيسية.',true);"
if 'window.EXPECT' not in idx:
    assert "async function run(){" in idx;idx=idx.replace("async function run(){",chk,1)
open('index.html','w',encoding='utf-8').write(idx)
# --- pages
for slug,h1,cmd,exp,acc,intro,faq,kw in T:
    s=idx;title=h1+' أونلاين مجانًا بدون تسجيل – حوّل ملفك'
    def sub(p,r,fl=0):
        global s
        s,n=re.subn(p,lambda m:r,s,count=1,flags=fl);assert n==1,p
    sub(r'<title>.*?</title>','<title>'+title+'</title>',re.S)
    sub(r'<meta name="description" content=".*?">','<meta name="description" content="'+intro+'">')
    sub(r'<meta name="keywords" content=".*?">','<meta name="keywords" content="'+kw+', '+h1+', حوّل ملفك">')
    sub(r'<meta property="og:title" content=".*?">','<meta property="og:title" content="'+h1+' أونلاين مجانًا – حوّل ملفك">')
    sub(r'<meta property="og:description" content=".*?">','<meta property="og:description" content="'+intro+'">')
    sub(r'<link rel="canonical" href=".*?">','<link rel="canonical" href="https://__DOMAIN__/'+slug+'">')
    ld={"@context":"https://schema.org","@graph":[{"@type":"WebApplication","name":h1,"applicationCategory":"UtilitiesApplication","operatingSystem":"Any","inLanguage":"ar","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"description":intro},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}]}
    sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>',re.S)
    sub(r'<h1>.*?</h1>','<h1><span>'+h1+'</span> أونلاين مجانًا</h1>',re.S)
    sub(r'<p class="sub">.*?</p>','<p class="sub">'+intro+'</p>',re.S)
    s=s.replace('id="cm" placeholder=','id="cm" value="'+cmd+'" placeholder=',1)
    sub(r'(<input id="fi"[^>]*accept=")[^"]*"',r'\1'+acc+'"' if False else '<input id="fi" type="file" multiple hidden accept="'+acc+'">')
    s=s.replace('<small>Word · Excel · صور · PDF</small>','<small>'+L[exp]+'</small>',1)
    s=s.replace('<b>حوّل ملفك</b>','<a href="/" style="color:inherit;text-decoration:none"><b>حوّل ملفك</b></a>',1)
    s=s.replace('</head>',"<script>window.EXPECT='%s';window.EXPECT_L='%s';</script>\n</head>"%(exp,L[exp]),1)
    rel=''.join('<li><a href="/%s" data-cmd="%s" data-from="%s" data-acc="%s" data-l="%s">%s</a></li>'%(t[0],t[2],t[3],t[4],L[t[3]],t[1]) for t in T if t[0]!=slug)
    seo='<section class="seo">\n<h2>كيف تستخدم أداة «%s»؟</h2>\n<ol><li>اضغط على المنطقة أعلاه واختر الملف، أو اسحبه وأفلته.</li><li>الأمر مكتوب جاهزًا في خانة الكتابة، فاضغط «حوّل».</li><li>نزّل الملف الناتج بعد ثوانٍ.</li></ol>\n<p>تعمل الأداة داخل متصفحك، فلا يُرفع ملفك لأي سيرفر. اقرأ <a href="/privacy">سياسة الخصوصية</a>.</p>\n<h2>أسئلة شائعة</h2>\n%s<details><summary>هل الأداة مجانية؟</summary><p>نعم، مجانية وبدون تسجيل.</p></details>\n<h2>أدوات أخرى</h2><ul>%s</ul>\n</section>'%(h1,''.join('<details><summary>%s</summary><p>%s</p></details>\n'%(q,a) for q,a in faq),rel)
    sub(r'<section class="seo">.*?</section>',seo,re.S)
    open(slug+'.html','w',encoding='utf-8').write(s)
print('built',len(T),'pages')

# RELATIVIZE: روابط نسبية عشان تشتغل على الدومين الخاص وعلى github.io/اسم-المستودع
import glob
for f in glob.glob('*.html'):
    s=open(f,encoding='utf-8').read()
    s=re.sub(r'(href|src)="/(?!/)([^"]*)"',lambda m:'%s="%s"'%(m.group(1),m.group(2) or './'),s)
    open(f,'w',encoding='utf-8').write(s)
