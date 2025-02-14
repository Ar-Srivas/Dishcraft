import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
from sklearn import preprocessing
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random
import joblib 
import os
import logging
from mlpro.llm_classifier import LLMClassifier
from typing import List, Dict

logging.basicConfig(level=logging.INFO)

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('vader_lexicon')   

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Use relative paths to access the data file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '..', 'data', 'reference_data.csv')
model_path = os.path.join(base_dir, '..', 'data', 'model.pkl')

# Load the dataset
df = pd.read_csv(data_path, encoding='latin-1')

# Log unique values in the diet column
logging.info(f"Unique diet values: {df['diet'].unique()}")

# Preprocess the data
df['course'] = df['course'].str.replace(' ', '').str.lower()
df['cuisine'] = df['cuisine'].str.replace(' ', '').str.lower()

# Define mood mapping
mood_mapping = {
    "happy": {
        "courses": ["Dessert", "Snack", "Appetizer", "South Indian Breakfast", "North Indian Breakfast", "World Breakfast"],
        "cuisines": ["south indian recipes", "north indian recipes", "bengali recipes", "punjabi", "mangalorean", "gujarati recipesï»¿"],
        "diet": None
    },
    "stressed": {
        "courses": ["Dinner", "Main Course", "Side Dish"],
        "cuisines": ["mughlai", "kashmiri", "rajasthani", "chettinad", "lucknowi", "hyderabadi", "andhra"],
        "diet": None
    },
    "tired": {
        "courses": ["Snack", "Lunch", "One Pot Dish"],
        "cuisines": ["indo chinese", "sichuan", "chinese", "thai", "malvani", "tamil nadu"],
        "diet": ["vegetarian", "vegan"]
    },
    "adventurous": {
        "courses": ["South Indian Breakfast", "World Breakfast", "One Pot Dish"],
        "cuisines": ["nepalese", "fusion", "sri lankan", "nagaland", "afghan", "coastal karnataka", "middle eastern"],
        "diet": None
    },
    "relaxed": {
        "courses": ["Brunch", "Lunch", "Dinner", "Side Dish"],
        "cuisines": ["continental", "malabar", "udupi", "parsi recipes", "north karnataka", "kerala recipes"],
        "diet": None
    },
    "celebratory": {
        "courses": ["Dessert", "Appetizer", "Dinner", "Main Course"],
        "cuisines": ["mughlai", "hyderabadi", "awadhi", "punjabi", "indo chinese", "south indian recipes"],
        "diet": None
    },
    "health-conscious": {
        "courses": ["Lunch", "Dinner", "Side Dish", "Snack"],
        "cuisines": ["high protein vegetarian", "sugar free diet", "no onion no garlic (sattvic)"],
        "diet": ["vegetarian", "vegan"]
    }
}

llm_classifier = LLMClassifier(mood_mapping)

def assign_mood(row, mood_mapping):
    course = str(row['course']).strip().lower()
    cuisine = str(row['cuisine']).strip().lower()
    
    for mood, criteria in mood_mapping.items():
        courses = [c.lower().strip() for c in criteria.get('courses', [])]
        cuisines = [c.lower().strip() for c in criteria.get('cuisines', [])]
        
        if course in courses or cuisine in cuisines:
            return mood
    return "neutral"

df['mood'] = df.apply(lambda row: assign_mood(row, mood_mapping), axis=1)

# Encode categorical variables
le_mood = preprocessing.LabelEncoder()
le_cuisine = preprocessing.LabelEncoder()
le_course = preprocessing.LabelEncoder()

df['mood_encoded'] = le_mood.fit_transform(df['mood'])
df['cuisine_encoded'] = le_cuisine.fit_transform(df['cuisine'])
df['course_encoded'] = le_course.fit_transform(df['course'])

# Split the data
X = df[['course_encoded', 'cuisine_encoded']]
y = df['mood_encoded']

if not os.path.exists(model_path):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    # Check the number of samples in the minority class
    min_class_count = y_train.value_counts().min()
    if min_class_count > 1:
        smote = SMOTE(random_state=0, k_neighbors=min(min_class_count - 1, 5))
        X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
    else:
        X_train_smote, y_train_smote = X_train, y_train
    
    model = RandomForestClassifier(random_state=0)
    model.fit(X_train_smote, y_train_smote)
    joblib.dump(model, model_path)
