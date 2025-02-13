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

Для запуска приложения - запустить app.py (сделать детальную инструкцию)

### Структура проекта

```
project/
├── logs/                   # Файлы с логами
├── src/
│   ├── dtos/               # Data Transfer Objects
│   ├── handlers/           # Обработчики запросов
│   │   ├── __init__.py
│   │   ├── base_handler.py
│   │   ├── index_handler.py 
│   │   ├── static_handler
│   │   ├── etc
│   ├── migrations/         # Миграции alembic
│   │   ├── versions/       # Версии миграций
│   │   ├── env.py          # Конфигурации alembic
│   │   ├── script.py.mako  # Шаблон для скрипов миграций
│   ├── models/             # Модели ORM
│   │   ├── match_model.py  # Модель матча
│   │   ├── player_model.py # Модель игрока
│   ├── services/           # Сервисы с логикой
│   ├── static/             # Статика (CSS, изображения)
│   │   ├── style.css
│   │   ├── images/         # Изображения для сайта
│   │   │   ├── player_first.png
│   │   │   ├── etc
│   ├── templates/          # HTML-шаблоны 
│   │   ├── index.html
│   │   ├── new_match.html
│   │   ├── match_score
│   │   ├── completed_matches
│   ├── tests/              # Юнит тесты
│   ├── validators/         # Валидатор данных
│   ├── __init__.py
│   ├── config.py           # Конфигурация проекта
│   ├── database.py         # Конфигурация базы данных
│   ├── logging_config.py   # Настройка логов
│   ├── router.py           # Маршрутизатор
│   ├── server.py           # Запуск сервера
├── .env                    # Настройки подключения к БД
├── alembic.ini             # Параметры конфигурации
├── README                  # О проекте
├── requirements            # Зависимости
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
- pytest. Юнит тестирование
- Docker

### Автор

Дмитрий Валюженич
Mitya0777@gmail.com