"""
    Using fast-api library develop a backend for blog
"""

from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    content = Column(Text)


class ArticleCreate(BaseModel):
    title: str
    author: str
    content: str


# Create database tables
Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    # articles = db.query(Article).all()
    articles = [
        {"id": 1, "title": "Article 1", "author": "John Doe", "content": "Content of Article 1."},
        {"id": 2, "title": "Article 2", "author": "Jane Smith", "content": "Content of Article 2."},
        {"id": 3, "title": "Article 3", "author": "Alice Johnson", "content": "Content of Article 3."},
    ]
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})


@app.get("/articles/{article_id}", response_class=HTMLResponse)
def get_article(request: Request, article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    return templates.TemplateResponse("article.html", {"request": request, "article": article})


@app.post("/articles/", response_class=HTMLResponse)
async def create_article(request: Request, db: Session = Depends(get_db)):
    data = await request.form()
    print(dict(data))
    new_article = Article(**article_data)
    db.add(new_article)
    db.commit()
    print("Created article")
    return templates.TemplateResponse("article_created.html", {"request": request, "article": article})


@app.get("/articles/", response_class=HTMLResponse)
def create_article(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("article_creation.html", {"request": request})


# def insert_articles():
#     articles_data = [
#         {"title": "Article 1", "author": "John Doe", "content": "Content of Article 1."},
#         {"title": "Article 2", "author": "Jane Smith", "content": "Content of Article 2."},
#         {"title": "Article 3", "author": "Alice Johnson", "content": "Content of Article 3."},
#     ]
#     with get_db() as db:
#         for article_data in articles_data:
#             article = Article(**article_data)
#             db.add(article)
#         db.commit()


if __name__ == "__main__":
    import uvicorn
    # insert_articles()
    uvicorn.run(app, host="0.0.0.0", port=8000)
