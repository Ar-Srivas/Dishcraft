# server.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import gc
import pickle
from typing import Dict, List
import threading

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global lock for model access
model_lock = threading.Lock()

class ModelService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.model = None
        self.df = None
        self.embeddings = None
        self.load_data()
    
    def load_data(self):
        try:
            # Load minimal required columns
            self.df = pd.read_csv(
                'data/balanced_reference_data.csv',
                encoding='latin-1',
                usecols=['name', 'course', 'cuisine', 'diet', 'image_url'],
                dtype={
                    'name': 'category',
                    'course': 'category',
                    'cuisine': 'category',
                    'diet': 'category',
                    'image_url': str
                }
            )
            
            # Load pre-computed embeddings
            self.embeddings = np.load('data/embeddings.npz', mmap_mode='r')['embeddings']
            
            # Load model with minimal footprint
            self.model = SentenceTransformer(
                'paraphrase-MiniLM-L3-v2',
                device='cpu'
            )
            
            # Force garbage collection
            gc.collect()
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

model_service = ModelService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up...")
    yield
    # Shutdown
    logger.info("Shutting down...")
    if model_service.model:
        del model_service.model
    gc.collect()

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dishcraftfrontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get('/search')
async def search(
    query: str = Query(..., max_length=500),
    diet: str = Query(None, max_length=50),
    cuisine: str = Query(None, max_length=50)
) -> Dict:
    try:
        with model_lock:
            query_embedding = model_service.model.encode([query])[0]
        
        # Use efficient numpy operations
        similarities = np.dot(model_service.embeddings, query_embedding)
        top_indices = np.argpartition(similarities, -3)[-3:]
        
        results = []
        for idx in top_indices:
            recipe = model_service.df.iloc[idx].to_dict()
            if (not diet or recipe['diet'].lower() == diet.lower()) and \
               (not cuisine or recipe['cuisine'].lower() == cuisine.lower()):
                results.append(recipe)
        
        return JSONResponse(
            content={
                "results": results,
                "count": len(results)
            },
            headers={
                "Cache-Control": "public, max-age=300"  # 5 minute cache
            }
        )
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Search processing error")

@app.get('/recommendation')
async def recommendation(
    input: str = Query(..., max_length=500),
    diet: str = Query(None, max_length=50),
    cuisine: str = Query(None, max_length=50)
) -> Dict:
    try:
        # Simple mood-based filtering for now
        filtered_df = model_service.df
        
        if diet:
            filtered_df = filtered_df[filtered_df['diet'].str.lower() == diet.lower()]
        if cuisine:
            filtered_df = filtered_df[filtered_df['cuisine'].str.lower() == cuisine.lower()]
        
        recommendations = filtered_df.sample(min(3, len(filtered_df))).to_dict('records')
        
        return JSONResponse(
            content={
                "recommendations": recommendations,
                "count": len(recommendations)
            },
            headers={
                "Cache-Control": "public, max-age=300"  # 5 minute cache
            }
        )
    
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail="Recommendation processing error")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        workers=1,  # Limit workers to control memory usage
        limit_max_requests=10000,  # Restart workers periodically
        timeout_keep_alive=30
    )