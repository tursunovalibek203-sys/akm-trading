# SCHEMA_SNAPSHOT.md — Database Holati
# MiyaAI har migration qo'shilganda YANGILAYDI
# FAQAT APPEND — eski versiya o'chirilmaydi, [ARXIV] belgilanadi

---

## FORMAT

```
## [jadval_nomi]
Yaratildi: [sana]
FIELDS:
  [field_nomi] [tip] [not null?] [default?] [izoh]
INDEXES:
  [index_nomi] → [field]
RLS:
  SELECT: [qoida]
  INSERT: [qoida]
  UPDATE: [qoida]
  DELETE: [qoida]
BOG'LIQLIK:
  → [boshqa jadval] ([field])
```

---

## MISOL (to'ldirilgan)

```
## users
Yaratildi: 2025-05-01
FIELDS:
  id          uuid         NOT NULL   DEFAULT gen_random_uuid()
  email       text         NOT NULL
  full_name   text
  role        text         NOT NULL   DEFAULT 'user'  -- admin | user
  created_at  timestamptz  NOT NULL   DEFAULT now()
INDEXES:
  users_email_idx → email (unique)
RLS:
  SELECT: auth.uid() = id
  INSERT: false (Supabase Auth boshqaradi)
  UPDATE: auth.uid() = id
  DELETE: false

## tasks
Yaratildi: 2025-05-05
FIELDS:
  id          uuid         NOT NULL   DEFAULT gen_random_uuid()
  user_id     uuid         NOT NULL
  title       text         NOT NULL
  status      text         NOT NULL   DEFAULT 'todo'  -- todo | doing | done
  priority    text                    DEFAULT 'medium' -- qo'shildi: 2025-05-10
  created_at  timestamptz  NOT NULL   DEFAULT now()
INDEXES:
  tasks_user_id_idx → user_id
  tasks_status_idx  → status
RLS:
  SELECT: auth.uid() = user_id
  INSERT: auth.uid() = user_id
  UPDATE: auth.uid() = user_id
  DELETE: auth.uid() = user_id
BOG'LIQLIK:
  → users (user_id)
```

---

## OXIRGI YANGILANISH: [sana]
## MIGRATION SONI: [N] ta