else:
    model = joblib.load(model_path)

def extract_mood(sentence):
    sentiment_scores = sia.polarity_scores(sentence)
    compound_score = sentiment_scores['compound']
    
    if compound_score >= 0.5:
        return "happy"
    elif 0.1 <= compound_score < 0.5:
        return "relaxed"
    elif -0.1 < compound_score < 0.1:
        return "neutral"
    elif -0.5 < compound_score <= -0.1:
        return "stressed"
    else:
        return "tired"

def extract_mood_with_nltk_keywords(input_sentence):
    mood_keywords = {
        "happy": ["happy", "joyful", "cheerful", "delighted"],
        "stressed": ["stressed", "anxious", "worried", "tense"],
        "tired": ["tired", "exhausted", "sleepy", "fatigued"],
        "adventurous": ["adventurous", "curious", "bold", "daring"],
        "relaxed": ["relaxed", "calm", "peaceful", "chill"],
        "celebratory": ["celebratory", "festive", "joyous", "celebrating"],
        "health-conscious": ["healthy", "fit", "well", "diet"]
    }

    # Tokenize the input sentence
    tokens = nltk.word_tokenize(input_sentence.lower())

    # Match tokens with mood keywords
    for mood, keywords in mood_keywords.items():
        if any(keyword in tokens for keyword in keywords):
            return mood
    return "neutral"

def hybrid_mood_detection(input_sentence):
    # Dummy implementation for mood detection
    return "happy"

def normalize_string(s):
    if pd.isna(s):
        return ''
    return str(s).strip().lower().replace(' ', '')

def recommend_by_mood(mood: str, diet: str = None, cuisine: str = None) -> List[Dict]:
    filtered_df = df.copy()
    
    # Apply mood-based filters from mapping
    if mood in mood_mapping:
        mood_criteria = mood_mapping[mood]
        
        # Filter by courses
        if mood_criteria["courses"]:
            filtered_df = filtered_df[
                filtered_df['course'].str.lower().isin([c.lower() for c in mood_criteria["courses"]])
            ]
            
        # Filter by cuisines
        if mood_criteria["cuisines"]:
            filtered_df = filtered_df[
                filtered_df['cuisine'].str.lower().isin([c.lower() for c in mood_criteria["cuisines"]])
            ]
            
        # Apply mood-specific diet if specified
        if mood_criteria["diet"]:
            filtered_df = filtered_df[
                filtered_df['diet'].str.lower().isin([d.lower() for d in mood_criteria["diet"]])
            ]
    
    # Apply user filters
    if diet:
        filtered_df = filtered_df[filtered_df['diet'].str.lower() == diet.lower()]
    if cuisine:
        filtered_df = filtered_df[filtered_df['cuisine'].str.lower() == cuisine.lower()]
    
    # Return random sample of matches
    return filtered_df.sample(min(3, len(filtered_df))).to_dict('records')

def recommend_dish(sentence: str, diet=None, cuisine=None) -> Dict:
    logging.info(f"Processing request: {sentence}")
    
    # Get classification from LLM
    classification = llm_classifier.classify_input(sentence)
    input_type = classification["type"]
    value = classification["value"]
    
    filtered_df = df.copy()
    
    if input_type == "event":
        # Get food characteristics for event
        characteristics = llm_classifier.get_event_food_characteristics(value)
        for char in characteristics:
            filtered_df = filtered_df[
                filtered_df['name'].str.contains(char, case=False) |
                filtered_df['cuisine'].str.contains(char, case=False)
            ]
    
    elif input_type == "mood":
        # Use existing mood-based logic
        return {
            "recommendations": recommend_by_mood(value, diet, cuisine),
            "classification": classification
        }
    
    else:  # food request
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(value, case=False) |
            filtered_df['ingredients'].str.contains(value, case=False)
        ]
    
    # Apply common filters
    if diet:
        filtered_df = filtered_df[filtered_df['diet'].str.lower() == diet.lower()]
    if cuisine:
        filtered_df = filtered_df[filtered_df['cuisine'].str.lower() == cuisine.lower()]
    
    recommendations = filtered_df.sample(min(3, len(filtered_df))).to_dict('records')
    
    return {
        "recommendations": recommendations,
        "classification": classification,
        "filters_applied": {
            "type": input_type,
            "value": value,
            "diet": diet,
            "cuisine": cuisine
        }
    }