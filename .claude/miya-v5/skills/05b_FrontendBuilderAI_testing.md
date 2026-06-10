# MODUL: FrontendBuilderAI — Testing & Visual
## Yuklanadi: faqat test yozish yoki visual regression sessiyasida
## Asosiy fayl: 05_FrontendBuilderAI.md

---

### K — E2E VA KOMPONENT TEST

**26. Playwright E2E Test**
```typescript
// /tests/e2e/tasks.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Task yaratish', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login')
    await page.fill('[name="email"]', 'test@test.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard')
  })

  test('yangi task yaratish', async ({ page }) => {
    // "+" tugmani bos
    await page.click('[aria-label="Yangi vazifa qo\'shish"]')

    // Modal ochildi
    await expect(page.locator('[role="dialog"]')).toBeVisible()

    // Form to'ldirish
    await page.fill('[name="title"]', 'Test vazifa')
    await page.selectOption('[name="priority"]', 'high')

    // Saqlash
    await page.click('button:has-text("Saqlash")')

    // Modal yopildi
    await expect(page.locator('[role="dialog"]')).not.toBeVisible()

    // Task ro'yxatda ko'rinadi
    await expect(page.locator('text=Test vazifa')).toBeVisible()
  })

  test('bo\'sh title bilan saqlash bloklanadi', async ({ page }) => {
    await page.click('[aria-label="Yangi vazifa qo\'shish"]')
    await page.click('button:has-text("Saqlash")')

    // Xato ko'rsatiladi
    await expect(page.locator('text=Sarlavha kiritish shart')).toBeVisible()
  })
})
```

**27. Komponent Test (Vitest + RTL)**
```typescript
// /tests/components/TaskCard.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { TaskCard } from '@/components/tasks/TaskCard'
import { taskFactory } from '@/tests/factories'

describe('TaskCard', () => {
  const mockTask = taskFactory.build()
  const onComplete = vi.fn()
  const onDelete = vi.fn()

  it('task ma\'lumotlarini ko\'rsatadi', () => {
    render(<TaskCard task={mockTask} />)
    expect(screen.getByText(mockTask.title)).toBeInTheDocument()
    expect(screen.getByText('O\'rta')).toBeInTheDocument() // priority
  })

  it('complete tugma ishlaydi', async () => {
    render(<TaskCard task={mockTask} onComplete={onComplete} />)
    await userEvent.click(screen.getByRole('button', { name: /bajarildi/i }))
    expect(onComplete).toHaveBeenCalledWith(mockTask.id)
  })

  it('loading holatida tugma disabled', () => {
    render(<TaskCard task={mockTask} isLoading={true} />)
    expect(screen.getByRole('button', { name: /bajarildi/i })).toBeDisabled()
  })

  it('accessibility: aria-label mavjud', () => {
    render(<TaskCard task={mockTask} onDelete={onDelete} />)
    expect(screen.getByRole('button', { name: /o'chirish/i })).toHaveAttribute('aria-label')
  })
})
```

**28. Hook Test**
```typescript
// /tests/hooks/useTaskFilter.test.ts
import { renderHook, act } from '@testing-library/react'
import { useTaskFilter } from '@/hooks/useTaskFilter'
import { taskFactory } from '@/tests/factories'

describe('useTaskFilter', () => {
  const tasks = taskFactory.buildList(5, { status: 'todo' })

  it('barcha tasklar ko\'rsatiladi (default)', () => {
    const { result } = renderHook(() => useTaskFilter(tasks))
    expect(result.current.filtered).toHaveLength(5)
  })

  it('status bo\'yicha filter', () => {
    const { result } = renderHook(() => useTaskFilter(tasks))
    act(() => result.current.setFilter({ status: 'done' }))
    expect(result.current.filtered).toHaveLength(0)
  })
})
```

---

## YANGILANGAN ISHLASH TARTIBI

```
1. MiyaAI dan instructions keladi
       ↓
2. Mavjud komponentlar tahlil qilinadi
       ↓
3. Komponent arxitekturasi belgilanadi
       ↓
4. TypeScript types yoziladi
       ↓
5. Komponent yoziladi
   → Props, State, Loading, Error, Accessibility
       ↓
6. Realtime integration (kerak bo'lsa)
       ↓
7. Komponent va hook testlar yoziladi
       ↓
8. E2E test (asosiy flow uchun)
       ↓
9. Natija MiyaAI ga qaytariladi
```

---

## EXECUTION STYLE
UX-first, type-safe, accessible, performance-aware, realtime-ready, fully-tested, production-grade frontend engineer.

---

## ⚡ UNIVERSAL QOIDA
→ 01_MiyaAI.md — "UNIVERSAL QOIDA — BARCHA AGENTLARGA MAJBURIY" bo'limiga qarang.


---

## ⚡ YANGI PROTOKOLLAR (v3.0)

### MULTI-VARIANT TAKLIF
Har muhim UI qaror uchun 3 variant:
```
VARIANT 1 — Tez: oddiy implementation, kam vaqt
VARIANT 2 — Balansli: UX + tezlik (TAVSIYA)
VARIANT 3 — Professional: to'liq accessible, animatsiya
```

