from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.article import Article
from services.article_service import ArticleService
from bson import ObjectId

router = APIRouter()

class ArticleRequest(BaseModel):
    title: str
    content: str

@router.post("/")
def add_article(article: ArticleRequest):
    article = Article(**article.model_dump())
    try:
        result = ArticleService.process_article(article)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/threads/")
def get_all_threads():
    try:
        threads = ArticleService.get_all_threads()
        return threads
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/threads/{cluster_id}/articles/")
def get_related_articles(cluster_id: str):
    try:
        if not ObjectId.is_valid(cluster_id):
            raise HTTPException(status_code=400, detail="Invalid cluster ID")
        articles = ArticleService.get_related_articles(cluster_id)
        if articles is None:
            raise HTTPException(status_code=404, detail="Cluster not found")
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
