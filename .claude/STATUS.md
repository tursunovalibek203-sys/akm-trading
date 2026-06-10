# STATUS.md — Trading AI Platform
# [YANGILANADI] — har modul o'zgarganda
# Oxirgi yangilanish: 2026-06-03

---

## FAZA 1 — Foundation MVP

### Backend modullar
| Modul | Holat | Izoh |
|-------|-------|------|
| Auth (register/login/logout) | ✓ Tayyor | RS256 JWT, HttpOnly cookie |
| Auth (refresh token) | ✓ Tayyor | Cookie-based, Redis blacklist |
| Auth (2FA TOTP) | ✓ Tayyor | setup/verify/disable |
| Auth (rate limiting) | ✓ Tayyor | slowapi: 5/10/20 per min |
| Auth dependencies | ✓ Tayyor | Cookie + Bearer ikkalasidan |
| Market data (REST) | ✓ Tayyor | price, klines, symbols |
| Market data (WebSocket) | ✓ Tayyor | real-time price push |
| Binance streams (multi-TF) | ✓ Tayyor | 1m,5m,15m,1h,4h |
| Zone trigger | ✓ Tayyor | narx zona → signal queue |
| Zones CRUD | ✓ Tayyor | create/get/update/delete |
| Signals CRUD | ✓ Tayyor | create/get/patch/delete |
| Signals WebSocket | ✓ Tayyor | real-time signal push |
| DB migration | ✓ Tayyor | 001_initial_schema |
| AI signal analyzer | ✓ Tayyor | Faza 2 uchun tayyor (API key kerak) |

### Frontend sahifalar
| Sahifa | Holat | Izoh |
|--------|-------|------|
| /login | ✓ Tayyor | email+password+2FA |
| /register | ✓ Tayyor | validatsiya bilan |
| /2fa | ✓ Tayyor | setup va verify rejimlari |
| /dashboard | ✓ Tayyor | real-time price cards |
| /chart | ✓ Tayyor | TradingView + zone editor + signal create |
| /signals | ✓ Tayyor | list, filter, create modal |
| /portfolio | ✓ Tayyor | Faza 4 stub |
| /settings | ✓ Tayyor | 2FA on/off, logout |

### Frontend komponentlar
| Komponent | Holat |
|-----------|-------|
| ChartWidget (TradingView) | ✓ Tayyor |
| ZoneEditor | ✓ Tayyor |
| ZoneLayer | ✓ Tayyor |
| SignalCard | ✓ Tayyor |
| SignalFeed (WS) | ✓ Tayyor |
| usePriceStream hook | ✓ Tayyor |

### Infratuzilma
| Element | Holat | Izoh |
|---------|-------|------|
| Docker Compose | ✓ Tayyor | PG15+TimescaleDB+Redis7 |
| Alembic migrations | ✓ Tayyor | 001 applied |
| JWT RS256 keys | ✓ Tayyor | .env da bor |
| .gitignore | ✓ Tayyor | |
| README.md | ✓ Tayyor | |
| SCHEMA_SNAPSHOT.md | ✓ Tayyor | |
| Security headers | ✓ Tayyor | next.config.ts |
| CORS | ✓ Tayyor | backend |
| Sentry (backend) | ✓ Tayyor | DSN optional |

---

## BLOKERLAR
Yo'q ✅

## KEYINGI FAZA
Faza 2 — AI Integration:
- Claude API kalitini .env ga qo'shish
- `/api/v1/ai/analyze` endpoint (tayyor, kalit kerak)
- AI signal feed UI
- Push bildirishnomalar (Firebase FCM)
