from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging

from app.api.v1.api import api_router
from app.api.websocket.connections import websocket_router
from app.database.connection import neo4j_db
from app.core.middleware import RequestLoggingMiddleware
from app.config import settings
from app.utils.logger import setup_logging

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan контекст для управления жизненным циклом приложения
    """
    # Startup
    logger.info("🚀 Starting Rabbit Hole Wiki Backend")
    
    try:
        # Подключаемся к базе данных
        await neo4j_db.connect()
        logger.info("✅ Connected to Neo4j database")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Neo4j: {e}")
        raise
    
    yield
    
    # Shutdown
    await neo4j_db.close()
    logger.info("👋 Shutting down Rabbit Hole Wiki Backend")

def create_application() -> FastAPI:
    """
    Фабрика для создания приложения FastAPI
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Interactive knowledge graph wiki with gamification",
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Кастомное middleware для логирования
    app.add_middleware(RequestLoggingMiddleware)
    
    # Подключаем статические файлы
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Подключаем роутеры
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(websocket_router, prefix="/ws")
    
    return app

# Создаем приложение
app = create_application()

@app.get("/")
async def root():
    """
    Корневой endpoint для проверки работы API
    """
    return {
        "message": "Welcome to Rabbit Hole Wiki API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "openapi": "/openapi.json",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint для мониторинга
    """
    from app.database.connection import neo4j_db
    
    try:
        # Проверяем подключение к базе данных
        await neo4j_db.verify_connectivity()
        
        return {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "database": "connected",
            "services": {
                "neo4j": "up",
                "api": "up"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "database": "disconnected"
        }