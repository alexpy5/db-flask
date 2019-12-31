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