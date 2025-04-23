# Проект “Табло теннисного матча”

## Ссылка с информацией

https://zhukovsd.github.io/python-backend-learning-course/projects/tennis-scoreboard/

### Описание

Веб-приложение, реализующее табло счёта теннисного матча

### Мотивация проекта

- Создать клиент-серверное приложение с веб-интерфейсом
- Получить практический опыт работы с ORM SQLAlchemy и Alembic
- Верстка веб-интерфейса без сторонних CSS-фреймворков
- Использовать MVC(S) в проектировании архитектуры

### Запуск приложения
1. Склонируйте репозиторий
```
git clone https://github.com/Dmitry-DVal/TennisScoreBoard
```
2. Установите MySQL и создайте базу данных
```
CREATE DATABASE name_db;
```
3. Настройте виртуальное окружение
```
# Windows
python -m venv venv
venv\Scripts\activate

# MacOS/Linux
python3 -m venv venv
source venv/bin/activate
```
4. Установите зависимости
```
pip install -r requirements.txt
```
5. Создайте папку logs/. В ней будут храниться логи.
(Папка должна быть на одном уровне с src)

6. Настройте подключение к БД
- Создайте файл ".env"
(Файл должен быть на одном уровне с src)
```
# содержание .env
DB_DRIVER = mysql+pymysql
DB_USER = your_username   # Имя пользователя MySQL
DB_PASSWORD = your_password   # Пароль MySQL
DB_HOST = localhost
DB_PORT = 3306
DB_NAME = name_bd  # Имя базы данных
```
7. Примените миграции базы данных
```
alembic upgrade head
```
8. Запустите сервер
```
# Windows
cd src
python -m tennis_app.server

# MacOS/Linux
python3 -m tennis_app.server

```
9. Теперь сервер доступен по адресу: http://127.0.0.1:8000

[page_overview.pdf](https://github.com/user-attachments/files/19160448/page_overview.pdf)

### Структура проекта

```
project/
├── logs/                          # Файлы с логами
├── src/
│   ├── __init__.py
│   ├── tennis_app/               
│	│   ├── core/                  
│	│   │   ├── __init__.py
│	│   │   ├── match_engine.py    # Модель подсчета очков
│	│   │   ├── match_state.py     # Работа с состоянием матча
│	│   ├── dao/                   # Data Access Objects
│	│   │   ├── __init__.py
│	│   │   ├── match_dao.py
│	│   │   ├── player_dao.py
│	│   ├── dtos/                  # Data Transfer Objects
│	│   │   ├── __init__.py
│	│   │   ├── player_dto.py
│	│   │   ├── point_winner_dto.py
│	│   ├── handlers/              # Обработчики запросов
│	│   │   ├── __init__.py
│	│   │   ├── base_handler.py
│	│   │   ├── index_handler.py 
│	│   │   ├── static_handler
│	│   │   ├── etc
│	│   ├── migrations/            # Миграции alembic
│	│   │   ├── versions/          # Версии миграций
│	│   │   ├── env.py             # Конфигурации alembic
│	│   │   ├── script.py.mako     # Шаблон для скрипов миграций
│	│   ├── models/                # Модели ORM
│	│   │   ├── __init__.py
│	│   │   ├── match_model.py     # Модель матча
│	│   │   ├── player_model.py    # Модель игрока
│	│   ├── services/              # Сервисы с логикой
│	│   │   ├── __init__.py
│	│   │   ├── match_service.py  
│	│   │   ├── player_service.py  
│	│   ├── static/                # Статика (CSS, изображения)
│	│   │   ├── style.css
│	│   │   ├── images/            # Изображения для сайта
│	│   │   │   ├── player_first.png
│	│   │   │   ├── etc
│	│   ├── templates/             # HTML-шаблоны 
│	│   │   ├── index.html
│	│   │   ├── new_match.html
│	│   │   ├── error.html
│	│   │   ├── etc
│	│   ├── __init__.py
│	│   ├── config.py             # Конфигурация проекта
│	│   ├── database.py           # Конфигурация базы данных
│	│   ├── exceptions.py         # Кастомные исключения приложения
│	│   ├── logging_config.py     # Настройка логов
│	│   ├── router.py             # Маршрутизатор
│	│   ├── server.py             # Запуск сервера
├── tests/                    # Юнит тесты
│   ├── __init__.py
│   ├── test_scoring_service.py
├── .env                      # Настройки подключения к БД
├── alembic.ini               # Параметры конфигурации alembic
├── mypy.ini                  # Параметры конфигурации mypy
├── pytest.ini                # Параметры конфигурации pytest
├── README                    # О проекте
├── requirements              # Зависимости для проды
├── requirements_dev          # Зависимости для разработки


```

### Функционал приложения

- Создание матча
- Отслеживание счета игры
- Поиск по завершенным матчам

### Используемые технологии:

- Python - коллекции, ООП
- Паттерн MVC(S)
- pip
- waitress
- GET и POST запросы, формы
- Jinja2
- MySQL
- SQLAlchemy, alembic
- HTML/CSS, блочная вёрстка
- pytest
- Pydantic

### Автор

Дмитрий Валюженич
Mitya0777@gmail.com
