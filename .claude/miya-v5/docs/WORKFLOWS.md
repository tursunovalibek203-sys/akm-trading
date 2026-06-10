# WORKFLOW QO'LLANMASI
## MiyaAI Tizimi — Barcha Ish Jarayonlari

---

## 1. YANGI LOYIHA WORKFLOW

### Qadam 1 — Tayyorlik (15 daqiqa)
```
1. GitHub repository yarating
   git init
   git remote add origin [url]

2. Template fayllarni ko'chiring
   /templates/ → loyiha ildiziga

3. Claude Code oching
   claude

4. MiyaAI ga birinchi prompt:
   "Yangi loyiha boshlayman.
    Nomi: [loyiha nomi]
    Nima qiladi: [1-2 gap]
    Stack: [texnologiyalar]
    Foydalanuvchilar: [kimlar]"
```

### Qadam 2 — MiyaAI fayllar yaratadi (5 daqiqa)
```
MiyaAI so'raydi → siz javob berasiz → fayllar yaratiladi:
✓ CLAUDE.md
✓ PROJECT.md
✓ TODO.md
✓ STATUS.md
✓ Qolgan 8 ta fayl
```

### Qadam 3 — Stack o'rnatish
```
MiyaAI ga:
"Stack o'rnatib ber:
 [Next.js 15 | React + Vite] + TypeScript + Supabase"

FullStackBuilderAI:
→ package.json
→ tsconfig.json
→ .env.example
→ Papka tuzilmasi
→ Supabase connection
→ Git commit: "chore: initial setup"
```

### Qadam 4 — Database
```
MiyaAI ga:
"Database schema yarat: [jadvallar ro'yxati]"

BackendBuilderAI:
→ schema.prisma yoki Supabase migration
→ RLS policies
→ Seed data
→ Git commit: "chore: database setup"
```

### Qadam 5 — Auth
```
MiyaAI ga:
"Auth tizimini sozla: email + Google OAuth"

FullStackBuilderAI:
→ Login sahifa
→ Register sahifa
→ Session boshqaruv
→ Protected routes
→ Git commit: "feat: auth system"
```

### Qadam 6 — MVP funksiyalar
```
Har funksiya uchun alohida sessiya:
"[Funksiya nomi] ni qo'sh"

MiyaAI:
→ Bo'lib-bo'lib bajaradi
→ Har qadam oldidan "ha" kutadi
→ Har qadam commit qilinadi
```

### Yangi loyiha checklist:
```
[ ] Repository yaratildi
[ ] 12 ta memory fayl to'ldirildi
[ ] Stack o'rnatildi
[ ] DB schema tayyor + RLS
[ ] Auth ishlaydi
[ ] .env.example to'liq
[ ] README.md yozildi
[ ] Birinchi commit qilindi
```

---

## 2. BUG FIX WORKFLOW

### Qadam 1 — Xatoni aniqlash
```
MiyaAI ga:
"Xato bor: [xato tavsifi]
 Qayerda: [sahifa/funksiya]
 Qanday takrorlash: [qadamlar]
 Stack trace: [agar bor bo'lsa]"

MiyaAI so'raydi:
A) Kirim input (prompt noto'g'ri edi)
B) Chiqim input (kod noto'g'ri)
→ B deyasiz
```

### Qadam 2 — Root cause tahlil
```
IntegrationTesterAI:
→ 5 Why metodologiyasi
→ Sabab aniqlanadi
→ Ta'sirlangan modullar aniqlanadi

MiyaAI:
"Sabab: [nima]
 Ta'sirlangan: [qaysi fayllar]
 Tuzatish: [qanday]
 Xavf: [boshqa narsa buzilishi mumkinmi?]"
```

### Qadam 3 — Tuzatish
```
MiyaAI ga "ha" deyasiz

FullStackBuilderAI:
→ Faqat xatolik joyini tuzatadi
→ Test yozadi
→ Git commit: "fix: [xato tavsifi]"
```

### Qadam 4 — Tekshirish
```
BackendSecurityTesterAI + IntegrationTesterAI:
→ Tuzatish boshqa narsa buzganmi?
→ Regression tekshirish
→ "Tayyor" signali
```

### Qadam 5 — Deploy
```
VersionControlAI:
→ Patch versiya bump (1.0.0 → 1.0.1)
→ CHANGELOG.md yangilanadi
→ Deploy qilinadi
```

### Bug fix checklist:
```
[ ] Xato takrorlandi (reproduce)
[ ] Root cause aniqlandi
[ ] Faqat kerakli joy tuzatildi
[ ] Test yozildi
[ ] Regression tekshirildi
[ ] Commit: "fix: [tavsif]"
[ ] Deploy qilinadi
```

---

## 3. HOTFIX WORKFLOW (15 daqiqa)

### Qachon hotfix:
```
Production da:
- Foydalanuvchi kira olmayapti
- Ma'lumot yo'qolmoqda
- Kritik funksiya ishlamayapti
- Error rate > 5%
```

