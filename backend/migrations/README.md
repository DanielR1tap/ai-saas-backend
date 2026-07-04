# Database Migrations

Alembic tracks database schema changes.

Common commands:

```powershell
alembic upgrade head
alembic revision --autogenerate -m "describe change"
alembic downgrade -1
```

For production-like runs, set `AUTO_CREATE_TABLES=false` and use migrations.
