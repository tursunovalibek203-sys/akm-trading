# Trading AI Platform

Crypto bozori uchun AI-signal va avtomatik savdo tizimi.

## Stack

| Qatlam | Texnologiya |
|--------|-------------|
| Frontend | Next.js 15 App Router + TypeScript 5 |
| Backend | Python FastAPI 0.115+ |
| DB | PostgreSQL 15 + TimescaleDB |
| Cache | Redis 7 |
| AI | Claude API (Haiku + Sonnet + Opus) |
| Auth | Custom JWT RS256 + TOTP 2FA |
| Charts | TradingView Lightweight Charts |

## Tezkor ishga tushirish

### 1. Talablar

- Docker Desktop
- Node.js 20+
- Python 3.12+

### 2. Docker (PostgreSQL + Redis)

```bash
cd docker
docker-compose up -d
```

### 3. Backend

```bash
cd backend

# Virtual muhit
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

# Kutubxonalar
pip install -r requirements.txt

# DB migration
alembic upgrade head

# Serverni ishga tushirish
uvicorn app.main:app --reload --port 8000
```

`http://localhost:8000/docs` — Swagger UI (DEBUG=true bo'lsa)

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

`http://localhost:3000` — Dastur

## Muhit o'zgaruvchilari

### Backend (`backend/.env`)

```env
DATABASE_URL=postgresql://trading_user:trading_pass@localhost:5432/trading_db
REDIS_URL=redis://localhost:6379

# JWT RS256 kalitlar yaratish:
# openssl genrsa -out private.pem 2048
# openssl rsa -in private.pem -pubout -out public.pem
JWT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"

# 32 bayt hex kalit: python -c "import secrets; print(secrets.token_hex(32))"
ENCRYPTION_KEY=your_hex_key_here

ANTHROPIC_API_KEY=sk-ant-...      # Faza 2 dan kerak
```

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/api/v1
```

## Loyiha tuzilmasi

```
trading-ai-platform/
  frontend/          ← Next.js ilovasi
  backend/           ← FastAPI ilovasi
  docker/            ← Docker Compose
  .claude/           ← MiyaAI memory fayllar
```

## Faza rejasi

| Faza | Nomi | Holat |
|------|------|-------|
| 1 | Foundation MVP | 🔄 Jarayonda |
| 2 | AI Integration | ⏳ Keyingi |
| 3 | Execution Engine | ⏳ |
| 4 | Risk & Auto Trade | ⏳ |
| 5 | Analysis Deep | ⏳ |

## API endpointlar

| Method | URL | Tavsif |
|--------|-----|--------|
| POST | `/api/v1/auth/register` | Ro'yxatdan o'tish |
| POST | `/api/v1/auth/login` | Kirish |
| POST | `/api/v1/auth/refresh` | Token yangilash |
| POST | `/api/v1/auth/logout` | Chiqish |
| GET | `/api/v1/auth/me` | Joriy foydalanuvchi |
| POST | `/api/v1/auth/2fa/setup` | 2FA sozlash |
| POST | `/api/v1/auth/2fa/verify` | 2FA tasdiqlash |
| POST | `/api/v1/auth/2fa/disable` | 2FA o'chirish |
| GET | `/api/v1/market/price/{symbol}` | Joriy narx |
| GET | `/api/v1/market/klines/{symbol}` | OHLCV |
| GET | `/api/v1/market/symbols` | Coinlar ro'yxati |
| WS | `/api/v1/market/ws/{symbol}` | Real-time narx |
| GET | `/api/v1/zones` | Zonalar |
| POST | `/api/v1/zones` | Zona yaratish |
| PUT | `/api/v1/zones/{id}` | Zonani yangilash |
| DELETE | `/api/v1/zones/{id}` | Zonani o'chirish |
| GET | `/api/v1/signals` | Signallar |
| POST | `/api/v1/signals` | Signal yaratish |
| PATCH | `/api/v1/signals/{id}/status` | Status yangilash |
| WS | `/api/v1/signals/ws` | Real-time signallar |
| GET | `/health` | Health check |

## Xavfsizlik

- JWT token — HttpOnly Secure cookie (localStorage YO'Q)
- API kalitlar — AES-256-GCM shifrlangan
- Withdrawal ruxsati — birja API kalitiga HECH QACHON berilmaydi
- Rate limiting — `register`: 5/min, `login`: 10/min
- Input validation — barcha endpointda Pydantic/Zod
