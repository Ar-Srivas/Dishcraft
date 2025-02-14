from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from mlpro.data_service import data_service
from mlpro.vector_search import VectorSearch
from mlpro.llm_classifier import LLMClassifier
from mlpro.recommender import recommend_dish, mood_mapping
import logging
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dishcraft.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve static files
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="static")

vector_search = VectorSearch(data_service.df, data_service.embeddings)
llm_classifier = LLMClassifier(mood_mapping)

@app.get('/')
async def root():
    return {'message': 'Hello World', "data": 0}

@app.get('/search')
async def search(query: str = Query(...), diet: str = Query(None), cuisine: str = Query(None)):
    logging.info(f"Search request - query: {query}, diet: {diet}, cuisine: {cuisine}")
    try:
        results = vector_search.search(query, diet, cuisine)
        return {"results": results, "message": f"Found {len(results)} results"}
    except Exception as e:
        logging.error(f"Search error: {e}")
        return {"results": [], "message": "Error processing search"}

@app.get('/recommendation')
async def recommendation(input: str = Query(...), diet: str = Query(None), cuisine: str = Query(None)):
    logging.info(f"Recommendation request - input: {input}, diet: {diet}, cuisine: {cuisine}")
    try:
        result = recommend_dish(input, diet, cuisine)
        if not result.get('recommendations'):
            return {"recommendations": [], "message": "No recommendations found"}
        return result
    except Exception as e:
        logging.error(f"Recommendation error: {e}")
        return {"recommendations": [], "message": "Error processing recommendation"}

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Run the app with the specified host and port
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload in production
    )