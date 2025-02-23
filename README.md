

Система управления заказами в кафе, разработанная на Django 5+ с использованием Django REST Framework (DRF).

Функциональность

_ Управление блюдами (CRUD)
_ Управление заказами (создание, обновление, удаление)
_ Подсчет общей суммы оплаченных заказов
_ Фильтрация заказов по статусу
_ API с документацией Swagger и Redoc
_ Веб-интерфейс для администраторов и сотрудников кафе

Требования

- Python 3.10+
- Django 5+
- Django REST Framework
- PostgreSQL (или SQLite для тестирования)

Установка и развертывание

1️) Клонирование репозитория

git clone git@github.com:RedC0mrade/em_test_django.git

2️) Создание виртуального окружения

python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate    # Для Windows

3️) Установка зависимостей

pip install -r requirements.txt

4️) Настройка базы данных

Настроить DATABASES в settings.py для использования SQLite.

5️) Применение миграций

python manage.py migrate

6️) Создание суперпользователя

python manage.py createsuperuser

7️) Запуск сервера разработки

python manage.py runserver

8️) Доступ к проекту

Веб-интерфейс: http://127.0.0.1:8000/ Панель администратора: http://127.0.0.1:8000/admin/ API: http://127.0.0.1:8000/api/ Документация API:

Redoc: http://127.0.0.1:8000/redoc/

Тестирование

pytest
