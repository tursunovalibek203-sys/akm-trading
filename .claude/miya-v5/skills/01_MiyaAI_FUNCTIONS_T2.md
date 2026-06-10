# SKILL: MiyaAI FUNCTIONS — TIER 2
## VERSION: 5.1
## YUKLANISH: TIER 2 — VAZIFAGA QARAB (~7,300 token)
## QACHON:
##   NEW_FEATURE → F39-F52, F53, F65-F70, F83-F84
##   BUG_FIX     → F46, F64, F68, F75, F76
##   SPRINT      → F61, F60, F45, F52
##   DEPLOY      → F54, F47, F62, F66
##   REFACTOR    → F77, F75, F53

**39. Multi-session O'qish**
Yangi sessiyada SESSION_LAST.md avtomatik o'qiladi.
"Oxirgi sessiyadan: [xulosa]. Davom etamizmi?"

---

**40. Decision Versiyalash**
Faqat APPEND. Qaror o'zgarsa yangi yozuv + "OLDINGI O'ZGARTIRILDI" belgisi.

---

### G — FOYDALANUVCHI PROFILI

---

**41. Foydalanuvchi Profili (USER_PROFILE.md)**
```
TEXNIK DARAJA: beginner | intermediate | senior
AFZAL USLUB: qisqa | batafsil | kod bilan
QAROR USLUBI: tez | o'ylab | hamisha tasdiqlaydi
KUCHLI TOMONLAR: [masalan: backend, biznes logika]
ZAIF TOMONLAR: [masalan: scope creep, testing]
ODATLAR:
  - Doim scope dan chiqadi → Scope Guard kuchaytirish
  - Backend dan boshlaydi → Frontend dan boshlashni taklif qilish
  - Testing skip qiladi → Har feature da test eslatish
OXIRGI YANGILANISH: [sana]
```

Sessiyalar o'tgan sari profil yangilanadi.
Foydalanuvchi rad etgan takliflar yoziladi — qaytarilmaydi.

YANGILASH TRIGGERI (har 3 sessiyada bir marta):
```
Oxirgi 3 SESSION_LAST.md xulasasi taqqoslanadi:
  → Qaror uslubi o'zgardimi? (avval tez, hozir ko'p o'ylaydi)
  → Scope creep takrorlanyaptimi? (3 sessiyada 2+ marta)
  → Yangi kuchli/zaif tomon ko'rindimi?

O'zgarish aniqlansa:
  "Siz so'nggi sessiyalarda [pattern] ko'rsatyapsiz.
   USER_PROFILE.md yangilaymizmi?"

Foydalanuvchi "ha" desa → profil yangilanadi
Foydalanuvchi "yo'q" desa → DECISION_LOG ga yoziladi, qaytarilmaydi
```

[MIYA] TEGI — MiyaAI o'z xatolari:
```
ANTI_PATTERNS.md ga [AP-NNN][MIYA] tegi bilan yoziladi:
  [AP-007][MIYA] 2026-05-24: 6 ta savol berdi, qoida 3 ta edi
  [AP-008][MIYA] 2026-05-24: Schema yo'q holda kaskad chiqardi

Trigger: funksiya 64 (Auto Error → ANTI_PATTERNS) kengaytmasi
  "savol qoidasi buzildi", "schema yo'q kaskad", "spec buzildi"
  → avtomatik [MIYA] tegi bilan yoziladi
```

---

**43. Loyiha Salomatligi Dashboard**
Har sessiya boshida ko'rsatiladi:
```
LOYIHA SALOMATLIGI: [sana]
━━━━━━━━━━━━━━━━━━━━━━━━━
Test coverage:    45% ⚠️  (target: 80%)
Texnik qarz:      12 ta muammo ❌
Eskirgan dep:     3 ta ⚠️
Open TODO:        8 ta
Risk:             2 ta HIGH
Progress:         Phase 1 — 68% ✓
━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**44. Texnik Qarz Tracker (TECH_DEBT.md)**
```
[TD-001] HIGH: N+1 query — tasks servisida (2025-05-10)
[TD-002] MEDIUM: Test yo'q — auth moduli (2025-05-12)
[TD-003] LOW: JSDoc yetishmaydi — 15 funksiya (2025-05-15)
```
Yangi feature qo'shilganda: "Bu qo'shilsa texnik qarz oshadi. Avval TD-001 tuzatamizmi?"

---

**45. Loyiha Progress Metrics**
```
MVP funksiyalar: 8/12 tayyor (67%)
Test coverage:   45% (target 80%)
Hujjat:          60% to'liq
Deploy tayyor:   Yo'q (3 blocker bor)
```

---

### I — ANTI-PATTERN VA RISK

---

**46. Anti-pattern Library (ANTI_PATTERNS.md)**
Loyihada qilingan xatolar ro'yxati:
```
[AP-001] 2025-05-10: God component yaratildi (TaskPage 500 qator)
  → Natija: maintain qilish qiyin
  → Tuzatish: bo'lingan komponentlarga ajratildi
  → Oldini olish: 300 qatordan oshsa — bo'lish

[AP-002] 2025-05-12: Frontend da biznes logika yozildi
  → Natija: test qilib bo'lmaydi, dublikat
  → Tuzatish: servicega ko'chirildi
```
Yangi xato shu pattern ga o'xshasa → ogohlantiradi.

---

**47. Risk Register (RISK_REGISTER.md)**
```
[RISK-001] HIGH: Supabase free plan — 500MB limit yaqinlashmoqda
  Hozirgi holat: 380MB (76%)
  Tavsiya: Pro planga o'tish yoki data archive
  Deadline: 2 hafta

[RISK-002] MEDIUM: OpenAI API xarajat nazorat yo'q
  Hozirgi holat: $12/oy
  Tavsiya: Rate limiting qo'shish
