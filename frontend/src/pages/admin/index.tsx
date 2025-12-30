// src/pages/article-explorer/index.tsx
import { ArticleGraphWidget } from '@/widgets/graph-visualizer';
import { NavigationSidebar } from '@/widgets/navigation-sidebar';
import { ArticleNavigation } from '@/features/article-navigation';
import { ArticleCard } from '@/entities/article';
import { Button, Card } from '@/shared/ui';

export function ArticleExplorerPage() {
  return (
    <div className="article-explorer">
      <NavigationSidebar />
      <main className="content">
        <ArticleGraphWidget />
        <div className="controls">
          <ArticleNavigation />
          <Button>Случайная статья</Button>
        </div>
        <ArticleCard />
      </main>
    </div>
  );
}