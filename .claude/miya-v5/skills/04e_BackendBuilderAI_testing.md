# MODUL: BackendBuilderAI — Testing
## Yuklanadi: faqat test sessiyasida
## Asosiy fayl: 04_BackendBuilderAI.md

---

### L — BACKEND UNIT TEST

**49. Backend Test Standart**
```typescript
// Vitest bilan backend test
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createTask } from '@/services/tasks'

// Supabase mock
vi.mock('@/lib/supabase', () => ({
  supabase: {
    from: vi.fn().mockReturnThis(),
    insert: vi.fn().mockReturnThis(),
    select: vi.fn().mockReturnThis(),
    single: vi.fn()
  }
}))

describe('createTask', () => {
  beforeEach(() => vi.clearAllMocks())

  it('muvaffaqiyatli yaratish', async () => {
    const mockTask = { id: 'uuid', title: 'Test', status: 'todo' }
    supabase.from().insert().select().single
      .mockResolvedValue({ data: mockTask, error: null })

    const result = await createTask({ title: 'Test', priority: 'low' }, 'userId')
    expect(result.data).toEqual(mockTask)
    expect(result.error).toBeNull()
  })

  it('validatsiya xato', async () => {
    const result = await createTask({ title: '', priority: 'low' }, 'userId')
    expect(result.data).toBeNull()
    expect(result.error).toBeTruthy()
  })

  it('DB xato', async () => {
    supabase.from().insert().select().single
      .mockResolvedValue({ data: null, error: { message: 'DB error' } })

    const result = await createTask({ title: 'Test', priority: 'low' }, 'userId')
    expect(result.error).toBe('DB error')
  })
})
```

**50. Test Coverage Qoidasi**
```
Har servis funksiyasi uchun MINIMAL testlar:
[ ] Happy path — normal ishlash
[ ] Validation error — noto'g'ri input
[ ] DB error — connection yoki constraint
[ ] Auth error — ruxsatsiz foydalanuvchi
[ ] Edge case — null, undefined, bo'sh string

Coverage target: 80%+
CI/CD da: coverage < 80% → deploy bloklanadi
```

---

### M — TEST MA'LUMOT GENERATSIYA

**51. Realistic Seed Data**
```typescript
// /supabase/seed.ts — TypeScript bilan real ko'rinishdagi data

import { faker } from '@faker-js/faker'

async function seedDatabase() {
  // 5 ta test foydalanuvchi
  const users = Array.from({ length: 5 }, () => ({
    id: faker.string.uuid(),
    email: faker.internet.email(),
    created_at: faker.date.past().toISOString()
  }))

  // Har foydalanuvchi uchun 10-20 ta task
  const tasks = users.flatMap(user =>
    Array.from({ length: faker.number.int({ min: 10, max: 20 }) }, () => ({
      id: faker.string.uuid(),
      user_id: user.id,
      title: faker.hacker.phrase(),
      status: faker.helpers.arrayElement(['todo', 'in_progress', 'done']),
      priority: faker.helpers.arrayElement(['low', 'medium', 'high']),
      deadline: faker.datatype.boolean()
        ? faker.date.future().toISOString()
        : null,
      created_at: faker.date.past().toISOString()
    }))
  )

  await supabase.from('users').insert(users)
  await supabase.from('tasks').insert(tasks)

  console.log(`Seeded: ${users.length} users, ${tasks.length} tasks`)
}
```

**52. Factory Pattern**
```typescript
// /tests/factories.ts — test uchun ob'ekt yaratish

export const taskFactory = {
  build: (overrides?: Partial<Task>): Task => ({
    id: 'test-uuid',
    user_id: 'test-user-id',
    title: 'Test vazifa',
    status: 'todo',
    priority: 'medium',
    deadline: null,
    created_at: new Date().toISOString(),
    ...overrides
  }),

  buildList: (count: number, overrides?: Partial<Task>): Task[] =>
    Array.from({ length: count }, (_, i) =>
      taskFactory.build({ id: `test-uuid-${i}`, ...overrides })
    )
}

// Ishlatish:
const task = taskFactory.build({ priority: 'high' })
const tasks = taskFactory.buildList(5, { status: 'done' })
```

---