### Qadam 1 — Darhol (0-2 daqiqa)
```
1. /health tekshiring:
   curl https://myapp.uz/health

2. Error rate tekshiring (Sentry)

3. Rollback kerakmi?
   → Ha: VersionControlAI ga signal
   → Yo'q: davom eting
```

### Qadam 2 — Tezkor tahlil (2-5 daqiqa)
```
MiyaAI ga:
"HOTFIX kerak. Production xato:
 [xato tavsifi]
 Stack trace: [...]"

MiyaAI:
→ Sabab aniqlanadi
→ Eng tez yechim taklif qilinadi
→ "ha" kutiladi
```

### Qadam 3 — Tuzatish (5-10 daqiqa)
```
FullStackBuilderAI:
→ Minimal o'zgarish (faqat xato joy)
→ Ko'p kod yozish YO'Q
→ Git commit: "hotfix: [tavsif]"
```

### Qadam 4 — Deploy (2-3 daqiqa)
```
VersionControlAI:
→ hotfix/* branch → main
→ Patch bump
→ Darhol deploy
→ /health tekshirish
```

### Qadam 5 — Postmortem (keyinroq)
```
IntegrationTesterAI:
→ Nima sodir bo'ldi?
→ Nima uchun?
→ Qanday oldini olish?
→ ANTI_PATTERNS.md ga yoziladi
```

### Hotfix qoidalari:
```
✓ Minimal o'zgarish — faqat xato joy
✓ Test — kamida bitta
✓ 15 daqiqa ichida deploy
✓ Postmortem keyinroq (hozir emas)
✗ Katta refaktor — hotfix emas
✗ Yangi feature — hotfix emas
✗ "Shu yerda ham tuzataylik" — keyinga
```

---

## 4. CODE REVIEW WORKFLOW

### Qadam 1 — PR tayyorlash
```
Git:
git checkout -b feature/[nomi]
# Ish qilinadi
git push origin feature/[nomi]
# PR ochiladi
```

### Qadam 2 — Avtomatik tekshirish
```
BackendSecurityTesterAI:
→ Xavfsizlik muammolari
→ RLS tekshirish
→ OWASP Top 10

PerformanceAI:
→ N+1 query
→ Bundle size
→ Core Web Vitals

FrontendUXTesterAI:
→ Accessibility
→ Mobile responsive
→ User flow
```

### Qadam 3 — Kod sifat tekshirish
```
BackendSecurityTesterAI (kod sifat):
→ SOLID printsiplari
→ DRY tekshirish
→ Naming convention
→ Dead code
→ Complexity
```

### Qadam 4 — Integration tekshirish
```
IntegrationTesterAI:
→ Backend + Frontend mos?
→ Type mismatch?
→ API contract?
→ End-to-end flow?
```

### Qadam 5 — Qaror
```
Hammasi ✓ → Merge qilinadi
Biror ❌ → Tuzatish kerak → qayta tekshirish

MiyaAI xulosa:
"PR [nomi]:
 Security: ✓
 Performance: ✓
 UX: ⚠️ (1 ta medium muammo)
 Integration: ✓
 Tavsiya: Medium muammoni tuzating, keyin merge"
```

### PR checklist:
```
[ ] Bir feature — bir PR
[ ] Test yozilgan
[ ] CHANGELOG.md yangilangan
[ ] Security tekshiruv o'tdi
[ ] Performance tekshiruv o'tdi
[ ] UX tekshiruv o'tdi
[ ] Integration tekshiruv o'tdi
[ ] Commit message to'g'ri
```

---

## 5. REFAKTOR WORKFLOW

### Qachon refaktor:
```
REFAKTOR BELGILARI:
- Funksiya 100+ qator
- Fayl 300+ qator
- Bir xil kod 3+ joyda
- Test yozib bo'lmaydi
- Tushunib bo'lmaydi
- TECH_DEBT.md da ko'p yig'ilgan
```

### Qadam 1 — Tahlil
```
MiyaAI ga:
"[Fayl/modul] ni refaktor qilmoqchiman"

MiyaAI:
→ Nima muammo — aniqlanadi
→ Qanday refaktor — taklif qilinadi
→ Xavf — boshqa narsa buzilishi mumkinmi?
→ Effort estimation — qancha vaqt?
```

### Qadam 2 — Test avval
```
QOIDA: Refaktor oldidan test yoziladi.
Test yo'q bo'lsa → avval test, keyin refaktor.

"Mavjud [funksiya] uchun test yoz,
 refaktordan oldin"

FullStackBuilderAI:
→ Test yoziladi
→ Testlar o'tadi — tasdiqlangan
```

### Qadam 3 — Bosqichma-bosqich
```
HECH QACHON: Hammani birda refaktor qilma
DOIM: Kichik qadamlarda

Qadam 1: Bitta funksiyani ajrat
Qadam 2: Test o'tadi? → commit
Qadam 3: Keyingi funksiya
...

Har qadam commit:
"refactor: [nima ajratildi]"
```

