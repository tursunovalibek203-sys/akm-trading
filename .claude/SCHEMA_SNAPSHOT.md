# SCHEMA_SNAPSHOT.md — Trading AI Platform
# [APPEND] — migration qo'shilganda yangilanadi
# Oxirgi yangilanish: 2026-06-03 | Migration: 001_initial_schema

---

## Jadvallar

### users
| Ustun | Tip | Cheklov |
|-------|-----|---------|
| id | UUID | PK, DEFAULT uuid_generate_v4() |
| email | VARCHAR(255) | UNIQUE NOT NULL, INDEX |
| password_hash | VARCHAR(255) | NOT NULL |
| role | ENUM(guest,free,pro,admin) | NOT NULL, DEFAULT 'free' |
| is_active | BOOLEAN | NOT NULL, DEFAULT true |
| is_2fa_enabled | BOOLEAN | NOT NULL, DEFAULT false |
| totp_secret | VARCHAR(64) | NULLABLE |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() |

### user_sessions
| Ustun | Tip | Cheklov |
|-------|-----|---------|
| id | UUID | PK |
| user_id | UUID | FK → users.id CASCADE, INDEX |
| token_jti | VARCHAR(36) | UNIQUE NOT NULL, INDEX |
| device_info | VARCHAR(255) | NULLABLE |
| is_active | BOOLEAN | NOT NULL, DEFAULT true |
| expires_at | TIMESTAMPTZ | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() |

### trading_zones
| Ustun | Tip | Cheklov |
|-------|-----|---------|
| id | UUID | PK |
| user_id | UUID | FK → users.id CASCADE, INDEX |
| symbol | VARCHAR(20) | NOT NULL, INDEX |
| zone_type | ENUM(support,resistance,demand,supply) | NOT NULL |
| price_from | NUMERIC(20,8) | NOT NULL |
| price_to | NUMERIC(20,8) | NOT NULL |
| label | VARCHAR(100) | NULLABLE |
| is_active | BOOLEAN | NOT NULL, DEFAULT true |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() |

### signals
| Ustun | Tip | Cheklov |
|-------|-----|---------|
| id | UUID | PK |
| user_id | UUID | FK → users.id CASCADE, INDEX |
| zone_id | UUID | FK → trading_zones.id SET NULL, NULLABLE |
| symbol | VARCHAR(20) | NOT NULL, INDEX |
| direction | ENUM(long,short) | NOT NULL |
| score | INTEGER | NULLABLE |
| entry_price | NUMERIC(20,8) | NOT NULL |
| stop_loss | NUMERIC(20,8) | NULLABLE |
| take_profit_1 | NUMERIC(20,8) | NULLABLE |
| take_profit_2 | NUMERIC(20,8) | NULLABLE |
| status | ENUM(pending,active,tp1_hit,tp2_hit,sl_hit,cancelled,expired) | NOT NULL, DEFAULT 'pending' |
| reasoning | TEXT | NULLABLE |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now(), INDEX |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() |

---

## Enum turlari
- `userrole`: guest, free, pro, admin
- `zonetype`: support, resistance, demand, supply
- `signaldirection`: long, short
- `signalstatus`: pending, active, tp1_hit, tp2_hit, sl_hit, cancelled, expired

## Migration tarixi
| ID | Fayl | Sana | Tavsif |
|----|------|------|--------|
| 001 | 001_initial_schema.py | 2026-06-03 | users, user_sessions, trading_zones, signals |
