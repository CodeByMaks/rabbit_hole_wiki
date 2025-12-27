from neo4j import AsyncGraphDatabase, AsyncDriver
from typing import Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class Neo4jDatabase:
    """
    Класс для управления подключением к Neo4j
    """
    _instance: Optional["Neo4jDatabase"] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "_driver"):
            self._driver: Optional[AsyncDriver] = None
    
    async def connect(self):
        """
        Подключение к базе данных Neo4j
        """
        try:
            self._driver = AsyncGraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
                max_connection_lifetime=30 * 60,  # 30 минут
                max_connection_pool_size=50,
                connection_acquisition_timeout=2 * 60,  # 2 минуты
            )
            await self.verify_connectivity()
            logger.info("✅ Successfully connected to Neo4j")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Neo4j: {e}")
            raise
    
    async def verify_connectivity(self):
        """
        Проверка подключения к базе данных
        """
        if not self._driver:
            raise RuntimeError("Driver not initialized")
        
        try:
            await self._driver.verify_connectivity()
            logger.debug("Neo4j connectivity verified")
            return True
        except Exception as e:
            logger.error(f"Neo4j connectivity check failed: {e}")
            return False
    
    async def close(self):
        """
        Закрытие подключения
        """
        if self._driver:
            await self._driver.close()
            self._driver = None
            logger.info("👋 Disconnected from Neo4j")
    
    def get_session(self):
        """
        Получение сессии для работы с базой
        """
        if not self._driver:
            raise RuntimeError("Database not connected")
        return self._driver.session()
    
    @property
    def driver(self) -> AsyncDriver:
        if not self._driver:
            raise RuntimeError("Database not connected")
        return self._driver

# Глобальный экземпляр
neo4j_db = Neo4jDatabase()