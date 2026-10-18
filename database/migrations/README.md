# Database Migrations

The application creates tables with SQLAlchemy `create_all()` on startup.

`create_all()` creates **missing tables** but does not **add columns** to existing tables. Schema changes to existing tables are applied with the SQL scripts in this folder.

---

## Migrations

| Migration | Issue | Description |
|-----------|-------|-------------|
| `001_add_interaction_fields.sql` | #72 | Add `attendees`, `samples_distributed`, `outcomes`, `follow_up_actions` to `interactions` |

---

## Running a Migration

### psql

```bash
psql -U postgres -d ai_first_crm_hcp -f database/migrations/001_add_interaction_fields.sql
```

### pgAdmin

1. Open **Query Tool** on the `ai_first_crm_hcp` database
2. Paste the script
3. Execute

---

## Rules

- Migrations are additive and safe to run more than once (`IF NOT EXISTS`)
- New installations do not need to run migrations; `create_all()` creates the full schema
- Run migrations in order

---

## Future

Alembic can replace manual scripts if schema changes become frequent.
