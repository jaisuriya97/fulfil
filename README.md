# Acme Inc. Product Importer

This project is a full-stack web application built to import large CSV files (500,000+ records) into a SQL database asynchronously.

**LIVE APPLICATION:** [https://product-importer-ui.onrender.com](https://product-importer-ui.onrender.com)
*(You will get this URL after you deploy)*

---

### ## Features

* **Asynchronous CSV Upload:** Handles large CSV imports using a Celery background worker, never timing out the API.
* **Real-time Progress:** Uses WebSockets (Socket.IO) to show real-time import progress in the UI.
* **Full CRUD API:** A RESTful API to manage products and webhooks.
* **Product Management UI:** A React frontend for all features (Upload, List, Filter, Delete).
* **Containerized Deployment:** Deployed using Docker and Render.

---

### ## Tech Stack

* **Frontend:** React
* **Backend:** Flask (Python)
* **Database:** PostgreSQL
* **Async Tasks:** Celery
* **Message Broker:** Redis
* **Real-time:** Flask-SocketIO
* **Deployment:** Render (with Docker)

---

### ## How to Run Locally

1.  **Clone the repo:**
    ```bash
    git clone [your-repo-url]
    cd product-importer
    ```

2.  **Set up Backend:**
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Set up a local PostgreSQL DB & create a .env file
    # (Example: DATABASE_URL="postgresql://user:pass@localhost:5432/db_name")
    
    export FLASK_APP=app.py
    flask db upgrade
    ```

3.  **Set up Frontend:**
    ```bash
    cd ../frontend
    npm install
    ```

4.  **Run all services:**
    * **Terminal 1 (Flask):** `cd backend && python3 app.py`
    * **Terminal 2 (Celery):** `cd backend && celery -A celery_app.celery worker --loglevel=info`
    * **Terminal 3 (React):** `cd frontend && npm start`