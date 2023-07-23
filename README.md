<h1 align="center">Тестовое задание Junior/Middle backend разработчик на Fast API 
<a href='https://webtronics.ru/'>
(Webtronics)
</a>
</h1>


<h2 align="center">1. Структура репозитория:
<img width="64" height="64" src="https://img.icons8.com/external-justicon-lineal-color-justicon/64/external-tree-tree-justicon-lineal-color-justicon-6.png" alt="external-tree-tree-justicon-lineal-color-justicon-6"/>
</h2>

    .
    ├── backend   -> Приложение
    ├── README.md -> Описание (мы тут)
    ├── SpcialTest.postman_collection.json -> примеры запросов в Postman
    └── TASK.docx -> ТЗ

*SpcialTest.postman_collection.json - нужно поставить свои токены после регистрации пользователей

<h2 align="center">2. Запуск
<img width="100" height="100" src="https://img.icons8.com/stickers/100/construction-worker.png" alt="construction-worker"/>
</h2>

1. Клонируем репозиторий
   * git clone git@github.com:Alset-Nikolas/SocialNetworkingApplication.git
2. Переходим в папку src
   * cd ./backend/src
3. Создаем файл .env
   * Смотри пункт 3
4. Переходим в папку ./backend
   * cd ../
5. Собираем контейнер
   * docker-compose build
6. Запускаем контейнер
   * docker-compose up
7. Смотрим документацию на api
   * Ссылка:  http://0.0.0.0:6002/docs

<h2 align="center"> 3. Настройка .env 
<img width="50" height="50" src="https://img.icons8.com/ios-filled/50/40C057/settings.png" alt="settings"/>
</h2>

1. Мы находимся в backend/src
2. Создаем файл .env с содержанием:
   SOCIAL_NETWORK_CONFIG=prod
   SECRET_KEY="6729c5d49148d5e65928a52c68d67a86305057f54ba83109"
   JWT_SECRET_KEY="69065b8f76b5820d374fedd540c52573d88c076776affbec"
   JWT_REFRESH_SECRET_KEY="1abbc41f49302e0916fc12021174edb58dc809efea31da79"
3. Проверяем сущестовавание файла ./backend/src/.env



<p>*SOCIAL_NETWORK_CONFIG=prod - для запуска в проде</p>
<p>*SOCIAL_NETWORK_CONFIG=test - для запуска тестов</p>
<p>*SOCIAL_NETWORK_CONFIG=dev - для запуска в разработке</p>


<h2  align="center"> 4. Запуск тестов 
<img width="50" height="50" src="https://img.icons8.com/ios/50/40C057/test-passed--v1.png" alt="test-passed--v1"/>
</h2>

1. В .env нужно постаить SOCIAL_NETWORK_CONFIG=test
2. В папке ./backend/src можно запустить команду 
*  pytest .

