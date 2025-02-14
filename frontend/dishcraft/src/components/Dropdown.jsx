import React from "react";

const Dropdown = ({ label, options, selectedValue, onSelect }) => {
  return (
    <div className="dropdown-container">
    <label>{label}</label>
    <select 
        value={selectedValue} 
        onChange={(e) => onSelect(e.target.value)}
        className="dropdown"
    >
        <option value="">{`Select ${label}`}</option>
        {options.map((option, index) => (
        <option key={index} value={option}>
            {option}
        </option>
        ))}
    </select>
    </div>
    );
};

export default Dropdown;
