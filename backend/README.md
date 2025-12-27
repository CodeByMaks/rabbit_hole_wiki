rabbit-hole-backend/
├── .env                    # Переменные окружения (не в git)
├── .env.example           # Пример переменных окружения
├── .gitignore
├── requirements.txt       # Зависимости Python
├── requirements-dev.txt   # Зависимости для разработки
├── pyproject.toml        # Конфигурация проекта (опционально)
├── README.md
├── Dockerfile
├── docker-compose.yml
│
├── app/                   # Основное приложение
│   ├── __init__.py
│   ├── main.py           # Точка входа FastAPI
│   ├── config.py         # Конфигурация приложения
│   │
│   ├── api/              # API endpoints
│   │   ├── __init__.py
│   │   ├── dependencies.py  # Зависимости (auth, etc.)
│   │   │
│   │   ├── v1/           # API версия 1
│   │   │   ├── __init__.py
│   │   │   ├── api.py    # Объединяющий роутер
│   │   │   │
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       ├── articles.py
│   │   │       ├── graph.py
│   │   │       ├── users.py
│   │   │       ├── search.py
│   │   │       ├── game.py
│   │   │       └── admin.py
│   │   │
│   │   └── websocket/    # WebSocket endpoints
│   │       ├── __init__.py
│   │       └── connections.py
│   │
│   ├── core/             # Ядро приложения
│   │   ├── __init__.py
│   │   ├── security.py   # Аутентификация, JWT
│   │   ├── exceptions.py # Кастомные исключения
│   │   └── middleware.py # Middleware
│   │
│   ├── database/         # Работа с БД
│   │   ├── __init__.py
│   │   ├── connection.py # Подключение к Neo4j
│   │   ├── models.py     # Graph модели (узлы, связи)
│   │   ├── queries.py    # Cypher запросы
│   │   └── repositories/ # Репозитории (паттерн Repository)
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── article_repo.py
│   │       ├── user_repo.py
│   │       └── graph_repo.py
│   │
│   ├── schemas/          # Pydantic схемы (DTO)
│   │   ├── __init__.py
│   │   ├── article.py
│   │   ├── user.py
│   │   ├── graph.py
│   │   ├── game.py
│   │   └── response.py   # Общие модели ответов
│   │
│   ├── services/         # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── article_service.py
│   │   ├── graph_service.py
│   │   ├── user_service.py
│   │   ├── game_service.py
│   │   ├── ai_service.py # OpenAI интеграция
│   │   └── cache_service.py # Redis кэширование
│   │
│   ├── utils/            # Вспомогательные функции
│   │   ├── __init__.py
│   │   ├── wiki_parser.py # Парсинг Wikipedia
│   │   ├── helpers.py    # Общие хелперы
│   │   ├── validators.py # Валидаторы
│   │   ├── formatters.py # Форматирование
│   │   └── logger.py     # Настройка логгера
│   │
│   ├── tasks/            # Фоновые задачи (Celery)
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── wiki_tasks.py # Задачи парсинга
│   │   └── ai_tasks.py   # Задачи AI
│   │
│   └── worker.py         # Celery worker
│
├── tests/                # Тесты
│   ├── __init__.py
│   ├── conftest.py      # Фикстуры pytest
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_articles.py
│   │   └── test_graph.py
│   ├── test_services/
│   │   ├── __init__.py
│   │   └── test_article_service.py
│   └── test_utils/
│       ├── __init__.py
│       └── test_wiki_parser.py
│
├── scripts/              # Скрипты для управления
│   ├── init_db.py       # Инициализация БД
│   ├── seed_data.py     # Заполнение тестовыми данными
│   ├── parse_wikipedia.py
│   └── backup_db.py
│
├── migrations/           # Миграции БД (если нужны)
│   ├── __init__.py
│   └── versions/
│
├── docs/                # Документация
│   ├── api.md
│   ├── architecture.md
│   └── deployment.md
│
├── logs/                # Логи приложения
│   ├── app.log
│   └── errors.log
│
└── static/              # Статические файлы
    ├── images/
    └── swagger/         # Кастомная Swagger UI