# CLAUDE.md — Loyiha Qoidalari
# HAR SESSIYADA BIRINCHI O'QILADI
# Bu faylni to'liq to'ldirmay loyiha boshlanmaydi

---

## MIYA AI YUKLANISH TARTIBI
# Bu bo'limni O'ZGARTIRMA — tizim shu orqali fayllarni yuklanadi

TIER 1 — sessiya boshida (har doim):
  @skills/01_MiyaAI_CORE.md
  @skills/01_MiyaAI_FUNCTIONS_T1.md
  @skills/01_MiyaAI_FUNCTIONS_INDEX.md
  @templates/SESSION_LAST.md
  @templates/TODO.md
  @templates/USER_PROFILE.md

TIER 2 — vazifaga qarab (prompt kelgandan keyin):
  NEW_FEATURE → @skills/01_MiyaAI_FUNCTIONS_T2.md @templates/PROJECT.md @templates/SCHEMA_SNAPSHOT.md
  BUG_FIX     → @skills/01_MiyaAI_FUNCTIONS_T2.md @templates/STATUS.md @templates/ANTI_PATTERNS.md
  DEPLOY      → @skills/01_MiyaAI_FUNCTIONS_T2.md @templates/RISK_REGISTER.md @templates/RUNBOOK.md
  SPRINT      → @skills/01_MiyaAI_FUNCTIONS_T2.md @templates/SPRINT_PLAN.md @templates/INCOMPLETE_WORK.md
  REFACTOR    → @skills/01_MiyaAI_FUNCTIONS_T2.md @templates/TECH_DEBT.md @templates/DEPENDENCY_MAP.md

TIER 3 — hodisada:
  @skills/01_MiyaAI_FUNCTIONS_T3.md

---

---

## MAJBURIY MAYDONLAR (barchasi to'ldirilishi shart)

### LOYIHA
```
Nomi:
Nima qiladi (1 gap):
Foydalanuvchilar:
Hozirgi faza:
Faza maqsadi:
```

### STACK
```
Frontend:
Backend:
Database:
Auth:
State management:
Styling:
Testing:
Deploy:
```

### PAPKA TUZILMASI
```
[haqiqiy papka tuzilmangizni yozing]
```

### MUHIT O'ZGARUVCHILARI
```
[barcha .env key larni yozing — qiymat emas, faqat nom]
Misol:
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_KEY
```

### MAJBURIY KODLASH QOIDALARI
```
[kamida 5 ta qoida — loyihangizga xos]
Misol:
- any type MUMKIN EMAS
- Har servis funksiyasi ServiceResult<T> qaytaradi
- Migration da UP + DOWN majburiy
- console.log production ga chiqmaydi
- Mavjud UI ga MiyaAI ruxsatisiz tegmaydi
```

---

## IXTIYORIY MAYDONLAR

### MUHIM QARORLAR (arxitektura)
```
[nima uchun shu stack tanlandi — 1-2 gap]
```

### CHEKLOVLAR
```
[nima qilinmaydi — loyihaga xos]
```

### TASHQI SERVISLAR
```
[API lar, webhook lar, integratsiyalar]
```

---

## AGENT UCHUN MINIMAL TALAB

Bu faylni o'qigan agent quyidagilarni bilishi SHART:
```
1. Qaysi framework ishlatilmoqda
2. Papka tuzilmasi qanday
3. Qaysi tiplar va pattern majburiy
4. Nima qilish mumkin emas
5. Hozir qaysi fazadamiz
```

Agar bulardan biri aniq emas bo'lsa — agent CLAUDE.md to'liq
emas deb hisoblab, foydalanuvchidan so'raydi. Taxmin qilmaydi.

---

## TO'LDIRILGAN MISOL

### LOYIHA
```
Nomi: CRM Pro
Nima qiladi: Kichik biznes uchun mijoz, sotuv va to'lov boshqaruvi
Foydalanuvchilar: Menejerlar va kassirlar (10-50 kishi)
Hozirgi faza: Faza 1
Faza maqsadi: Auth + Mijozlar + Sotuv MVP
```

### STACK
```
Frontend: Next.js 15 App Router + TypeScript 5
Backend: Supabase Edge Functions
Database: Supabase (PostgreSQL 15)
Auth: Supabase Auth (email + Google OAuth)
State management: Zustand 4
Styling: Tailwind CSS 3 + shadcn/ui
Testing: Vitest + Playwright
Deploy: VPS (Ubuntu 22) + nginx + PM2 + GitHub Actions
```

### PAPKA TUZILMASI
```
src/
  app/              ← Next.js App Router sahifalar
    (auth)/         ← auth group layout
    (dashboard)/    ← asosiy layout
  components/
    ui/             ← shadcn/ui base komponentlar
    features/       ← biznes komponentlar
  services/         ← Supabase bilan ishlash (ServiceResult pattern)
  store/            ← Zustand store lar
  types/            ← global TypeScript tiplar
  lib/              ← constants, helpers, config
supabase/
  migrations/       ← numbered migrations (001_, 002_...)
  functions/        ← Edge Functions
```

### MUHIT O'ZGARUVCHILARI
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_KEY
NEXT_PUBLIC_APP_URL
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
```

### MAJBURIY KODLASH QOIDALARI
```
- any type MUMKIN EMAS — TypeScript strict mode
- Har servis funksiyasi ServiceResult<T> qaytaradi
- Migration da UP + DOWN majburiy
- console.log yo'q — src/lib/logger.ts ishlatiladi
- Mavjud UI ga MiyaAI ruxsatisiz tegmaydi
- Zustand faqat server/global state — UI state useState da
- Biznes logika hooks da — komponent ichida emas
- Hardcode string yo'q — src/lib/constants.ts
```

### MUHIM QARORLAR
```
Supabase tanlandi: Firebase o'rniga — RLS built-in,
PostgreSQL to'liq quvvati, pricing maqbul.
Monolith arxitektura: Faza 3 gacha, keyin mikroservis ko'riladi.
```

### CHEKLOVLAR
```
- Real-time Faza 2 gacha yo'q
- AI integratsiya Faza 3 gacha yo'q
- Mobile app yo'q (responsive web yetarli)
```

### TASHQI SERVISLAR
```
Stripe: to'lov (webhook: /api/webhooks/stripe)
Google OAuth: Supabase Auth orqali
Resend: email (Faza 2)
```
