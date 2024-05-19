from fastapi import FastAPI
from routes.article import router as articles_router
import uvicorn

app = FastAPI()

app.include_router(articles_router, prefix="/articles", tags=["articles"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
