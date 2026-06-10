# DECISION_LOG.md — Qarorlar Tarixi

## QOIDA: Faqat APPEND. Eski qarorlar hech qachon o'chirilmaydi.

---

## FORMAT:

```
[SANA VAQT] QAROR: [nima qilindi]
SABAB: [nima uchun]
MUQOBIL: [boshqa variant va nima uchun rad etildi]
XAVF: [nima noto'g'ri ketishi mumkin]
KIM: [Foydalanuvchi / MiyaAI tavsiyasi]
```

---

## MISOL:

```
[2025-05-10 10:30] QAROR: Supabase Auth tanlandi (Firebase o'rniga)
SABAB: Supabase DB bilan to'liq integratsiya, RLS built-in, bepul tier yetarli
MUQOBIL: Firebase rad etildi — alohida DB kerak, narxi yuqori
XAVF: Supabase free plan 500MB limit — 3-4 oyda to'liq bo'lishi mumkin
KIM: Foydalanuvchi tasdiqladi

[2025-05-15 14:00] QAROR: Real-time bildirishnomalar Phase 2 ga qoldirildi
SABAB: MVP scope dan tashqari, 2 kun qo'shimcha ish
MUQOBIL: WebSocket Phase 1 da — rad etildi (vaqt yo'q)
XAVF: Foydalanuvchi real-time kutishi mumkin — onboarding da tushuntirish kerak
KIM: MiyaAI tavsiya qildi, Foydalanuvchi tasdiqladi
```
