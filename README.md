<div id="header" align="center">
  <h1>Проект Collect-Together</h1>
</div>

## Что это за проект, какую задачу он решает, в чём его польза:
> [!NOTE]
> Collect-Together собирает пожертвования на различные целевые проекты

## Как развернуть проект на локальной машине.
> [!IMPORTANT]
> * 1 (Клонируем проект) : [ git@github.com:OsKaLis/collect_together.git ]
> * 2 (Переходим в директорию проекта) :cd collect_together/
> * 3 (Устанавливаем виртуальное окружение) :python -m venv venv
> * 4 (Запускаем виртуальное окружение из папки "collect_together") :source venv/Scripts/activate
> * 5 (Установка всех нужных библиотек) :pip install -r requirements.txt
> * 6 (Создаём фаил '.env')
>   ```
>   APP_TITLE=Приложение собирает пожертвования на различные целевые проекты.
>   DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
>   APP_AUTHOR=ЮрийЮЮ
>   AUTHOR_PASS=[password]
>   DEADLINE_DATE=[05.02.2024]
>   DESCRIPTION=[ОПИСАНИЕ]
>   SECRET=[password]
>   FIRST_SUPERUSER_EMAIL=[MAIL-ADMINA]
>   FIRST_SUPERUSER_PASSWORD=[PASSWORD-ADMINA]
>   EMAIL=[ Свой @gmail.com]
> * 7 (Создаём проект в Google Cloud Platform)
> * 8 (Дополнить .env параметры можно Получаем JSON-файл с ключом доступа к сервисному аккаунту)
>   ```
>   TYPE=service_account
>   PROJECT_ID=[fluid-dreamer-3.3.1.]
>   PRIVATE_KEY_ID=[47169bcc4c4......8a331d4b769eb1ff]
>   PRIVATE_KEY=[-----BEGIN PRIVATE KEY-----\n....bTxwcv\n-----END PRIVATE KEY-----\n]
>   CLIENT_EMAIL=[test-praktikum@fluid-dreamer-3.3.1..iam.gserviceaccount.com]
>   CLIENT_ID=[1..10...669..782...07]
>   AUTH_URI=https://accounts.google.com/o/oauth2/auth
>   TOKEN_URI=https://oauth2.googleapis.com/token
>   AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
>   CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/pt-project%40operating-tiger-415107.iam.gserviceaccount.com
>   UNIVERSE_DOMAIN=googleapis.com
> * 9 (Запускаем) :uvicorn app.main:app --reload

## Cтек технологий:
<img src="https://img.shields.io/badge/Python_-3.9.10-Green"> <img src="https://img.shields.io/badge/FastAPI_-0.78.0-blue">
<img src="https://img.shields.io/badge/SQLAlchemy_-1.4.36-yellow"> <img src="https://img.shields.io/badge/Alembic_-1.7.7-red">

## Пример работы Collect-Together :
<div id="header" align="center">
  <h2>Возвращает список всех проектов</h2>
</div>

> [!NOTE]
> <img src="https://img.shields.io/badge/http://127.0.0.1:8000/charity_project/_-GET-blue">
> ```
> [
>   {
>     "name": "Lipton",
>     "description": "чай!!!",
>     "full_amount": 100,
>     "id": 1,
>     "invested_amount": 0,
>     "fully_invested": false,
>     "create_date": "2024-02-10T17:43:17.387156",
>     "close_date": null
>   },
>   {
>     "name": "Moloko-44",
>     "description": "Пропитание бойца на некоторое время!!!",
>     "full_amount": 55,
>     "id": 3,
>     "invested_amount": 10,
>     "fully_invested": false,
>     "create_date": "2024-02-10T18:06:55.502816",
>     "close_date": null
>   },
>   {
>     "name": "Ракета",
>     "description": "рус-125477888",
>     "full_amount": 55000,
>     "id": 4,
>     "invested_amount": 5200,
>     "fully_invested": false,
>     "create_date": "2024-02-10T18:09:40.212076",
>     "close_date": null
>   },
>   ...
> ]
> ```

<div id="header" align="center">
  <h2>Сделать пожертвование</h2>
</div>

> [!NOTE]
> <img src="https://img.shields.io/badge/http://127.0.0.1:8000/donation/_-POST-Green">
>
> ### Ввод
> ```
> {
>   "full_amount": 550,
>   "comment": "На корм котикам!"
> }
> ```
> ### Вывод
> ```
> {
>   "full_amount": 550,
>   "comment": "На корм котикам!",
>   "id": 5,
>   "create_date": "2019-08-24T14:15:22Z"
> }
> ```

<div id="header" align="center">
  <h2>Регистрации Пользователя.</h2>
</div>

> [!NOTE]
> <img src="https://img.shields.io/badge/http://127.0.0.1:8000/auth/register/_-POST-Green">
> 
> ### Ввод
> ```
> {
>   "email": "user@example.com",
>   "password": "password",
>   "is_active": true,
>   "is_superuser": false,
>   "is_verified": false
> }
> ```
> 
> ### Вывод
> ```
> {
>   "id": 2,
>   "email": "user@example.com",
>   "is_active": true,
>   "is_superuser": false,
>   "is_verified": false
> }
> ```

<div id="header" align="center">
  <h2>Отчёт в Google Sheets.</h2>
</div>

> [!NOTE]
> <img src="https://img.shields.io/badge/http://127.0.0.1:8000/google/_-GET-blue">
> 
> ### Вывод
> ![Интерфейс программы GEryCH](https://github.com/OsKaLis/QRkot_spreadsheets/blob/a4e61499ee06313e1933aaa3d4331c5667e3a8b7/google_report.png)

<div id="header" align="center">
  <h2>Полная документайия команд проекта</h2>
</div>

> [!NOTE]
> ***`http://127.0.0.1:8000/docs#`***

## Автор: Юшко Ю.Ю.