### QAROR ASOSLASH
```
NIMA: [UI qaror]
NIMA UCHUN: [UX sabab]
MUQOBIL: [rad etilgan variant]
FOYDALANUVCHI TA'SIRI: [qanday his qiladi]
```

### EFFORT ESTIMATION
```
KICHIK  (< 1 soat): tugma, input, kichik komponent
O'RTA   (1-4 soat): sahifa, form, modal
KATTA   (4-8 soat): murakkab komponent, animatsiya
EPIC    (1+ kun):   to'liq modul UI

Token sarfi: KICHIK ~3K | O'RTA ~10K | KATTA ~25K | EPIC ~50K+
```

### UI QARZ NAZORAT
```
- Accessibility qo'shilmadimi? → TD ga yoz
- Test yozilmadimi? → TD ga yoz
- Responsive tekshirilmadimi? → TD ga yoz
```

### DEPLOY READINESS SIGNAL
```json
{
  "agent": "FrontendBuilderAI",
  "status": "done",
  "deploy_blockers": [],
  "accessibility_issues": [],
  "tests_missing": []
}
```

---

## ⚡ XATO OLDINI OLISH TIZIMI (v3.3)

### KOD YOZILAYOTGANDA

**Lint on Save (VS Code)**
```json
// .vscode/settings.json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.formatOnSave": true,
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

**Prettier Konfiguratsiya**
```json
// .prettierrc
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

**Snapshot Testing**
```typescript
// Komponent UI o'zgarsa — avtomatik aniqlanadi
import { render } from '@testing-library/react'
import { TaskCard } from './TaskCard'

it('TaskCard snapshot', () => {
  const { container } = render(
    <TaskCard task={mockTask} />
  )
  expect(container).toMatchSnapshot()
})
// Tasodifan UI o'zgartirsa → test fail → bloklaydi
```

**API Contract Testing**
```typescript
// Backend endpoint o'zgarganda — Frontend bilan mos?
import { describe, it, expect } from 'vitest'
import { taskSchema } from '@/types/schemas'

it('API response schema mos', async () => {
  const response = await fetch('/api/tasks')
  const data = await response.json()

  // Har response typed schema bilan tekshiriladi
  expect(() => taskSchema.parse(data.data[0])).not.toThrow()
})
```

### COMMIT QILISHDAN OLDIN

**Frontend lint-staged**
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "vitest related --run"
    ],
    "*.{css,scss}": [
      "prettier --write",
      "stylelint --fix"
    ]
  }
}
```

**Accessibility Check**
```bash
# Pre-commit da
npx axe-core-cli src/**/*.tsx
# WCAG qoidalari buzilsa → bloklanadi
```

### DEFINITION OF DONE (Frontend)

```
UI:
[ ] Mobile (375px) tekshirildi
[ ] Skeleton loading bor
[ ] Empty state bor
[ ] Error state bor
[ ] Loading state bor

ACCESSIBILITY:
[ ] aria-label lar bor
[ ] Keyboard navigation ishlaydi
[ ] Kontrast ratio 4.5:1+
[ ] Touch target 44px+

TEST:
[ ] Komponent test yozilgan
[ ] Snapshot test o'tdi
[ ] Hook test yozilgan
[ ] E2E (asosiy flow) o'tdi

KOD:
[ ] any type yo'q
[ ] Console.log yo'q
[ ] Props interface yozilgan
[ ] Fayl 300 qatordan kam

PERFORMANCE:
[ ] React.memo kerak joyda
[ ] Lazy load katta sahifalar
[ ] Bundle size o'smadi

HAMMASI ✓ → "Tayyor"
BIROR ❌  → "Tayyor emas"
```

---

## ⚡ SYSTEM IMPACT ANALYSIS (v3.3)

### NIMA BU?
Yangi UI element yoki o'zgarish bajarishdan OLDIN —
butun frontend tizimini ko'rib, ta'sirlangan barcha joylarni aniqlaydi.

### ISHLASH TARTIBI:
```
1. MiyaAI dan instructions keladi
2. FrontendBuilderAI BAJARMAYDI — avval tekshiradi:

FRONTEND IMPACT TAHLILI:
━━━━━━━━━━━━━━━━━━━━━━
O'zgarish: [nima]

Komponent ta'siri:
→ Qaysi komponentlar o'zgaradi?
→ Yangi komponent kerakmi?
→ Mavjud props o'zgaradimi?

State ta'siri:
→ Qaysi Zustand store o'zgaradi?
→ Yangi store kerakmi?
→ Selector lar o'zgaradimi?

UI izchillik:
→ Boshqa sahifalarda ham ko'rsatilishi kerakmi?
→ Bir joyda o'zgartirish boshqa joy bilan mos kelmay qoladimi?

Type ta'siri:
→ /types/index.ts o'zgaradimi?
→ Boshqa komponentlar bu typeni ishlatadimi?

