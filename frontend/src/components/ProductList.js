import React from "react";
import ProductCard from "./ProductCard";
import "../index.css";

const ProductList = ({ products }) => {
  if (!products || products.length === 0) {
    return (
      <p className="no-products-found">
        No products found. Try a different search!
      </p>
    );
  }

  return (
    <div className="product-list-grid">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
};

export default ProductList;
