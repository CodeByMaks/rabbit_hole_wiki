// src/entities/article/model/article.ts
export interface Article {
  id: string;
  title: string;
  content: string;
  summary: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  connections: Connection[];
  createdAt: string;
  updatedAt: string;
}

export interface Connection {
  id: string;
  targetId: string;
  type: string;
  strength: number;
  description?: string;
}

// src/entities/article/ui/ArticleCard.tsx
import { Article } from '../model/article';
import { formatDate } from '@/shared/lib/utils';

interface ArticleCardProps {
  article: Article;
  onExplore?: () => void;
}

export function ArticleCard({ article, onExplore }: ArticleCardProps) {
  return (
    <div className="article-card">
      <h2>{article.title}</h2>
      <p className="summary">{article.summary}</p>
      <div className="meta">
        <span className="category">{article.category}</span>
        <span className="difficulty">{article.difficulty}</span>
        <span className="date">{formatDate(article.updatedAt)}</span>
      </div>
      {onExplore && (
        <button onClick={onExplore}>Исследовать связи</button>
      )}
    </div>
  );
}