# Hotel Booking Service
REST API сервис для управления номерами отелей и бронированиями.


## Ссылки для работы
API: http://localhost:8000/api/v1/
Админка: http://localhost:8000/admin/


## Описание
Сервис предоставляет API для:
- Управления номерами отелей (создание, удаление, список с сортировкой)
- Управления бронированиями (создание, удаление, список по номеру)
- Проверки пересечения дат при бронировании
- Валидации данных на всех уровнях
- JWT аутентификации (регистрация, логин, refresh, logout)
- Redis кэширования
- Docker контейнеризации


## Технологии
- Python 3.12, Django 5.2, DRF 3.17
- Poetry 2.4, Docker, PostgreSQL 17/SQLite
- Ruff 0.16, MyPy 2.3, Bandit 1.9, pre-commit
- Loguru 0.7, pytest 9.1
- JWT (SimpleJWT 5.5), Redis 7
- ASGI сервер (Uvicorn 0.30)


##  Установка и запуск
### Локальный запуск

# 1. Клонирование репозитория
git clone git@github.com:Vladimir-koven/Hotelroom_reservation-Django-.git
cd hotel-booking-service
# 2. Установка зависимостей
poetry install --with dev
# 3. Активация виртуального окружения
poetry shell
# 4. Применение миграций
python manage.py migrate
# 5. Создание суперпользователя
python manage.py createsuperuser
# 6. Запуск сервера
python manage.py runserver


### Docker
# 1. Запуск всех сервисов
docker-compose up --build
# 2. Применение миграций
docker-compose exec web python manage.py migrate
# 3. Создание суперпользователя
docker-compose exec web python manage.py createsuperuser
# 4. Проверка API
curl http://localhost:8000/api/v1/rooms/list


# Запуск Redis (для кэширования)
Запуск Redis контейнера
docker run -d -p 6379:6379 --name redis-hotel redis:7
# Запуск созданного контейнера
docker start redis-hotel


### API Эндпоинты
Аутентификация
Метод	Эндпоинт	        Описание
POST	/auth/register/	    Регистрация пользователя
POST	/auth/token/	    Получение JWT токена
POST	/auth/token/refresh/	Обновление токена
POST	/auth/logout/	    Выход
GET	    /auth/profile/	    Профиль пользователя 🔒

Номера отелей
Метод	Эндпоинт	                            Описание
POST	/rooms/create	                        Создание номера 🔒
DELETE	/rooms/delete/<id>	                    Удаление номера 🔒
GET	    /rooms/list	                            Список номеров
GET	    /rooms/list?sort_by=price&order=asc	    Сортировка по цене
GET	    /rooms/list?sort_by=created_at&order=desc	Сортировка по дате

Бронирования
Метод	Эндпоинт	                Описание
POST	/bookings/create	        Создание брони 🔒
DELETE	/bookings/delete/<id>	    Удаление брони 🔒
GET	    /bookings/list?room_id=<id>	Список броней

🔒 - Требуется JWT аутентификация (Bearer токен)


Примеры запросов
# 1. Регистрация пользователя
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "Test123!",
    "password2": "Test123!",
    "email": "test@example.com"
  }'
# 2. Получение JWT токена
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type": application/json" \
  -d '{"username": "test", "password": "Test123!"}'
# Сохраните access_token из ответа
ACCESS_TOKEN="your_access_token_here"

# 3. Создание номера (с токеном)
curl -X POST http://localhost:8000/api/v1/rooms/create \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": "Люкс с видом на море", "price_per_night": "299.99"}'
# 4. Список номеров (публичный)
curl http://localhost:8000/api/v1/rooms/list
# 5. Список с сортировкой по цене
curl "http://localhost:8000/api/v1/rooms/list?sort_by=price_per_night&order=asc"
# 6. Создание брони (с токеном)
curl -X POST http://localhost:8000/api/v1/bookings/create \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"room_id": 1, "date_start": "2026-08-10", "date_end": "2026-08-15"}'
# 7. Список броней
curl "http://localhost:8000/api/v1/bookings/list?room_id=1"
# 8. Удаление брони (с токеном)
curl -X DELETE http://localhost:8000/api/v1/bookings/delete/1 \
  -H "Authorization: Bearer $ACCESS_TOKEN"
# 9. Удаление номера (с токеном)
curl -X DELETE http://localhost:8000/api/v1/rooms/delete/1 \
  -H "Authorization: Bearer $ACCESS_TOKEN"


### Структура проекта
hotel-booking-service/
├── api/                    # API слой
│   └── v1/                 # Версия API v1
├── apps/                   # Django приложения
│   ├── rooms/              # Номера (MVC)
│   │   ├── models.py       # Модель
│   │   ├── controllers.py  # Контроллер (бизнес-логика)
│   │   ├── views.py        # Представление
│   │   ├── serializers.py  # Сериализатор
│   │   └── urls.py         # Маршруты
│   ├── bookings/           # Бронирования (MVC)
│   └── users/              # Пользователи (JWT)
├── config/                 # Django конфигурация
├── tests/                  # Тесты (32 теста)
├── utils/                  # Утилиты (logger, cache, exceptions)
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md


### Команды разработки

# Установка зависимостей
make install
# Проверка кода (Ruff)
make lint
# Форматирование кода (Ruff)
make format
# Проверка типов (MyPy)
make type
# Проверка безопасности (Bandit)
make security
# Запуск тестов
make test
# Все проверки вместе
make check
