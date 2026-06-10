# CLAUDE BILAN PROFESSIONAL ISHLASH
## Amaliy Bilimlar To'plami

---

## 1. PROMPT CHAINING

Bir promptning natijasi keyingisiga kiradi.

### Nima uchun kerak?
```
YOMON (hammasi birda):
"Login, dashboard, CRUD, hisobot yoz"
→ Claude chalkashadi, sifat tushadi

YAXSHI (zanjir):
Prompt 1: "Login servisini yoz" → natija A
Prompt 2: "A natijasidan foydalanib dashboard yoz" → natija B
Prompt 3: "A va B dan foydalanib CRUD yoz" → natija C
→ Har qadam sifatli, oldingi ustiga quriladi
```

### Zanjir turlari:
```
KETMA-KET:
Prompt 1 → Prompt 2 → Prompt 3
Har biri oldingisiga bog'liq

PARALLEL:
Prompt 1 ─┐
Prompt 2 ─┼→ Yig'ish prompt
Prompt 3 ─┘
Bir-biriga bog'liq emas, keyin birlashtiriladi

SHARTLI:
Prompt 1 → Natija yaxshimi?
  → Ha: Prompt 2A
  → Yo'q: Prompt 2B
```

### Amaliy misol:
```
1. "Bu funksiya nima qiladi? Faqat tushuntir, kod yozma"
   → Tushunish tasdiqlandi

2. "Endi shu funksiya uchun test yoz"
   → Test yozildi

3. "Test asosida implementatsiya yoz"
   → Kod yozildi, testga mos

4. "Kodni review qil, xavfsizlik muammosi bormi?"
   → Tekshirildi
```

---

## 2. CONTEXT ENGINEERING

Claude ga to'g'ri kontekst berish = sifat 2x oshadi.

### XML Teglari Bilan Strukturalash:
```xml
<role>Sen senior Next.js dasturchisi san</role>

<context>
  Stack: Next.js 15 + TypeScript + Supabase
  Mavjud: auth.ts, db.ts
  Muammo: Login sahifa kerak
</context>

<task>
  Email + parol login sahifa yoz
</task>

<constraints>
  - src/app/(auth)/login/page.tsx ga yoz
  - any type ishlatma
  - Mavjud auth.ts ga tegma
</constraints>

<output>
  - Fayl: src/app/(auth)/login/page.tsx
  - Format: TypeScript React komponent
  - Uzunlik: ~100 qator
</output>
```

### Nima uchun XML?
```
Claude XML tuzilmasini yaxshi tushunadi.
Har qism aniq chegaralangan.
Claude qaysi ma'lumot qaysi maqsad uchun — biladi.

Oddiy matn: Claude o'zi ajratadi (xato bo'lishi mumkin)
XML: Aniq ko'rsatilgan → xato kamayadi
```

### Few-shot Misol Berish:
```
Yaxshi natija uchun — misol ko'rsating:

"Quyidagi formatda yoz:

MISOL KIRISH:
getUserById(id: string)

MISOL CHIQISH:
/**
 * Foydalanuvchini ID bo'yicha topadi
 * @param id - UUID format
 * @returns User yoki null
 */
async function getUserById(id: string): Promise<User | null>

Endi shu formatda yoz: createTask(data: TaskInput)"
```

### Negative Prompting:
```
Nima QILMASIN — aniq ayting:

"- Markdown ishlatma
 - Tushuntirish berma
 - Faqat kod
 - any type ishlatma
 - console.log yozma"

Nima qilmasin aytilmasa — Claude o'zi hal qiladi.
Ko'p hollarda siz kutmagan narsa qiladi.
```

### Chiqish Formatini Belgilash:
```
NOANIQ: "Javob ber"
ANIQ:   "Faqat JSON qaytart, boshqa narsa yo'q:
         {\"status\": \"ok\", \"data\": [...]}"

NOANIQ: "Kodni tushuntir"
ANIQ:   "3 qatordan oshmaydigan, oddiy tilda tushuntir"

NOANIQ: "Ro'yxat tuzib ber"
ANIQ:   "Raqamlangan ro'yxat, har band 1 gap"
```

---

## 3. CLAUDE SHAXSINI BILISH

### Claude nima yaxshi qiladi:
```
✓ Kod yozish va tushuntirish
✓ Refaktor va optimizatsiya
✓ Xatolarni topish
✓ Test yozish
✓ Hujjat yozish
✓ Arxitektura tavsiya
✓ Kodni o'qib tahlil qilish
✓ Bir tildan boshqasiga tarjima (kod)
```

### Claude nima qilmaydi yaxshi:
```
✗ Hozirgi vaqt ma'lumoti (bilim chegarasi bor)
✗ Katta loyihani bir sessiyada eslab qolish
✗ 100% aniq raqamlar (taxminiy bo'lishi mumkin)
✗ Murakkab matematik hisob (tekshiring)
✗ O'z xatosini doim sezish
```

