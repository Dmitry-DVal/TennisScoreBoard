# Проект “Табло теннисного матча”

## Ссылка с информацией

https://zhukovsd.github.io/python-backend-learning-course/projects/tennis-scoreboard/

### Описание

Веб-приложение, реализующее табло счёта теннисного матча

### Мотивация проекта

- Создать клиент-серверное приложение с веб-интерфейсом
- Получить практический опыт работы с ORM SQLAlchemy и инструментом миграций Alembic
- Сверстать простой веб-интерфейс без сторонних библиотек
- Закрепление знакомства с архитектурным паттерном MVC(S)

Для запуска приложения - запустить server.py (сделать детальную инструкцию)

### Структура проекта

```
project/
├── logs/                      # Файлы с логами
├── src/
│   ├── dtos/                  # Data Transfer Objects
│   │   ├── __init__.py
│   │   ├── player_dto.py
│   │   ├── point_winner_dto.py
│   ├── handlers/              # Обработчики запросов
│   │   ├── __init__.py
│   │   ├── base_handler.py
│   │   ├── index_handler.py 
│   │   ├── static_handler
│   │   ├── etc
│   ├── migrations/            # Миграции alembic
│   │   ├── versions/          # Версии миграций
│   │   ├── env.py             # Конфигурации alembic
│   │   ├── script.py.mako     # Шаблон для скрипов миграций
│   ├── models/                # Модели ORM
│   │   ├── __init__.py
│   │   ├── match_model.py     # Модель матча
│   │   ├── player_model.py    # Модель игрока
│   ├── services/              # Сервисы с логикой
│   │   ├── __init__.py
│   │   ├── match_service.py   # Сервис матча
│   │   ├── player_service.py  # Сервис игрока
│   │   ├── scoring_service.py # Модель подсчета очков
│   │   ├── match_state.py     # Работа с состоянием матча
│   ├── static/                # Статика (CSS, изображения)
│   │   ├── style.css
│   │   ├── images/            # Изображения для сайта
│   │   │   ├── player_first.png
│   │   │   ├── etc
│   ├── templates/             # HTML-шаблоны 
│   │   ├── index.html
│   │   ├── new_match.html
│   │   ├── error.html
│   │   ├── etc
│   ├── __init__.py
│   ├── config.py             # Конфигурация проекта
│   ├── database.py           # Конфигурация базы данных
│   ├── logging_config.py     # Настройка логов
│   ├── router.py             # Маршрутизатор
│   ├── server.py             # Запуск сервера
├── tests/                    # Юнит тесты
│   ├── __init__.py
│   ├── test_scoring_service.py
├── .env                      # Настройки подключения к БД
├── __init__.py
├── alembic.ini               # Параметры конфигурации alembic
├── pytest.ini                # Параметры конфигурации pytest
├── README                    # О проекте
├── requirements              # Зависимости

```

### Функционал приложения

- Создание матча
- Отслеживание счета игры
- Поиск по завершенным матчам

### Используемые технологии: (Внести уточнения)

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