# Komtek тестовое задание
Задание выполнено согласно требованиям, с помощью Django, DRF, Swagger. В качестве хранилища данных используется SQLite.
## API

- **GET /api/refbooks/[?date=\<date\>]**: Получение списка справочников (+ актуальных на указанную дату)
- **GET /api/refbooks/\<id\>/elements [?version=\<version\>]**: Получение элементов заданного справочника
- **GET /api/refbooks/\<id\>/check_element?code=\<code\>&value=\<value\>[&version=\<version\>]**: Валидация элементов
- **/admin** Панель админа Django 
- **/api/schema/swagger-ui/** Swagger UI
## Установка

Для установки проекта вам нужно выполнить следующие шаги:

1. Клонируйте репозиторий
   ```bash
   git clone https://github.com/RaifGaripov/Komtek.git
   ```
2. Создайте виртуальное окружение
   ```bash
   python -m venv venv
   ```
3. Активируйте виртуальное окружение (в Windows)
   ```bash
   venv\Scripts\activate
   ```
4. Установите зависимости
   ```bash
   pip install -r requirements.txt
   ```
6. Внесите миграции в базу данных
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ``` 
7. Загрузите фикстуры
   ```bash
   python manage.py loaddata fixtures/initial_data.json 
   ```
8. Запустите сервер
   ```bash
   python manage.py runserver
   ```
9. Для входа в панель админа возпользуйтесь логином и паролем `admin`

10. Для запуска тестов
   ```bash
   python manage.py test doc_managment
   ```
