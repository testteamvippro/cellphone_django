"""
News article repository for data access layer
"""
from store.models import NewsArticle
from store.repositories.base import BaseRepository


class NewsArticleRepository(BaseRepository):
    """Repository for NewsArticle model"""

    def __init__(self):
        super().__init__(NewsArticle)

    def get_all_articles(self, limit: int = None) -> list:
        """Get all articles ordered by newest"""
        query = self.filter().order_by('-created_at')
        if limit:
            query = query[:limit]
        return list(query)

    def get_by_slug(self, slug: str):
        """Get article by slug"""
        return self.get_single(slug=slug)

    def get_by_category(self, category: str) -> list:
        """Get articles by category"""
        return list(self.filter(category=category).order_by('-created_at'))

    def get_related_articles(self, article: NewsArticle, limit: int = 3) -> list:
        """Get related articles"""
        return list(
            self.filter(category=article.category)
            .exclude(id=article.id)
            .order_by('-created_at')[:limit]
        )

    def increment_views(self, article: NewsArticle) -> None:
        """Increment article views"""
        article.views += 1
        article.save(update_fields=['views'])

    def search(self, query: str) -> list:
        """Search articles by title or content"""
        from django.db.models import Q
        return list(
            self.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            ).order_by('-created_at')
        )
