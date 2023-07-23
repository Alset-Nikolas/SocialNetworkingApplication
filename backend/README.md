<h1 align="center">Подробное описание репозитория</h1>


<h1>Структура:</h1>


    ├── docker-compose.yml     -  файл docker-compose для запусков контейнеров 
    ├── README.md              -  Техническое описание (мы тут)
    └── src                    -  Приложение
        ├── alembic.ini        -  Настройки alembic
        ├── app                -> Содержание приложения
        ├── Dockerfile         -  Dockerfile
        ├── __init__.py       
        ├── main.py            -  Точка входа
        ├── migration          -  Миграции
        ├── pytest.ini         -  Настройка тестов
        ├── requirements.txt   -  Зависимости
        └── tests              -  Тесты



<h1>Содержание приложения</h1>

    app
    ├── api                   -> Роуты приложения
    ├── core                  -> Глобальные настройки
    ├── database.py           - Запуск БД
    ├── factory.py            - Запуск через фабрику
    ├── __init__.py
    ├── init_utils.py         - Утилиты запуска
    ├── orm                   -> БД
    ├── schemas               -> Схемы запросов и ответов
    └── services              -> Логика приложения разделена на сервисы 

<h2>Детали приложения</h2>

    app
    ├── api                   
    │   ├── __init__.py
    │   └── resources        -> Ресуры    
    │       ├── grade_post        - Оценка поста
    │       ├── __init__.py
    │       ├── posts             - CRUD поста
    │       └── users             - Регистрация/авторизация итд пользователя
    ├── core
    │   ├── config.py        - Конфигурация приложения 
    │   ├── __init__.py
    │   └── settings.py      - Настрйоки конфигурации
    ├── database.py
    ├── factory.py
    ├── __init__.py
    ├── init_utils.py
    ├── orm
    │   ├── grade_post.py     - Модель оценки поста
    │   ├── __init__.py  
    │   ├── post.py           - Модель поста
    │   └── user.py           - Модель пользователя
    ├── schemas
    │   ├── grade.py          - Схема запросов к оценке поста
    │   ├── __init__.py
    │   ├── jwt.py            - --//-- к токенам
    │   ├── post.py           - --//-- к постам
    │   └── user.py           - --//-- к пользователям
    └── services
        ├── grade.py          - Сервис работы с оценками
        ├── __init__.py
        ├── jwt.py            - --//-- с токенам
        ├── password.py       - --//-- с паролем
        ├── post.py           - --//-- с постам
        └── user.py           - --//-- с пользователям
