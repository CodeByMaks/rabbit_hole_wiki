from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
import logging

from app.schemas.article import (
    Article, ArticleCreate, ArticleUpdate, ArticleWithConnections,
    Connection, ConnectionCreate, PathFindingRequest, PathFindingResponse
)
from app.services.article_service import ArticleService
from app.services.graph_service import GraphService
from app.api.dependencies import get_current_user, rate_limit
from app.core.exceptions import NotFoundException, ValidationException

router = APIRouter(prefix="/articles", tags=["articles"])
logger = logging.getLogger(__name__)

@router.get("/random", response_model=Article)
@rate_limit(limit=10, period=60)  # 10 запросов в минуту
async def get_random_article(
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    difficulty: Optional[str] = Query(None, description="Уровень сложности")
):
    """
    Получить случайную статью
    
    - **category**: Фильтрация по категории (опционально)
    - **difficulty**: Уровень сложности (beginner, intermediate, advanced)
    """
    try:
        article = await ArticleService.get_random_article(
            category=category,
            difficulty=difficulty
        )
        if not article:
            raise NotFoundException("No articles found")
        return article
    except Exception as e:
        logger.error(f"Error getting random article: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/{article_id}", response_model=ArticleWithConnections)
async def get_article(
    article_id: str,
    include_connections: bool = Query(True, description="Включить связи")
):
    """
    Получить статью по ID
    
    - **article_id**: UUID статьи
    - **include_connections**: Включить связанные статьи в ответ
    """
    try:
        article = await ArticleService.get_article(
            article_id=article_id,
            include_connections=include_connections
        )
        if not article:
            raise NotFoundException(f"Article with ID {article_id} not found")
        return article
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting article {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    current_user = Depends(get_current_user)
):
    """
    Создать новую статью (требуется аутентификация)
    """
    try:
        return await ArticleService.create_article(
            article_data=article_data,
            user_id=current_user.id
        )
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating article: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{article_id}", response_model=Article)
async def update_article(
    article_id: str,
    article_data: ArticleUpdate,
    current_user = Depends(get_current_user)
):
    """
    Обновить статью (требуется аутентификация)
    """
    try:
        updated = await ArticleService.update_article(
            article_id=article_id,
            article_data=article_data,
            user_id=current_user.id
        )
        if not updated:
            raise NotFoundException(f"Article with ID {article_id} not found")
        return updated
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating article {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: str,
    current_user = Depends(get_current_user)
):
    """
    Удалить статью (требуется аутентификация)
    """
    try:
        deleted = await ArticleService.delete_article(
            article_id=article_id,
            user_id=current_user.id
        )
        if not deleted:
            raise NotFoundException(f"Article with ID {article_id} not found")
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting article {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{article_id}/connections", response_model=Connection)
async def create_connection(
    article_id: str,
    connection_data: ConnectionCreate,
    current_user = Depends(get_current_user)
):
    """
    Создать связь из текущей статьи
    
    - **article_id**: ID исходной статьи
    - **connection_data**: Данные связи
    """
    if connection_data.source_id != article_id:
        raise HTTPException(
            status_code=400,
            detail="Source ID must match article ID in path"
        )
    
    try:
        return await ArticleService.create_connection(
            source_id=connection_data.source_id,
            target_id=connection_data.target_id,
            connection_type=connection_data.connection_type,
            strength=connection_data.strength,
            description=connection_data.description,
            user_id=current_user.id
        )
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating connection: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{article_id}/explore", response_model=List[Article])
async def explore_around(
    article_id: str,
    radius: int = Query(2, ge=1, le=4, description="Радиус обхода (1-4)"),
    limit: int = Query(20, ge=1, le=100, description="Лимит статей")
):
    """
    Исследовать статьи вокруг данной
    
    - **article_id**: ID центральной статьи
    - **radius**: Радиус обхода (сколько шагов от центра)
    - **limit**: Максимальное количество статей
    """
    try:
        articles = await GraphService.explore_around(
            article_id=article_id,
            radius=radius,
            limit=limit
        )
        return articles
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error exploring around {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/path/find", response_model=PathFindingResponse)
async def find_path(path_request: PathFindingRequest):
    """
    Найти путь между двумя статьями
    
    - **start_id**: ID начальной статьи
    - **end_id**: ID конечной статьи
    - **max_depth**: Максимальная глубина поиска
    - **min_strength**: Минимальная сила связи
    """
    try:
        path = await GraphService.find_shortest_path(
            start_id=path_request.start_id,
            end_id=path_request.end_id,
            max_depth=path_request.max_depth,
            min_strength=path_request.min_strength
        )
        if not path:
            raise NotFoundException("Path not found")
        return path
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error finding path: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{article_id}/graph", response_model=Dict[str, Any])
async def get_article_graph(
    article_id: str,
    depth: int = Query(2, ge=1, le=3, description="Глубина графа (1-3)")
):
    """
    Получить граф для визуализации вокруг статьи
    
    - **article_id**: ID центральной статьи
    - **depth**: Глубина графа (сколько уровней связей включить)
    """
    try:
        graph = await GraphService.get_article_graph(
            article_id=article_id,
            depth=depth
        )
        if not graph:
            raise NotFoundException(f"Article with ID {article_id} not found")
        return graph
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting graph for {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")