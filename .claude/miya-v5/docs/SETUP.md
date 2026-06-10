# SETUP.md — Infratuzilma Sozlash Qo'llanmasi
## MiyaAI tizimi bilan ishlashdan oldin loyihada bir marta sozlanadi

---

## 1. PAPKA TUZILMASI

Loyiha ildizida quyidagi tuzilma bo'lishi kerak:

```
your-project/
├── .claude/
│   ├── settings.json     ← ruxsatlar
│   └── hooks/            ← avtomatik tekshiruvlar
├── .miya/
│   └── results/          ← agent natijalari
├── [loyiha fayllari]
└── [MiyaAI template fayllar]
```

Yaratish:
```bash
mkdir -p .claude/hooks
mkdir -p .miya/results
```

---

## 2. PERMISSION SYSTEM (.claude/settings.json)

Claude Code da har tool uchun ruxsat sozlanadi.
Bu fayl bo'lmasa — Claude hamma narsaga ruxsat so'raydi (sekin va xavfli).

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Write(src/**)",
      "Write(supabase/migrations/**)",
      "Write(.miya/results/**)",
      "Bash(npx tsc --noEmit)",
      "Bash(npx eslint src/**)",
      "Bash(npm run test)",
      "Bash(npm run build)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(mkdir *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push *)",
      "Bash(git reset --hard *)",
      "Bash(DROP TABLE *)",
      "Bash(supabase db push *)",
      "Write(.env*)"
    ]
  }
}
```

**Nima uchun deny ro'yxati muhim:**
- `rm -rf` — tasodifiy fayl o'chirish yo'q
- `git push` — siz tekshirmasdan hech narsa remote ga ketmaydi
- `git reset --hard` — ish yo'qolmaydi
- `supabase db push` — migration siz tasdiqlaymasdan apply bo'lmaydi
- `.env` — secret keylar o'zgartirilmaydi

---

## 3. HOOKS (.claude/hooks/)

Hooks — Claude biror amal bajarishidan oldin yoki keyin avtomatik ishlaydigan skriptlar.
Bu checksum pattern ni qo'lda emas, avtomatik bajaradi.

### TypeScript tekshiruv (PostToolUse)

`.claude/hooks/post-write-ts.sh`:
```bash
#!/bin/bash
# TypeScript fayl yozilgandan keyin avtomatik type check

FILE=$1
if [[ "$FILE" == *.ts || "$FILE" == *.tsx ]]; then
  echo "TypeScript tekshirilmoqda..."
  npx tsc --noEmit
  if [ $? -ne 0 ]; then
    echo "❌ TypeScript xato — Claude tuzatsin"
    exit 1
  fi
  echo "✅ TypeScript OK"
fi
```

### Migration validatsiya (PostToolUse)

`.claude/hooks/post-write-migration.sh`:
```bash
#!/bin/bash
# Migration fayl yozilgandan keyin validatsiya

FILE=$1
if [[ "$FILE" == *migrations* && "$FILE" == *.sql ]]; then
  echo "Migration tekshirilmoqda..."
  
  # UP va DOWN mavjudligini tekshirish
  if ! grep -q "-- UP" "$FILE"; then
    echo "❌ Migration da UP yo'q"
    exit 1
  fi
  if ! grep -q "-- DOWN" "$FILE"; then
    echo "❌ Migration da DOWN yo'q"
    exit 1
  fi
  echo "✅ Migration format OK"
fi
```

### Git snapshot (PreToolUse)

`.claude/hooks/pre-write.sh`:
```bash
#!/bin/bash
# Har yozishdan oldin git snapshot

git add -A
git stash
echo "✅ Snapshot saqlandi — xato bo'lsa: git stash pop"
```

### Hooks sozlash (settings.json ga qo'shish):

```json
{
  "permissions": { ... },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/post-write-ts.sh $TOOL_INPUT_PATH"
          },
          {
            "type": "command", 
            "command": ".claude/hooks/post-write-migration.sh $TOOL_INPUT_PATH"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/pre-write.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 4. MCP SERVERLAR

MCP (Model Context Protocol) — Claude ga tashqi ma'lumot ulash.
Claude Code → Settings → Integrations → MCP Servers dan sozlanadi.

### Supabase MCP (eng muhim)

**Nima beradi:** Claude to'g'ridan Supabase DB ga ulanadi.
- SCHEMA_SNAPSHOT.md o'qilmaydi — to'g'ridan DB sxemasi ko'riladi
- Migration apply holatini Claude o'zi biladi
- RLS policies to'g'ridan tekshiriladi

**Sozlash:**
```bash
# Claude Code integrations panelidan:
# MCP Server → Add → Supabase
# Connection string: postgresql://[user]:[password]@[host]/[db]
```

**MiyaAI bilan ishlash:**
Supabase MCP ulangan bo'lsa — SCHEMA_SNAPSHOT.md avtomatik o'tkazib yuboriladi.
Claude sessiya boshida `use_mcp_schema: true` ko'rsa — fayldan emas, MCPdan o'qiydi.

### GitHub MCP (ixtiyoriy)

**Nima beradi:** PR, issue, commit to'g'ridan Claude dan boshqarish.

```bash
# Claude Code → Settings → Integrations → GitHub
# Token: github.com/settings/tokens → repo ruxsat
```

### Playwright MCP (katta loyihalar uchun)

**Nima beradi:** Claude o'zi browser ochib E2E test bajaradi.

```bash
npx @playwright/mcp@latest
# Claude Code → Settings → Integrations → Playwright
```

---

## 5. SESSIYA BOSHQARUV

### --continue va --resume

```bash
# Oxirgi sessiyani davom ettirish (sessiya uzilsa)
claude --continue

# Ma'lum sessiyani qayta ochish
claude --resume [SESSION_ID]

# Sessiya ID ni qayerdan topish:
# Claude Code → History → [sessiya] → Copy ID
```

**Qachon ishlatiladi:**
- Internet uzildi, sessiya to'xtadi → `--continue`
- Kecha boshladingiz, bugun davom etmoqchisiz → `--resume`
- INCOMPLETE_WORK.md da falon sessiya ID yozilgan → `--resume [ID]`

**INCOMPLETE_WORK.md ga yozish tavsiyasi:**
```
Sessiya 1 (2025-05-20): Backend API ✅
Session ID: sess_abc123
Keyingi sessiya: claude --resume sess_abc123
```

### --print (CI/CD uchun)

```bash
# Interaktif emas — stdout ga chiqadi
claude --print "security audit" < src/services/payment.ts

# GitHub Actions da:
- name: Security Review
  run: |
    claude --print "RLS va auth tekshir, muammo topsang CRITICAL deb belgilab chiqar" \
      < src/services/payment.ts > security-report.txt
    cat security-report.txt
```

---

## 6. BIRINCHI MARTA SOZLASH TARTIBI

```bash
# 1. Papkalar
mkdir -p .claude/hooks .miya/results

# 2. Hooks fayllar
cat > .claude/hooks/post-write-ts.sh << 'EOF'
#!/bin/bash
FILE=$1
if [[ "$FILE" == *.ts || "$FILE" == *.tsx ]]; then
  npx tsc --noEmit || exit 1
fi
EOF
chmod +x .claude/hooks/post-write-ts.sh

cat > .claude/hooks/post-write-migration.sh << 'EOF'
#!/bin/bash
FILE=$1
if [[ "$FILE" == *migrations* ]]; then
  grep -q "-- DOWN" "$FILE" || exit 1
fi
EOF
chmod +x .claude/hooks/post-write-migration.sh

# 3. settings.json
# Yuqoridagi JSON ni .claude/settings.json ga ko'chiring

# 4. MCP
# Claude Code → Settings → Integrations → Supabase ulang

# 5. Tekshirish
claude --version
claude "CLAUDE.md o'qi va loyiha holatini ayt"
```

---

## 7. MUAMMOLAR VA YECHIMLAR

```
Hooks ishlamayapti:
→ chmod +x .claude/hooks/*.sh

Permission xato:
→ settings.json syntax tekshiring (jsonlint.com)

MCP ulanmayapti:
→ Connection string to'g'riligini tekshiring
→ Supabase → Settings → Database → Connection string

--continue ishlamayapti:
→ Claude Code yangi versiyasiga yangilang
```
