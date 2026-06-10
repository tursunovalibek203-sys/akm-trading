# CLAUDE.md — Trading AI Platform
# HAR SESSIYADA BIRINCHI O'QILADI
# Bu faylni to'liq o'qimay loyiha boshlanmaydi

---

## MIYA AI YUKLANISH TARTIBI

TIER 1 — sessiya boshida (har doim):
  @.claude/miya-v5/skills/01_MiyaAI_CORE.md
  @.claude/miya-v5/skills/01_MiyaAI_FUNCTIONS_T1.md
  @.claude/miya-v5/skills/01_MiyaAI_FUNCTIONS_INDEX.md
  @.claude/SESSION_LAST.md
  @.claude/TODO.md
  @.claude/USER_PROFILE.md

TIER 2 — vazifaga qarab (prompt kelgandan keyin):
  NEW_FEATURE → @.claude/miya-v5/skills/01_MiyaAI_FUNCTIONS_T2.md @.claude/PROJECT.md @.claude/SCHEMA_SNAPSHOT.md
  BUG_FIX     → @.claude/miya-v5/skills/01_MiyaAI_FUNCTIONS_T2.md @.claude/STATUS.md @.claude/ANTI_PATTERNS.md
  DEPLOY      → @.claude/miya-v5/skills/01_MiyaAI_FUNCTIONS_T2.md @.claude/RISK_REGISTER.md @.claude/RUNBOOK.md
  SPRINT      → @.claude/miya-v5/skills/01_MiyaAI_FUNCTIONS_T2.md @.claude/SPRINT_PLAN.md @.claude/INCOMPLETE_WORK.md
  REFACTOR    → @.claude/miya-v5/skills/01_MiyaAI_FUNCTIONS_T2.md @.claude/TECH_DEBT.md @.claude/DEPENDENCY_MAP.md

TIER 3 — hodisada:
  @.claude/miya-v5/skills/01_MiyaAI_FUNCTIONS_T3.md

---

## LOYIHA
```
Nomi: Trading AI Platform
Nima qiladi: Crypto bozori uchun AI-signal va avtomatik savdo tizimi (Binance, Bybit)
Foydalanuvchilar: Crypto treyderlar — Guest / Free / Pro / Admin
Hozirgi faza: Faza 1 — Foundation MVP
Faza maqsadi: Auth + Market Data + Real-time chart + Manual signal + Dashboard
TZ versiyasi: v4.0 (Professional Edition — 35 bo'lim)
```

---

## STACK
```
Frontend:         Next.js 15 App Router + TypeScript 5 (strict)
Backend:          Python FastAPI 0.115+ (asosiy API, Faza 1 monolith)
Auth Service:     Node.js 20 + JWT RS256 (Faza 3+ da ajratiladi)
Database:         PostgreSQL 15 + TimescaleDB extension
Cache:            Redis 7 Cluster
Column Store:     ClickHouse (Faza 5 backtestdan)
Message Queue:    Apache Kafka (Faza 3+ dan)
Auth:             Custom JWT RS256 — access 15 daqiqa / refresh 7 kun + TOTP 2FA
State:            Zustand 4
Styling:          Tailwind CSS 3 + Radix UI (accessibility)
Charts:           TradingView Lightweight Charts (ochiq manba)
Animations:       Framer Motion
AI Engine:        Claude API — Haiku (pre-screen) + Sonnet (asosiy) + Opus (kritik)
Testing:          Vitest + Playwright + Pytest
Deploy (dev):     Docker Compose
Deploy (prod):    AWS multi-region (ECS + RDS + ElastiCache)
Mobile:           React Native (Faza 7)
```

---

