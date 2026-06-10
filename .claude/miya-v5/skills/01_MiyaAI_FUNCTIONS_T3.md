# SKILL: MiyaAI FUNCTIONS — TIER 3
## VERSION: 5.1
## YUKLANISH: TIER 3 — HODISADA (~2,300 token)
## QACHON:
##   Agent 2x fail      → F63, F64, F74
##   7+ kun tanaffus    → F71
##   Scope kengaydi     → F72
##   Migration xato     → F79
##   Agent output xato  → F88, F89

**63. Postmortem Protokoli**
Xato, bug yoki muvaffaqiyatsiz deploy bo'lganda — avtomatik ishga tushadi:
```
TRIGGER:
  → Agent 2 urinishdan keyin FAIL qaytarsa
  → Foydalanuvchi "xato", "ishlamayapti", "bug" desa
  → Deploy muvaffaqiyatsiz bo'lsa

POSTMORTEM FORMATI (.miya/postmortem_SANA.md):
─────────────────────────────────────────────
VOQEA: [qisqa tavsif]
SANA:  [timestamp]
DARAJA: KRITIK | YUQORI | O'RTA

NIMA BO'LDI:
  → [xato xabari yoki belgilari]

SABAB TAHLILI (5-WHY):
  Nima bo'ldi?   → [simptom]
  Nega?          → [birinchi sabab]
  Nega?          → [ikkinchi sabab]
  Nega?          → [uchinchi sabab]
  Asosiy sabab:  → [ildiz sabab]

TA'SIR:
  → Foydalanuvchi: [ta'sirlangan?]
  → Ma'lumot: [yo'qolgan/buzilgan?]
  → Vaqt: [qancha vaqt]

TUZATISH:
  → Nima qilindi: [aniq qadam]
  → Qachon tuzatildi: [timestamp]

QAYTARILMASLIGI UCHUN:
  → [aniq o'zgarish — kod, jarayon, yoki qoida]
  → ANTI_PATTERNS.md ga yoziladi: ha/yo'q
  → RISK_REGISTER.md yangilanadi: ha/yo'q
─────────────────────────────────────────────
```

---

**64. Auto Error → ANTI_PATTERNS**
Foydalanuvchi xatoni bildirsa — avtomatik ANTI_PATTERNS.md ga yoziladi.
Qo'lda yozishni kutmaydi:
```
TRIGGER SO'ZLAR:
  "xato", "bug", "ishlamayapti", "noto'g'ri", "yo'q qil",
  "bu yomon", "buning keragi yo'q", "qayta qil", "o'chirgin"

AVTOMATIK JARAYON:
  1. Xato kontekstini aniqlaydi (qaysi fayl, qaysi qaror)
  2. Pattern sifatida formatlaydi
  3. ANTI_PATTERNS.md ga APPEND qiladi
  4. Foydalanuvchiga: "Yozib qo'ydim — keyingi sessiyalarda takrorlanmaydi"

ANTI_PATTERNS FORMAT:
─────────────────────────────────────────────
[AP-NNN] DARAJA: TAVSIF
Sessiya: [sana]
Nima qilindi (xato): [agent nima qildi]
Nega xato: [foydalanuvchi nima dedi]
To'g'risi: [qanday bo'lishi kerak edi]
Trigger: [qaysi holatda bu xato takrorlanishi mumkin]
─────────────────────────────────────────────

MISOL:
[AP-007] HIGH: Migration faylni avval, kod faylni keyin yozmadi
Sessiya: 2026-05-24
Nima qilindi: service.ts va migration.sql bir vaqtda yaratildi
Nega xato: Migration avval apply bo'lishi kerak, keyin kod
To'g'risi: migration.sql → apply → service.ts tartibida
Trigger: Yangi jadval yoki field qo'shilganda

QOIDA:
  → Bir sessiyada bir xil AP 2 marta chiqsa → TECH_DEBT ga ko'chiriladi
  → AP-lar sessiya boshida yuklanadi (top 5 ta eng ko'p takrorlangan)
```

---

### N — QAROR SIFATI (v5.0)

