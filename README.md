# 🎟️ Event Booking API (Платформа мероприятий и билетов)

Этот проект представляет собой RESTful API, который позволяет пользователям бронировать билеты на мероприятия (концерты, конференции, спортивные игры),а администраторам - управлять мероприятиями и билетами.

## 🚀Основные возможности
Аутентификация и авторизация защищены JWT (JSON Web Token).

**Управление событиями:** Фильтрация и поиск по категориям, времени, имени и адресу (Django Filter, Search).

**Покупка безопасного билета:** Проверка и уменьшение количества мест выполняется через transaction.atomic () (для обеспечения безопасности на валюте).

**Автоматический QR-код:** При покупке билета автоматически генерируется QR-код с данными билета.

**Список ожидания (Waitlist):** В случае распродажи билетов пользователи могут присоединиться к списку ожидания и будут уведомлены о возврате билета.

**Admin Dashboard:** API для администраторов (Общий доход, наиболее продаваемое мероприятие, общее количество проданных билетов).

**Документация API:** Автоматизированная документация через Swagger и Redoc

## 🛠️ Технологии Stack
**Язык:** Python 3.x

**Фреймворк:** Django 4.x / 5.x, Django REST Framework (DRF)

**База данных:** SQLite (Raw)

**Аутентификация:** SimpleJWT

**Изображение и QR Код:** Pillow, qrcode

**Документирование:** drf-spectacular (Swagger UI)


## ⚙️Установка проекта (Installation)


**1.Клонирование репозитории:**
```
git clone https://github.com/SizinUsername/event-booking-api.git
cd event-booking-api
```

**2. Создание и запуск виртуальной среды (Virtual Environment):**
```
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

**3. Установка необходимых библиотек:**
```
pip install -r requirements.txt
```

**4. Создание базы данных (Миграция):**
```
python manage.py makemigrations
python manage.py migrate
```


**5. Создание аккаунта администратора (Superuser):**
```
python manage.py createsuperuser
```

**6. Запуск сервера:**
```
python manage.py runserver
```

#### 👤Author:
#### Musabek. GitHub: [Musabek03](https://github.com/Musabek03)


