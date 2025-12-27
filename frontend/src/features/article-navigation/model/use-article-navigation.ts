// src/features/article-navigation/model/use-article-navigation.ts
import { useState } from 'react';
import { articleApi } from '@/shared/lib/api';
import { Article } from '@/entities/article';

export function useArticleNavigation() {
  const [currentArticle, setCurrentArticle] = useState<Article | null>(null);
  const [history, setHistory] = useState<string[]>([]);
  
  const navigateToArticle = async (articleId: string) => {
    const article = await articleApi.getArticle(articleId);
    setCurrentArticle(article);
    setHistory(prev => [...prev, articleId]);
  };
  
  const goBack = () => {
    if (history.length > 1) {
      const previousId = history[history.length - 2];
      navigateToArticle(previousId);
      setHistory(prev => prev.slice(0, -1));
    }
  };
  
  return {
    currentArticle,
    history,
    navigateToArticle,
    goBack,
  };
}