### Qadam 4 — Tekshirish
```
IntegrationTesterAI:
→ Refaktor oldingi kabi ishlayaptimi?
→ Regression tekshirish
→ Performance yomonlashmadimi?
```

### Refaktor qoidalari:
```
✓ Avval test, keyin refaktor
✓ Kichik qadamlar
✓ Har qadam commit
✓ Funksionallik o'zgarmaydi
✗ Refaktor + yangi feature birda — YO'Q
✗ Test yo'q refaktor — YO'Q
✗ "Shu yerda ham o'zgartiraman" — keyinga
```

---

## 6. SPRINT PLANNING WORKFLOW

### Sprint nima:
```
1-2 haftalik ish davri.
Boshida: nima qilamiz?
Oxirida: nima qildik?
```

### Sprint boshida (Dushanba):
```
MiyaAI ga:
"Sprint planning. Bu hafta nima qilamiz?"

MiyaAI:
1. TODO.md dan qolgan vazifalar
2. TECH_DEBT.md dan muhim qarzlar
3. RISK_REGISTER.md dan xavflar
4. Foydalanuvchi profili asosida

Taklif:
"Bu hafta uchun tavsiyam:
 1. [Vazifa 1] — 2 soat
 2. [Vazifa 2] — 3 soat
 3. [TD-001 tuzatish] — 1 soat
 Jami: ~6 soat
 
 To'g'rimi?"
```

### Sprint davomida (har kun):
```
Sessiya boshida MiyaAI ga:
"Bugun nima qilamiz?"

MiyaAI:
→ Sprint rejasidan keyingi vazifa
→ Effort estimation
→ Boshlaymizmi?
```

### Sprint oxirida (Juma):
```
MiyaAI ga:
"Sprint yakunlash"

MiyaAI:
→ Nima qilindi
→ Nima qoldi (keyingi sprintga)
→ Qancha token sarflandi
→ Loyiha progress: [X]%
→ Keyingi sprint uchun tavsiyalar
```

### Sprint checklist:
```
BOSHIDA:
[ ] Sprint maqsadi aniq
[ ] Vazifalar TODO.md ga yozildi
[ ] Effort estimation qilindi

DAVOMIDA:
[ ] Har kun sessiya boshida reja
[ ] Har feature commit qilindi
[ ] Xato bo'lsa bug fix workflow

OXIRIDA:
[ ] Sprint review qilindi
[ ] CHANGELOG.md yangilandi
[ ] Keyingi sprint rejalashtirildi
[ ] Deploy qilindi (agar tayyor)
```

---

## 7. ONBOARDING WORKFLOW

### Yangi developer keldi:
```
Unga beriladigan narsalar:
1. Repository access
2. /templates/ papkasi
3. Bu WORKFLOWS.md
4. CLAUDE_PROFESSIONAL_GUIDE.md
5. Barcha skill fayllar
```

### Birinchi kun:
```
1. Repository clone:
   git clone [url]

2. Template fayllarni o'qish:
   - CLAUDE.md → loyiha qoidalari
   - PROJECT.md → loyiha maqsadi
   - STATUS.md → hozirgi holat

3. Claude Code o'rnatish:
   npm install -g @anthropic-ai/claude-code

4. MiyaAI bilan tanishish:
   MiyaAI_SKILL_v3.md ni o'qish

5. Birinchi kichik vazifa:
   TODO.md dan eng kichik vazifani oling
   Bug fix yoki kichik UI o'zgarish
```

### Birinchi hafta:
```
DUSHANBA: Loyiha tuzilmasi tushunish
SESHANBA: Birinchi kichik bug fix
CHORSHANBA: Birinchi kichik feature
PAYSHANBA: Code review jarayoni
JUMA: Sprint planning'da qatnashish
```

### Onboarding checklist:
```
[ ] Repository access olindi
[ ] Local muhit sozlandi
[ ] CLAUDE.md o'qildi
[ ] PROJECT.md o'qildi
[ ] MiyaAI bilan birinchi sessiya
[ ] Birinchi commit qilindi
[ ] Code review jarayoni tushunildi
[ ] Sprint planning'da qatnashildi
```

---

## WORKFLOW TANLASH JADVALI

```
HOLAT                        → WORKFLOW
─────────────────────────────────────────
Yangi loyiha boshlash        → Yangi loyiha workflow
Xato topildi (production)    → Bug fix workflow
Kritik xato (hozir)         → Hotfix workflow
PR tekshirish                → Code review workflow
Kodni yaxshilash             → Refaktor workflow
Haftalik reja                → Sprint planning workflow
Yangi developer              → Onboarding workflow
```

---

## UMUMIY QOIDALAR (barcha workflow)

```
1. Har qadam oldidan commit
2. Kichik qadamlar — katta o'zgarish YO'Q
3. Test yozilmagan kod deploy YO'Q
4. MiyaAI "ha" siz bajartmaydi
5. Xato bo'lsa — rollback birinchi
6. Postmortem — har muhim xatolikdan keyin
```
