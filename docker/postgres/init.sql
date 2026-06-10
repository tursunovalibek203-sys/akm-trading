-- TimescaleDB extension yoqish
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Status check
SELECT timescaledb_pre_restore();
SELECT timescaledb_post_restore();
