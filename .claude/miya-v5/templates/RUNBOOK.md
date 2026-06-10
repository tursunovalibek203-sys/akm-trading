# RUNBOOK.md — Production Muammo Yo'riqnomasi

## Foydalanish
Muammo chiqganda — tegishli bo'limni toping, qadamlarni bajaring.

---

## 1. SAYT ISHLAMAYAPTI

```
1. Vercel status: vercel.com/status
2. Supabase status: status.supabase.com
3. Vercel dashboard → Deployments → oxirgi deploy xatosi bormi?

Xato topilsa:
  Deploy xatosi → "Rollback to previous" (Vercel dashboard)
  Supabase xatosi → maintenance page ko'rsatish (quyida)
```

---

## 2. DB SEKIN YOKI ISHLAMAYAPTI

```
1. Supabase dashboard → Database → "Database health"
2. Supabase dashboard → Logs → "Postgres logs"

Sekin so'rovlar:
  Logs da qaysi query sekin? → INDEX yetishmayaptimi?
  Vaqtincha yechim: sekin endpoint ni cache qiling

To'xtab qolgan:
  Supabase dashboard → "Restart database"
  Agar ishlamasa: Supabase support → support.supabase.com
```

---

## 3. DEPLOY MUVAFFAQIYATSIZ

```
1. Vercel → Deployments → oxirgi → "Build logs"
2. Xato qatorini toping

TypeScript xatosi:
  Local: npx tsc --noEmit → xatoni tuzating → push

Migration xatosi:
  Local: npx supabase db push → xatoni tuzating
  Staging da sinang → keyin production

Rollback kerak bo'lsa:
  Vercel → deployment → "..." → "Rollback to this deployment"
  DB rollback: npx supabase migration down --target [migration_nomi]
```

---

## 4. MIGRATION XATOSI (PRODUCTION)

```
AVVAL: Nima bo'ldi? Ma'lumot yo'qoldimi?
  Supabase → Table Editor → tekshiring

MA'LUMOT YO'QOLMAGAN:
  1. Migration rollback:
     npx supabase migration down --target [oldingi_migration]
  2. Xatoni tuzating
  3. Staging da sinang
  4. Qayta deploy

MA'LUMOT YO'QOLGAN (jiddiy):
  1. Supabase → Database → "Backups" → oxirgi backup
  2. Backup restore: Supabase dashboard → "Restore"
  3. Supabase support bilan bog'laning
```

---

## 5. AUTH ISHLAMAYAPTI

```
Foydalanuvchi kira olmayapti:
  1. Supabase → Auth → "Logs" → xatoni toping
  2. Email provider ishlayaptimi? (SMTP sozlash)
  3. Redirect URL to'g'rimi? (Supabase → Auth → URL Configuration)

Token muddati:
  Supabase config: autoRefreshToken: true bormi?
  Tekshirish: supabase/lib/client.ts
```

---

## 6. FOYDALANUVCHI XATO MA'LUMOT KO'RYAPTI

```
JIDDIY — darhol:
  1. Qaysi jadval, qaysi foydalanuvchi?
  2. Supabase → Authentication → Users → tekshiring
  3. RLS policy: Supabase → Table Editor → [jadval] → RLS
  4. Muvaqqat: shu jadvalni read-only qiling (RLS qattiqlash)
  5. Keyin: policy xatosini toping va tuzating
```

---

## 7. MAINTENANCE PAGE

```typescript
// src/middleware.ts ga qo'shish (vaqtincha)
export function middleware(request: NextRequest) {
  return NextResponse.redirect(new URL('/maintenance', request.url))
}

// src/app/maintenance/page.tsx
// "Texnik ishlar olib borilmoqda. Tez orada qaytamiz." sahifasi
```

---

## KONTAKTLAR

```
Supabase support:   support.supabase.com
Vercel support:     vercel.com/support
Jamoa:              [telegram/slack guruh]
```