## PAPKA TUZILMASI
```
trading-ai-platform/        ← loyiha root
  frontend/                 ← Next.js ilovasi
    src/
      app/
        (auth)/             ← login, register, 2fa
        (dashboard)/        ← asosiy UI layout
          dashboard/        ← bosh sahifa
          chart/            ← TradingView + zonalar
          signals/          ← signal tarixi
          portfolio/        ← pozitsiyalar
          risk/             ← risk dashboard
          execution/        ← execution monitor (Faza 3+)
          settings/         ← foydalanuvchi sozlamalari
        api/                ← Next.js proxy routes
      components/
        ui/                 ← Radix UI asosiy komponentlar
        features/
          trading/          ← Chart, ZoneEditor, SignalCard
          portfolio/        ← PositionRow, PnLWidget
          risk/             ← HeatGauge, CircuitBreakerStatus
          auth/             ← LoginForm, TwoFactorSetup
      services/             ← backend API call funksiyalari
      store/                ← Zustand store lar
      types/                ← global TypeScript tiplar
      lib/                  ← constants.ts, helpers, config
      hooks/                ← custom React hooks
    public/
    .env.local
    next.config.ts
    tailwind.config.ts
    tsconfig.json

  backend/                  ← FastAPI ilovasi
    app/
      api/
        v1/
          auth/             ← register, login, refresh, logout, 2fa
          market/           ← price, klines, orderbook
          signals/          ← signal CRUD, trigger
          zones/            ← zone CRUD
          trades/           ← savdo tarixi
          portfolio/        ← pozitsiyalar, P&L
          execution/        ← analytics (Faza 3+)
          ai/               ← Claude API endpoints (Faza 2+)
      core/
        config.py           ← settings (env vars)
        database.py         ← PostgreSQL + TimescaleDB ulanish
        redis.py            ← Redis ulanish
        security.py         ← JWT, password hashing
        logger.py           ← logging config
      models/               ← SQLAlchemy ORM modellari
      schemas/              ← Pydantic request/response
      services/
        market/             ← Binance/Bybit WebSocket + REST
        ai/                 ← Claude API (Faza 2+)
        risk/               ← risk hisoblash (Faza 4+)
        execution/          ← order management (Faza 3+)
      migrations/           ← Alembic migration fayllar
    tests/
    .env
    requirements.txt
    alembic.ini

  docker/
    docker-compose.yml      ← dev: PostgreSQL + TimescaleDB + Redis
    docker-compose.prod.yml
    postgres/
      init.sql              ← TimescaleDB extension yoqish

  .claude/                  ← MiyaAI memory fayllar
  .gitignore
  README.md
```

---

## MUHIT O'ZGARUVCHILARI
```
# Frontend (.env.local)
NEXT_PUBLIC_API_URL              ← Backend API base URL
NEXT_PUBLIC_WS_URL               ← WebSocket URL

# Backend (.env)
DATABASE_URL                     ← PostgreSQL ulanish string
REDIS_URL                        ← Redis ulanish string
KAFKA_BROKERS                    ← Kafka broker lar (Faza 3+)
CLICKHOUSE_URL                   ← ClickHouse (Faza 5+)
ANTHROPIC_API_KEY                ← Claude API kalit (Faza 2+)
ANTHROPIC_MODEL_SONNET           ← claude-sonnet-4-20250514
ANTHROPIC_MODEL_HAIKU            ← claude-haiku-4-5-20251001
ANTHROPIC_MODEL_OPUS             ← claude-opus-4-20250514
BINANCE_BASE_URL                 ← https://api.binance.com
BINANCE_WS_URL                   ← wss://stream.binance.com:9443
BYBIT_BASE_URL                   ← https://api.bybit.com
JWT_PRIVATE_KEY                  ← RSA 2048-bit private key
JWT_PUBLIC_KEY                   ← RSA public key
ENCRYPTION_KEY                   ← API kalit shifrlash (AES-256-GCM)
AWS_KMS_KEY_ID                   ← AWS KMS (prod da)
FCM_SERVER_KEY                   ← Firebase push (Faza 2+)
SENTRY_DSN                       ← Xato monitoring
```

---

