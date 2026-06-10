# FEATURE_FLAGS.md — Feature Flaglar Ro'yxati

## FORMAT
[flag_nomi]: [true/false] — [tavsif] — [sana]

## Flaglar
# currency_support: false — $ va sum qo'llab-quvvatlash — 2025-05-19
# ai_scheduling: false — AI avtomatik rejalashtirish — Phase 3

## Cleanup Tartibi
Flag 1 oy davomida barqaror ishlasa → kodni o'chirish vaqti:
1. Flag true qilinadi (doimiy)
2. if (isEnabled('flag')) bloki olib tashlanadi
3. Faqat true branch qoladi
4. Flag ro'yxatdan o'chiriladi
