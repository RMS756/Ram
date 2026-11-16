"""Exact Arabic architecture illustration for the exploratory HV candidate."""
from pathlib import Path
import sys,json
from PIL import Image,ImageDraw,ImageFont
OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=True)
S=2;W=1500;H=2110
im=Image.new('RGB',(W*S,H*S),'white');d=ImageDraw.Draw(im);fonts={};regions=[]
def font(n,b=False):
    k=(n,b)
    if k not in fonts:fonts[k]=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n*S)
    return fonts[k]
def text(value,right,y,width,n=23,b=False,color='#244257',center=False):
    ls=[]
    for paragraph in value.split('\n'):
        line=''
        for word in paragraph.split():
            trial=(line+' '+word).strip()
            if d.textlength(trial,font=font(n,b),direction='rtl')>width*S and line:ls.append(line);line=word
            else:line=trial
        ls.append(line)
    for i,line in enumerate(ls):
        xy=((right-width/2 if center else right)*S,(y+i*n*1.65)*S);anchor='mt' if center else 'rt'
        bbox=d.textbbox(xy,line,font=font(n,b),anchor=anchor,direction='rtl');regions.append(bbox)
        d.text(xy,line,font=font(n,b),anchor=anchor,direction='rtl',fill=color)
    return len(ls)*n*1.65
def rect(x,y,w,h,bg='#f4f8fb',edge='#b6c9d6',r=14):
    d.rounded_rectangle((x*S,y*S,(x+w)*S,(y+h)*S),radius=r*S,fill=bg,outline=edge,width=2*S)
def arrow(points,color='#476f89'):
    p=[(int(x*S),int(y*S)) for x,y in points];d.line(p,fill=color,width=3*S,joint='curve')
    (x0,y0),(x,y)=points[-2:]
    if y>y0:tri=[(x,y),(x-6,y-9),(x+6,y-9)]
    elif x<x0:tri=[(x,y),(x+9,y-6),(x+9,y+6)]
    else:tri=[(x,y),(x-9,y-6),(x-9,y+6)]
    d.polygon([(int(a*S),int(b*S)) for a,b in tri],fill=color)
def numbered(n,title,body,y):
    rect(50,y,1400,110)
    d.ellipse((1375*S,(y+16)*S,1421*S,(y+62)*S),fill='#185475')
    d.text((1398*S,(y+39)*S),str(n),font=font(22,True),anchor='mm',fill='white')
    text(title,1350,y+15,1250,n=26,b=True,color='#184e70')
    text(body,1350,y+62,1250,n=21)
