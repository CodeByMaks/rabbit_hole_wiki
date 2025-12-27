from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ConnectionType(str, Enum):
    """Типы связей между статьями"""
    RELATED_TO = "RELATED_TO"
    PART_OF = "PART_OF"
    PREREQUISITE = "PREREQUISITE"
    SIMILAR_TO = "SIMILAR_TO"
    OPPOSES = "OPPOSES"
    INSPIRES = "INSPIRES"
    APPLIES = "APPLIES"

class DifficultyLevel(str, Enum):
    """Уровень сложности статьи"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ArticleBase(BaseModel):
    """Базовая модель статьи"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=10)
    summary: str = Field(..., min_length=10, max_length=500)
    category: str = Field(..., min_length=1, max_length=100)
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    tags: List[str] = Field(default_factory=list)

class ArticleCreate(ArticleBase):
    """Модель для создания статьи"""
    pass

class ArticleUpdate(BaseModel):
    """Модель для обновления статьи"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    summary: Optional[str] = Field(None, min_length=10, max_length=500)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    difficulty: Optional[DifficultyLevel] = None
    tags: Optional[List[str]] = None

class Article(ArticleBase):
    """Модель статьи с ID и временными метками"""
    id: str
    created_at: datetime
    updated_at: datetime
    views_count: int = 0
    connections_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)

class ConnectionBase(BaseModel):
    """Базовая модель связи"""
    source_id: str
    target_id: str
    connection_type: ConnectionType = ConnectionType.RELATED_TO
    strength: float = Field(0.5, ge=0.0, le=1.0)
    description: Optional[str] = Field(None, max_length=500)

class ConnectionCreate(ConnectionBase):
    """Модель для создания связи"""
    pass

class Connection(ConnectionBase):
    """Модель связи с ID"""
    id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ArticleWithConnections(Article):
    """Статья со всеми её связями"""
    connections: List[Connection] = []
    
    model_config = ConfigDict(from_attributes=True)

class GraphNode(BaseModel):
    """Узел для визуализации графа"""
    id: str
    label: str
    group: str  # category
    size: int = 10
    color: Optional[str] = None

class GraphLink(BaseModel):
    """Связь для визуализации графа"""
    source: str
    target: str
    value: float  # strength
    type: str

class GraphVisualization(BaseModel):
    """Модель для визуализации графа"""
    nodes: List[GraphNode]
    links: List[GraphLink]
    
class PathFindingRequest(BaseModel):
    """Запрос на поиск пути"""
    start_id: str
    end_id: str
    max_depth: int = Field(6, ge=2, le=10)
    min_strength: float = Field(0.3, ge=0.0, le=1.0)

class PathFindingResponse(BaseModel):
    """Результат поиска пути"""
    path: List[Article]
    connections: List[Connection]
    length: int
    total_strength: float
    is_complete: bool