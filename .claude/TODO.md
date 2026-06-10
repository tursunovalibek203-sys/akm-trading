# TODO.md — Trading AI Platform
# MASTER MANBA — bu fayl barcha vazifalarning asosiy manbasi
# Sprint/Session emas — bu loyihaning to'liq vazifalar ro'yxati
# [x] = bajarildi | [ ] = kutmoqda | [~] = jarayonda

---

## FAZA 1 — FOUNDATION MVP ✅ YAKUNLANDI (2026-06-04)
### Maqsad: Auth + Market Data + Real-time chart + Manual signal + Dashboard

---

### 1.0 Loyiha Infratuzilmasi
```
[x] 1.0.1  Proyekt papka tuzilmasini yaratish (frontend/ + backend/ + docker/)
[x] 1.0.2  Docker Compose sozlash (PostgreSQL 15 + TimescaleDB + Redis 7)
[x] 1.0.3  docker/postgres/init.sql — TimescaleDB extension yoqish
[x] 1.0.4  Next.js 15 App Router + TypeScript 5 (strict) sozlash
[x] 1.0.5  FastAPI 0.115+ proyekt skeleti (app/ tuzilmasi)
[x] 1.0.6  Alembic migration tizimi sozlash
[x] 1.0.7  Tailwind CSS 3 sozlash (Radix UI emas, to'g'ridan Tailwind)
[x] 1.0.8  Framer Motion qo'shish (package.json da)
[x] 1.0.9  ESLint (frontend) sozlash
[x] 1.0.10 Black + Ruff (backend Python) sozlash
[x] 1.0.11 .env.example va .env.local.example yaratish
[x] 1.0.12 .gitignore (session fayllar, .env, __pycache__)
[x] 1.0.13 requirements.txt (backend)
[x] 1.0.14 package.json dependencies (frontend)
[x] 1.0.15 Sentry integratsiyasi (backend — DSN optional)
```

---

### 1.1 Auth — Backend (FastAPI)
```
[x] 1.1.1  users jadvali migration
[x] 1.1.2  user_sessions jadvali migration (refresh token boshqaruvi)
[x] 1.1.3  bcrypt (cost 12) password hashing utility
[x] 1.1.4  JWT RS256 — private/public key yaratish + config
[x] 1.1.5  Access token (15 daqiqa) yaratish funksiyasi
[x] 1.1.6  Refresh token (7 kun) yaratish + Redis blacklist
[x] 1.1.7  POST /api/v1/auth/register endpoint
[x] 1.1.8  POST /api/v1/auth/login endpoint (access + refresh cookie qaytaradi)
[x] 1.1.9  POST /api/v1/auth/refresh endpoint (cookie-based)
[x] 1.1.10 POST /api/v1/auth/logout endpoint (cookie tozalash)
[x] 1.1.11 GET  /api/v1/auth/me endpoint (joriy foydalanuvchi)
[x] 1.1.12 TOTP 2FA — pyotp kutubxona
[x] 1.1.13 POST /api/v1/auth/2fa/setup endpoint (QR code qaytaradi)
[x] 1.1.14 POST /api/v1/auth/2fa/verify endpoint
[x] 1.1.15 POST /api/v1/auth/2fa/disable endpoint
[x] 1.1.16 Rate limiting — slowapi (5/min register, 10/min login, 20/min refresh)
[x] 1.1.17 Auth middleware — JWT tekshirish dependency (cookie + Bearer)
```

---

### 1.2 Auth — Frontend (Next.js)
```
[x] 1.2.1  Dark mode dizayn tizimi (Tailwind config — rang palitrasi TZ 17.1 dan)
[x] 1.2.2  Auth layout (auth group)
[x] 1.2.3  Login sahifasi + inline validatsiya
[x] 1.2.4  Register sahifasi + forma
[x] 1.2.5  2FA verify sahifasi (TOTP kodi kiritish)
[x] 1.2.6  2FA setup sahifasi (QR code ko'rsatish)
[x] 1.2.7  Auth Zustand store (user, token in-memory, isAuthenticated)
[x] 1.2.8  Axios interceptor — token refresh (401 da avtomatik, cookie-based)
[x] 1.2.9  Protected route middleware (Next.js middleware.ts)
[x] 1.2.10 Logout funksiyasi (cookie + store tozalash)
[x] 1.2.11 "Meni eslab qol" checkbox (refresh token 30 kunga uzayadi)
```

