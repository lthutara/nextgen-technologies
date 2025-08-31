import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, RawArticle
from datetime import datetime

# Setup for an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_add_raw_article(db_session):
    """Tests adding a RawArticle to the database and verifying its properties."""
    # 1. Prepare test data
    test_article_data = {
        "title": "Test Title",
        "content": "Test content.",
        "summary": "Test summary.",
        "source_url": "http://test.com/article",
        "source_name": "Test Source",
        "category": "Testing",
        "published_date": datetime.utcnow()
    }

    # 2. Create and save the RawArticle
    new_article = RawArticle(**test_article_data)
    db_session.add(new_article)
    db_session.commit()

    # 3. Retrieve the article from the database
    retrieved_article = db_session.query(RawArticle).filter_by(source_url="http://test.com/article").first()

    # 4. Assert that the retrieved article is not None and its properties match
    assert retrieved_article is not None
    assert retrieved_article.title == test_article_data["title"]
    assert retrieved_article.source_name == test_article_data["source_name"]
    assert retrieved_article.category == test_article_data["category"]