"""
News service handling news/article operations
"""
from typing import List, Optional
from store.models import NewsArticle
from store.repositories.news import NewsArticleRepository


class NewsService:
    """
    Service for news/article operations.
    Handles article retrieval and view counting.
    """

    def __init__(self):
        self.repo = NewsArticleRepository()

    def get_article(self, slug: str) -> Optional[NewsArticle]:
        """
        Get article by slug with view increment.
        """
        article = self.repo.get_by_slug(slug)
        if article:
            self.repo.increment_views(article)
        return article

    def get_all_articles(self, limit: int = None) -> List[NewsArticle]:
        """
        Get all articles.
        """
        return self.repo.get_all_articles(limit)

    def get_articles_by_category(self, category: str) -> List[NewsArticle]:
        """
        Get articles by category.
        """
        return self.repo.get_by_category(category)

    def get_related_articles(self, article: NewsArticle, limit: int = 3) -> List[NewsArticle]:
        """
        Get articles related to given article.
        """
        return self.repo.get_related_articles(article, limit)

    def search_articles(self, query: str) -> List[NewsArticle]:
        """
        Search articles by title or content.
        """
        return self.repo.search(query)

    def get_homepage_news(self, limit: int = 3) -> List[NewsArticle]:
        """
        Get news for homepage display.
        """
        return self.get_all_articles(limit)

    def get_popular_articles(self, limit: int = 5) -> List[NewsArticle]:
        """
        Get articles sorted by views (most popular).
        """
        articles = self.repo.get_all_articles()
        return sorted(articles, key=lambda x: x.views, reverse=True)[:limit]
