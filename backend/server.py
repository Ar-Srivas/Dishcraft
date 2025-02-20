# server.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
import os
from dotenv import load_dotenv
from mlpro.data_service import data_service
from mlpro.vector_search import VectorSearch
from mlpro.llm_classifier import LLMClassifier
from mlpro.recommender import recommend_dish, mood_mapping

# Configure logging and environment
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS with specific origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "port": os.getenv('PORT', '10000'),
        "environment": os.getenv('ENVIRONMENT', 'development')
    }

@app.get('/search')
async def search(query: str = Query(...), diet: str = Query(None), cuisine: str = Query(None)):
    try:
        vector_search = VectorSearch(data_service.df, data_service.embeddings)
        results = vector_search.search(query, diet, cuisine)
        return JSONResponse(
            content={"results": results[:3], "count": len(results)},
            headers={"Cache-Control": "public, max-age=300"}
        )
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Search processing error")

@app.get('/recommendation')
async def recommendation(input: str = Query(...), diet: str = Query(None), cuisine: str = Query(None)):
    try:
        result = recommend_dish(input, diet, cuisine)
        return JSONResponse(
            content={
                "recommendations": result.get('recommendations', [])[:3],
                "count": len(result.get('recommendations', []))
            },
            headers={"Cache-Control": "public, max-age=300"}
        )
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail="Recommendation processing error")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        workers=1,
        log_level="info",
        limit_max_requests=10000,
        timeout_keep_alive=30
    )