# ANTI_PATTERNS.md — Qilingan Xatolar

## QOIDA: Faqat APPEND. Bir xil xato qaytarilmaslik uchun saqlanadi.

---

## FORMAT:
```
[AP-NNN] SANA: TAVSIF
Natija: [nima bo'ldi]
Tuzatish: [qanday hal qilindi]
Oldini olish: [qoidasi]
```

---

## MISOL:

```
[AP-001] 2025-05-10: God component — TaskPage.tsx 500+ qatorga yetdi
Natija: Maintain qilish qiyin, test yozib bo'lmaydi
Tuzatish: TaskList, TaskCard, TaskFilter ga ajratildi
Oldini olish: Komponent 300 qatordan oshsa — bo'lish kerak

[AP-002] 2025-05-12: Frontend da biznes logika yozildi (TaskPage da filter)
Natija: Test qilib bo'lmaydi, backend bilan dublikat
Tuzatish: useTaskFilter hook ga ko'chirildi
Oldini olish: Biznes logika doim service yoki hook da

[AP-003] 2025-05-15: Migration DOWN yozilmadi
Natija: Rollback qilib bo'lmadi, manual tuzatish kerak bo'ldi
Tuzatish: Manual rollback qilindi (1 soat yo'qotildi)
Oldini olish: Har migration da UP + DOWN MAJBURIY
```
