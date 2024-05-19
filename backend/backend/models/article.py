from pydantic import BaseModel, Field
from typing import List

class Article(BaseModel):
    title: str
    content: str

class RelatedArticles(BaseModel):
    main_title: str
    keywords: List[str]
    article_ids: List[str] = Field(default_factory=list)
