import React from 'react';

const Modal = ({ isOpen, onClose, dish }) => {
  if (!isOpen) return null;

  const handleOverlayClick = (e) => {
    if (e.target.className === 'modal-overlay') {
      onClose();
    }
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    alert('Link copied to clipboard!');
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>×</button>
        <div className="recipe-actions">
          <button onClick={handleShare}>Share 📤</button>
          <button onClick={handlePrint}>Print 🖨️</button>
        </div>
        <div className="recipe-detail">
          <div className="recipe-header">
            <img src={dish.image_url} alt={dish.name} className="recipe-image" />
            <h2>{dish.name}</h2>
          </div>
          <div className="recipe-info">
            <p><strong>Course:</strong> {dish.course}</p>
            <p><strong>Diet:</strong> {dish.diet}</p>
            <p><strong>Cuisine:</strong> {dish.cuisine}</p>
          </div>
          <div className="recipe-instructions">
            <h3>Instructions:</h3>
            <div className="steps-list">
              {dish.instructions && dish.instructions.split('\n').map((step, index) => (
                <div key={index} className="step-item">
                  <span className="step-number">{index + 1}.</span>
                  <span className="step-text">{step.trim()}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;