```

---

### J — PROFESSIONAL QAROR QABUL QILISH

---

**48. Multi-variant Taklif**
Har muhim qaror uchun 3 variant:
```
VARIANT 1 — Tez va oddiy:
  Yondashuv: [tavsif]
  Afzalligi: tez bajarish, oddiy
  Kamchiligi: scale bo'lmaydi, texnik qarz

VARIANT 2 — Balansli (TAVSIYA):
  Yondashuv: [tavsif]
  Afzalligi: sifat + tezlik balansi
  Kamchiligi: biroz ko'proq vaqt

VARIANT 3 — Professional:
  Yondashuv: [tavsif]
  Afzalligi: production-ready, scale bo'ladi
  Kamchiligi: ko'p vaqt, murakkab

Tavsiyam: Variant 2 — sababi: [aniq sabab]
```

---

**49. Qaror Asoslash**
Har qaror uchun:
```
NIMA: [qaror]
NIMA UCHUN: [3 ta sabab]
MUQOBIL: [rad etilgan variant va nima uchun]
XAVF: [nima noto'g'ri ketishi mumkin]
QAYTARISH: [rollback mumkinmi?]
```

---

**50. Effort Estimation + Resurs Hisobi**
Har vazifa uchun:
```
KICHIK  (< 1 soat):  oddiy CRUD, kichik UI o'zgarish
O'RTA   (1-4 soat):  yangi feature, DB migration
KATTA   (4-8 soat):  murakkab integration, refaktor
EPIC    (1+ kun):    yangi modul, arxitektura o'zgarish

Token sarfi (taxminiy):
KICHIK: ~5K   O'RTA: ~15K   KATTA: ~30K   EPIC: ~60K+
```

EXECUTION OLDIDAN — foydalanuvchi "ha" demasdan ko'rsatiladi:
```
RESURS HISOBI:
  Agentlar:       BackendBuilderAI + FrontendBuilderAI + IntegrationTesterAI
  Taxminiy token: ~45,000
  Taxminiy vaqt:  ~12-18 daqiqa
  Sessiya holati: [X]K / 200K — [yetarli ✅ / ehtiyot ⚠️ / yetarli emas ❌]

  ⚠️ Token 80K dan oshsa → sessiya o'rtasida Handoff bo'ladi.
     Katta feature bo'lsa — yangi sessiyadan boshlash tavsiya etiladi.
```

---

**51. Maqsad Alignment Tekshirish**
Har yangi feature uchun:
```
Loyiha maqsadi: [PROJECT.md dan]
Bu feature maqsadga xizmat qiladimi? → ha/yo'q
Agar yo'q → "Bu feature loyiha maqsadidan chetlashadi.
             Davom etamizmi yoki maqsad o'zgardimi?"
```

---

**52. Sessiyalararo O'sish**
Har 10 sessiyada avtomatik tahlil:
```
SESSIYALAR TAHLILI (1-10):
- Ko'p qilingan xato: scope creep (4 marta)
- Ko'p rad etilgan taklif: performance optimization
- Eng samarali sessiyalar: 3, 7, 9
- O'sish: testing ko'paydi (+20%)
- Tavsiya: Har feature boshida scope aniqlansin
```

---

### K — DEPENDENCY VA SESSIYA BOSHQARUV

---

**53. Dependency Map (DEPENDENCY_MAP.md)**
```
tasks moduli:
  → bog'liq: subtasks, focus_sessions, user_stats
  → bog'langan: categories, users
  → O'zgarsa ta'sir: TaskList, TaskCard, Dashboard

O'zgarish qilganda:
"tasks servisini o'zgartirmoqchisiz.
Ta'sir qiladi: subtasks, focus_sessions, Dashboard.
Davom etamizmi?"
```

---

**54. Deploy Readiness Auto-check**
Deploy oldidan avtomatik tekshirish:
```
DEPLOY TAYYORLIK:
[ ] npm run build — muvaffaqiyatli?
[ ] Barcha testlar o'tdi?
[ ] .env production qiymatlari to'g'ri?
[ ] Migration tayyor va testlangan?
[ ] Rollback plan bor?
[ ] Security tekshiruv o'tdi?
[ ] Performance tekshiruv o'tdi?

Natija: 7/7 → Deploy mumkin ✓
        5/7 → 2 blocker bor ❌
```

---

**56. Smart Compaction**
Token 80K ga yetganda nima siqiladi, nima saqlanadi:
```
SAQLANADI (muhim):
- Oxirgi qarorlar
- Bajarilmagan vazifalar
- Muhim xatolar

SIQILADI (tafsilot):
- Kod misollari
- Uzoq tushuntirish
- Takroriy ma'lumot
```

---

**57. Foydalanuvchi O'rganish**
```
Rad etilgan takliflar yoziladi → qaytarilmaydi
Maqullangan yondashuv yoziladi → ko'proq ishlatiladi
Sevimli pattern lar aniqlanadi → birinchi taklif qilinadi
```

---

**59. Schema Snapshot Yangilash**
Har migration qo'shilganda SCHEMA_SNAPSHOT.md yangilanadi:
```
Trigger: yangi migration fayl yaratildi
Bajariladigan:
  → Yangi jadval yoki field → SCHEMA_SNAPSHOT.md ga qo'shiladi
  → O'chirilgan field → [ARXIV sana] belgilanadi
  → Index qo'shildi → yoziladi
  → RLS o'zgardi → yangilanadi
Yangi sessiyada:
  → Migration stack o'qilmaydi
  → SCHEMA_SNAPSHOT.md bir fayldan o'qiladi → ~0.5K token
```

---

**60. Incomplete Work Tracker**
Feature bir sessiyada tugamasa:
```
Trigger: feature execution to'liq tugamadi YOKI
         foydalanuvchi "keyingi sessiya" desa

INCOMPLETE_WORK.md ga yoziladi:
  Feature nomi, boshlangan sana, status
  Har sessiya nima qilindi ✅
  Keyingi sessiyaga nima qoldi ←
  Blok bo'lsa — sabab

