import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, RawArticle, Article, ArticleSection
from datetime import datetime
from app.curation.services import CurationService
from app.curation.schemas import FinalArticleData # Import FinalArticleData

# Setup for an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine) # Create tables
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine) # Drop tables after test

def test_publish_final_article(db_session):
    """
    Tests the publishing of a RawArticle into a final curated Article.
    """
    # 1. Create a mock RawArticle
    raw_article_data = {
        "title": "Test Raw Article Title",
        "content": "This is the content of the test raw article. It has multiple sentences. The second sentence.",
        "summary": "Short summary.",
        "source_url": "http://testraw.com/article1",
        "source_name": "Test Raw Source",
        "category": "Technology",
        "published_date": datetime.utcnow(),
        "image_url": "http://testraw.com/image.jpg",
        "status": "pending",
        "content_type": "News"
    }
    raw_article = RawArticle(**raw_article_data)
    db_session.add(raw_article)
    db_session.commit()
    db_session.refresh(raw_article)

    # 2. Prepare FinalArticleData from raw_article (simulate previous curation steps)
    final_article_data = FinalArticleData(
        title_en=raw_article.title,
        summary_en=raw_article.summary,
        content_en=raw_article.content,
        title_te=raw_article.title + "_te", # Placeholder for Telugu
        summary_te=raw_article.summary + "_te", # Placeholder for Telugu
        content_te=raw_article.content + "_te", # Placeholder for Telugu
        image_url=raw_article.image_url,
        source_url=raw_article.source_url,
        source_name=raw_article.source_name,
        category=raw_article.category,
        published_date=raw_article.published_date,
        content_type=raw_article.content_type
    )

    # 3. Simulate the final publishing process
    curation_service = CurationService(db_session)
    published_article = curation_service.publish_final_article(raw_article.id, final_article_data)

    # 4. Verify the RawArticle's status is updated to 'published'
    db_session.refresh(raw_article)
    assert raw_article.status == "published"

    # 5. Verify a new Article is created and its properties match
    assert published_article is not None
    assert published_article.title_en == final_article_data.title_en
    assert published_article.category == final_article_data.category
    assert published_article.image_url == final_article_data.image_url
    assert published_article.source_url == final_article_data.source_url
    assert published_article.content_type == final_article_data.content_type
    assert published_article.is_active is True

    # Ensure ArticleSections are NOT created by publish_final_article, but the content is combined.
    # The CurationService.publish_final_article method explicitly creates a single Article
    # and sets its content_en/content_te fields, it does not manage ArticleSection directly.
    # Therefore, no assertions for ArticleSection here.
