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

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/RaifGaripov/Komtek.git
   ```
2. Откройте папку
   ```bash
   cd Komtek
   ```
3. Запустите сервер
   ```bash
   python manage.py runserver
   ```
4. Для входа в панель админа возпользуйтесь логином и паролем `admin`

5. Для запуска тестов
   ```bash
   python manage.py test doc_managment
   ```