---

### 1.3 Market Data — Backend
```
[x] 1.3.1  Binance WebSocket ulanish klient (websockets kutubxona)
[x] 1.3.2  bookTicker stream — best bid/ask real-time
[x] 1.3.3  klineStream — OHLCV 1m, 5m, 15m, 1h, 4h real-time
[x] 1.3.4  Redis kesh — joriy narx (TTL: 10 soniya)
[x] 1.3.5  Redis kesh — OHLCV (ltrim 500 ta)
[x] 1.3.6  WebSocket reconnect logika (max 5 urinish, exponential backoff)
[x] 1.3.7  GET /api/v1/market/price/{symbol} — joriy narx
[x] 1.3.8  GET /api/v1/market/klines/{symbol} — OHLCV (limit, interval)
[x] 1.3.9  GET /api/v1/market/symbols — qo'llab-quvvatlanadigan coinlar ro'yxati
[x] 1.3.10 WebSocket endpoint — /ws/market/{symbol} (frontend uchun)
[x] 1.3.11 Birja ulanmasa — REST endpoint mavjud (WS qayta ulanadi)
```

---

### 1.4 Dashboard va Chart — Frontend
```
[x] 1.4.1  Dashboard layout (sidebar + main content area)
[x] 1.4.2  Sidebar komponenti (navigatsiya, logo, user info, logout)
[x] 1.4.3  Dashboard sahifasi (coin narx kartalar)
[x] 1.4.4  TradingView Lightweight Charts o'rnatish + sozlash
[x] 1.4.5  ChartWidget komponenti (dark theme, TZ 17.1 ranglar)
[x] 1.4.6  Candlestick chart — OHLCV ma'lumotlari bilan
[x] 1.4.7  Real-time narx yangilanishi (WebSocket → chart)
[x] 1.4.8  Timeframe tanlash (1m, 5m, 15m, 1h, 4h, 1D)
[x] 1.4.9  Coin tanlash (BTC, ETH, BNB, SOL, XRP)
[x] 1.4.10 PriceWidget — joriy narx dashboard va chart toolbarda
[x] 1.4.11 Portfolio widget (statik stub — Faza 4)
[x] 1.4.12 WebSocket hook — usePriceStream(symbol)
[x] 1.4.13 Responsive layout (grid, sidebar + main)
```

---

### 1.5 Trading Zones va Manual Signal
```
[x] 1.5.1  trading_zones jadvali migration
[x] 1.5.2  signals jadvali migration
[x] 1.5.3  POST /api/v1/zones — zona yaratish
[x] 1.5.4  GET  /api/v1/zones — foydalanuvchi zonalari (filter: symbol, active_only)
[x] 1.5.5  PUT  /api/v1/zones/{id} — zonani tahrirlash
[x] 1.5.6  DELETE /api/v1/zones/{id} — zonani o'chirish
[x] 1.5.7  Zona trigger logika (narx zona ichiga kirdi → Redis queue → signal yaratish)
[x] 1.5.8  POST /api/v1/signals — manual signal yaratish
[x] 1.5.9  GET  /api/v1/signals — signal tarixi (pagination, filter)
[x] 1.5.10 ZoneEditor komponenti (UI orqali zona yaratish/o'chirish)
[x] 1.5.11 ZoneLayer — chart da zonalarni price lines orqali ko'rsatish
[x] 1.5.12 SignalCard komponenti (coin, yo'nalish, narx, status)
[x] 1.5.13 SignalFeed — oxirgi signallar (real-time WebSocket)
[x] 1.5.14 Signal WebSocket — yangi signal kelganda frontend ga push
```

---

### 1.6 Infratuzilma Yakunlash
```
[x] 1.6.1  Vitest sozlash (frontend unit test)
[x] 1.6.2  Pytest sozlash (backend unit test — tests/test_auth.py)
[ ] 1.6.3  Playwright sozlash (E2E test) — Faza 2 oldidan
[ ] 1.6.4  GitHub Actions CI pipeline skeleton — Faza 2 oldidan
[x] 1.6.5  SCHEMA_SNAPSHOT.md to'ldirildi (Faza 1 DB holati)
[x] 1.6.6  STATUS.md to'ldirildi (har modul holati)
[x] 1.6.7  README.md (local setup qo'llanma)
[x] 1.6.8  docker-compose.yml final tekshiruv ✓
[x] 1.6.9  Health check endpoint (GET /health — backend)
[x] 1.6.10 CORS sozlash (frontend → backend)
```

