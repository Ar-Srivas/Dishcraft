import { Link } from 'react-router-dom';

function Header({ searchType, onToggleSearch }) {
    return (
        <header>
            <Link to="/" className="titleName">Dishcraft</Link>
            <div className="search-mode">
                <span 
                    className={`toggle-option ${!searchType ? 'active-mode' : ''}`}
                    onClick={() => onToggleSearch(false)}
                >
                    Plain Search
                </span>
                <span 
                    className={`toggle-option ${searchType ? 'active-mode' : ''}`}
                    onClick={() => onToggleSearch(true)}
                >
                    Mood Search
                </span>
            </div>
            <Link to="/favorites" className="favorites-btn">
                Favorites ❤️
            </Link>
        </header>
    );
}

export default Header;