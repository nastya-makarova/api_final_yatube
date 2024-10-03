# Проект Yatube (v1)

## Описание проекта
### Yatube — это платформа для блогов. 
Yatube предполагает возможность зарегистрироваться, создать, отредактировать или удалить собственный пост, прокомментировать пост другого автора и подписаться на него.

## Установка

### Клонировать репозиторий и перейти в него в командной строке:

```git@github.com:nastya-makarova/api_final_yatube.git```

```cd api_final_yatube```

### Cоздать и активировать виртуальное окружение:

```python3 -m venv env```

```source env/bin/activate```

### Установить зависимости из файла requirements.txt:

```python3 -m pip install --upgrade pip```

```pip install -r requirements.txt```

### Выполнить миграции:

```python3 manage.py migrate```

### Запустить проект:

```python3 manage.py runserver```

## Примеры запросов к API.

+ Получить список всех публикаций.

  ```GET http://127.0.0.1:8000/api/v1/posts/```
  
  Пример ответа с пагинацией:
  ```
  {
    "count": 123,
    "next": "http://api.example.org/accounts/?offset=400&limit=100",
    "previous": "http://api.example.org/accountsoffset=200&limit=100",
    "results": [
        {}
      ]
    }
  ```
+ Добавление новой публикации в коллекцию публикаций. Анонимные запросы запрещены.
  
  ```POST http://127.0.0.1:8000/api/v1/posts/```

  Пример ответа:
  ```
  {
    "text": "string",
    "image": "string",
    "group": 0
  }
  ```

+ Получение публикации по id.
  
  ```GET http://127.0.0.1:8000/api/v1/posts/{id}/```

  Пример ответа:
  ```
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "pub_date": "2019-08-24T14:15:22Z",
    "image": "string",
    "group": 0
  }
  ```

+ Получение комментария к публикации по id.

  ```GET http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/```

  Пример ответа:
  ```
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
  ```

### Документация для API Yatube доступна:

```http://127.0.0.1:8000/redoc/```


