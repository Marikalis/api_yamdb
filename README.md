# Учебный проект "YaMDb API"

Проект YaMDb позволяет добавлять новых пользователей,
собирает отзывы пользователей на различные произведения.

### Авторы:
- Maria Lisitskaya https://github.com/Marikalis
- Alexander Morozov https://github.com/amorozov89

### Технологии:
- Python
- Django
- DRF

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Marikalis/api_yambd.git
```

```
cd api_yambd
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Если необходимо, заполненить базу данных тестовыми данными:

1. перейдите в корневую папку проекта, где находится файл csv_importer.py
2. запустите скрипт csv_importer.py:
```
python3 csv_importer.py
```

Запустить проект:

```
python3 manage.py runserver
```

## Документация к API:

```
http://127.0.0.1:8000/redoc/
```

Регистрация нового пользователя:

```
http://127.0.0.1:8000/api/v1/auth/signup/
```
