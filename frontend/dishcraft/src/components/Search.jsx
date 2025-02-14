import React, { useState } from 'react';

function Search({ onSearch }) {
  const [input, setInput] = useState('');

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(input);
  };

  return (
    <form className="input-box" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Search..."
        value={input}
        onChange={handleInputChange}
      />
      <button type="submit">Search</button>
    </form>
  );
}

export default Search;