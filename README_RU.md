[Read in English](README.md)
---

# ✒️ Vacancies Collector: Асинхронный сервис для мониторинга вакансий

[![Run Python Tests](https://github.com/Varenik-vkusny/Vacancies-Collector/actions/workflows/ci.yml/badge.svg)](https://github.com/Varenik-vkusny/Vacancies-Collector/actions/workflows/ci.yml)

Приложение представляет собой микросервисную систему для автоматического сбора и доставки вакансий пользователям в Telegram. Бэкенд реализован на FastAPI, асинхронный воркер обрабатывает задачи парсинга, а Telegram-бот выступает в роли клиентского интерфейса.

---

## 🚀 Архитектура и технологии

Этот проект демонстрирует полный цикл backend-разработки с применением современных асинхронных инструментов и практик DevOps.

*   **API на FastAPI:** Асинхронный REST API для управления пользователями и их подписками (ключевыми словами).
*   **Асинхронный Воркер:** Изолированный сервис, который получает задачи на парсинг через брокер сообщений и выполняет их в фоновом режиме, не блокируя API.
*   **Telegram-бот на Aiogram 3:** Клиентский интерфейс для взаимодействия с пользователями.
*   **Планировщик (APScheduler):** Регулярно ставит задачи на парсинг в очередь.
*   **База данных (PostgreSQL):** Хранит данные о пользователях и их ключевых словах для поиска.
*   **Брокер сообщений (RabbitMQ):** Обеспечивает надежную асинхронную коммуникацию между API и воркером.
*   **Кэш (Redis):** Используется для кэширования запросов к базе данных, что значительно снижает нагрузку и ускоряет ответы API.

### 🛠️ Стек

*   **Бэкенд:** Python 3.12, **FastAPI**, **SQLAlchemy 2.0 (async)**, Pydantic V2, Alembic
*   **Асинхронность:** **asyncio**, **RabbitMQ** (через aio-pika), **Redis**
*   **База данных:** **PostgreSQL**
*   **Инфраструктура и DevOps:** **Docker**, **Docker Compose**, CI/CD (GitHub Actions)
*   **Тестирование:** **Pytest**, pytest-mock, httpx

---

## ✨ Ключевые возможности

*   **Асинхронная архитектура:** Все компоненты (API, воркер, работа с БД и кэшем) полностью асинхронны, что обеспечивает высокую производительность.
*   **Оптимизация производительности:**
    *   **`selectinload` вместо `joinedload`:** Для эффективной загрузки связанных данных "один-ко-многим".
    *   **Кэширование на уровне API:** Снижение нагрузки на БД и ускорение `GET` запросов с помощью Redis.
    *   **Управление ресурсами через `lifespan`:** Корректное создание и закрытие пулов соединений.
*   **Надежность и качество кода:**
    *   **Полное покрытие тестами:** E2E-тесты для API и Unit-тесты для бизнес-логики (включая мокинг внешних сервисов).
    *   **Изолированное окружение:** Полная контейнеризация через Docker Compose для разработки и развертывания.
    *   **Миграции БД:** Безопасное управление схемой базы данных с помощью Alembic.
*   **Пользовательский функционал:**
    *   Бесшовная регистрация пользователей через Telegram.
    *   CRUD-операции для управления ключевыми словами.
    *   Персональные уведомления о новых вакансиях.

---

## 🏁 Запуск и Развертывание

### С помощью Docker Compose (для локальной разработки)

#### Требования
*   Docker
*   Docker Compose

#### Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Varenik-vkusny/Vacancies-Collector.git
    cd Vacancies-Collector
    ```

2.  **Настройте переменные окружения:**
    *   Скопируйте `.env.example` в `.env`, `.env.db.example` в `.env.db` и `.env.rabbit.example` в `.env.rabbit`.
    *   Заполните необходимые значения в `.env` (в первую очередь `BOT_TOKEN`).

3.  **Запустите приложение:**
    ```bash
    docker-compose up --build
    ```

4.  **Примените миграции (в отдельном терминале):**
    *   Дождитесь, пока контейнеры запустятся, и выполните:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
5.  **Готово!**
    *   API доступен по адресу `http://localhost:8000`
    *   Интерактивная документация API: `http://localhost:8000/docs`
    *   Ваш Telegram-бот и воркер запущены и готовы к работе.

#### Остановка приложения
```bash
docker-compose down
```

---

### 🚀 В Kubernetes (для продакшн-подобного окружения)

Этот раздел описывает, как развернуть приложение в локальном кластере Kubernetes, например, в Minikube.

#### Предварительные требования

1.  **kubectl**: Установленный и настроенный клиент командной строки Kubernetes.
2.  **Minikube**: Установленный локальный кластер Kubernetes.
3.  **Nginx Ingress Controller**: Установленный в Minikube. Включается командой:
    ```bash
    minikube addons enable ingress
    ```

#### 1. Настройка секретов

Все чувствительные данные должны быть созданы внутри кластера Kubernetes. Выполните следующую команду, чтобы создать секрет `app-secret`. **Замените значение `BOT_TOKEN` на свое.**

```bash
kubectl create secret generic app-secret --namespace=vacancies-collector \
  --from-literal=DB_USER='Varenik' \
  --from-literal=DB_PASSWORD='Vkusny' \
  --from-literal=RABBITMQ_USER='user' \
  --from-literal=RABBITMQ_PASSWORD='password' \
  --from-literal=BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN_HERE'
```

#### 2. Применение манифестов

1.  **Создайте Namespace**, в котором будут жить все компоненты приложения:
    ```bash
    kubectl apply -f k8s/00-namespace.yaml
    ```
    
2.  **Примените все остальные манифесты** одной командой. `migration-job` автоматически применит миграции.
    ```bash
    kubectl apply -f k8s/
    ```

#### 3. Проверка статуса развертывания
```bash
kubectl get all --namespace=vacancies-collector
```

Вы должны увидеть запущенные поды для `app`, `bot`, `worker`, `postgres`, `redis` и `rabbitmq`. Убедитесь, что джоба миграции `migration-job` имеет статус `Completed`.

#### 4. Доступ к приложению

Для доступа к API через Ingress в Minikube мы будем использовать прямой проброс порта к Ingress-контроллеру.

1.  **Получите прямой URL для доступа:**
    ```bash
    minikube service ingress-nginx-controller -n ingress-nginx --url
    ```
    Команда выведет URL, например `http://127.0.0.1:57135`. **Скопируйте его**.

2.  **Проверьте API с помощью `curl`:**
    Отправьте запрос, используя полученный URL и заголовок `-H "Host: vacancies.local"`, чтобы Ingress понял, куда направить трафик.
    ```bash
    # Замените http://127.0.0.1:XXXXX на URL из предыдущего шага
    curl -v -H "Host: vacancies.local" http://127.0.0.1:XXXXX/
    ```
    **Ожидаемый результат:** Ответ `HTTP/1.1 200 OK`.

#### 5. Проверка и отладка (если что-то не работает)

1.  **Проверьте Ingress Controller:**
    ```bash
    kubectl get pods -n ingress-nginx
    ```
    *   **Ожидаемый результат:** Pod `ingress-nginx-controller-...` должен быть в статусе `Running`.

2.  **Проверьте ваш Ingress ресурс:**
    ```bash
    kubectl describe ingress app-ingress -n vacancies-collector
    ```
    *   **Что искать:** `Host` должен быть `vacancies.local`, а в секции `Backends` должны быть IP-адреса подов вашего `app-service`.

#### 6. Очистка

Чтобы удалить все созданные в Kubernetes ресурсы, просто удалите `namespace`:
```bash
kubectl delete namespace vacancies-collector
```

---

### Запуск тестов

1.  **Запустите Redis и RabbitMQ в фоновом режиме:**
    ```bash
    docker-compose up -d redis rabbitmq
    ```
2.  **Установите зависимости и запустите тесты:**
    ```bash
    pip install -r requirements.txt
    pytest
    ```
3.  **Остановите сервисы после тестов:**
    ```bash
    docker-compose down
