from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from typing import List, Dict
import pandas as pd

class VectorSearch:
    def __init__(self, df: pd.DataFrame, embeddings: np.ndarray):
        self.df = df
        self.embeddings = embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def search(self, query: str, diet: str = None, cuisine: str = None) -> List[Dict]:
        try:
            query_embedding = self.model.encode([query])[0]
            similarities = np.dot(self.embeddings, query_embedding)
            top_3 = np.argsort(similarities)[-3:][::-1]
            
            results = []
            for idx in top_3:
                recipe = self.df.iloc[idx].to_dict()
                if self._matches_filters(recipe, diet, cuisine):
                    results.append(recipe)
            
            logging.info(f"Found {len(results)} results for query: {query}")
            return results
        except Exception as e:
            logging.error(f"Search error: {e}")
            return []

    def _matches_filters(self, recipe, diet, cuisine):
        return (not diet or recipe['diet'].lower() == diet.lower()) and \
               (not cuisine or recipe['cuisine'].lower() == cuisine.lower())