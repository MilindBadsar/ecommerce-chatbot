import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import SearchBar from "./components/SearchBar";
import ProductList from "./components/ProductList";
import { searchProducts } from "./services/api";
import "./index.css";

function App() {
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchError, setSearchError] = useState(null);

  const handleSearch = async (query) => {
    setIsSearching(true);
    setSearchError(null);
    setSearchResults([]); // Clearing previous results

    try {
      const products = await searchProducts(query);
      setSearchResults(products);
    } catch (error) {
      console.error("Error during product search:", error);
      setSearchError("Failed to fetch products. Please try again.");
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="App">
      {/* Main container for chatbot and product display */}
      <div className="main-content-container">
        <div className="chatbot-section">
          <ChatWindow />
        </div>
        <div className="product-search-section">
          <SearchBar onSearch={handleSearch} />
          {isSearching && (
            <p className="loading-message">Searching for products...</p>
          )}
          {searchError && <p className="error-message">{searchError}</p>}
          <ProductList products={searchResults} />
        </div>
      </div>
    </div>
  );
}

export default App;
