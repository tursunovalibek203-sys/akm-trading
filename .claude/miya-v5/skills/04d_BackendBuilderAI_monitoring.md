# MODUL: BackendBuilderAI — Monitoring & Observability
## Yuklanadi: faqat monitoring/performance sessiyasida
## Asosiy fayl: 04_BackendBuilderAI.md

---

### K — MONITORING VA OBSERVABILITY

**45. Sentry Setup**
```typescript
// src/lib/sentry.ts
import * as Sentry from '@sentry/node'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,  // 10% request larda trace

  // Sensitive ma'lumotlarni o'chirish
  beforeSend(event) {
    if (event.request?.data) {
      delete event.request.data.password
      delete event.request.data.token
    }
    return event
  }
})

// Xatoni Sentry ga yuborish:
try {
  await riskyOperation()
} catch (error) {
  Sentry.captureException(error, {
    tags: { module: 'tasks', operation: 'create' },
    user: { id: userId }
  })
  throw error
}
```

**46. Structured Logging**
```typescript
// /utils/logger.ts
const logger = {
  info: (message: string, meta?: object) => {
    console.log(JSON.stringify({
      level: 'info',
      message,
      timestamp: new Date().toISOString(),
      ...meta
    }))
  },
  error: (message: string, error: unknown, meta?: object) => {
    console.error(JSON.stringify({
      level: 'error',
      message,
      error: error instanceof Error ? {
        name: error.name,
        message: error.message,
        stack: error.stack
      } : error,
      timestamp: new Date().toISOString(),
      ...meta
    }))
  }
}

// Ishlatish:
logger.info('Task created', { taskId, userId })
logger.error('DB connection failed', error, { retryCount: 3 })
```

**47. Health Check Endpoint**
```typescript
// /api/health — monitoring uchun majburiy
app.get('/health', async (req, res) => {
  const checks = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version,
    database: 'unknown',
    uptime: process.uptime()
  }

  try {
    // DB tekshirish
    await supabase.from('users').select('count').limit(1)
    checks.database = 'ok'
  } catch {
    checks.database = 'error'
    checks.status = 'degraded'
  }

  const statusCode = checks.status === 'ok' ? 200 : 503
  res.status(statusCode).json(checks)
})
```

**48. Alert Qoidalari**
```
Monitoring qoidalari (UptimeRobot / Grafana):

CRITICAL → darhol xabar (SMS + Telegram):
- /health endpoint 1 daqiqa javob bermasa
- Error rate > 5% (5 daqiqada)
- DB connection yo'q

HIGH → Telegram xabar:
- API response > 2s (o'rtacha)
- Memory > 80%
- Disk > 85%

MEDIUM → Email:
- Error rate > 1%
- API response > 1s
- CPU > 80% (5 daqiqa davomida)
```

---

