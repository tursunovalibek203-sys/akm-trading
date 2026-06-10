# ONBOARDING.md — Loyihaga Kirish Yo'riqnomasi

## Loyiha nima?
[1-2 jumla: nima qiladi, kim uchun]

---

## Texnologiyalar
```
Frontend:  Next.js 15, TypeScript, Tailwind CSS
Backend:   Supabase (DB + Auth + Storage + Realtime)
Deploy:    Vercel
AI tizim:  MiyaAI v5.0 (Claude Code bilan)
```

---

## Lokal ishga tushirish (5 qadam)

```bash
# 1. Klonlash
git clone [repo] && cd [loyiha]

# 2. Paketlar
npm install

# 3. Environment
cp .env.example .env.local
# .env.local ni to'ldiring (quyida ko'rsatilgan)

# 4. DB
npx supabase start
npx supabase db push

# 5. Ishga tushirish
npm run dev
# http://localhost:3000
```

---

## .env.local uchun kerakli qiymatlar

```
NEXT_PUBLIC_SUPABASE_URL=        # Supabase dashboard → Settings → API
NEXT_PUBLIC_SUPABASE_ANON_KEY=   # Supabase dashboard → Settings → API
SUPABASE_SERVICE_ROLE_KEY=       # Jamoa a'zosidan so'rang (git da yo'q)
```

---

## Papka tuzilmasi

```
src/
  app/          — sahifalar (Next.js App Router)
  components/   — UI komponentlar
  lib/          — servislar, utility funksiyalar
  types/        — TypeScript type/interface
supabase/
  migrations/   — DB migration fayllar
  seed.sql      — boshlang'ich data
.miya/          — MiyaAI memory fayllar
```

---

## Birinchi o'zgarish — qayerdan boshlash

```
Kichik UI o'zgarish:   src/components/ → tegishli komponent
Yangi sahifa:          src/app/[nomi]/page.tsx
Yangi API endpoint:    src/app/api/[nomi]/route.ts
DB o'zgartirish:       supabase/migrations/ → yangi fayl
```

---

## MiyaAI bilan ishlash

```bash
# Yangi sessiya boshlash
claude

# Davom etish (tugallanmagan ish bo'lsa)
# INCOMPLETE_WORK.md → Resume Prompt ni ko'ring
```

Birinchi xabar:
```
"Salom MiyaAI. [Nima qilmoqchiman]."
```

---

## Savollar uchun

```
Texnik arxitektura:   .miya/PROJECT.md
Qoidalar:             CLAUDE.md
Qarorlar tarixi:      .miya/DECISION_LOG.md
Tugallanmagan ishlar: .miya/INCOMPLETE_WORK.md
```