---

**71. Cold Start Detector**
```
TRIGGER: Sessiya ochilganda, CLAUDE.md o'qilgandan keyin

JARAYON:
  SESSION_LAST.md dagi sana → bugun bilan taqqos

  N < 1 kun   → Normal davom, hech narsa ko'rsatilmaydi
  N = 1-7 kun → STATUS.md alohida e'tibor bilan o'qiladi
                 "3 kun bo'libdi. Muhim o'zgarishlar bor emasmikin?"
  N > 7 kun   → ⚠️ COLD START rejimi

COLD START REJIMI (N > 7 kun):
  1. Barcha memory fayllar to'liq qayta o'qiladi
  2. TODO.md dagi "IN_PROGRESS" larni tekshir → hali aktualmi?
  3. INCOMPLETE_WORK.md ni ko'rsat → tugallanmagan ishlar
  4. RISK_REGISTER.md → muddati o'tgan risklar
  5. Foydalanuvchiga:
     "[N] kun bo'ldi. Loyihada nimalar o'zgardi?
      Men bilmasligi mumkin bo'lgan o'zgarishlar bormi?
      (yangi stack, yangi biznes qoida, o'chirilgan feature)"

  Javob olgandan keyin → SESSION_LAST va ASSUMPTIONS.md yangilanadi
  Keyin davom etiladi
```

---

**72. Scope Creep Early Warning**
```
HOZIR: F19 Scope Guard — scope tashqarisiga chiqqanda to'xtatadi (reaktiv)
BU YANGI: Chiqishdan OLDIN ogohlantiradi (proaktiv)

TRIGGER: Sessiya davomida yangi vazifa qo'shilganda

HISOB:
  Sessiya boshlanganda: 1 ta asosiy vazifa (bazaviy)
  Har yangi qo'shimcha vazifa → hisob oshadi

  3 ta vazifada: "ℹ️ Sessiya doirasi kengaydi: 3 ta vazifa"
  5 ta vazifada: "⚠️ Sprint xavfi: 5 ta vazifa. Hammasi bu sessiyada realistikmi?"
  7 ta vazifada: "🛑 Scope creep: Yangi sprint ochilsinmi?
                  Yoki qaysi 3 tasiga fokuslanish kerak?"

QOIDA:
  Ogohlantirish faqat bir marta (har daraja uchun)
  Foydalanuvchi "davom et" desa → DECISION_LOG ga yoziladi
```

---

**74. Hallucination Pattern Memory**
```
HOZIR: Hallucination Detector — real-time tekshiradi (bir sessiyada)
BU YANGI: Qaysi turdagi hallucination ko'p bo'lishini ESLAB QOLADI

TRIGGER: Hallucination aniqlanganda (har safar)

JARAYON:
  Aniqlangan pattern → ANTI_PATTERNS.md ga [HALL] tegi bilan yoziladi:
    "[AP-015][HALL][BackendBuilderAI] 2026-05-24:
     Mavjud bo'lmagan Supabase funksiyasini ishlatdi (rpc('get_stats'))
     Haqiqiy: bunday funksiya yo'q"

  Bir agent 2+ marta bir xil hallucination:
    → O'sha agent instructions ga qo'shimcha "DON'T" qoidasi qo'shiladi
    → Negative Prompting Protokoli (mavjud bo'lim) kuchaytiriladi

TRIGGER SESSIYA BOSHIDA:
  "BackendBuilderAI uchun eslatma: Bu agent
   Supabase rpc() ni 3 marta noto'g'ri ishlatdi.
   Tekshiruv kuchaytiriladi."
```

---

