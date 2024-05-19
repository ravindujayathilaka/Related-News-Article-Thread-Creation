from pymongo import MongoClient
from bson import ObjectId
from models.article import Article, RelatedArticles
from utils.ml_model import calculate_similarity, extract_keywords
from config import settings

client = MongoClient(settings.MONGODB_URI)
db = client.news_db
articles_collection = db.articles
clusters_collection = db.related_articles

class ArticleService:

    @staticmethod
    def process_article(article: Article):
        article_data = article.model_dump()
        
        # Insert the article into the articles collection and get the inserted ID
        result = articles_collection.insert_one(article_data)
        article_id = str(result.inserted_id)

        # Update the article with the article_id field
        articles_collection.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {"article_id": article_id}}
        )

        keywords = extract_keywords(article_data["title"])
        
        related_articles = list(clusters_collection.find({}))
        max_similarity = 0
        best_match = None

        for related in related_articles:
            similarity = calculate_similarity(keywords, related["keywords"])
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = related

        if max_similarity > 0.2 and best_match:
            clusters_collection.update_one(
                {"_id": best_match["_id"]},
                {"$push": {"article_ids": article_id}}
            )
            return {"message": "Article added to existing cluster", "cluster_id": str(best_match["_id"])}
        else:
            new_cluster = RelatedArticles(
                main_title=article_data["title"],
                keywords=keywords,
                article_ids=[article_id]
            )
            result = clusters_collection.insert_one(new_cluster.model_dump())
            return {"message": "New cluster created", "cluster_id": str(result.inserted_id)}

    @staticmethod
    def get_all_threads():
        threads = list(clusters_collection.find({}))
        return [{"cluster_id": str(thread["_id"]), "main_title": thread["main_title"], "article_ids": thread["article_ids"]} for thread in threads]

    @staticmethod
    def get_related_articles(cluster_id: str):
        thread = clusters_collection.find_one({"_id": ObjectId(cluster_id)})
        if thread:
            article_ids = thread["article_ids"]
            articles = list(articles_collection.find({"_id": {"$in": [ObjectId(article_id) for article_id in article_ids]}}))
            return [{"article_id": str(article["_id"]), "title": article["title"], "content": article["content"]} for article in articles]
        else:
            return None
