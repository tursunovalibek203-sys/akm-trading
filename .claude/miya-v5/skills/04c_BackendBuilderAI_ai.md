# MODUL: BackendBuilderAI — AI Integration
## Yuklanadi: faqat AI/LLM integratsiya sessiyasida
## Asosiy fayl: 04_BackendBuilderAI.md

---

### J — AI PROMPT ENGINEERING

**41. System Prompt Dizayni**
```typescript
// /services/ai.ts da system prompt standartlari:

const TASK_BREAKDOWN_PROMPT = `
Sen vazifalarni kichik qismlarga bo'luvchi assistentsan.

QOIDALAR:
- Faqat JSON qaytarasan, boshqa hech narsa yo'q
- subtasks: 3-7 ta bo'lishi kerak
- estimatedTime: daqiqada, 15-480 orasida
- Har subtask aniq va bajariladigan bo'lishi kerak

TAQIQLANGAN:
- Markdown yozma
- Tushuntirish berma
- JSON dan tashqari hech narsa yozma

FORMAT:
{"subtasks": ["string"], "estimatedTime": number}
`
// Nima uchun muhim:
// - Aniq format = hallucination kamayadi
// - TAQIQLANGAN bo'lim = kutilmagan chiqish yo'q
// - Misol format = to'g'ri parse qilinadi
```

**42. Token Tejash Strategiyasi**
```typescript
// 1. Input qisqartirish
function truncateContext(text: string, maxTokens: number = 500): string {
  const words = text.split(' ')
  // ~1 token = 0.75 so'z
  const maxWords = Math.floor(maxTokens * 0.75)
  return words.slice(0, maxWords).join(' ')
}

// 2. Faqat kerakli ma'lumot
// YOMON: Barcha task historiyani yuborish
// YAXSHI: Faqat oxirgi 5 ta task

// 3. Model tanlash
// GPT-4o: murakkab tahlil (qimmat)
// GPT-3.5-turbo: oddiy classification (arzon, 10x)

// 4. Caching — bir xil input = bir xil natija
const cache = new Map<string, AITaskBreakdown>()
async function getCachedBreakdown(title: string) {
  const key = title.toLowerCase().trim()
  if (cache.has(key)) return cache.get(key)!
  const result = await generateTaskBreakdown(title)
  cache.set(key, result)
  return result
}
```

**43. Hallucination Kamaytirish**
```typescript
// 1. Typed output — schema bilan validatsiya
const AISchema = z.object({
  subtasks: z.array(z.string()).min(1).max(10),
  estimatedTime: z.number().min(5).max(480)
})

async function safeAICall(prompt: string) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    temperature: 0.3,  // Past = deterministik
    response_format: { type: 'json_object' }, // JSON mode
    messages: [{ role: 'user', content: prompt }]
  })

  const text = response.choices[0].message.content
  const parsed = JSON.parse(text ?? '{}')

  // Validatsiya — xato bo'lsa fallback
  const result = AISchema.safeParse(parsed)
  if (!result.success) {
    return { data: null, error: 'AI invalid response' }
  }
  return { data: result.data, error: null }
}

// 2. Temperature: 0.0-0.3 (faktlar va kod uchun)
// 3. Few-shot examples: 1-2 ta misol bering
// 4. Negative instructions: "Taxmin qilma"
```

**44. AI Xato Boshqarish**
```typescript
async function robustAICall<T>(
  fn: () => Promise<T>,
  fallback: T
): Promise<T> {
  const maxRetries = 3
  const delays = [1000, 2000, 4000] // Exponential backoff

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      if (error instanceof RateLimitError) {
        await sleep(delays[i])
        continue
      }
      if (error instanceof InvalidResponseError) {
        // Retry prompt bilan
        continue
      }
      // Boshqa xato — fallback qaytarish
      console.error('AI call failed:', error)
      return fallback
    }
  }
  return fallback
}
```

---

