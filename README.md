# ✒️ Vacancies Collector

An application with a FastAPI backend and a user-friendly Telegram bot client.
---

## 🚀 About The Project

This project is a tool for parsing job vacancies from two platforms (hh.ru and kwork.ru) and features a scheduling system to send notifications about the results. It consists of five key parts:

*   **REST API on FastAPI:** A backend that handles processing, storage, and delivery of vacancy data, and provides the ability to save parsed jobs.
*   **Telegram Bot on aiogram 3:** An interactive client that allows users to add, modify, view, and delete keywords for which they want to receive relevant job openings.
*   **Scheduler:** A scheduler that, at set intervals, triggers notifications about new vacancies on the job platforms and determines which vacancies to send to which users.
*   **Scripts (Scrapers):** Scrapers responsible for collecting data from the job platforms.
*   **Services (Notification Sender):** A service that automatically sends a message to the user containing details about a new vacancy.

This project demonstrates a comprehensive approach to backend development: from data collection and storage to API creation, process automation, and user interaction.

---

## 🛠️ Tech Stack

*   **Backend:**
    *   ![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)
    *   ![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-009688?style=for-the-badge&logo=fastapi)
    *   ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-DB4437?style=for-the-badge&logo=sqlalchemy)
    *   ![Pydantic](https://img.shields.io/badge/Pydantic-v2-E96F00?style=for-the-badge)
*   **Telegram Bot:**
    *   ![aiogram](https://img.shields.io/badge/aiogram-3.x-26A5E4?style=for-the-badge)
    *   ![httpx](https://img.shields.io/badge/httpx-async-000000?style=for-the-badge)
*   **Database & Migrations:**
    *   ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)
    *   ![Alembic](https://img.shields.io/badge/Alembic-migrations-4E2A84?style=for-the-badge)
*   **Parsing & Scheduling:**
    *   ![APScheduler](https://img.shields.io/badge/APScheduler-tasks-5C65F1?style=for-the-badge)
    *   ![Selenium](https://img.shields.io/badge/Selenium-automation-43B02A?style=for-the-badge&logo=selenium)
    *   ![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-parsing-C41424?style=for-the-badge)
*   **Tooling, Containerization & Testing:**
    *   ![Docker](https://img.shields.io/badge/Docker-compose-2496ED?style=for-the-badge&logo=docker)
    *   ![Pytest](https://img.shields.io/badge/Pytest-testing-0A9EDC?style=for-the-badge&logo=pytest)
    *   `Uvicorn` & `python-dotenv`

---

## ✨ Key Features

*   **Authorization:**
    *   👤 Seamless registration and identification of users via their Telegram ID.
*   **Automation & Parsing:**
    *   ⚙️ **Automated Parsing:** Scripts for collecting data from multiple web resources.
    *   ⏰ **Scheduled Tasks:** Regular execution of parsing and notification tasks using `APScheduler`.
    *   🔔 **Personalized Notifications:** Users receive only the vacancies that match their specified keywords in Telegram.
*   **Data Management:**
    *   ✍️ Full CRUD operations for keywords.
    *   🤖 Saving and associating keywords with specific users.
*   **Telegram Bot as a Client:**
    *   🔑 Easy registration for receiving notifications.
    *   💬 Convenient navigation using a persistent Reply Keyboard.
    *   🧠 Use of a Finite State Machine (FSM) to implement step-by-step dialogues.
*   **Code Quality & Infrastructure:**
    *   📄 **API Documentation:** Automatically generated interactive documentation (Swagger UI, ReDoc).
    *   🐋 **Full Containerization:** The application and PostgreSQL database are fully configured to run with a single command via Docker Compose.
    *   🧪 **Testing:** Key API logic is covered by integration tests using Pytest.
    *   🔄 **DB Migrations:** Database schema versioning is managed with Alembic.

---

## 🏁 Getting Started (via Docker)

This is the recommended and easiest way to run the project.

### Prerequisites
*   [Docker](https://www.docker.com/products/docker-desktop/)
*   A Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Installation and Launch

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Varenik-vkusny/Vacancies-Collector.git
    cd Vacancies-Collector
    ```

2.  **Create the `.env` file:**
    *   Create a `.env` file in the root directory based on the `.env.example` template.
    *   Paste your bot token from @BotFather into the `BOT_TOKEN` variable.

3.  **Build and run the application:**
    *   Build and start the application with the following command:
    ```bash
    docker-compose up --build -d
    ```

4.  **Apply the migrations:**
    *   Apply the Alembic migrations with the following command:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
5.  **Done! Your application is up and running!**

*   The API is available at `http://localhost:8000`.
*   The documentation is available at `http://localhost:8000/docs`.
*   Your bot is now running!

---
### Stopping the Application
   *   You can stop the application with the command:
    ```bash
    docker-compose down
    ```
