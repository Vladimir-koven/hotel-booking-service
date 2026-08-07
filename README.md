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
- JWT аутентификации
- Redis кэширования

## Технологии
- Python 3.14, Django 5.2, DRF 3.17
- Poetry, Docker, PostgreSQL/SQLite
- Ruff, MyPy, Bandit, pre-commit
- Loguru, pytest
- JWT, Redis

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
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Запуск Redis (для кэширования)
Запуск Redis контейнера
docker run -d -p 6379:6379 --name redis-hotel redis:7
# Запуск созданного контейнера
docker start redis-hotel

### API Эндпоинты
Номера отелей
POST	/api/v1/rooms/create	    Создание номера
GET	    /api/v1/rooms/list	        Список номеров (сортировка: ?sort_by=price&order=asc)
DELETE	/api/v1/rooms/delete/<id>	Удаление номера

Бронирования
POST	/api/v1/bookings/create	            Создание брони
GET	    /api/v1/bookings/list?room_id=<id>	Список броней номера
DELETE	/api/v1/bookings/delete/<id>	    Удаление брони

Аутентификация
POST	/api/v1/auth/register/	    Регистрация пользователя
POST	/api/v1/auth/token/	        Получение JWT токена
POST	/api/v1/auth/token/refresh/	Обновление токена
POST	/api/v1/auth/logout/	    Выход (blacklist токена)
GET	    /api/v1/auth/profile/	    Профиль пользователя

### Структура проекта
Hotelroom_reservation/
├── api/                     # API слой
│   └── v1/                  # Версия API v1
├── apps/
│   ├── rooms/               # Номера (MVC)
│   │   ├── models.py        # Модель
│   │   ├── controllers.py   # Контроллер (бизнес-логика)
│   │   ├── views.py         # Представление
│   │   ├── serializers.py   # Сериализатор
│   │   └── urls.py          # Маршруты
│   └── bookings/            # Бронирования (MVC)
│       ├── models.py
│       ├── controllers.py
│       ├── views.py
│       ├── serializers.py
│       └── urls.py
├── config/                  # Настройки Django
├── tests/                   # Тесты (25 тестов)
├── utils/                   # Утилиты (logger, cache)
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
