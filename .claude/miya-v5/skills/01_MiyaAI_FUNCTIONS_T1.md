# SKILL: MiyaAI FUNCTIONS — TIER 1
## VERSION: 5.1
## YUKLANISH: TIER 1 — HAR SESSIYADA MAJBURIY (~2,000 token)
## QACHON: Sessiya boshlanishi bilan darhol — har doim

**29b. Rubber Duck Debugging Protokoli**

```
TRIGGER (MiyaAI o'zi aniqlaydi):
  "xato topolmayapman"
  "nega ishlamayapti"
  "tushunmayapman"
  "nima muammo"
  Agent 2 marta FAIL qaytarganda

PROTOKOL:
  MiyaAI agentga:
  "Kodni O'ZGARTIRMA.
   Faqat quyidagilarni ayt — qator-qator:

   1. Bu funksiya/komponent nima qilishi kerak?
   2. Har qadam: qanday kirish → qanday chiqish kutiladi?
   3. Haqiqatda nima bor? (qiymat, tip, holat)
   4. Qaysi qadamda kutilgan va haqiqiy qiymat farqlanyapti?"

NATIJA:
  → Agent tushuntirayotganda xatoni o'zi topadi (90% holat)
  → Topsa: o'zi tuzatadi, foydalanuvchiga aytadi
  → Topmasa: MiyaAI foydalanuvchiga ko'rsatadi, birga qaraladi

NIMA UCHUN ISHLAYDI:
  "Tuzat" deyilsa → Claude birinchi yechimga o'tadi
  "Tushuntir" deyilsa → Claude mantiqni qayta yuritadi
  → Mantiq yuritish jarayonida xato ko'rinadi

MISOL:
  Foydalanuvchi: "payment funksiyam ishlamayapti"
  MiyaAI: "Kodni o'zgartirma. Menga qator-qator ayt:
           createPayment() nima qilishi kerak?
           amount parametri qanday keladi?
           Supabase ga nima yuborilyapti?
           Xato qaysi qatorda, qanday xabar?"
  Agent: "amount string kelayapti, number kutilgan edi..."
  → Xato o'zi topildi.
```

---

**29. Agent Xato Qaytarish**
```
TIMEOUT    → retry (max 2)
TYPE_ERROR → instructions aniqlanadi, qayta yuboriladi
CONFLICT   → foydalanuvchiga aytiladi
CRITICAL   → to'xtatiladi, xabar beriladi
```

---

**30. Error Propagation**
Bir agent xatosi butun pipeline ni to'xtatmaydi.
Mustaqil agentlar davom etadi.

---

### F — MEMORY BOSHQARUV

---

**85. Memory Tier System**
```
MUAMMO: Har sessiyada barcha memory fayllar o'qilsa →
        ~4000 token sarflanadi, hali bitta kod yozilmagan.

YECHIM: 3 daraja — faqat kerak bo'lganda yuklanadi.

TIER 1 — HAR SESSIYADA MAJBURIY (~600 token):
  CLAUDE.md        → stack, qoidalar, forbidden
  SESSION_LAST.md  → oxirgi sessiya natijasi
  TODO.md          → faqat [ ] va [~] qatorlar (filter qilinadi)

TIER 2 — VAZIFAGA QARAB (trigger: foydalanuvchi prompt bergandan keyin):
  NEW_FEATURE  → PROJECT.md + SCHEMA_SNAPSHOT.md
  BUG_FIX      → STATUS.md + ANTI_PATTERNS.md (top 5 ta)
  DEPLOY       → RISK_REGISTER.md + TECH_DEBT.md (faqat HIGH) + RUNBOOK.md
  SPRINT       → SPRINT_PLAN.md + INCOMPLETE_WORK.md
  REFACTOR     → TECH_DEBT.md + DEPENDENCY_MAP.md → RefactorAI zanjiri

TIER 3 — HODISA BO'LGANDA (aniq trigger):
  Migration yozildi      → SCHEMA_SNAPSHOT.md + PAGE_REGISTRY.md (F65)
  7+ kun tanaffus        → SESSION_HISTORY.md oxirgi 5 sessiya (F71)
  Scope kengaydi         → SPRINT_PLAN.md (F72)
  Agent 2x fail          → ANTI_PATTERNS.md to'liq (F74)
  Qaror qayta ko'riladi  → DECISION_LOG.md (F68, F83)
  Shared komponent o'zg. → PAGE_REGISTRY.md (F84)

HECH QACHON AVTOMATIK O'QILMAYDI (faqat so'ralganda):
  USER_PROFILE.md      → faqat uslub o'zgarganda (har 3 sessiyada)
  DECISION_LOG.md to'liq → faqat qaror qayta ko'rilganda
  FEATURE_FLAGS.md     → faqat flag yozilganda/o'qilganda
  ADR_TEMPLATE.md      → faqat yangi ADR yozilganda
  DEPENDENCY_MAP.md    → faqat kaskad tahlilda

TOKEN TEJASH:
  Oldin (hamma narsa): ~4000 token/sessiya
  Keyin (TIER tizim):  ~600 token (normal) | ~1500 token (TIER 2) | ~2500 (TIER 3)
  Tejash: 60-85% har sessiyada
```

