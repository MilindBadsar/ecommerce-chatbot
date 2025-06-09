# E-commerce AI Sales Chatbot (Full-Stack)

This project implements a full-stack e-commerce sales chatbot system. It features a Django-powered backend with a PostgreSQL database and Groq AI integration, combined with a responsive React frontend for an interactive user experience, including product search functionality.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Backend Setup (Django)](#backend-setup-django)
  - [Frontend Setup (React)](#frontend-setup-react)
- [Execution Instructions](#execution-instructions)
- [API Endpoints](#api-endpoints)
- [Project Summary](#project-summary)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Interactive AI Chatbot:** Engage with an AI sales assistant powered by Groq to get product information, recommendations, and general assistance.
- **Product Search:** Search for e-commerce products by name or description.
- **Product Display:** View search results with essential product details (name, price, description, image, stock, category).
- **Session Management:** Chat sessions are maintained and logged on the backend.
- **Responsive UI:** A user-friendly interface designed to work across various devices (desktop, tablet, mobile).
- **Scalable Backend:** Built with Django REST Framework, providing a robust and extensible API.

## Technology Stack

### Backend

- **Framework:** Django 5.0.6
- **API:** Django REST Framework
- **Database:** PostgreSQL
- **AI Integration:** Groq Python SDK (using Llama 3 8B model)
- **Environment Management:** Python `venv`, `python-dotenv`
- **CORS Handling:** `django-cors-headers`

### Frontend

- **Framework:** React.js (created with Create React App)
- **State Management:** React Hooks (`useState`, `useEffect`, `useRef`)
- **API Communication:** Browser `fetch` API
- **Unique IDs:** `uuid` library
- **Styling:** Pure CSS

## Setup and Installation

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Node.js & npm (or Yarn)**: [Download Node.js](https://nodejs.org/en/download/) (npm comes with Node.js)
- **PostgreSQL**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Groq API Key**: Obtain one from [Groq Cloud](https://console.groq.com/keys) (it's free to get started).

### Backend Setup (Django)

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-project-folder>
    ```

2.  **Navigate to the `backend` directory:**

    ```bash
    cd backend
    ```

3.  **Create and activate a Python virtual environment:**

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

4.  **Install backend dependencies:**

    ```bash
    pip install -r requirements.txt # (Assuming you'll generate this: pip freeze > requirements.txt)
    # Alternatively, manually install:
    pip install Django djangorestframework psycopg2-binary groq python-dotenv django-cors-headers
    ```

5.  **Configure PostgreSQL:**

    - Create a new PostgreSQL database (e.g., `ecommerce_chatbot_db`).
    - Create a new PostgreSQL user (e.g., `ecommerce_user`) with a strong password. Grant this user ownership of the `ecommerce_chatbot_db`.
      - Example `psql` commands:
        ```sql
        CREATE DATABASE ecommerce_chatbot_db;
        CREATE USER ecommerce_user WITH PASSWORD 'your_db_password';
        ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
        ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
        ALTER ROLE ecommerce_user SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE ecommerce_chatbot_db TO ecommerce_user;
        ```
      - Alternatively, use `pgAdmin` to create the database and user.

6.  **Update Django settings:**

    - Open `backend/core/settings.py`.
    - Update the `DATABASES` setting with your PostgreSQL credentials:
      ```python
      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql',
              'NAME': 'ecommerce_chatbot_db',
              'USER': 'ecommerce_user',
              'PASSWORD': 'your_db_password',
              'HOST': 'localhost',
              'PORT': '5432',
          }
      }
      ```
    - Ensure `corsheaders` and `rest_framework` are in `INSTALLED_APPS`, and `corsheaders.middleware.CorsMiddleware` is in `MIDDLEWARE`.
    - Add CORS settings at the bottom (as provided in our discussion).

7.  **Set up Groq API Key:**

    - Create a file named `.env` in the `backend/` directory (next to `manage.py`).
    - Add your Groq API key:
      ```
      GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
      ```
    - **IMPORTANT:** Add `.env` to your `.gitignore` file to prevent committing your API key.

8.  **Run Django migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

9.  **Populate mock product data:**
    ```bash
    python manage.py populate_products
    ```

### Frontend Setup (React)

1.  **Navigate to the `frontend` directory:**

    ```bash
    cd ../frontend
    ```

2.  **Install frontend dependencies:**
    ```bash
    npm install
    # or if you use yarn:
    # yarn install
    ```
    This will install `react`, `react-dom`, `uuid`, etc.

## Execution Instructions

1.  **Start the Django Backend Server:**

    - Open a new terminal.
    - Navigate to the `backend/` directory.
    - Activate your virtual environment (`source venv/bin/activate` or `.\venv\Scripts\activate`).
    - Run the Django development server:
      ```bash
      python manage.py runserver
      ```
    - The backend will typically run on `http://127.0.0.1:8000/`.

2.  **Start the React Frontend Development Server:**
    - Open another new terminal.
    - Navigate to the `frontend/` directory.
    - Start the React development server:
      ```bash
      npm start
      # or yarn start
      ```
    - The frontend will typically open in your browser at `http://localhost:3000/`.

## API Endpoints

The backend provides the following REST API endpoints:

### Products API (`http://127.0.0.1:8000/api/products/`)

- **GET `/api/products/`**: Retrieve a list of all products.
- **GET `/api/products/<int:id>/`**: Retrieve details of a specific product by its ID.
- **GET `/api/products/search/?query=<search_term>`**: Search for products by name or description (case-insensitive).

### Chatbot API (`http://127.0.0.1:8000/api/chat/`)

- **POST `/api/chat/`**: Send a user message to the chatbot and receive an AI-generated response.
  - **Request Body (JSON):**
    ```json
    {
      "message": "Your user query here",
      "session_id": "a_unique_session_id_string"
    }
    ```
  - **Response Body (JSON):**
    ```json
    {
      "response": "The chatbot's generated reply"
    }
    ```

## Project Summary

This project successfully integrates a robust Django backend with a dynamic React frontend to create an interactive e-commerce sales chatbot. The backend efficiently manages product data in a PostgreSQL database and utilizes the Groq AI API for rapid, intelligent conversational responses. The frontend provides a seamless user experience, allowing for natural language interaction with the chatbot and direct product searching. Key features include mock product data population, RESTful APIs for product and chat functionalities, secure API key handling, and a responsive design that adapts to various screen sizes. The modular structure of both the backend (Django apps) and frontend (React components) ensures maintainability and scalability for future enhancements.

## Future Enhancements

- **User Authentication:** Implement user registration and login to personalize experiences (e.g., chat history per user).
- **Advanced Chatbot AI:** Integrate function calling for the AI model to directly perform actions like searching products based on chat context.
- **Shopping Cart/Order Management:** Extend product functionality to include adding items to a cart and managing orders.
- **Admin Panel Improvements:** Customize Django Admin for easier product and chat interaction management.
- **Real-time Communication:** Implement WebSockets for more fluid chat interactions.
- **Deployment:** Deploy the application to cloud platforms for public access.

## Contributing

Feel free to fork the repository, create feature branches, and submit pull requests.