---

## FAZA 2 — AI INTEGRATION (5-6 hafta) — KEYINGI
```
[ ] 2.0  ANTHROPIC_API_KEY ni backend/.env ga qo'shish (BIRINCHI QADAM)
[ ] 2.1  Claude API ulanishi — tayyor (claude_client.py, signal_analyzer.py mavjud)
[ ] 2.2  Multi-prompt tahlil tizimi — TAYYOR (signal_analyzer.py)
[ ] 2.3  Reflection loop — TAYYOR (signal_analyzer.py)
[ ] 2.4  Signal scoring engine — TAYYOR (signal_analyzer.py)
[ ] 2.5  Prompt caching — TAYYOR (signal_analyzer.py)
[ ] 2.6  AI signal feed UI (dashboard da AI tahlil natijasi)
[ ] 2.7  Claude reasoning ko'rsatish UI
[ ] 2.8  Push bildirishnoma (Firebase FCM)
```

## FAZA 3 — EXECUTION ENGINE (5-6 hafta)
```
[ ] 3.1  Smart order routing (Binance vs Bybit)
[ ] 3.2  Pre-trade impact analysis
[ ] 3.3  TWAP algoritmi
[ ] 3.4  Iceberg order
[ ] 3.5  Slippage monitoring
[ ] 3.6  Execution Analytics DB (TimescaleDB)
[ ] 3.7  Execution Monitor UI ekrani
[ ] 3.8  Kafka microservices ajratish
```

## FAZA 4 — RISK & AUTO TRADE (4-5 hafta)
```
[ ] 4.1  Risk Engine (pozitsiya + portfolio darajasi)
[ ] 4.2  Volatility-adjusted position sizing
[ ] 4.3  Dynamic SL/TP (Claude boshqaradi)
[ ] 4.4  Circuit Breaker tizimi
[ ] 4.5  Trade Executor (avtomatik order yuborish)
[ ] 4.6  Portfolio Heat real-time
```

## FAZA 5 — ANALYSIS DEEP (6-8 hafta)
```
[ ] 5.1  Backtesting moduli (ClickHouse + deterministik engine)
[ ] 5.2  Walk-forward analysis
[ ] 5.3  Paper trading
[ ] 5.4  On-chain tahlil (Exchange inflow/outflow, Whale Alert)
[ ] 5.5  Derivatives ko'rsatkichlari (Funding rate, OI, L/S ratio, GEX)
[ ] 5.6  Multi-timeframe confluence
```

## FAZA 6 — STRATEGY BUILDER (4-5 hafta)
```
[ ] 6.1  Visual drag-drop builder
[ ] 6.2  Strategiya template kutubxona
[ ] 6.3  AI-Assisted Builder (Claude bilan suhbat)
[ ] 6.4  Strategiya health check (overfitting, bias)
```

## FAZA 7 — MOBILE (4-5 hafta)
```
[ ] 7.1  React Native scaffolding
[ ] 7.2  Biometrik auth (Face ID / Touch ID)
[ ] 7.3  Mobile chart va signal feed
[ ] 7.4  App Store + Play Store
```

## FAZA 8 — LEARNING & PRO (3-4 hafta)
```
[ ] 8.1  Trader DNA profili tizimi (26-bo'lim TZ)
[ ] 8.2  Personalized Edge Tracker (27-bo'lim)
[ ] 8.3  Session-aware trading (28-bo'lim)
[ ] 8.4  Kelly Criterion + Bankroll management (33-bo'lim)
[ ] 8.5  Gamification + Streak tizimi (34-bo'lim)
[ ] 8.6  "Bugun savdo qilma" tizimi (35-bo'lim)
[ ] 8.7  Telegram Bot integratsiyasi
[ ] 8.8  Obuna tizimi (Free / Pro $29 / Enterprise)
[ ] 8.9  Adaptive learning + A/B test
```

## FAZA 9 — POLISH & SCALE (2-3 hafta)
```
[ ] 9.1  Lighthouse > 90 (performance audit)
[ ] 9.2  Penetration test (OWASP)
[ ] 9.3  Load testing (k6)
[ ] 9.4  Disaster Recovery test
[ ] 9.5  Multi-region AWS deploy
[ ] 9.6  Canary release pipeline
```
