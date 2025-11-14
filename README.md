# Acme Inc. Product Importer

This project is a full-stack web application built to import large CSV files (500,000+ records) into a SQL database asynchronously.

**LIVE APPLICATION:** [https://product-importer-ui.onrender.com](https://product-importer-ui.onrender.com)
*(You will get this URL after you deploy)*

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

### ## Deployment

This project is deployed on Render using a `render.yaml` Blueprint, which automatically provisions:
* A PostgreSQL database
* A Redis instance
* A Dockerized Flask/SocketIO web service (API)
* A Dockerized Celery background worker
* A static React site