# Acme Inc. Product Importer

This project is a full-stack web application designed to handle asynchronous, high-volume product imports from CSV files into a PostgreSQL database.

## 🚀 Architecture and Stack

The application uses a microservice-like pattern to separate the web responsibilities from the long-running data processing tasks.

* **Frontend (UI):** React
* **Backend (API & WebSockets):** Flask (Python) with Gunicorn
* **Background Tasks:** Celery
* **Database:** PostgreSQL (local or AWS RDS)
* **Message Broker:** Redis (Upstash or local)

---

## 🛠️ Local Setup and Installation

Follow these steps to get all three services running on your local machine using Docker Compose.

### Prerequisites

You must have the following installed:

1.  **Git**
2.  **Node.js & npm** (Use an LTS version like Node 18 or 20 for stability)
3.  **Docker & Docker Compose** (Installed and running)
4.  **PostgreSQL** (Running locally via Postgres.app or Docker, or connected to AWS RDS)
5.  **Redis** (Running locally or using an external service like Upstash)

### Step 1: Clone and Configure

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/jaisuriya97/fulfil.git](https://github.com/jaisuriya97/fulfil.git)
    cd fulfil
    ```

2.  **Set up the local environment file:**
    The application loads configuration from a `.env` file in the `backend/` directory.

    * Navigate to the backend folder: `cd backend`
    * Create the file: `touch .env`
    * Edit the `.env` file with your **local connection details**:

    ```.env
    # --- Local Database (Postgres.app) ---
    # Replace with your actual username and password
    DATABASE_URL="YOUR_DB_STRING"

    # --- Redis Broker (Local) ---
    # Use the default for a local Redis Docker container
    REDIS_URL="YOUR_REDIS_STRING"

    # --- Application Key ---
    SECRET_KEY="your-strong-random-key" 
    ```

### Step 2: Install Python Dependencies and Migrate DB

1.  **Install dependencies** (Flask, SQLAlchemy, etc.) in your virtual environment:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Run Database Migrations:**
    This creates the `product` and `webhook` tables in your local PostgreSQL database.
    ```bash
    export FLASK_APP=app.py
    flask db upgrade
    ```

### Step 3: Install Frontend Dependencies

1.  **Navigate to the frontend folder:**
    ```bash
    cd ../frontend
    ```
2.  **Install Node.js packages:**
    ```bash
    npm install
    ```

---

## ▶️ How to Run All Services

You will need three separate terminal windows or tabs running concurrently.

### Terminal 1: Run the Backend API (Flask/SocketIO)

This starts the web server and the real-time progress handler.

```bash
cd backend
source venv/bin/activate
python3 app.py
```

## 🏞️ Screen Short
<img width="1465" height="680" alt="Screenshot 2025-11-15 at 9 47 52 AM" src="https://github.com/user-attachments/assets/0b29ef87-ad6d-43da-92b6-092c8666b086" />
<img width="1470" height="844" alt="Screenshot 2025-11-15 at 9 47 37 AM" src="https://github.com/user-attachments/assets/70d99185-9766-4c32-93ad-b7aafd122169" />
<img width="1470" height="841" alt="Screenshot 2025-11-15 at 9 47 16 AM" src="https://github.com/user-attachments/assets/e6b9de7b-88bc-4b3c-b244-1046aaf30536" />
<img width="1470" height="842" alt="Screenshot 2025-11-15 at 9 46 49 AM" src="https://github.com/user-attachments/assets/fc58ffb4-d0f2-4460-8233-0e6d5dbe6bee" />


