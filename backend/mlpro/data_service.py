from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os
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
        current_dir = Path(os.path.dirname(__file__))
        data_dir = current_dir.parent / 'data'
        
        # Load minimal data
        self.df = pd.read_csv(
            data_dir / 'balanced_reference_data.csv',
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
        
        # Load compressed embeddings
        self.embeddings = np.load(data_dir / 'embeddings.npz')['embeddings']
        self.model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
        self.preprocess_data()

    def preprocess_data(self):
        self.df['course'] = self.df['course'].str.replace(' ', '').str.lower()
        self.df['cuisine'] = self.df['cuisine'].str.replace(' ', '').str.lower()

data_service = DataService()