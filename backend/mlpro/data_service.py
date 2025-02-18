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
        # Get the absolute path to the data directory
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = current_dir.parent.parent / 'data'
        
        logger.info(f"Looking for data in: {self.data_dir}")
        
        try:
            # Load CSV data
            self.df = pd.read_csv(
                self.data_dir / 'balanced_reference_data.csv',
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
            
            # Load embeddings from pickle file
            embeddings_path = self.data_dir / 'embeddings.pkl'
            logger.info(f"Loading embeddings from: {embeddings_path}")
            with open(embeddings_path, 'rb') as f:
                self.embeddings = pickle.load(f)
            logger.info("Embeddings loaded successfully")
            
            # Load model from pickle file
            model_path = self.data_dir / 'model.pkl'
            logger.info(f"Loading model from: {model_path}")
            with open(model_path, 'rb') as f:
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