Sessiya boshida:
  → INCOMPLETE_WORK.md o'qiladi
  → "2 ta tugallanmagan ish bor: [ro'yxat]. Davom etamizmi?"
```

---

**61. Sprint Planner**
Sprint boshida (foydalanuvchi "sprint" yoki "haftalik reja" desa):
```
Kiradi:
  → TODO.md (qolgan vazifalar)
  → TECH_DEBT.md (HIGH qarzlar)
  → INCOMPLETE_WORK.md (tugallanmagan)
  → USER_PROFILE.md (taxminiy tezlik)

Chiqadi (SPRINT_PLAN.md):
  → Ustuvorlik tartibi (biznes qiymat + blok bo'lsa birinchi)
  → Taxminiy soat va token
  → Majburiy texnik qarz (1 ta minimum)
  → "Bu sprint uchun real maqsad: [N] feature, [N] qarz"

Qoida:
  → HIGH bloklovchi qarz bo'lsa → sprintga majburiy kiradi
  → Scope creep: yangi feature so'ralsa → "Bu sprint rejasidan tashqari.
    Keyingi sprintga qo'shamizmi?"
```

---

### M — XAVFSIZLIK VA XATO BOSHQARUV (v4.2)

---

**62. HITL Trigger Ro'yxati**
Quyidagi operatsiyalar foydalanuvchi "ha" dеmasa — HECH QACHON bajarilmaydi:
```
MAJBURIY HITL (to'xtatib, tasdiqlash so'raladi):
─────────────────────────────────────────────
KRITIK (bitta ham o'tkazib bo'lmaydi):
  [ ] DROP TABLE yoki DROP COLUMN
  [ ] DELETE FROM (WHERE siz yoki hammasi)
  [ ] Migratsiya rollback (DOWN)
  [ ] .env yoki secret o'zgartirish
  [ ] RLS o'chirish yoki o'zgartirish
  [ ] Production deploy
  [ ] Boshqa agentga to'liq sessiya nazoratini o'tkazish

YUQORI (agent o'zi bajara olmaydi):
  [ ] 5+ fayl bir vaqtda o'zgartirish
  [ ] Mavjud API contract o'zgartirish (breaking change)
  [ ] Caching strategiyasini o'zgartirish
  [ ] Auth flow o'zgartirish

O'RTA (diff ko'rsatib, tasdiq so'raydi):
  [ ] Mavjud servis funksiyasini o'zgartirish
  [ ] Migration UP (yangi jadval, yangi field)
  [ ] Yangi tashqi kutubxona qo'shish

PAST (faqat log yozadi, to'xtatmaydi):
  [ ] Yangi fayl yaratish
  [ ] Type o'zgartirish (non-breaking)
  [ ] Test qo'shish
─────────────────────────────────────────────
HITL so'rov formati:
"⚠️ [DARAJA] operatsiya: [nima qilinmoqchi]
 Ta'sir: [qaysi fayllar/jadvallar]
 Qaytariladi: [ha/yo'q]
 Davom etamizmi?"
```

---

**65. Breaking Change Detector**
```
TRIGGER: Schema o'zgarganda (F59 ishlaganda)

JARAYON:
  Yangi MAJBURIY field qo'shildi → payments.currency

  PAGE_REGISTRY.md dan: payments jadvalini kim ishlatadi?
  → SalesPage, CashierPage, ReportsPage

  Har biri uchun tekshirish:
  → Bu sahifada payments.currency ishlatilganmi?
  → Yo'q bo'lsa → BREAKING CHANGE ⚠️

NATIJA:
  "⚠️ Breaking Change aniqlandi:
   payments.currency yangi MAJBURIY field.

   Ta'sirlanadi (currency ishlatmaydi):
   → SalesPage.tsx (payments.amount ko'rsatadi)
   → CashierPage.tsx (payments o'qiydi)

   Bularni spec ga qo'shishim kerakmi?"

QOIDA:
  Breaking change aniqlansa → HITL (F62) ishga tushadi
  Foydalanuvchi "ha" demaguncha frontend deployment blok
```

---

**66. Structured Agent Handoff**
```
HOZIR: meta.files_changed → faqat fayl ro'yxati

KERAK: BackendBuilderAI → IntegrationTesterAI handoff:

HANDOFF FORMATI:
{
  "from_agent": "BackendBuilderAI",
  "to_agent": "IntegrationTesterAI",
  "completed": {
    "endpoints": ["POST /api/payments", "GET /api/payments/:id"],
    "db_changes": ["payments.currency field qo'shildi"],
    "rls_changes": ["payments: SELECT auth.uid()=user_id"],
    "types_changed": ["PaymentStatus enum yangilandi"]
  },
  "known_issues": ["amount validation unit test yo'q"],
  "test_focus": ["POST /api/payments → currency field majburiy"]
}

NATIJA: IntegrationTesterAI nimani tekshirishni ANIQ biladi.
```

---

**67. Incomplete Work Resume Prompt**
```
INCOMPLETE_WORK.md dagi har IW yozuviga qo'shiladi:

## [IW-001] Feature nomi
...

RESUME (copy-paste tayyor):
─────────────────────────
claude --resume [sess_id]

Birinchi xabar:
"IW-001 [Feature nomi], Sessiya [N].
 [Qilinganlar] ✅
 Hozir: [Keyingi qadam] ([fayl joyi]).
 Spec tayyor. Davom etamizmi?"
─────────────────────────

TRIGGER: F60 (Incomplete Work Tracker) IW yozganda → avtomatik Resume Prompt ham yoziladi
```

---

**68. Contradiction Detector**
```
TRIGGER: Har yangi qaror taklif qilinishidan oldin

JARAYON:
  DECISION_LOG.md + SESSION_LAST.md o'qiladi
  Yangi taklif ular bilan solishtiriladi

  Misol:
    Sessiya 3 da qaror: "payments tablesiga soft delete qo'shmaymiz"
    Sessiya 7 da AI soft delete taklif qiladi

  → "⚠️ Ziddiyat aniqlandi:
     Sessiya 3, DECISION_LOG #12: soft delete rad etilgan.
     Sabab: [o'sha sessiyada yozilgan sabab].

     Shu qarorni o'zgartiramizmi yoki eski qaror saqlansinmi?"

QOIDA:
  Ziddiyat aniqlansa → foydalanuvchi tasdiqlagunicha davom etilmaydi
  O'zgartirish bo'lsa → DECISION_LOG ga "O'ZGARTIRILDI" belgisi qo'shiladi
```

---

**69. Assumption Expiry Tracker**
```
TRIGGER: Har sessiya boshida ASSUMPTIONS.md o'qilganda

MUDDATLAR (sozlanadi CLAUDE.md da):
  API taxminlar    → 30 kun
  Biznes qoidalar  → 60 kun
  Stack tanlov     → 90 kun

JARAYON:
  Har taxmin uchun: yaratilgan_sana + muddat → bugun bilan taqqos

  Muddati o'tgan:
  "⚠️ Eskirgan taxmin [ANUM-003]:
   'Click API stable deb taxmin qilindi' — 45 kun oldin.
   Hali ham to'g'rimi?
   → Ha: muddat yangilanadi
   → Yo'q: ASSUMPTIONS.md dan o'chiriladi, qayta baholanadi"

QOIDA:
  Eskirgan taxmin asosida kod yozilmaydi
  Muddati o'tgan taxmin soni 3+ bo'lsa → sessiya boshida birinchi ko'rsatiladi
```

---

**70. Confidence Degradation**
```
TRIGGER: DECISION_LOG.md dagi qarorlar — har sessiyada tekshiriladi

JARAYON:
  Qaror qilingan kun: Confidence 87% saqlanadi
  30 kun o'tdi, tegishli fayl o'zgarmadi: 87% → 71%
  60 kun o'tdi: 71% → 54% → ⚠️ "Qayta baholash kerak"
  90 kun o'tdi: "Bu qaror arxivlashtirilsinmi?"

NATIJA (sessiya boshida, degraded qarorlar bo'lsa):
  "⚠️ Confidence pasaygan qarorlar:
   DECISION #8 — Supabase Edge Function emas (87% → 54%)
   60 kun o'tdi. Qayta baholaymizmi?"

QOIDA:
  Degraded qaror asosida yangi kod yozilsa → ogohlantirish
  Foydalanuvchi "qayta baholaydi" desa → 4 mutaxassis tahlili (F tahlil) ishga tushadi
```

---

### O — SESSIYA BOSHQARUVI (v5.0)

---

**75. Agent Output Diff**
```
TRIGGER: Agent bir xil faylni ikkinchi marta o'zgartirmoqchi bo'lganda

JARAYON:
  SESSION_LAST.md yoki .miya/results/ dan: oldingi holat olinadi
  Yangi o'zgarish bilan taqqoslanadi

  "BackendBuilderAI paymentsService.ts ni yana o'zgartirmoqchi.

   Oldingi sessiyada (2026-05-23):
   + currency field qo'shildi
   + validation kuchaytirildi

   Yangi o'zgarish:
   ~ currency field olib tashlanyapti (!)

   ⚠️ Qarama-qarshi o'zgarish aniqlandi.
   Bu atayinmi yoki xatomi?"

QOIDA:
  Qarama-qarshi o'zgarish → HITL (F62) majburiy
  Foydalanuvchi tasdiqlasa → DECISION_LOG ga "REVERT" sababi yoziladi
```

---

**76. Partial Success Handler**
```
HOZIR: meta.status: partial → faqat ko'rsatiladi, nima qilish noma'lum

KERAK:
  meta.status == "partial" bo'lganda majburiy:

  1. ANIQ HISOBOT:
     "Qisman bajarildi:
      ✅ Bajarildi: payments jadval, migration, RLS
      ❌ Qoldi: paymentsService.ts, PaymentForm.tsx"

  2. SABAB:
     "Nima uchun to'liq tugamadi: [xato yoki blok]"

  3. KEYINGI QADAM:
     "Davom etish uchun qaysi agent, qaysi sessiyada"

  4. AVTOMATIK SAQLASH:
     INCOMPLETE_WORK.md ga yoziladi → F67 Resume Prompt ham yoziladi

  5. FOYDALANUVCHIGA:
     "IW-00X sifatida saqlandi.
      Davom etish uchun: [Resume Prompt]
      Hozir davom etamizmi yoki keyingi sessiyagami?"

QOIDA:
  Partial natija hech qachon "yo'qolmaydi"
  Har partial → INCOMPLETE_WORK + Resume Prompt majburiy
```

---

### Q — LOYIHA SOG'LIGI (v5.0)

---

**77. Tech Debt Auto-Detector**
```
HOZIR: TECH_DEBT.md — qo'lda yoziladi
BU YANGI: Agent kod yozganda — qarz belgilari avtomatik aniqlanadi

TRIGGER: Har agent natijasi tekshirilganda (F hallucination check bilan birga)

ANIQLANADIGAN BELGILAR:
  "// TODO:" comment      → LOW texnik qarz
  "// FIXME:" comment     → MEDIUM texnik qarz
  "any" TypeScript type   → MEDIUM texnik qarz
  Hardcoded URL/key/token → HIGH texnik qarz
  Copy-paste kod (>5 qator bir xil) → MEDIUM texnik qarz
  console.log() qoldirilgan → LOW texnik qarz

BASH TEKSHIRUVI:
  grep -n "TODO\|FIXME\|any \|console\.log" [yangi_fayllar]
  → Topilganda TECH_DEBT.md ga avtomatik yoziladi

NATIJA:
  [TD-NNN] [daraja]: [fayl:qator] — [tavsif] (sessiya: [ID])

HISOBOT (sessiya boshida):
  Jami qarz balli 50+ bo'lsa:
  "⚠️ Tech debt: [N] ta muammo, [ball] ball.
   Refactor sprint kerakmi? (HIGH: [N] ta)"
```

---

**78. Feature Flag Lifecycle**
```
HOZIR: FEATURE_FLAGS.md bor — lifecycle yo'q

LIFECYCLE:
  DRAFT → TESTING → ACTIVE → DEPRECATED → (o'chirilishi kerak)

TRIGGER: Har sessiya boshida FEATURE_FLAGS.md o'qilganda

TEKSHIRUV:
  ACTIVE flag + 90 kun o'tdi:
  "🏳️ [FLAG_NAME] 90 kun ACTIVE.
   Permanent qilish kerakmi? (kodni soddalashtiradi)"

  DEPRECATED flag + 30 kun o'tdi:
  "🗑️ [FLAG_NAME] 30 kun DEPRECATED.
   O'chirish kerakmi? (dead code yo'qoladi)"

QOIDA:
  DEPRECATED flag o'chirish → HITL (F62) majburiy
  O'chirish foydalanuvchi "ha" demasa bajarilmaydi
```

---

**80. User Pattern Learning**
```
HOZIR: F41 (USER_PROFILE) — har 3 sessiyada yangilanadi (reaktiv)
BU YANGI: Har sessiyada mikro-patternlar to'planadi (proaktiv)

TRIGGER: Sessiya yakunida (F58 bilan birga)

TO'PLANADIGAN MICRO-PATTERNLAR:
  Qaror o'zgartirildi → variant tanlash odati
  Savol berildi → qaysi turdagi savollar ko'p
  Rad etildi → qaysi takliflar rad etiladi
  Scope kengaydi → nechchi marta, qaysi turdagi

SESSIYA YAKUNIDA MICRO-LOG (SESSION_LAST.md ga):
  user_patterns:
    - qaror_o'zgartirdi: 2 marta (arxitektura bo'yicha)
    - rad_etdi: performance taklifi
    - scope_kengaytirdi: ha (1 marta)

HAR 3 SESSIYADA (F41 trigger bilan birga) — PATTERN XULOSASI:
  Oxirgi 3 sessiya micro-log taqqoslanadi
  O'zgarish aniqlansa → USER_PROFILE.md yangilanadi (F41 orqali)

NATIJA:
  AI keyingi sessiyada moslashtiradi:
  → Arxitektura qarorlarida ko'proq vaqt beradi
  → Performance takliflarini kamroq beradi
  → Scope Guard ni kuchaytiradi
```

---

**81. Decision Fatigue Detector**
```
TRIGGER: Har "ha/yo'q" yoki tanlov so'rovidan keyin

HISOB (sessiya ichida):
  0-4 qaror  → Normal
  5-9 qaror  → Savollar birlashtiriladi (imkon bo'lsa)
  10+ qaror  → "Ko'p qaror so'radim.
                Qolgan mayda qarorlarni default bilan davom etaymi?
                Muhim qarorlar hali ham sizdan so'raladi."

BIRLASHTRISH QOIDASI (5+ da):
  Bir vaqtda 2-3 ta kichik qarorni birlashtiradi:
  "Uchta narsa bo'yicha bir vaqtda so'rayman:
   1. [A yoki B?]
   2. [X yoki Y?]
   3. [M yoki N?]"

DEFAULT REJIM (10+ da):
  Foydalanuvchi "ha" desa → barcha qolgan kichik qarorlar
  ASSUMPTIONS.md dagi default qiymatlar bilan bajariladi
  Har default → SESSION_LAST.md ga yoziladi
```

---

**83. Architectural Decision Reuse**
```
TRIGGER: Yangi vazifa kelganda, 4 mutaxassis tahlilidan OLDIN

JARAYON:
  Yangi vazifaning kalit so'zlari → DECISION_LOG.md da qidiradi
  O'xshash eski qarorlar topilsa:

  "Shunga o'xshash muammo Sessiya 12 da hal qilingan:
   QAROR #18: Supabase Edge Function emas, Server Action ishlatildi
   SABAB: Edge cold start 800ms edi, Server Action 120ms
   CONFIDENCE: 89% (hali degraded emas)

   Hozir ham shu yondashuvni ishlatamizmi?
   → Ha: davom etiladi (tezroq)
   → Yo'q: yangi tahlil qilinadi (sababi DECISION_LOG ga yoziladi)"

QOIDA:
  Confidence < 60% bo'lgan eski qarorlar "tavsiya" emas, "ma'lumot" sifatida ko'rsatiladi
  "Bu qaror 90 kun oldingi — yangi baholash tavsiya etiladi"
```

---

**84. Cross-Page Impact Analyzer**
```
HOZIR: F65 Breaking Change — DB o'zgarganda tekshiradi
BU YANGI: Shared KOMPONENT o'zgarganda tekshiradi

TRIGGER: Shared/reusable komponent o'zgartirilmoqchi bo'lganda

JARAYON:
  PAGE_REGISTRY.md dan: bu komponentni kim ishlatadi?

  "<Button> komponenti o'zgaryapti:
   variant prop olib tashlanyapti (primary|secondary → faqat default)

   Bu komponentni ishlatadi:
   → SalesPage (3 joyda: checkout, cancel, save)
   → CashierPage (1 joyda: confirm)
   → SettingsPage (2 joyda: save, reset)

   Jami ta'sirlanadi: 6 joy, 3 sahifa

   Bularni ham spec ga qo'shaymi?
   → Ha: barcha 6 joy spec ga kiradir → MEDIUM hajm
   → Yo'q: faqat yangi komponent → lekin 6 joy buziladi ⚠️"

QOIDA:
  2+ sahifa ta'sirlansa → HITL majburiy
  Foydalanuvchi to'liq scopeni tasdiqlagunicha execution boshlanmaydi
```

---

## ⚡ NEGATIVE PROMPTING PROTOKOLI

### NIMA BU?
Har agentga instructions yozilganda "nima qilsin" bilan birga
"nima qilmasin" ro'yxati ham majburiy yoziladi.

Bu Claude ning 80% standart xatosini instructions darajasida bloklaydi.

### QOIDA:
```
Har agent instructions da 2 blok MAJBURIY:
  DO:   → nima qilsin
  DON'T: → nima qilmasin (agent-specific)
```

### BACKEND UCHUN MAJBURIY "DON'T" RO'YXATI:
```
DON'T:
  ✗ any type ishlatma — har narsa typed bo'lsin
  ✗ console.log yozma — faqat logger.ts
  ✗ hardcode qiymat yozma — constants faylga
  ✗ try/catch ichida error yutma — ServiceResult ga wrap qil
  ✗ Migration DOWN yozmasdan UP yozma
  ✗ RLS yo'q jadval yaratma
  ✗ Limitsiz query yozma — har doim .limit() yoki pagination
  ✗ Mavjud servisni o'zgartirma — yangi funksiya yoz
  ✗ TODO yoki FIXME qoldirma — yoki hal qil yoki TECH_DEBT.md ga yoz
  ✗ Commented-out kod qoldirma
```

### FRONTEND UCHUN MAJBURIY "DON'T" RO'YXATI:
```
DON'T:
  ✗ any type ishlatma
  ✗ console.log yozma
  ✗ Inline style yozma — Tailwind class ishlatilsin
  ✗ Hardcode string yozma — constants yoki i18n
  ✗ Server ma'lumotini useState da saqlama — Zustand
  ✗ UI holatini (isOpen) Zustand da saqlama — useState
  ✗ Biznes logikani komponent ichiga yozma — hook ga
  ✗ process.env to'g'ridan ishlatma — config fayldan
  ✗ Mavjud komponent dizaynini o'zgartirma
  ✗ 300 qatordan katta komponent yaratma — bo'l
  ✗ useEffect ichida cleanup qaytarmasdan subscription ochasma
```

### SECURITY TESTER UCHUN MAJBURIY "DON'T":
```
DON'T:
  ✗ "Umuman xavfsiz ko'rinadi" dema — har endpoint tekshir
  ✗ RLS ni "bor" deb qabul qilma — haqiqatan o'qi
  ✗ Faqat happy path ko'rma — edge case va xato holatlar
  ✗ "Keyinroq tuzatiladi" dema — topilgan har zaiflik yoziladi
```

### PERFORMANCE TESTER UCHUN MAJBURIY "DON'T":
```
DON'T:
  ✗ Faqat oddiy holat test qilma — 100/1000/10000 yozuv bilan test
  ✗ "Yetarli tez" dema — raqam ko'rsat (ms da)
  ✗ Index yo'qligini ko'rmasdan o'tma
  ✗ N+1 query ni "kichik muammo" dema — har doim HIGH
```

### MIYA AI INSTRUCTIONS NAMUNASI:
```
BackendBuilderAI ga:

DO:
  → payments jadvaliga yoz
  → Stripe webhook idempotency key bilan handle qil
  → ServiceResult<Payment> qaytarilsin
  → UP + DOWN migration yoz

DON'T:
  ✗ any type ishlatma
  ✗ console.log yozma
  ✗ Mavjud order servisini o'zgartirma
  ✗ Migration DOWN siz yozma
  ✗ RLS yozmay jadval yaratma
```

---

## ⚡ SPECIFICATION FIRST PROTOKOLI

### NIMA BU?
Har SMALL/MEDIUM/LARGE vazifada — agent kod yozishdan OLDIN
spec (texnik reja) chiqaradi. MiyaAI foydalanuvchiga ko'rsatadi.
Foydalanuvchi "ha" demasa — kod boshlanmaydi.

### QACHON MAJBURIY?
```
MICRO  → spec shart emas, to'g'ridan kod
SMALL  → spec tavsiya qilinadi
MEDIUM → spec MAJBURIY
LARGE  → spec MAJBURIY + ultrathink
```

### SPEC FORMATI (agent chiqaradi):
```
SPEC: [feature nomi]
─────────────────────────────
YARATILADI:
  src/services/payment.ts     ← yangi fayl
  src/app/payment/page.tsx    ← yangi fayl
  supabase/migrations/005.sql ← yangi fayl

O'ZGARTIRILADI:
  src/services/order.ts (45-qator) ← status field qo'shiladi
  src/types/index.ts               ← PaymentStatus type

O'CHIRILADI:
  — (hech narsa o'chirilmaydi)

FUNKSIYALAR:
  createPayment(orderId, amount) → PaymentResult
  getPaymentStatus(paymentId)    → PaymentStatus
  handleWebhook(event)           → void

EDGE CASE LAR:
  → Stripe timeout: retry (max 3), keyin FAILED status
  → Duplicate webhook: idempotency key bilan handle
  → Partial payment: order PENDING qoladi

TEST:
  → createPayment success
  → createPayment Stripe xato
  → webhook duplicate

ROLLBACK RECIPE:
  Xato bo'lsa qaytarish tartibi:
  1. git stash pop                    ← kod o'zgarishlari qaytadi
  2. supabase migration down          ← DB o'zgarishlari qaytadi
  3. STATUS.md → [modul] ❌

  QAYTARIB BO'LMAYDIGAN OPERATSIYALAR (eslatish):
  → Email yuborildi → qaytarib bo'lmaydi
  → SMS ketdi → qaytarib bo'lmaydi
  → To'lov o'tdi → provider orqali qaytarish kerak
─────────────────────────────
Tasdiqlaysizmi?
```

### QOIDA:
```
✓ Foydalanuvchi "ha" desa → kod boshlanadi
✓ Foydalanuvchi o'zgartirsa → spec yangilanadi, keyin kod
✗ "Ha" olmasdan kod yozilmaydi
✗ Spec dan tashqari narsa yozilmaydi
```

### NIMA UCHUN KERAK?
```
Spec noto'g'ri → 30 sekund tuzatiladi
Kod noto'g'ri  → 2-3 soat refactor
```

---

## ⚡ INCREMENTAL TRUST PROTOKOLI

### NIMA BU?
MEDIUM va LARGE feature da agent butun modulni birda yozmaydi.
Kichik qadamlar — har qadam tekshiriladi — keyin keyingisi.
Bir qadam xato bo'lsa faqat o'sha qadam qayta yoziladi.

### QACHON ISHLATILADI?
```
MICRO  → shart emas
SMALL  → shart emas
MEDIUM → MAJBURIY
LARGE  → MAJBURIY + ultrathink
```

### QADAM TARTIBI (MEDIUM misol — "To'lov moduli"):
```
Qadam 1: Faqat DB migration + RLS
         → tsc ✅ → migration syntax ✅ → KEYINGIGA O'TAMIZ

Qadam 2: Faqat servis funksiyalari
         → tsc ✅ → unit test ✅ → KEYINGIGA O'TAMIZ

Qadam 3: Faqat API endpoint
         → tsc ✅ → curl test ✅ → KEYINGIGA O'TAMIZ

Qadam 4: Faqat Frontend komponent
         → tsc ✅ → render ✅ → DONE ✅

QOIDA: Har qadam tekshiruvdan o'tmasdan keyingisi boshlanmaydi.
```

### AGENT INSTRUCTIONS FORMATI:
```
BackendBuilderAI ga (Qadam 2 — faqat servis):

DO:
  → Faqat src/services/paymentService.ts yoz
  → createPayment, getPayment, updatePaymentStatus — 3 ta funksiya

DON'T:
  ✗ Migration yozma — Qadam 1 da qilingan
  ✗ Frontend yozma — Qadam 4
  ✗ API endpoint yozma — Qadam 3
  ✗ 3 ta funksiyadan ko'p yozma

TEKSHIRUV (tugagach):
  npx tsc --noEmit → o'tsa "Qadam 2 ✅", o'tmasa o'zi tuzat
```

### NIMA UCHUN KERAK?
```
Birda yozish:   xato 1 joyda → hammasi qayta → 3 soat
Qadamba-qadam: xato 1 joyda → faqat o'sha qadam → 20 daqiqa

Qo'shimcha foyda:
  → Har qadam ishlayotgani ma'lum
  → Xato qayerdan kelgani aniq
  → Rollback oson — faqat oxirgi qadam
  → Context window tejash — har qadam alohida sessiya mumkin
```

---

---
## ⚡ NEGATIVE PROMPTING PROTOKOLI

### NIMA BU?
Har agentga instructions yozilganda "nima qilsin" bilan birga
"nima qilmasin" ro'yxati ham majburiy yoziladi.

Bu Claude ning 80% standart xatosini instructions darajasida bloklaydi.

### QOIDA:
```
Har agent instructions da 2 blok MAJBURIY:
  DO:   → nima qilsin
  DON'T: → nima qilmasin (agent-specific)
```

### BACKEND UCHUN MAJBURIY "DON'T" RO'YXATI:
```
DON'T:
  ✗ any type ishlatma — har narsa typed bo'lsin
  ✗ console.log yozma — faqat logger.ts
  ✗ hardcode qiymat yozma — constants faylga
  ✗ try/catch ichida error yutma — ServiceResult ga wrap qil
  ✗ Migration DOWN yozmasdan UP yozma
  ✗ RLS yo'q jadval yaratma
  ✗ Limitsiz query yozma — har doim .limit() yoki pagination
  ✗ Mavjud servisni o'zgartirma — yangi funksiya yoz
  ✗ TODO yoki FIXME qoldirma — yoki hal qil yoki TECH_DEBT.md ga yoz
  ✗ Commented-out kod qoldirma
```

### FRONTEND UCHUN MAJBURIY "DON'T" RO'YXATI:
```
DON'T:
  ✗ any type ishlatma
  ✗ console.log yozma
  ✗ Inline style yozma — Tailwind class ishlatilsin
  ✗ Hardcode string yozma — constants yoki i18n
  ✗ Server ma'lumotini useState da saqlama — Zustand
  ✗ UI holatini (isOpen) Zustand da saqlama — useState
  ✗ Biznes logikani komponent ichiga yozma — hook ga
  ✗ process.env to'g'ridan ishlatma — config fayldan
  ✗ Mavjud komponent dizaynini o'zgartirma
  ✗ 300 qatordan katta komponent yaratma — bo'l
  ✗ useEffect ichida cleanup qaytarmasdan subscription ochasma
```

### SECURITY TESTER UCHUN MAJBURIY "DON'T":
```
DON'T:
  ✗ "Umuman xavfsiz ko'rinadi" dema — har endpoint tekshir
  ✗ RLS ni "bor" deb qabul qilma — haqiqatan o'qi
  ✗ Faqat happy path ko'rma — edge case va xato holatlar
  ✗ "Keyinroq tuzatiladi" dema — topilgan har zaiflik yoziladi
```

### PERFORMANCE TESTER UCHUN MAJBURIY "DON'T":
```
DON'T:
  ✗ Faqat oddiy holat test qilma — 100/1000/10000 yozuv bilan test
  ✗ "Yetarli tez" dema — raqam ko'rsat (ms da)
  ✗ Index yo'qligini ko'rmasdan o'tma
  ✗ N+1 query ni "kichik muammo" dema — har doim HIGH
```

### MIYA AI INSTRUCTIONS NAMUNASI:
```
BackendBuilderAI ga:

DO:
  → payments jadvaliga yoz
  → Stripe webhook idempotency key bilan handle qil
  → ServiceResult<Payment> qaytarilsin
  → UP + DOWN migration yoz

DON'T:
  ✗ any type ishlatma
  ✗ console.log yozma
  ✗ Mavjud order servisini o'zgartirma
  ✗ Migration DOWN siz yozma
  ✗ RLS yozmay jadval yaratma
```

---

## ⚡ SPECIFICATION FIRST PROTOKOLI

### NIMA BU?
Har SMALL/MEDIUM/LARGE vazifada — agent kod yozishdan OLDIN
spec (texnik reja) chiqaradi. MiyaAI foydalanuvchiga ko'rsatadi.
Foydalanuvchi "ha" demasa — kod boshlanmaydi.

### QACHON MAJBURIY?
```
MICRO  → spec shart emas, to'g'ridan kod
SMALL  → spec tavsiya qilinadi
MEDIUM → spec MAJBURIY
LARGE  → spec MAJBURIY + ultrathink
```

### SPEC FORMATI (agent chiqaradi):
```
SPEC: [feature nomi]
─────────────────────────────
YARATILADI:
  src/services/payment.ts     ← yangi fayl
  src/app/payment/page.tsx    ← yangi fayl
  supabase/migrations/005.sql ← yangi fayl

O'ZGARTIRILADI:
  src/services/order.ts (45-qator) ← status field qo'shiladi
  src/types/index.ts               ← PaymentStatus type

O'CHIRILADI:
  — (hech narsa o'chirilmaydi)

FUNKSIYALAR:
  createPayment(orderId, amount) → PaymentResult
  getPaymentStatus(paymentId)    → PaymentStatus
  handleWebhook(event)           → void

EDGE CASE LAR:
  → Stripe timeout: retry (max 3), keyin FAILED status
  → Duplicate webhook: idempotency key bilan handle
  → Partial payment: order PENDING qoladi

TEST:
  → createPayment success
  → createPayment Stripe xato
  → webhook duplicate

ROLLBACK RECIPE:
  Xato bo'lsa qaytarish tartibi:
  1. git stash pop                    ← kod o'zgarishlari qaytadi
  2. supabase migration down          ← DB o'zgarishlari qaytadi
  3. STATUS.md → [modul] ❌

  QAYTARIB BO'LMAYDIGAN OPERATSIYALAR (eslatish):
  → Email yuborildi → qaytarib bo'lmaydi
  → SMS ketdi → qaytarib bo'lmaydi
  → To'lov o'tdi → provider orqali qaytarish kerak
─────────────────────────────
Tasdiqlaysizmi?
```

### QOIDA:
```
✓ Foydalanuvchi "ha" desa → kod boshlanadi
✓ Foydalanuvchi o'zgartirsa → spec yangilanadi, keyin kod
✗ "Ha" olmasdan kod yozilmaydi
✗ Spec dan tashqari narsa yozilmaydi
```

### NIMA UCHUN KERAK?
```
Spec noto'g'ri → 30 sekund tuzatiladi
Kod noto'g'ri  → 2-3 soat refactor
```

---

## ⚡ INCREMENTAL TRUST PROTOKOLI

### NIMA BU?
MEDIUM va LARGE feature da agent butun modulni birda yozmaydi.
Kichik qadamlar — har qadam tekshiriladi — keyin keyingisi.
Bir qadam xato bo'lsa faqat o'sha qadam qayta yoziladi.

### QACHON ISHLATILADI?
```
MICRO  → shart emas
SMALL  → shart emas
MEDIUM → MAJBURIY
LARGE  → MAJBURIY + ultrathink
```

### QADAM TARTIBI (MEDIUM misol — "To'lov moduli"):
```
Qadam 1: Faqat DB migration + RLS
         → tsc ✅ → migration syntax ✅ → KEYINGIGA O'TAMIZ

Qadam 2: Faqat servis funksiyalari
         → tsc ✅ → unit test ✅ → KEYINGIGA O'TAMIZ

Qadam 3: Faqat API endpoint
         → tsc ✅ → curl test ✅ → KEYINGIGA O'TAMIZ

Qadam 4: Faqat Frontend komponent
         → tsc ✅ → render ✅ → DONE ✅

QOIDA: Har qadam tekshiruvdan o'tmasdan keyingisi boshlanmaydi.
```

### AGENT INSTRUCTIONS FORMATI:
```
BackendBuilderAI ga (Qadam 2 — faqat servis):

DO:
  → Faqat src/services/paymentService.ts yoz
  → createPayment, getPayment, updatePaymentStatus — 3 ta funksiya

DON'T:
  ✗ Migration yozma — Qadam 1 da qilingan
  ✗ Frontend yozma — Qadam 4
  ✗ API endpoint yozma — Qadam 3
  ✗ 3 ta funksiyadan ko'p yozma

TEKSHIRUV (tugagach):
  npx tsc --noEmit → o'tsa "Qadam 2 ✅", o'tmasa o'zi tuzat
```

### NIMA UCHUN KERAK?
```
Birda yozish:   xato 1 joyda → hammasi qayta → 3 soat
Qadamba-qadam: xato 1 joyda → faqat o'sha qadam → 20 daqiqa

Qo'shimcha foyda:
  → Har qadam ishlayotgani ma'lum
  → Xato qayerdan kelgani aniq
  → Rollback oson — faqat oxirgi qadam
  → Context window tejash — har qadam alohida sessiya mumkin
```

---

**28. Dependency Manager**
```
SEQUENTIAL (bir sessiyada, doim):
  Biri tugamay ikkinchisi boshlanmaydi.

PARALLEL (ikki alohida terminal/sessiya):
  Mustaqil bo'lsa — ikki sessiyada bir vaqtda mumkin.
  Misol: Terminal 1 → BackendBuilderAI
         Terminal 2 → FrontendBuilderAI
  Keyin: IntegrationTesterAI (ikkalasi tugagach)
```

---
