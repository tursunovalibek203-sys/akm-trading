# SKILL: MiyaAI KNOWLEDGE
## VERSION: 5.0
## YUKLANISH: SO'RALGANDA — faqat kerak bo'lganda (~2,000 token)
## QACHON:
##   S — Texnik qaror: "qaysi texnologiya?" deyilganda
##   T — Bosqich bilimi: faza o'tish, arxitektura qaror
##   U — Muammo pattern: simptom → sabab → yechim

### S — TEXNIK QAROR BILIMI (v5.0)

Bu bo'lim AI ning "qaysi texnologiya qachon to'g'ri" ekanini bilish uchun.
Har qaror taklif qilishda — shu bilim asosida tavsiya beriladi.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FRONTEND ARXITEKTURA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Server Component vs Client Component:
  Server Component qachon:
    → Ma'lumot faqat ko'rsatiladi (o'qiladi)
    → DB yoki API dan to'g'ridan yuklanadi
    → SEO muhim
    → Interaktivlik yo'q (onClick, useState yo'q)

  Client Component qachon:
    → onClick, onChange, hover — interaktivlik bor
    → useState, useEffect ishlatiladi
    → Browser API (localStorage, window) kerak
    → Real-time yangilanish kerak

  XATO: hamma narsani Client Component qilish
  → Server da render qilish mumkin bo'lgan narsani Client qilish
  → Natija: sekin sahifa, ko'p JS bundle

Server Action vs API Route:
  Server Action qachon:
    → Forma submit, bir xil loyiha ichida
    → Tez, kam kod, Next.js bilan integratsiya zo'r
    → Cold start muammo yo'q

  API Route qachon:
    → Tashqi servis (mobil, webhook, boshqa loyiha) so'raydi
    → Auth boshqaruvi aniq kerak (middleware)
    → REST/GraphQL standart kerak

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATE BOSHQARUVI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
useState qachon:
  → Faqat bitta komponent ichida ishlatiladigan holat
  → Forma input, modal ochiq/yopiq, tab tanlangan

useContext qachon:
  → 2-3 ta komponent o'rtasida umumiy holat
  → Prop drilling muammo bo'lganda
  → Auth user, til, tema

Zustand/Jotai qachon:
  → Ko'p sahifada umumiy holat
  → Server dan kelgan ma'lumot keshlanadi
  → Cart, foydalanuvchi sessiyasi, global filter

Server State (TanStack Query, SWR) qachon:
  → API dan kelgan ma'lumot
  → Cache, refetch, loading/error holatlari
  → Real-time yangilanish kerak

  XATO: API ma'lumotni useState ga soling
  → Cache yo'q, refetch yo'q, loading boshqaruvi qiyin

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATABASE QARORLARI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Index qachon:
  → WHERE da ko'p ishlatiladigan field
  → JOIN da ishlatiladigan foreign key
  → ORDER BY da ishlatiladigan field
  → XATO: hamma fieldga index → write sekin bo'ladi

RLS (Row Level Security) qachon:
  → Har foydalanuvchi faqat o'z ma'lumotini ko'rishi kerak
  → Multi-tenant loyiha
  → QOIDA: har jadvalga RLS — yoqilgan, qoida yozilgan

