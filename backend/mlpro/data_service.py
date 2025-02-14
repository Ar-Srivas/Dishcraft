from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os
import pickle
import logging

class DataService:
    def __init__(self):
        self.df = pd.read_csv(r'backend\data\reference_data.csv', encoding='latin-1')
        self.embeddings_path = r'backend\data\embeddings.pkl'
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.preprocess_data()
        self.embeddings = self.load_or_create_embeddings()
    
    def preprocess_data(self):
        self.df['course'] = self.df['course'].str.replace(' ', '').str.lower()
        self.df['cuisine'] = self.df['cuisine'].str.replace(' ', '').str.lower()
    
    def load_or_create_embeddings(self):
        if os.path.exists(self.embeddings_path):
            logging.info("Loading cached embeddings")
            with open(self.embeddings_path, 'rb') as f:
                return pickle.load(f)
        
        logging.info("Creating new embeddings")
        texts = self.df['name'].tolist()
        embeddings = self.model.encode(texts)
        
        with open(self.embeddings_path, 'wb') as f:
            pickle.dump(embeddings, f)
        
        return embeddings

data_service = DataService()