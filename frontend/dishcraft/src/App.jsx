import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dropdown from './components/Dropdown';
import Search from './components/Search';
import Card from './components/Card';
import Header from './components/Header';
import Footer from './components/Footer';
import Modal from './components/Modal';
import Favorites from './pages/Favorites';
import './index.css';

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [message, setMessage] = useState('');
  const [dietFilter, setDietFilter] = useState('');
  const [cuisineFilter, setCuisineFilter] = useState('');
  const [selectedDish, setSelectedDish] = useState(null);
  const [searchType, setSearchType] = useState(false); // false = plain, true = mood

  const dietOptions = [
    "Vegetarian",
    "Non Vegeterian",
    "High Protein Vegetarian",
    "Diabetic Friendly",
    "High Protein Non Vegetarian",
    "Gluten Free",
    "No Onion No Garlic (Sattvic)",
    "Eggetarian",
    "Vegan",
    "Sugar Free Diet"
  ].filter(Boolean);
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const handleSearch = (input) => {
    const endpoint = searchType ? 'recommendation' : 'search';
    setMessage('Searching...');
    
    const params = new URLSearchParams();
    params.append(searchType ? 'input' : 'query', input);
    if (dietFilter) params.append('diet', dietFilter);
    if (cuisineFilter) params.append('cuisine', cuisineFilter);
    
    fetch(`${API_BASE_URL}/${endpoint}?${params}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Response data:', data); // Debug log
        if (endpoint === 'search') {
          setRecommendations(data.results || []);
        } else {
          setRecommendations(data.recommendations || []);
        }
        setMessage(data.message || '');
        
        if (!data.results?.length && !data.recommendations?.length) {
          setMessage('No results found');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setMessage('Error fetching results. Please try again.');
      });
  };

  const handleCardClick = (dish) => {
    setSelectedDish(dish);
  };

  const closeModal = () => {
    setSelectedDish(null);
  };

  return (
    <Router>
      <Header searchType={searchType} onToggleSearch={setSearchType} />
      <div className="main-container">
        <Routes>
          <Route path="/" element={
            <>
              <div className="filters-container">
                <Dropdown
                  label="Diet"
                  options={dietOptions}
                  selectedValue={dietFilter}
                  onSelect={setDietFilter}
                />
                <Dropdown
                  label="Cuisine"
                  options={['southindianrecipes', 'goanrecipes', 'assamese',
                            'northindianrecipes', 'bengalirecipes', 'indian', 'chettinad',
                            'andhra', 'tamilnadu', 'maharashtrianrecipes', 'kashmiri',
                            'uttarpradesh', 'northkarnataka', 'awadhi', 'keralarecipes',
                            'rajasthani', 'konkan', 'southkarnataka', 'malabar', 'karnataka',
                            'nepalese', 'fusion', 'hyderabadi', 'oriyarecipes', 'lucknowi',
                            'Indian', 'South Indian Recipes', 'Andhra', 'Udupi', 'Mexican',
                            'Fusion', 'Continental', 'Bengali Recipes', 'Punjabi', 'Chettinad',
                            'Tamil Nadu', 'Maharashtrian Recipes', 'North Indian Recipes',
                            'Italian Recipes', 'Sindhi', 'Thai', 'Chinese', 'Kerala Recipes',
                            'Gujarati Recipes', 'Coorg', 'Rajasthani', 'Asian',
                            'Middle Eastern', 'Coastal Karnataka', 'European', 'Kashmiri',
                            'Karnataka', 'Lucknowi', 'Hyderabadi', 'Side Dish', 'Goan Recipes',
                            'Arab', 'Assamese', 'Bihari', 'Malabar', 'Himachal', 'Awadhi',
                            'Cantonese', 'North East India Recipes', 'Sichuan', 'Mughlai',
                            'Japanese', 'Mangalorean', 'Vietnamese', 'British',
                            'North Karnataka', 'Parsi Recipes', 'Greek', 'Nepalese',
                            'Oriya Recipes', 'French', 'Indo Chinese', 'Konkan',
                            'Mediterranean', 'Sri Lankan', 'Haryana', 'Uttar Pradesh',
                            'Malvani', 'Indonesian', 'African', 'Shandong', 'Korean',
                            'American', 'Kongunadu', 'Pakistani', 'Caribbean',
                            'South Karnataka', 'Appetizer', 'Uttarakhand-North Kumaon',
                            'World Breakfast', 'Malaysian', 'Dessert', 'Hunan', 'Dinner',
                            'Snack', 'Jewish', 'Burmese', 'Afghan', 'Brunch', 'Jharkhand',
                            'Nagaland', 'Lunch']}
                  selectedValue={cuisineFilter}
                  onSelect={setCuisineFilter}
                />
              </div>

              <Search onSearch={handleSearch} />

              {message && <p>{message}</p>}
              <div className="cards-container">
                {recommendations.length > 0 ? (
                  recommendations.slice(0, 3).map((dish, index) => (
                    <Card
                      key={index}
                      dish_name={dish.name}
                      dish_course={dish.course}
                      dish_image={dish.image_url}
                      dish_diet={dish.diet}
                      onClick={() => handleCardClick(dish)}
                    />
                  ))
                ) : (
                  <p>No recommendations found.</p>
                )}
              </div>
            </>
          } />
          <Route path="/favorites" element={<Favorites />} />
        </Routes>
      </div>
      <Footer />
      <Modal 
        isOpen={!!selectedDish} 
        onClose={closeModal}
        dish={selectedDish}
      />
    </Router>
  );
}

export default App;