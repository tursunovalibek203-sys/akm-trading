# MODUL: BackendBuilderAI — DevOps & Infra
## Yuklanadi: faqat deploy yoki infra sessiyasida
## Asosiy fayl: 04_BackendBuilderAI.md

---

### H — DEVOPS VA INFRATUZILMA

**31. Dockerfile**
```dockerfile
# Multi-stage build — kichik image
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**32. Docker Compose**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports: ["3000:3000"]
    env_file: .env
    depends_on: [db, redis]
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

**33. Nginx Konfiguratsiya**
```nginx
# /etc/nginx/sites-available/myapp.conf
# YANGI FAYL — mavjud konfig larga TEGMAYDI

server {
    listen 80;
    server_name myapp.uz www.myapp.uz;

    # HTTPS ga redirect
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name myapp.uz www.myapp.uz;

    ssl_certificate /etc/letsencrypt/live/myapp.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.uz/privkey.pem;

    # Gzip compression
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;

    # Static files (frontend)
    location / {
        root /var/www/myapp/dist;
        try_files $uri /index.html;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_bypass $http_upgrade;
    }

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header Strict-Transport-Security "max-age=31536000";
}
```

**34. PM2 Konfiguratsiya**
```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'myapp',
    script: 'dist/index.js',
    instances: 'max',        // CPU core soni
    exec_mode: 'cluster',    // Load balancing
    env: { NODE_ENV: 'development' },
    env_production: { NODE_ENV: 'production' },
    max_memory_restart: '500M',
    error_file: 'logs/error.log',
    out_file: 'logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    watch: false,            // Production da off
    autorestart: true
  }]
}

// Buyruqlar:
// pm2 start ecosystem.config.js --env production
// pm2 save
// pm2 startup
// pm2 monit
```

**35. GitHub Actions CI/CD**
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run type-check
      - run: npm test
      - run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.10
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/myapp
            git pull origin main
            npm ci --only=production
            npm run build
            pm2 restart myapp
            nginx -t && systemctl reload nginx
```

**36. SSL Setup**
```bash
# Let's Encrypt — bepul, 90 kunda avtomatik yangilanadi
apt install certbot python3-certbot-nginx -y
certbot --nginx -d myapp.uz -d www.myapp.uz

# Avtomatik yangilash tekshirish:
certbot renew --dry-run

# Crontab (avtomatik):
0 12 * * * /usr/bin/certbot renew --quiet
```

**37. Zero-Downtime Deploy**
```bash
# Blue-Green deployment pattern:

# 1. Yangi versiya parallel ishga tushiriladi (port 3001)
pm2 start ecosystem.config.js --name myapp-new -p 3001

# 2. Health check — yangi versiya ishlayaptimi?
curl http://localhost:3001/health

# 3. Nginx yangi versiyaga yo'naltiradi
# proxy_pass http://localhost:3001;
nginx -s reload

# 4. Eski versiya to'xtatiladi
pm2 delete myapp-old

# Rollback: nginx ni eski portga qaytarish = 30 soniya
```

---

### I — ZERO-DOWNTIME MIGRATION

**38. Additive Migration Pattern**
```
XAVFSIZ migration (zero-downtime):
✓ Ustun QO'SHISH (nullable)
✓ Yangi jadval yaratish
✓ Index qo'shish (CONCURRENTLY)
✓ Default qiymat o'zgartirish

XAVFLI migration (downtime kerak):
✗ Ustun O'CHIRISH (avval kod, keyin migration)
✗ Ustun RENAME (avval yangi ustun, keyin eski)
✗ Type O'ZGARTIRISH
✗ NOT NULL qo'shish (mavjud null qatorlar bor bo'lsa)

TARTIB:
1. Nullable yangi ustun qo'shiladi
2. Kod yangi ustunni ishlatadi (eski ham)
3. Ma'lumot ko'chiriladi (background)
4. Eski ustun o'chiriladi (keyingi deploy)
```

**39. Data Migration Pattern**
```sql
-- Katta jadval migration — batch da (server qotmasin)
DO $$
DECLARE
  batch_size INT := 1000;
  offset_val INT := 0;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE tasks
    SET new_column = old_column
    WHERE id IN (
      SELECT id FROM tasks
      WHERE new_column IS NULL
      LIMIT batch_size
    );

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;

    PERFORM pg_sleep(0.1); -- Server ga nafas berish
  END LOOP;
END $$;
```

**40. Migration Rollback Test**
```bash
# Har migration uchun — staging da test:
# 1. UP migration bajariladi
npx supabase db push

# 2. Ilova tekshiriladi (ishlayaptimi?)
curl http://staging.myapp.uz/health

# 3. DOWN migration bajariladi (rollback)
# Supabase da: migration fayl DOWN qismini bajarish

# 4. Ilova yana tekshiriladi
# Eski holat qaytganmi?

# Faqat shu test o'tgandan keyin production ga!
```

---

