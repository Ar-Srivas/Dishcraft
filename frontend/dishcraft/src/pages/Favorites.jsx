import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import Modal from '../components/Modal';
function Favorites() {
    const [favorites, setFavorites] = useState([]);
    const [selectedDish, setSelectedDish] = useState(null);

    useEffect(() => {
    const storedFavorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    setFavorites(storedFavorites);
    }, []);

    const handleCardClick = (dish) => {
    setSelectedDish(dish);
    };

    return (
    <div className="favorites-page">
        <h1>Your Favorite Recipes</h1>
    <div className="cards-container">
        {favorites.length === 0 ? (
        <p>No favorites yet! Start adding some recipes.</p>
        ) : (
        favorites.map((dish, index) => (
            <Card
            key={index}
            dish_name={dish.name}
            dish_course={dish.course}
            dish_image={dish.image_url}
            dish_diet={dish.diet}
            onClick={() => handleCardClick(dish)}
            />
        ))
        )}
    </div>
    {selectedDish && (
        <Modal 
        isOpen={!!selectedDish}
        onClose={() => setSelectedDish(null)}
        dish={selectedDish}/>
    )}
    </div>
);
}

export default Favorites;