text('تصميم تجريبي لدمج G3 وL4 داخل REM',1450,38,1400,n=35,b=True,color='#113b58')
text('مرشّح HV: خمس طبقات، مع قيود مالية ملزمة داخل محرك القرار',1450,104,1400,n=24,color='#506b7e')
text('المدخل: طلب المستخدم + استدعاء الأداة المقترح + التاريخ ومخرجات الأدوات',1450,160,1400,n=22,color='#506b7e')
numbered(1,'المدخلات والسياق','وسم المصادر؛ مخرجات الأداة لا تمنح تفويضًا جديدًا.',225)
arrow([(750,340),(750,365)])
numbered(2,'الكشف: الأدلة المتاحة','مؤشرات السياق النصية؛ مصنّف حقن التعليمات المقترح غير موجود في المسار المختبر.',375)
arrow([(750,490),(750,515)])
numbered(3,'التحليل والتاريخ','حفظ التاريخ ومصدر المعاملات؛ نموذج F4 لا يستخدم المؤشرات السلوكية الأربعة.',525)
arrow([(750,640),(750,662)])
rect(50,670,1400,970,bg='#f7f4fb',edge='#b7a3d1')
text('4 • اتخاذ القرار: مكونات المرشّح داخل طبقة واحدة',1410,690,1320,n=28,b=True,color='#674c91')
rect(355,755,1060,130,bg='#edf8f5',edge='#8dc8b8')
text('G3 • ترجمة الطلب ومطابقة الفعل',1388,772,1005,n=26,b=True,color='#137768')
text('العملية وأثرها، الحساب، المبلغ، الشرط، التكرار، والتنفيذ الناجح السابق.',1388,821,1005,n=22)
arrow([(885,891),(885,925)],'#137768')
rect(355,935,1060,130,bg='#fff',edge='#b9a5d1')
text('حارس الصلاحيات في L4',1388,950,1005,n=25,b=True,color='#674c91')
text('هل العملية والحساب مدعومان، والشرط متحقق، ولا يوجد تناقض أو تكرار؟',1388,999,1005,n=22)
rect(78,943,220,155,bg='#fbeef0',edge='#dba7b2')
text('لم يجتز الحارس\nحجب الاستدعاء\nلا تتجاوزه درجة النموذج',285,963,195,n=19,b=True,color='#9b3444',center=True)
arrow([(352,995),(304,995)],'#b34f60')
text('اجتاز',1040,1074,260,n=18,color='#674c91',center=True)
arrow([(885,1068),(885,1110)],'#674c91')
rect(355,1120,1060,145,bg='#fff',edge='#b9a5d1')
text('المتعلّم ومحرك القرار',1388,1136,1005,n=25,b=True,color='#674c91')
text('F4 → Ridge Logistic Regression → Platt Calibration\nقاعدة الخسارة المتوقعة: Allow / Block؛ تبقى قواعد D1 وD2 ملزمة.',1388,1184,1005,n=21)
arrow([(885,1270),(885,1315)],'#674c91')
rect(355,1325,1060,180,bg='#fff8e8',edge='#d7b65f')
text('القيد الإضافي: المبلغ المباشر في الطلب',1388,1340,1005,n=25,b=True,color='#89620a')
text('مطابقة المبلغ الصريح مع الحساب وأثر العملية ضمن الصياغة المدعومة.\nلا يسمح المتعلّم بمضاعفته أو بحسم تنسيق عددي ملتبس.\nدرجة النموذج لا تتجاوز هذا القيد.',1388,1390,1005,n=21)
rect(78,1332,220,170,bg='#fff5db',edge='#d7b65f')
text('مبلغ مخالف:\nBlock\nصيغة ملتبسة:\nEscalate',285,1350,195,n=19,b=True,color='#89620a',center=True)
arrow([(352,1415),(304,1415)],'#b58c2d')
text('يسمح فقط إذا لم ترفضه القيود وكان قرار L4 هو السماح',1388,1530,1005,n=21,b=True,color='#137768',center=True)
text('الشرط الوصفي غير القابل للتقييم يبقى محجوبًا؛ لا يوجد مراجع بشري في التجربة.',1388,1584,1005,n=18,color='#5f5471',center=True)
arrow([(885,1644),(885,1660),(750,1660),(750,1680)])
numbered(5,'التخفيف والتدقيق','تمرير المسموح أو حجب الاستدعاء؛ تسجيل السبب والنتيجة، ثم تحديث التاريخ.',1690)
rect(50,1840,1400,225,bg='#f6f9fb',edge='#c7d4de')
text('حالة التصميم والدليل',1410,1860,1320,n=24,b=True,color='#244d67')
text('مرشّح تطوير بعد اكتشاف إخفاقات معروفة؛ ليس بديلًا معتمدًا عن REM الأصلي.\nالتجارب إعادة تشغيل لتسجيلات داخل بنك محاكى، دون وكيل حي أو استدعاء نموذج لغوي.\nالمقارنة المنفّذة مع سياسة Progent اليدوية؛ التفوق على الإطار الكامل غير مثبت.\nالقيد الجديد يدعم صياغات محدودة، ويحتاج طلبات يكتبها ويراجعها أشخاص مستقلون.',1410,1912,1320,n=21)
bad=[list(b) for b in regions if b[0]<0 or b[1]<0 or b[2]>W*S or b[3]>H*S]
assert not bad,bad
im.save(OUT/'REM_G3_L4_Integrated_Design_AR.png',dpi=(250,250))
(OUT/'design_validation.json').write_text(json.dumps({'pixels':im.size,'out_of_canvas':bad,'text_lines':len(regions)},indent=2))
print('Saved',OUT/'REM_G3_L4_Integrated_Design_AR.png')
