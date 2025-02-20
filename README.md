# DishCraft - Setup Guide

Instructions to set up and run the backend (FastAPI) and frontend (React with Vite) for DishCraft.

## Prerequisites

Ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 16+](https://nodejs.org/)

## Backend (FastAPI) Setup

1. **Navigate to the backend directory:**
   ```sh
   cd backend
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the FastAPI server:**
   ```sh
   uvicorn server:app --reload
   ```
4. **API Documentation:** Open the following URLs in your browser:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Frontend (React + Vite) Setup

1. **Navigate to the frontend directory:**
   ```sh
   cd frontend/dishcraft
   ```
2. **Install dependencies:**
   ```sh
   npm install
   ```
3. **Run the frontend development server:**
   ```sh
   npm run dev
   ```
4. **Access the app:** Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## Running the Full Stack Application

To run both the backend and frontend simultaneously:

1. **Open two terminal windows**
2. **Run the backend server:**
   ```sh
   cd backend
   uvicorn server:app --reload
   ```
3. **Run the frontend server:**
   ```sh
   cd frontend/dishcraft
   npm run dev
   ```

Now, your DishCraft app should be fully functional! 🚀

