# Работа с базой данной и Flask

Flask использует ОРМ SQLAlchemy, что позволяет нам обращаться с БД как обычным
объектом Python.

Создадим файл requirements.txt со списоком необходимых для установки модулей

```
Flask
Flask-SQLAlchemy
Flask-Migrate
```

Устанавливаем модули

`pip install -r requirements.txt`

Модуль Flask-Migrate нужен для того, чтобы после того как вы создали модель
для базы данных, например модель для пользователей, в котором будет ИД и имя,
могли внести эту новую модель в вашу базу данных.

Создадим наше приложение app.py со следующим содержимым

```
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User # Импорт специально сделан после создания приложения
                        # Раньше импортировать нельзя


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        users = User.query.all() # Получаем всех пользователей из БД
        return render_template('index.html', users=users)
    if request.method == 'POST':
        name = request.form.get('name')
        u = User(name=name)
        db.session.add(u) # Добавляем пользователя в сессию
        db.session.commit() # Записываем пользователя в БД
        users = User.query.all() # Получаем всех пользователей из БД
        return render_template('index.html', users=users)

```

Укажем фласку файл с нашим приложением

`export FLASK_APP=app.py`

Создадим файл для моделей базы данных models.py. Модели всегда лучше писать
в отдельном файле. А не в одном.
В файле конфига config.py все уже известно. Нового ничего не добавил.
Также не забудем про темплейты.

После того как мы создали models.py и прописали туда модели, мы можем создать БД,
и сделать миграцию.

```
flask db init
flask db migrate
```

Миграция создаем из наших моделей код на языке SQL. Для того, чтобы мы могли
записать в БД наши модели.

Для этого выполняем апгрейд

`flask db upgrate`

Внесение новых пользователей в БД происходит в тексте в этих строчках:

```
u = User(name=name)
db.session.add(u) # Добавляем пользователя в сессию
db.session.commit() # Записываем пользователя в БД
```

Но ранее не забудьте импортировать модель

`from models import User`

После того как мы добавили пользователя и закоммитили его он уже записан в БД.