# AI SaaS Backend

Backend-проект для AI SaaS продукта на Python.

Я делаю этот проект как учебно-портфолио backend-разработку: здесь нет фронтенда, лендинга или визуальной части. Основной фокус - API, база данных, авторизация, работа с AI-сервисом, лимиты использования и структура, похожая на реальный SaaS backend.

Проект был разработан с помощью ИИ, но под моим контролем: я задавал направление, проверял смысл решений, разбирал архитектуру и постепенно собирал backend как учебный и практический проект.

## Что Уже Есть

- FastAPI backend.
- Регистрация и логин пользователя.
- JWT-авторизация.
- Tenant-модель: пользователь принадлежит организации.
- AI endpoint для генерации ответа.
- Mock AI provider для локальной разработки без API-ключа.
- OpenAI provider для будущей реальной интеграции.
- Лимиты AI-кредитов на tenant.
- История AI-запросов в базе данных.
- SQLAlchemy models.
- Alembic migrations.
- Dockerfile и Docker Compose.
- API-тесты через pytest и httpx.

## Зачем Этот Проект

Я хочу прокачать backend-навыки на проекте, который ближе к реальной работе, чем обычный ToDo list.

В этом проекте я тренирую:

- проектирование REST API;
- работу с FastAPI;
- авторизацию через JWT;
- SQLAlchemy и связи между таблицами;
- миграции базы данных через Alembic;
- разделение кода на routes, schemas, services, models;
- тестирование backend-flow;
- базовую AI-интеграцию;
- Docker-запуск проекта.

## Как Работает Backend Flow

1. Пользователь регистрируется с названием организации, email и паролем.
2. Backend создаёт tenant и owner-пользователя.
3. Пользователь логинится и получает JWT access token.
4. Защищённые endpoints читают текущего пользователя из токена.
5. AI-запрос списывает кредиты у tenant.
6. Prompt, ответ AI, модель, provider и кредиты сохраняются в историю.

## Структура Проекта

```text
backend/
  app/
    api/
      routes/          HTTP endpoints
      dependencies.py  общие зависимости FastAPI
    core/              настройки и безопасность
    models/            SQLAlchemy модели
    schemas/           Pydantic схемы запросов и ответов
    services/          бизнес-логика и AI-логика
    db.py              подключение к базе данных
    main.py            точка входа FastAPI
  migrations/          Alembic migrations
  tests/               тесты backend-а
```

## Основные Endpoints

- `GET /api/v1/health` - проверка, что сервер работает.
- `POST /api/v1/auth/register` - регистрация tenant и owner-пользователя.
- `POST /api/v1/auth/login` - логин и получение JWT.
- `GET /api/v1/auth/me` - данные текущего пользователя.
- `POST /api/v1/ai/complete` - AI-запрос с сохранением истории.
- `GET /api/v1/ai/requests` - история AI-запросов tenant-а.

## Локальный Запуск

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn backend.app.main:app --reload
```

После запуска документация API будет здесь:

```text
http://127.0.0.1:8000/docs
```

По умолчанию проект может работать через SQLite. Это удобно для локального старта и обучения.

## Запуск Через Docker

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Docker поднимает:

- `api` - FastAPI backend на `http://127.0.0.1:8000`;
- `db` - PostgreSQL на порту `5432`.

В Docker-режиме схема базы применяется через Alembic:

```powershell
docker compose exec api alembic upgrade head
```

## Миграции Базы Данных

Миграции лежат в `backend/migrations`.

Полезные команды:

```powershell
alembic upgrade head
alembic revision --autogenerate -m "add table name"
alembic downgrade -1
```

Смысл миграций простой: модели описывают таблицы в Python, а миграции описывают, как изменить реальную базу данных. В production-разработке это обязательная часть backend-а.

## Тесты

Запуск тестов:

```powershell
pytest
```

Сейчас тесты проверяют:

- работу AI service;
- JWT token roundtrip;
- регистрацию owner-пользователя;
- сохранение AI request;
- полный API-flow: register -> login -> me -> AI complete -> AI history.

## AI Provider

Для локальной разработки используется mock provider:

```env
AI_PROVIDER=mock
```

Чтобы подключить OpenAI:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_api_key
AI_MODEL=gpt-4.1-mini
```

## Статус Проекта

Проект ещё не является production-ready SaaS, но уже имеет крепкую backend-основу.