---

---

**31. Memory Yangilash Tartibi**
```
DIALOG paytida:     Assumption Tracker, Token Monitor
EXECUTION boshida:  Decision Log
AGENT tugagach:     STATUS.md (o'sha modul)
BARCHA tugagach:    TODO.md, PROJECT.md, SESSION_LAST.md
SESSIYA yakunida:   Session Handoff, ASSUMPTIONS.md
```

---

**32. TODO.md Sync**
Bajarilgan: [x]. Yangi: qo'shiladi. Faqat APPEND.

---

**33. STATUS.md Yangilash**
```
✓  Tayyor
⚠️  Muammo (sabab)
❌  Bajarilmadi (sabab)
🔄  Jarayonda
```

---

**34. PROJECT.md Sync**
Faqat arxitektura o'zgarsa yangilanadi. Faqat APPEND.

---

**35. Decision Log (APPEND)**
```
[2025-05-19 14:30] QAROR: real-time Phase 2 ga qoldirildi
SABAB: MVP scope dan tashqarida
KIM: Foydalanuvchi tasdiqladi
```
Eski qarorlar HECH QACHON o'chirilmaydi.

---

**36. Session Handoff**
Token 80K ga yetsa:
```
BAJARILDI: [ro'yxat]
JARAYONDA: [ro'yxat]
QOLDI: [ro'yxat]
KEYINGI SESSIYA: [qayerdan boshlash]
```

---

**37. Assumption Tracker**
```
[ ] taxmin (tasdiqlanmagan)
[x] taxmin (tasdiqlangan — sana)
```

---

**38. Token Budget Monitor**
```
0-50K:  Yashil — normal
50-80K: Sariq — /compact tavsiya
80K+:   Qizil — Session Handoff majburiy
```

---

**42. Shaxsiylashtirilgan Dialog**
Profil asosida:
- Beginner → ko'proq tushuntirish, oddiy til
- Senior → qisqa, texnik, to'g'ridan-to'g'ri
- Tez qaror qiluvchi → kam savol, ko'proq taklif
- O'ylab qaror qiluvchi → ko'proq variant, trade-off

---

### H — LOYIHA SALOMATLIGI

---

**55. Sessiya Maqsadi Boshqaruv**
Har sessiya boshida:
"Bu sessiyada nima qilmoqchisiz? (1-2 gap)"

Sessiya oxirida:
"Maqsad bajarildi? Bajarilmagan narsa keyingi sessiyaga yozilsinmi?"

---

**58. Sessiya Samaradorligi**
Har sessiya yakunida:
```
Vaqt: [daqiqa]
Bajarildi: [soni]
Token: [sarflangan]
Samaradorlik: yuqori | o'rta | past
Sabab: [agar past bo'lsa]
```

---

### L — YANGI MEMORY PROTOKOLLARI

---

**73. Energy Budget Tracker**
```
TRIGGER: Har agent instructions berilganda

MURAKKABLIK BALLI:
  Kichik fix (1 fayl, logic yo'q)     → 1 ball
  Yangi komponent (UI)                → 3 ball
  Yangi servis/API endpoint           → 4 ball
  Yangi jadval + migration            → 5 ball
  Multi-agent zanjir (3+ agent)       → 8 ball
  Tashqi servis integratsiya          → 10 ball

SESSION BUDGET: 20 ball (CLAUDE.md da sozlanadi)

JARAYON:
  15 ballda: "ℹ️ Sessiya energiyasi 75%.
              Keyingi murakkab vazifa oxirgisi bo'lishi mumkin."
  20 ballda: "⚠️ Sessiya limiti yaqinlashdi.
              Yangi feature boshlash tavsiya etilmaydi.
              Mavjudni yoping, commit qiling, yangi sessiyada davom eting."
  25+ ballda: "🛑 Limit oshdi. Keyingi murakkab agent BLOK.
               Commit va yangi sessiya majburiy."

NIMA UCHUN:
  Context window to'lganda Claude sifati pasayadi.
  Murakkab vazifani yarim qoldirib tugatmaslik uchun.
```

---

### P — AGENT SIFATI (v5.0)

---

**82. Silent Progress Indicator**
```
TRIGGER: 3+ agent ketma-ket ishlaydigan zanjir boshlanishida

JARAYON:
  Zanjir boshida: "[Loyiha nomi] — [N] bosqich boshlanmoqda"

  Har agent tugaganda qisqa signal:
  "✓ BackendBuilderAI [1/5] — paymentsService.ts yaratildi"
  "✓ Migration [2/5] — 20260524_payments_currency.sql tayyor"
  "✓ FrontendBuilderAI [3/5] — PaymentForm.tsx yaratildi"
  "⏳ IntegrationTesterAI [4/5] — tekshirilmoqda..."
  "✓ SecurityAI [5/5] — ✅ Xavfsiz"

  Yakunida:
  "✅ Zanjir tugadi [5/5] — [N] fayl yaratildi, [N] o'zgartirildi"

QOIDA:
  Progress siqiq — 1 qator, ortiqcha emas
  FAIL bo'lsa: "❌ [Agent] [N/M] — [sabab] — to'xtadi"
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

---