## MAJBURIY KODLASH QOIDALARI
```
TYPESCRIPT (Frontend):
- any type MUMKIN EMAS — TypeScript strict: true
- Har service funksiyasi ServiceResult<T> qaytaradi
- Zustand faqat global/server state — UI state useState da
- Biznes logika hooks da — komponent ichida emas
- Hardcode string yo'q — src/lib/constants.ts da
- console.log yo'q — src/lib/logger.ts ishlatiladi
- Mavjud UI komponentga MiyaAI ruxsatisiz tegmaydi

PYTHON (Backend):
- Type hints barcha funksiyalarda majburiy
- Pydantic model barcha request/response uchun
- Har endpoint ResponseModel ko'rsatiladi
- print() yo'q — app/core/logger.py ishlatiladi
- Hardcode qiymat yo'q — app/core/config.py da
- Migration da upgrade() + downgrade() ikkalasi majburiy

XAVFSIZLIK (har doim):
- API kalit plain text DB da HECH QACHON — AES-256-GCM shifrlash
- Withdrawal ruxsati birja API kalitiga HECH QACHON berilmaydi
- JWT token HttpOnly Secure cookie da — localStorage YO'Q
- SQL injection — faqat SQLAlchemy ORM / parametrlangan query
- Input validation — barcha endpoint da Pydantic/Zod
```

---

## MUHIM QARORLAR
```
1. Faza 1 da monolith FastAPI (microservices emas)
   Sabab: MVP tezligi muhim, Faza 3+ dan Kafka orqali ajratiladi

2. AI model zanjiri: Haiku → Sonnet → Opus
   Sabab: Xarajat optimizatsiya — zaif signal Haiku da filtrlash

3. TradingView Lightweight Charts (to'liq TradingView emas)
   Sabab: Ochiq manba, yengil, professional ko'rinish

4. Custom JWT (Supabase Auth emas)
   Sabab: API kalit xavfsizligi muhim, to'liq nazorat kerak

5. TimescaleDB PostgreSQL extension (alohida DB emas)
   Sabab: Faza 1 da murakkablikni kamaytirish, keyin ajratish mumkin
```

---

## CHEKLOVLAR
```
FAZA 1 DA YO'Q:
- Avtomatik savdo — Faza 4 da
- Claude AI signal — Faza 2 da
- On-chain tahlil — Faza 5 da
- Backtesting — Faza 5 da
- Iceberg/TWAP order — Faza 3 da
- Mobile app — Faza 7 da
- Telegram bot — Faza 8 da
- Kafkа — Faza 3 da
- ClickHouse — Faza 5 da

HAR DOIM YO'Q:
- Withdrawal ruxsati birja API kalitida
- Foydalanuvchi shaxsiy ma'lumoti Claude API ga
- Plain text API kalit DB da
- Real pul Faza 4 gacha savdo
```

---

## TASHQI SERVISLAR
```
Binance API:      narx ma'lumoti + WebSocket stream + savdo (Faza 4+)
Bybit API:        narx ma'lumoti + WebSocket stream + savdo (Faza 4+)
Claude API:       AI signal tahlili — Faza 2 dan (Anthropic)
TradingView:      chart — Lightweight Charts kutubxona
Firebase FCM:     push bildirishnoma — Faza 2 dan
Telegram Bot API: signal bildirishnomasi — Faza 8 dan
AWS KMS:          API kalit shifrlash — prod da
Sentry:           xato monitoring — Faza 1 dan
```

---

## AGENT UCHUN MINIMAL TALAB
```
1. Frontend Next.js 15 App Router, backend FastAPI — alohida papkalar
2. frontend/src/ va backend/app/ tuzilmasini bil
3. ServiceResult<T> (TS) va ResponseModel (Python) majburiy
4. Withdrawal ruxsati YO'Q — bu qattiq cheklov, hech qachon
5. Faza 1 da — Auth + Market Data + Chart + Manual signal
6. Har migration da upgrade() + downgrade() ikkalasi bor
7. JWT HttpOnly Secure cookie — localStorage MUMKIN EMAS
```