3. MiyaAI ga tahlil yuboriladi
4. Foydalanuvchi qaror bergandan keyin bajariladi
```

### MISOL:
```
So'rov: "Sotув sahifaga $ va sum valyuta tanlash qo'sh"

FrontendBuilderAI tahlili:
→ SalesPage o'zgaradi (valyuta selector)
→ CashierPage ham o'zgarishi kerak (izchillik)
→ ClientBalance ham o'zgarishi kerak (balans valyutasi)
→ Zustand: usePaymentStore ga currency field kerak
→ Types: Payment interface ga currency: 'USD'|'UZS' kerak
→ Boshqa komponentlar Payment typeni ishlatadi — ta'sirlanadi

MiyaAI ga:
"4 ta sahifa va 2 ta store ta'sirlanadi.
 Faqat SalesPage yoki hammasi?"
```

---

## ⚡ SYSTEM UNDERSTANDING — FRONTEND (v3.4)

### KOD SKANERLASH
```
Yangi o'zgarish oldidan frontend fayllarni skanerlaydi:

1. Kalit so'z → /components/, /store/, /hooks/, /pages/ da qidirish
2. Topilgan komponentlar → ta'sirlanadi
3. Ishlatilmagan joylar → qo'shish kerak bo'lishi mumkin

Misol:
"currency" → SalesPage da bor, CashierPage da yo'q
→ CashierPage ham o'zgarishi kerak (MiyaAI ga xabar)
```

### KASKAD SIMULATSIYASI
```
Type o'zgarse:
Daraja 1: O'sha type + uni ishlatgan komponentlar
Daraja 2: O'sha komponentni ishlatgan sahifalar
Daraja 3: Sahifani ishlatgan layout/router

Props o'zgarse:
→ Barcha ishlatgan joylar topiladi
→ Breaking change bormi? → ogohlantiradi
```

---

## ⚡ PROFESSIONAL METODOLOGIYALAR (v3.6)

### Storybook
```typescript
// Har yangi komponent uchun .stories.tsx:
// Barcha state lar ko'rsatiladi:
// Default, Loading, Error, Empty, Disabled
// UI regression — screenshot bilan avtomatik
```

### Feature Flags
```typescript
// Katta yangi funksiya uchun:
import { isEnabled } from '@/lib/flags'

if (isEnabled('currency_support')) {
  return <CurrencySelector />
}
// Deploy = xavfsiz (flag o'chiq)
// Test = flag yoqiladi
// Muammo = flag o'chiriladi (30 soniya rollback)
```

### Contract Testing
```typescript
// API response format o'zgarganda:
// Frontend shartnoma yozadi
// Backend shart bajaradi
// Mos kelmasa → CI/CD da bloklanadi
```

### Observability
```typescript
// Har muhim user action:
span.setAttributes({
  'user.action': 'payment.create',
  'payment.currency': data.currency
})
// "Tugma bosildi → qancha vaqt → qayerda sekin" — aniq ko'rinadi
```

### Visual Regression Testing
```bash
# Har PR da screenshot taqqoslanadi:
npx chromatic --project-token=[token]
# UI tasodifan o'zgarse → bloklanadi
```

---

## ⚡ DB-FRONTEND SINXRONLIGI (v3.7)

### QATTIQ QOIDA — HAR ELEMENT UCHUN
```
Har komponent yozilganda MAJBURIY tekshirish:

1. Bu element qaysi DB field dan keladi?
   → aniq ko'rsatiladi: payments.amount, stock.quantity

2. Ulanish zanjiri to'liqmi?
   DB field → servis funksiya → typed response → store → UI

3. any type bormi? → FORBIDDEN
   payments.amount: number (emas: any)
   stock.quantity: number (emas: any)

4. Realtime: DB o'zgarganda UI ham o'zgaradimi?
   → Supabase realtime yoki polling

MISOL:
Kassa balansi komponenti:
→ DB: cashier.balance (numeric)
→ Servis: cashierService.getBalance(): Promise<number>
→ Store: usePaymentStore(state => state.cashierBalance)
→ UI: <span>{formatCurrency(cashierBalance)}</span>
→ Realtime: payments o'zgarganda → store yangilanadi → UI yangilanadi
→ any: YO'Q — har qadamda number type
```

### REALTIME CONSISTENCY
```typescript
// DB o'zgarganda Frontend DARHOL yangilanadi:
useEffect(() => {
  const channel = supabase
    .channel('cashier-updates')
    .on('postgres_changes',
      { event: '*', schema: 'public', table: 'payments' },
      async () => {
        // Yangi balans DB dan olinadi — taxmin EMAS
        const { data } = await cashierService.getBalance()
        setCashierBalance(data)
      }
    )
    .subscribe()

  return () => supabase.removeChannel(channel)
}, [])
```


---

## ⚡ NATIJA PERSISTENCE (v4.0)

Natija ekranda ko'rsatiladi VA faylga yoziladi:
```
.miya/results/[YYYYMMDD_HHMMSS]_[agent_nomi].json
```
Papka yo'q bo'lsa: mkdir -p .miya/results/ buyrug'i beriladi.
