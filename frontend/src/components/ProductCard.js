import React from "react";
import "../index.css";

const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <img
        src={product.image_url || "https://via.placeholder.com/150"}
        alt={product.name}
        className="product-image"
      />
      <h3 className="product-name">{product.name}</h3>
      <p className="product-price">₹{product.price}</p>
      <p className="product-description">
        {product.description.substring(0, 100)}...
      </p>
      <p className="product-stock">In Stock: {product.stock_quantity}</p>
      {product.category && (
        <p className="product-category">Category: {product.category.name}</p>
      )}
    </div>
  );
};

export default ProductCard;
