# Проект “Табло теннисного матча”

## Ссылка с информацией

https://zhukovsd.github.io/python-backend-learning-course/projects/tennis-scoreboard/

### Описание

Веб-приложение, реализующее табло счёта теннисного матча


### Мотивация проекта

- Создать клиент-серверное приложение с веб-интерфейсом
- Получить практический опыт работы с ORM SQLAlchemy и инструментом миграций Alembic
- Сверстать простой веб-интерфейс без сторонних библиотек
- Закрпеление знакомства с архитектурным паттерном MVC(S)

Для запуска приложения - запустить app.py (сделать детальную инструкцию)

### Структура проекта
```
project/
├── logs/ # Файлы с логами
├── requirements # Зависимости
├── README # О проекте
│
├── src/
│   ├── handlers/           # Обработчики запросов
│   │   ├── __init__.py
│   │   ├── base_handler.py
│   │   ├── index_handler.py 
│   │   ├── etc
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
│   ├── __init__.py
│   ├── config.py           # Конфигурация проекта
│   ├── logging_config.py   # Настройка логов
│   ├── router.py           # Маршрутизатор
│   ├── server.py           # Запуск сервера
│   ├── static_handler.py   # Раздает статические файлы
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
- SQLAlchemy
- HTML/CSS, блочная вёрстка
- Юнит тестирование
- Docker


- Backend - Wsgiref.simple_server
- Templates - Jinja2
- Базы данных - Postgres, SQLAlchemy
- Frontend - HTML/CSS, блочная вёрстка 
- Тесты - Unittest
- Паттерн MVC(S)

### Автор

Дмитрий Валюженич
Mitya0777@gmail.com