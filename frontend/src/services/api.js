// Base URL for your Django backend API
const API_BASE_URL = "http://localhost:8000/api";

// --- Chatbot API Calls ---
export const sendMessageToChatbot = async (message, sessionId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, session_id: sessionId }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to get bot response");
    }

    const data = await response.json();
    return data.response; // The actual bot response
  } catch (error) {
    console.error("Error sending message to chatbot:", error);
    throw error;
  }
};

// --- Product Search API Calls ---
export const searchProducts = async (query) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/products/search/?query=${encodeURIComponent(query)}`
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to search products");
    }

    const data = await response.json();
    return data; // Array of products
  } catch (error) {
    console.error("Error searching products:", error);
    throw error;
  }
};

export const getProductDetails = async (productId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/${productId}/`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.error || `Failed to fetch product ${productId}`
      );
    }

    const data = await response.json();
    return data; // Single product object
  } catch (error) {
    console.error(`Error fetching product ${productId}:`, error);
    throw error;
  }
};
