# TECH_DEBT.md — Texnik Qarz Ro'yxati

## QOIDA: Faqat APPEND. Hal qilingan qarzlar [YOPILDI] belgilanadi.

---

## FORMAT:
```
[TD-NNN] DARAJA: TAVSIF — joyi (sana)
STATUS: ochiq | jarayonda | yopildi
```

---

## MISOL:

```
[TD-001] HIGH: N+1 query — tasks servisida getTasks() funksiyasi (2025-05-10)
STATUS: ochiq
NATIJA: 100 task = 101 query = ~3 sekund. Target: 1 query = 50ms
TUZATISH: Supabase select bilan join ishlatish

[TD-002] MEDIUM: Test yo'q — auth moduli (2025-05-12)
STATUS: ochiq
NATIJA: Refaktor qilib bo'lmaydi, regression xavfi
TUZATISH: vitest bilan unit test yozish (2 soat)

[TD-003] LOW: JSDoc yetishmaydi — 15 funksiya (2025-05-15)
STATUS: jarayonda
NATIJA: Keyingi dasturchi tushunmaydi
TUZATISH: DocumentationAI ga topshirish

[TD-001] HIGH: N+1 query — HAL QILINDI (2025-05-20) [YOPILDI]
```