Soft Delete vs Hard Delete:
  Soft Delete (deleted_at field):
    → Tarix muhim (audit, qayta tiklash)
    → Boshqa jadval bu yozuvga bog'liq
    MUAMMO: WHERE deleted_at IS NULL — har so'rovda unutiladi
    YECHIM: View yoki RLS orqali filtr

  Hard Delete:
    → Tarix kerak emas
    → GDPR — ma'lumot o'chirilishi shart
    → Bog'liq jadval yo'q

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
XAVFSIZLIK BILIMI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tokenni qayerda saqlash:
  httpOnly Cookie → TO'G'RI (JS o'qiy olmaydi)
  localStorage   → XATO (XSS hujumiga ochiq)
  sessionStorage → XATO (tab yopilsa yo'qoladi)

Input validatsiya:
  Client + Server IKKALASIDA majburiy
  Client: tez feedback foydalanuvchiga
  Server: xavfsizlik (client chetlab o'tish mumkin)
  XATO: faqat client validatsiya

Environment o'zgaruvchilari:
  NEXT_PUBLIC_ prefix → client ga chiqadi (faqat public narsalar)
  Prefix yo'q → faqat server (API key, DB URL)
  XATO: API key ni NEXT_PUBLIC_ bilan berish
```

---

### T — LOYIHA O'SISH BOSQICHLARI BILIMI (v5.0)

Bu bo'lim "hozir qaysi bosqichdasiz, nima qilish kerak" ni aniqlash uchun.
PROJECT.md dagi faza bilan birgalikda ishlatiladi.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOSQICH 1 — MVP (0-3 oy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MAQSAD: Ishlaydi, foydalanuvchi ishlatishi mumkin

QILISH KERAK:
  ✓ Asosiy feature — faqat bittasi, yaxshi ishlaydi
  ✓ Auth (login/logout)
  ✓ Asosiy DB jadvallar
  ✓ Error handling (yiqilmaydi)
  ✓ Deploy (ishlaydi)

QILMASLIK KERAK:
  ✗ Performance optimization — hali foydalanuvchi yo'q
  ✗ Murakkab caching — ortiqcha
  ✗ Mikroservis — haddan oshiq
  ✗ Test coverage 100% — vaqt sarfi

AI TAVSIYA USULI:
  "MVP bosqichasiz. Bu feature uchun
   sodda yechim tavsiya qilaman — keyin o'stiramiz."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOSQICH 2 — GROWTH (3-12 oy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MAQSAD: Ko'p foydalanuvchi, barqarorlik

QILISH KERAK:
  ✓ Performance — sekin joylarni optimallashtirish
  ✓ Error monitoring (Sentry yoki shunaqa)
  ✓ Test — muhim yo'llar (happy path + xato)
  ✓ Kod tuzilmasi yaxshilash (refaktor)
  ✓ Analytics — nima ishlatiladi?

HALI KUTISH KERAK:
  ✗ Mikroservis — 10K foydalanuvchigacha kerak emas
  ✗ Custom infra — Supabase/Vercel yetarli

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOSQICH 3 — SCALE (12+ oy, 10K+ foydalanuvchi)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MAQSAD: Tezlik, ishonchlilik, katta hajm

QILISH KERAK:
  ✓ Caching strategiyasi (Redis yoki CDN)
  ✓ DB optimizatsiya (index tahlili, query optim.)
  ✓ Rate limiting, queue
  ✓ Monitoring chuqur (APM)
  ✓ CI/CD to'liq avtomatlashgan

AI TAVSIYA USULI:
  Bosqich aniqlanmasa → PROJECT.md dan o'qiladi
  Bosqichga mos bo'lmagan taklif berilsa:
  "Bu SCALE bosqichi yechimi. Hozir MVP/GROWTH
   bosqichasiz — soddaroq yechim ko'proq mos."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QACHON ARXITEKTURA O'ZGARADI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Monolitdan mikroservisga o'tish signal:
  → Bir servis o'zgarishi boshqasini buzadi (hafta)
  → Deploy: bir narsa o'zgarsa hamma deploy
  → Jamoa: 5+ developer, parallel ish qiyin
  → DB: bitta jadval 50M+ qator

Supabase dan custom backendga signal:
  → RLS yetarli emas, murakkab biznes logika
  → Supabase Edge Function ham yetmaydi
  → Tashqi servislar soni 5+ (webhook, queue)
```

---

### U — KENG TARQALGAN MUAMMO PATTERNLARI (v5.0)

Bu bo'lim "ko'p loyihada ko'riladigan xatolar va ularning sababi" bilimi.
AI muammo aniqlashda shu patternga qarab tez diagnoz qiladi.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PERFORMANCE MUAMMOLARI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIMPTOM: Sahifa sekin yuklanyapti
  PATTERN 1 — N+1 query:
    Sabab: Ro'yxat uchun har element uchun alohida DB so'rovi
    Belgi: 100 ta mahsulot → 101 ta DB so'rovi
    Yechim: JOIN yoki include (Prisma: include: {category: true})

  PATTERN 2 — Keraksiz re-render:
    Sabab: Parent o'zgarsa child ham qayta render
    Belgi: useState yuqorida, hamma child yangilanadi
    Yechim: State pastga tushirish, React.memo, useMemo

  PATTERN 3 — Bundle hajmi katta:
    Sabab: Hamma narsa Client Component
    Belgi: JS bundle 500KB+
    Yechim: Server Component, dynamic import

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTH MUAMMOLARI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIMPTOM: Foydalanuvchi boshqa odamning ma'lumotini ko'ryapti
  PATTERN — RLS yoqilmagan yoki noto'g'ri:
    Sabab: Supabase da RLS yoqilmagan jadval
    Belgi: SELECT * FROM payments — hamma to'lovlar ko'rinadi
    Yechim: RLS yoqish + policy: auth.uid() = user_id

SIMPTOM: Login qilsa ham tushib qoladi
  PATTERN — Token muddati:
    Sabab: Access token 1 soat, refresh yo'q
    Yechim: autoRefreshToken: true Supabase config da

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMA VA VALIDATSIYA MUAMMOLARI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIMPTOM: Forma submit bo'lmayapti, sabab noma'lum
  PATTERN — Xato ko'rsatilmayapti:
    Sabab: catch da console.log, foydalanuvchiga xato yo'q
    Yechim: toast.error() yoki error state

SIMPTOM: Bir xil data ikki marta submit bo'lyapti
  PATTERN — Double submit:
    Sabab: isLoading holati yo'q, button disabled emas
    Yechim: const [isLoading, setIsLoading] = useState(false)
            button disabled={isLoading}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARXITEKTURA MUAMMOLARI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIMPTOM: Bir joyni o'zgartirsa boshqa joy buziladi
  PATTERN — Tight coupling:
    Sabab: Komponentlar to'g'ridan to'g'ri bir-birini import
    Belgi: A komponent B ni import, B komponent C ni, C A ni
    Yechim: Servis layer, props orqali, event orqali

SIMPTOM: Bir xil kod bir necha joyda
  PATTERN — DRY buzilishi:
    Sabab: Copy-paste, "tez" deb qo'yilgan
    Belgi: Bir xil validatsiya 3 formada, bir xil API call 5 joyda
    Yechim: Custom hook yoki utility funksiya

SIMPTOM: TypeScript xatolari ko'p, any ishlatilgan
  PATTERN — Type qarz:
    Sabab: Tez yozish uchun any qo'yilgan, to'g'rilanmagan
    Belgi: any count: 15+
    Yechim: Unknown → type guard, generics
    QOIDA: any = FAIL, hech qachon production da

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUPABASE XUSUSIY MUAMMOLAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIMPTOM: Edge Function sekin (800ms+)
  PATTERN — Cold start:
    Sabab: Edge Function uzoq vaqt chaqirilmagan → cold start
    Yechim: Server Action (Next.js) — cold start yo'q
            Yoki: Edge Function ni "warm" saqlash (cron)

SIMPTOM: Realtime ishlamayapti
  PATTERN — RLS + Realtime conflict:
    Sabab: RLS policy Realtime subscription uchun ruxsat bermaydi
    Yechim: Realtime publication uchun alohida policy

SIMPTOM: Migration apply bo'lmayapti
  PATTERN — Migration tartib muammosi:
    Sabab: Jadval yaratilmagan, lekin foreign key unga bog'liq
    Yechim: Har migration oldidan bog'liq jadvallar tekshiriladi
```

---


---

