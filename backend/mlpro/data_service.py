import os
from pathlib import Path
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import logging
import pickle

logger = logging.getLogger(__name__)

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
        # Get the path to backend root
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.root_dir = current_dir.parent
        
        logger.info(f"Looking for data in: {self.root_dir}")
        
        try:
            # Load CSV data from root
            self.df = pd.read_csv(
                self.root_dir / 'balanced_reference_data.csv',
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
            logger.info("CSV data loaded successfully")
            
            # Load embeddings from root
            with open(self.root_dir / 'embeddings.pkl', 'rb') as f:
                self.embeddings = pickle.load(f)
            logger.info("Embeddings loaded successfully")
            
            # Load model from root
            with open(self.root_dir / 'model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            logger.info("Model loaded successfully")
            
            self.preprocess_data()
            logger.info("Data preprocessing completed")
            
        except Exception as e:
            logger.error(f"Error initializing data service: {e}")
            raise

    def preprocess_data(self):
        self.df['course'] = self.df['course'].str.replace(' ', '').str.lower()
        self.df['cuisine'] = self.df['cuisine'].str.replace(' ', '').str.lower()
        logger.info("Data preprocessing completed successfully")

# Initialize the data service
data_service = DataService()