### Claude ishonchli bo'lgan holatlar:
```
ISHONCHLI:
- Standart kod pattern lar
- Keng tarqalgan kutubxonalar (React, TypeScript)
- Xato tuzatish (stack trace bilan)
- Refaktor (kichik funksiyalar)

EHTIYOT BO'LING:
- Yangi kutubxona versiyalari (eskirgan bilim)
- Murakkab matematik
- Spesifik API detallar (rasmiy hujjat tekshiring)
- "Ishlaydi" desa ham — sinab ko'ring
```

### Claude xatosini qanday aniqlash:
```
1. IKKITA MARTA SO'RANG:
   "Bu kod to'g'rimi? Xatolik bor bo'lsa toping"
   → Claude o'z xatosini ko'rishi mumkin

2. TEKSHIRISH SO'RANG:
   "Bu yechimning zaif joylari nima?"
   → Muammolarni o'zi aytadi

3. MUQOBIL SO'RANG:
   "Boshqa usul bormi?"
   → Yaxshiroq yechim chiqishi mumkin

4. AMALDA SINANG:
   Kod ishlaganda — ishonchli
   Ishlamasa — Claude xato qildi

5. RASMIY HUJJAT BILAN SOLISHTIRING:
   API, kutubxona — hujjat aniq
```

---

## 4. TOKEN HISOBLASH VA TEJASH

### Token nima?
```
1 token ≈ 0.75 so'z (inglizcha)
1 token ≈ 0.5 so'z (o'zbekcha/ruscha)

Misollar:
"Hello" = 1 token
"getUserById" = 3 token
100 qatorli kod = ~500-800 token
```

### Token sarfi:
```
ARZON (1K token):
- Qisqa savol-javob
- Kichik kod tuzatish
- Tushuntirish

O'RTA (5-15K token):
- Yangi komponent
- Servis funksiya
- Unit test

QIMMAT (20-50K token):
- Yangi modul
- Murakkab refaktor
- Ko'p fayl bir vaqtda

JUDA QIMMAT (50K+):
- Butun loyiha tahlil
- Ko'p sessiya kontekst
```

### Token tejash usullari:
```
1. ANIQ PROMPT:
   Yomon: "Loyiha haqida gapir" (noaniq → ko'p so'raydi)
   Yaxshi: "Faqat auth.ts faylini tushuntir"

2. KERAKLI QISMNI BERING:
   Yomon: Butun loyihani paste qilish
   Yaxshi: Faqat tegishli fayl yoki funksiya

3. /compact ISHLATISH:
   Token 80K ga yetganda → /compact
   Muhim kontekst siqiladi

4. BIR SESSIYA = BIR VAZIFA:
   Ko'p vazifa = ko'p kontekst = ko'p token

5. CHIQISH HAJMINI CHEKLASH:
   "Faqat o'zgargan qismni ko'rsat, butun faylni emas"
   "3 qatordan oshmaydigan javob ber"
```

### Token monitoring:
```
Claude Code da:
- Sessiya token soni ko'rinadi
- 80K ga yetganda /compact
- 100K da sifat tushadi

Tejash hisob:
Yaxshi prompt = 1 iteratsiya = ~5K token
Yomon prompt = 5 iteratsiya = ~25K token
TEJASH: 80%
```

---

## 5. CLAUDE CODE SHORTCUTS

### Asosiy buyruqlar:
```
/plan     → Avval reja ko'rsatadi, keyin bajartadi
           QACHON: Yangi feature, murakkab o'zgarish

/compact  → Sessiyani siqadi, muhim kontekst saqlanadi
           QACHON: Token 80K ga yetganda

/agents   → Sub-agentlarni boshqarish
           QACHON: Parallel ish kerak bo'lganda

Escape    → Bajarilayotgan amalni to'xtatish
           QACHON: Xato ketayotganini sezganda
```

### CLAUDE.md kuchi:
```
CLAUDE.md = Har sessiyada o'qiladigan qoida fayli

Yaxshi CLAUDE.md:
- Stack aniq yozilgan
- Papka tuzilmasi ko'rsatilgan
- Qoidalar aniq (nima qilsin, nima qilmasin)
- Mavjud fayllar ro'yxati

Natija:
Yaxshi CLAUDE.md bilan → savol 3x kamayadi
Yomon CLAUDE.md bilan → har sessiyada bir xil savollar
```

### /plan qachon MAJBURIY:
```
MAJBURIY:
- DB migration
- Auth tizimi o'zgarishi
- Ko'p fayl bir vaqtda o'zgarsa
- Yangi modul

IXTIYORIY:
- Kichik bug fix
- Kichik UI o'zgarish
- Test yozish
```

---

## 6. SESSIYA REJALASHTIRISH

