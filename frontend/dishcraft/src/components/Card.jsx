import React, { useState, useEffect } from 'react';

const Card = ({ dish_name, dish_course, dish_image, dish_diet, onClick }) => {
  const [isFavorite, setIsFavorite] = useState(false);
  const [rating, setRating] = useState(0);

  const toggleFavorite = (e) => {
    e.stopPropagation();
    setIsFavorite(!isFavorite);
    const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    const recipe = {
      name: dish_name,
      course: dish_course,
      image_url: dish_image,
      diet: dish_diet
    };
    
    if (!isFavorite) {
      localStorage.setItem('favorites', JSON.stringify([...favorites, recipe]));
    } else {
      localStorage.setItem('favorites', 
        JSON.stringify(favorites.filter(f => f.name !== dish_name))
      );
    }
  };

  useEffect(() => {
    const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    setIsFavorite(favorites.some(f => f.name === dish_name));
  }, [dish_name]);

  return (
    <div className="card" onClick={onClick}>
      <div className="card-actions">
        <button onClick={toggleFavorite} className="favorite-btn">
          {isFavorite ? '❤️' : '🤍'}
        </button>
        <div className="rating">
          {[1,2,3,4,5].map(star => (
            <span 
              key={star}
              onClick={(e) => {
                e.stopPropagation();
                setRating(star);
              }}
              className={star <= rating ? 'star active' : 'star'}
            >
              ★
            </span>
          ))}
        </div>
      </div>
      <img src={dish_image} alt={dish_name} />
      <h3>{dish_name}</h3>
      <p>{dish_course}</p>
      <p>{dish_diet}</p> {/* Display diet information */}
    </div>
  );
};

export default Card;