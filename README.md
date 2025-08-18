# ✒️ Vacancies Collector: Asynchronous Vacancy Monitoring Service

This application is a microservice-based system for automatically collecting and delivering job vacancies to users via Telegram. The backend is implemented with FastAPI, an asynchronous worker processes parsing tasks, and a Telegram bot acts as the client interface.

---

## 🚀 Architecture and Technology

This project demonstrates a full-cycle backend development process using modern asynchronous tools and DevOps practices.

*   **FastAPI API:** An asynchronous REST API for managing users and their subscriptions (keywords).
*   **Asynchronous Worker:** An isolated service that receives parsing tasks from a message broker and executes them in the background without blocking the API.
*   **Aiogram 3 Telegram Bot:** The client interface for user interaction.
*   **Scheduler (APScheduler):** Periodically enqueues parsing tasks.
*   **Database (PostgreSQL):** Stores data about users and their search keywords.
*   **Message Broker (RabbitMQ):** Ensures reliable asynchronous communication between the API and the worker.
*   **Cache (Redis):** Used for caching database queries, significantly reducing load and speeding up API responses.

### 🛠️ Tech Stack

*   **Backend:** Python 3.12, **FastAPI**, **SQLAlchemy 2.0 (async)**, Pydantic V2, Alembic
*   **Asynchrony:** **asyncio**, **RabbitMQ** (via aio-pika), **Redis**
*   **Database:** **PostgreSQL**
*   **Infrastructure & DevOps:** **Docker**, **Docker Compose**, CI/CD (GitHub Actions)
*   **Testing:** **Pytest**, pytest-mock, httpx

---

## ✨ Key Features

*   **Asynchronous Architecture:** All components (API, worker, DB, and cache interactions) are fully asynchronous, ensuring high performance.
*   **Performance Optimization:**
    *   **`selectinload` over `joinedload`:** For efficient loading of one-to-many related data.
    *   **API-level Caching:** Reduces database load and accelerates `GET` requests using Redis.
    *   **Resource Management via `lifespan`:** Ensures proper startup and shutdown of connection pools.
*   **Reliability & Code Quality:**
    *   **Comprehensive Test Coverage:** E2E tests for the API and Unit tests for business logic, including mocking of external services.
    *   **Isolated Environment:** Fully containerized with Docker Compose for consistent development and deployment.
    *   **DB Migrations:** Safe database schema management using Alembic.
*   **User Features:**
    *   Seamless user registration via Telegram.
    *   CRUD operations for managing keywords.
    *   Personalized notifications for new vacancies.

---

## 🏁 Getting Started

### Prerequisites
*   Docker
*   Docker Compose

### Installation & Launch

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Varenik-vkusny/Vacancies-Collector.git
    cd Vacancies-Collector
    ```

2.  **Configure environment variables:**
    *   Copy `.env.example` to `.env` and `.env.db.example` to `.env.db`.
    *   Fill in the required values in `.env` (especially `BOT_TOKEN`).

3.  **Run the application:**
    ```bash
    docker-compose up --build
    ```

4.  **Apply migrations (in a separate terminal):**
    *   Wait for the containers to start up, then execute:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
5.  **Done!**
    *   The API is available at `http://localhost:8000`
    *   Interactive API documentation: `http://localhost:8000/docs`
    *   Your Telegram bot is now running and ready to use.

---

### Running Tests

A running Redis container is required to run the E2E tests.

1.  **Start Redis in detached mode:**
    ```bash
    docker-compose up -d redis
    ```
2.  **Install dependencies and run tests:**
    ```bash
    # (Activate your virtual environment)
    pip install -r requirements.txt
    pytest
    ```
3.  **Stop Redis after testing:**
    ```bash
    docker-compose down
    ```

---
### Stopping the Application
```bash
docker-compose down