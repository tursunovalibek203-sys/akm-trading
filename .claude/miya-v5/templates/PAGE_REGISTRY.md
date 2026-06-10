# PAGE_REGISTRY.md — Sahifalar Xaritasi
# MiyaAI har yangi funksiya tahlilida shu fayldan foydalanadi
# Yangi sahifa qo'shilganda — yangi yozuv qo'shiladi

## FORMAT
---
## [Sahifa nomi] — /[route]
FAYL: src/pages/[Fayl].tsx
VAZIFA: [nima qiladi — 1 gap]

ELEMENTLAR:
→ Tugmalar:
   - [Tugma] → [servis.funksiya()] → [jadval]
→ Inputlar:
   - [Input] → [Zod schema] → [jadval.field]
→ Ko'rsatiladigan ma'lumot:
   - [Element] → [servis.query()] → [jadval.field]
→ Formalar:
   - [Forma] → [action] → [endpoint]

BOG'LIQLIKLAR:
→ Servislar: [ro'yxat]
→ Store: [Zustand store lar]
→ DB jadvallar: [ro'yxat]
→ Boshqa sahifalar: [ro'yxat]

AUTH:
→ Kim ko'ra oladi: [rol]
→ RLS: [qoida]
---

## Sahifalar
[Hali sahifa yo'q — MiyaAI loyiha o'rgangach to'ldiradi]
