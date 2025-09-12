[Read in Russian](README.ru.md)
---

# ✒️ Vacancies Collector: An Asynchronous Service for Monitoring Job Postings

[![Run Python Tests](https://github.com/Varenik-vkusny/Vacancies-Collector/actions/workflows/ci.yml/badge.svg)](https://github.com/Varenik-vkusny/Vacancies-Collector/actions/workflows/ci.yml)

This application is a microservice-based system for automatically collecting and delivering job vacancies to users via Telegram. The backend is implemented with FastAPI, an asynchronous worker handles parsing tasks, and a Telegram bot serves as the client interface.

---

## 🚀 Architecture and Technologies

This project demonstrates a full-cycle backend development process using modern asynchronous tools and DevOps practices.

*   **API with FastAPI:** An asynchronous REST API for managing users and their subscriptions (keywords).
*   **Asynchronous Worker:** An isolated service that receives parsing tasks through a message broker and executes them in the background without blocking the API.
*   **Telegram Bot with Aiogram 3:** The client interface for user interaction.
*   **Scheduler (APScheduler):** Periodically enqueues parsing tasks.
*   **Database (PostgreSQL):** Stores data about users and their search keywords.
*   **Message Broker (RabbitMQ):** Ensures reliable asynchronous communication between the API and the worker.
*   **Cache (Redis):** Used for caching database queries, significantly reducing load and speeding up API responses.

### 🛠️ Tech Stack

*   **Backend:** Python 3.12, **FastAPI**, **SQLAlchemy 2.0 (async)**, Pydantic V2, Alembic
*   **Asynchronicity:** **asyncio**, **RabbitMQ** (via aio-pika), **Redis**
*   **Database:** **PostgreSQL**
*   **Infrastructure & DevOps:** **Docker**, **Docker Compose**, CI/CD (GitHub Actions)
*   **Testing:** **Pytest**, pytest-mock, httpx

---

## ✨ Key Features

*   **Asynchronous Architecture:** All components (API, worker, DB and cache operations) are fully asynchronous, ensuring high performance.
*   **Performance Optimization:**
    *   **`selectinload` over `joinedload`:** For efficient loading of one-to-many related data.
    *   **API-level Caching:** Reducing DB load and speeding up `GET` requests with Redis.
    *   **Resource Management via `lifespan`:** Proper creation and closing of connection pools.
*   **Reliability and Code Quality:**
    *   **Full Test Coverage:** E2E tests for the API and unit tests for business logic (including mocking external services).
    *   **Isolated Environment:** Full containerization via Docker Compose for development and deployment.
    *   **DB Migrations:** Safe database schema management with Alembic.
*   **User Functionality:**
    *   Seamless user registration via Telegram.
    *   CRUD operations for managing keywords.
    *   Personalized notifications about new job vacancies.

---

## 🏁 Launch and Deployment

### Using Docker Compose (for local development)

#### Prerequisites
*   Docker
*   Docker Compose

#### Installation and Startup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Varenik-vkusny/Vacancies-Collector.git
    cd Vacancies-Collector
    ```

2.  **Set up environment variables:**
    *   Copy `.env.example` to `.env`, `.env.db.example` to `.env.db`, and `.env.rabbit.example` to `.env.rabbit`.
    *   Fill in the required values in `.env` (especially `BOT_TOKEN`).

3.  **Run the application:**
    ```bash
    docker-compose up --build
    ```

4.  **Apply migrations (in a separate terminal):**
    *   Wait for the containers to start, then run:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
5.  **Done!**
    *   The API is available at `http://localhost:8000`
    *   Interactive API documentation: `http://localhost:8000/docs`
    *   Your Telegram bot and worker are running and ready to go.

#### Stopping the Application
```bash
docker-compose down
```

---

### 🚀 In Kubernetes (for a production-like environment)

This section describes how to deploy the application in a local Kubernetes cluster, such as Minikube.

#### Prerequisites

1.  **kubectl**: An installed and configured Kubernetes command-line client.
2.  **Minikube**: An installed local Kubernetes cluster.
3.  **Nginx Ingress Controller**: Installed in Minikube. It can be enabled with the command:
    ```bash
    minikube addons enable ingress
    ```

#### 1. Secret Configuration

All sensitive data must be created within the Kubernetes cluster. Run the following command to create the `app-secret`. **Replace the `BOT_TOKEN` value with your own.**

```bash
kubectl create secret generic app-secret --namespace=vacancies-collector \
  --from-literal=DB_USER='Varenik' \
  --from-literal=DB_PASSWORD='Vkusny' \
  --from-literal=RABBITMQ_USER='user' \
  --from-literal=RABBITMQ_PASSWORD='password' \
  --from-literal=BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN_HERE'
```

#### 2. Applying the Manifests

1.  **Create the Namespace where all application components will reside:**
    ```bash
    kubectl apply -f k8s/00-namespace.yaml
    ```
    
2.  **Apply all other manifests** with a single command. The `migration-job` will automatically apply migrations.
    ```bash
    kubectl apply -f k8s/
    ```

#### 3. Checking Deployment Status
```bash
kubectl get all --namespace=vacancies-collector
```
You should see running pods for `app`, `bot`, `worker`, `postgres`, `redis`, and `rabbitmq`. Ensure that the `migration-job` has a `Completed` status.

#### 4. Accessing the Application

To access the API via Ingress in Minikube, we will use a direct port-forward to the Ingress controller.

1.  **Get the direct access URL:**
    ```bash
    minikube service ingress-nginx-controller -n ingress-nginx --url
    ```
    The command will output a URL, for example, `http://127.0.0.1:57135`. **Copy it**.

2.  **Test the API using `curl`:**
    Send a request using the obtained URL and the `-H "Host: vacancies.local"` header, so Ingress knows where to route the traffic.
    ```bash
    # Replace http://127.0.0.1:XXXXX with the URL from the previous step
    curl -v -H "Host: vacancies.local" http://127.0.0.1:XXXXX/
    ```
    **Expected result:** An `HTTP/1.1 200 OK` response.

#### 5. Verification and Debugging (if something goes wrong)

1.  **Check the Ingress Controller:**
    ```bash
    kubectl get pods -n ingress-nginx
    ```
    *   **Expected result:** The `ingress-nginx-controller-...` pod should be in the `Running` status.

2.  **Check your Ingress resource:**
    ```bash
    kubectl describe ingress app-ingress -n vacancies-collector
    ```
    *   **What to look for:** The `Host` should be `vacancies.local`, and the `Backends` section should contain the IP addresses of your `app-service` pods.

#### 6. Cleanup

To delete all the Kubernetes resources created, simply delete the namespace:
```bash
kubectl delete namespace vacancies-collector
```

---

### Running Tests

1.  **Start Redis and RabbitMQ in the background:**
    ```bash
    docker-compose up -d redis rabbitmq
    ```
2.  **Install dependencies and run tests:**
    ```bash
    pip install -r requirements.txt
    pytest
    ```
3.  **Stop the services after testing:**
    ```bash
    docker-compose down
