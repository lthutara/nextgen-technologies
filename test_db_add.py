from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Article, Base

if __name__ == "__main__":
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_article = Article(
        title="Test Article",
        content="This is a test article.",
        summary="Test summary.",
        source_url="http://example.com/test",
        source_name="Test Source",
        category="AI"
    )

    session.add(new_article)
    session.commit()

    retrieved_article = session.query(Article).filter_by(title="Test Article").first()
    if retrieved_article:
        print("Article added successfully!")
    else:
        print("Failed to add article.")

    session.close()