**79. Dependency Vulnerability Watch**
```
TRIGGER: Har 14 kunda bir marta (SESSION_LAST.md dagi sana bo'yicha)

JARAYON:
  DEPENDENCY_MAP.md dagi paketlar ro'yxati + oxirgi tekshirilgan sana

  14 kun o'tgan bo'lsa:
  "📦 Dependency tekshiruvi (14 kun o'tdi):
   Quyidagilarni tekshirishni tavsiya qilaman:
   → next.js: package.json dagi versiyani ko'ring
   → @supabase/supabase-js: yangilanish bormi?
   → [boshqa asosiy paketlar]

   npm audit yoki npm outdated ishlatib tekshirasizmi?"

QOIDA:
  AI paketlarni o'zi yangilamaydi → foydalanuvchiga ko'rsatadi
  Critical CVE aniqlansa → RISK_REGISTER ga qo'shiladi
  14 kunlik check o'tkazilsa → DEPENDENCY_MAP.md dagi sana yangilanadi
```

---

### R — FOYDALANUVCHI VA ARXITEKTURA (v5.0)

---

**88. Agent Output Validator (JSON Schema Check)**
```
MUAMMO: Agent "partial" qaytaradi, lekin meta.files_changed bo'sh — 
        MiyaAI bu holatni maxsus ushlashi kerak.
        Yoki meta.status = "success" lekin hech fayl o'zgarmagan — silent fail.

TRIGGER: Har agent natijasi kelganda — HALLUCINATION CHECK bilan birga (Qadam 8)

TEKSHIRISH ALGORITMI:
  1. meta maydonlari to'liqmi?
     Majburiy maydonlar: agent, status, files_changed, errors
     → Yo'q bo'lsa: "Agent natijasi noto'liq (meta.X yo'q)" → FAILED deb qabul

  2. status va real natija mos keladi mi?
     status=success + files_changed=[]  → SUSPICIOUS — agent qayta so'raladi (max 1)
     status=partial  + errors=[]        → SUSPICIOUS — sabab yo'q partial → agent qayta
     status=failed   + blocked=false    → CONFLICT — blocked=true ga o'zgartiriladi

  3. files_changed haqiqiy mi?
     Har fayl uchun: ls [fayl] → yo'q bo'lsa → HALLUCINATION
     status=success edi → partial ga tushiriladi
     INCOMPLETE_WORK ga yoziladi

  4. next_agent mantiqiy mi?
     next_agent ko'rsatilgan lekin blocked=true → next_agent=null ga o'zgartiriladi
     next_agent=null, status=success → zanjir davom: MiyaAI keyingi agent aniqlaydi

NATIJA:
  Hamma 4 tekshiruv o'tdi → ✅ agent natijasi qabul qilinadi
  1-2 tekshiruv fail     → ⚠️  agent qayta so'raladi (max 1 marta)
  3-4 tekshiruv fail     → ❌  ZANJIR TO'XTATILADI, foydalanuvchiga aniq xabar

XABAR FORMATI (foydalanuvchiga):
  "⚠️ [AgentNomi] natijasi tekshiruvdan o'tmadi:
   - [Muammo: masalan 'files_changed bo'sh, lekin status=success']
   Davom etishim uchun: [variant 1] yoki [variant 2]?"
```

---

---

**89. Feature Flag Auto-Register**
```
MUAMMO: BackendBuilderAI yoki FrontendBuilderAI feature flag yozadi,
        lekin FEATURE_FLAGS.md ga qo'shishni unutadi → flag yo'qoladi.

TRIGGER: Har agent natijasi ichida isEnabled() yoki featureFlag pattern topilsa

ANIQLASH:
  Agent chiqargan kodni skanerlash:
  → isEnabled('[flag_nomi]') topilsa
  → FEATURE_FLAGS.md da shu flag bormi? → yo'q bo'lsa: AVTOMATIK QO'SHILADI

FORMAT (FEATURE_FLAGS.md ga):
  [flag_nomi]: false — [agent tomonidan yaratildi: sessiya] — [sana]
  ⚠️ Foydalanuvchiga xabar: "Yangi flag aniqlandi: [flag_nomi] → FEATURE_FLAGS.md ga qo'shildi"

CLEANUP ESLATMASI (flag 30 kun o'tgandan keyin):
  → SESSION_LAST.md da sana tekshiriladi
  → 30 kun o'tgan va hali false → foydalanuvchiga: "Flag [nomi] 30 kun o'tdi — o'chirish kerakmi?"
```
