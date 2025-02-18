from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os
import pickle
import logging
from pathlib import Path

class DataService:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
            
        self.initialized = True
        logging.basicConfig(level=logging.INFO)
        
        # Use relative paths from current directory
        current_dir = Path(os.path.dirname(__file__))
        data_dir = current_dir.parent / 'data'
        
        # Load data with minimal columns
        data_path = data_dir / 'balanced_reference_data.csv'
        self.df = pd.read_csv(
            data_path, 
            encoding='latin-1',
            usecols=['name', 'course', 'cuisine', 'diet', 'image_url']
        )
        
        # Load model once
        self.embeddings_path = data_dir / 'embeddings.pkl'
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.preprocess_data()
        self.embeddings = self.load_or_create_embeddings()

    def preprocess_data(self):
        self.df['course'] = self.df['course'].str.replace(' ', '').str.lower()
        self.df['cuisine'] = self.df['cuisine'].str.replace(' ', '').str.lower()
    
    def load_or_create_embeddings(self):
        if os.path.exists(self.embeddings_path):
            with open(self.embeddings_path, 'rb') as f:
                return pickle.load(f)
        
        texts = self.df['name'].tolist()
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        with open(self.embeddings_path, 'wb') as f:
            pickle.dump(embeddings, f)
        return embeddings

data_service = DataService()