### Bir sessiyada nima qilish mumkin:
```
KICHIK (30 daqiqa, ~10K token):
- 1 ta bug fix
- 1 ta kichik komponent
- 1 ta servis funksiya

O'RTA (1-2 soat, ~30K token):
- 1 ta feature (backend + frontend)
- 1 ta modul refaktor
- Test yozish

KATTA (2-4 soat, ~60K token):
- 1 ta yangi modul
- Murakkab integratsiya
- Arxitektura o'zgarish

EPIC (1+ kun):
- Bo'lib-bo'lib qilish MAJBURIY
- Har qism alohida sessiya
```

### Sessiya boshlash qoidasi:
```
1. Oldingi sessiya xulosasini o'qing
2. Bu sessiyada FAQAT bitta maqsad
3. Maqsadni Claude ga aniq ayting
4. /plan bilan boshlang (murakkab bo'lsa)
5. Har muhim qadam oldidan commit
```

### Sessiya yakunlash qoidasi:
```
1. "Bu sessiyani xulosa qil" → SESSION_LAST.md
2. "STATUS.md ni yangilang"
3. "TODO.md ni yangilang"
4. Git commit: "sessiya: [nima qilindi]"
5. Keyingi sessiya boshlanish nuqtasini yozing
```

### Sessiya sifatini saqlash:
```
Token 50K:  Normal. Davom eting.
Token 80K:  /compact ishlatish vaqti.
Token 100K: Sifat tushadi. Yangi sessiya oching.

Belgilari sifat tushganining:
- Claude oldingi narsani unutadi
- Bir xil savolni qayta beradi
- Kod avvalgi bilan mos kelmaydi
- "Yuqorida aytganimdek" desa — /compact vaqti
```

---

## 7. CLAUDE XATOSINI ANIQLASH VA TUZATISH

### Keng tarqalgan Claude xatolari:
```
1. HALLUCINATION (yo'q narsani ixtiro qilish)
   Belgi: API, funksiya, paket — aslida yo'q
   Tuzatish: Rasmiy hujjat tekshiring

2. ESKIRGAN MA'LUMOT
   Belgi: Kutubxona versiyasi eski
   Tuzatish: "Eng yangi versiya qanday?" so'rang

3. KONTEKST YO'QOTISH
   Belgi: Oldingi narsani unutadi
   Tuzatish: /compact yoki yangi sessiya

4. OVER-ENGINEERING
   Belgi: Oddiy narsa uchun murakkab yechim
   Tuzatish: "Eng oddiy usul nima?" so'rang

5. SCOPE CREEP
   Belgi: So'rilmagan narsa qo'shadi
   Tuzatish: "Faqat so'ralgan narsani qil" qoida
```

### Xatoni qanday tuzatish:
```
KICHIK XATO (bir qator):
"X qatorda xato bor, Y bo'lishi kerak"
→ Faqat o'sha qator tuzatiladi

O'RTA XATO (bir funksiya):
"createTask funksiyasi xato, sababi: [...]"
→ Faqat o'sha funksiya qayta yoziladi

KATTA XATO (butun yondashuv):
"Bu yondashuv noto'g'ri, chunki [...]
 To'g'ri yondashuv: [...]"
→ Arxitektura qayta ko'rib chiqiladi

HECH QACHON:
"Hammasi noto'g'ri, qaytadan yoz"
→ Token isrofi, bir xil xato takrorlanadi
```

### Ishonchlilikni tekshirish:
```
MUHIM KOD UCHUN:
1. "Bu kodni review qil" → o'zi topadi
2. "Bu yechimning muammolari nima?" → zaif joylar
3. Amalda sinash → eng ishonchli usul
4. Rasmiy hujjat bilan solishtirish

QOIDA:
Claude "ishlaydi" desa — sinang.
Claude "ishlamaydi" desa — baribir sinang.
```

---

## TEZKOR NAZORAT RO'YXATI

### Har prompt yozishdan oldin:
```
[ ] Rol aniqmi? ("Sen senior ... san")
[ ] Kontekst yetarlimi? (stack, mavjud holat)
[ ] Vazifa bittami? (ko'p bo'lsa bo'ling)
[ ] Cheklov aniqmi? (nima qilmasin)
[ ] Chiqish formatimi? (qaysi fayl, qanday)
[ ] Misolmi? (few-shot kerakmi)
```

### Sessiya boshida:
```
[ ] Oldingi sessiya o'qildi?
[ ] Bu sessiya maqsadi aniqmi?
[ ] CLAUDE.md yangilimi?
[ ] Token holati qanday?
```

### Sessiya yakunida:
```
[ ] Sessiya xulosa yozildi?
[ ] Git commit qilindi?
[ ] TODO.md yangilandi?
[ ] Keyingi sessiya boshlanish nuqtasi yozildi?
```
