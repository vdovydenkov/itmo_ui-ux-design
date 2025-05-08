from flask import Flask, render_template, request, redirect, url_for

# Заголовок для всех страниц
app_title = 'DATE NEXUS'

app = Flask(__name__)

# Индексная страница
@app.route('/')
def home():
    return render_template('index.html', app_title=app_title)

# Прислали логин и пароль
@app.route('/login', methods=['POST'])
def login():
    user_email = request.form['email']
    user_password = request.form['password']
    # Проверяем пользователя
    if user_email != 'ok@mail.ru':
        return render_template('index.html', app_title=app_title, app_message='Такой email не зарегистрирован.')

    # Авторизация прошла успешно, переходим к основному окну событий и календарей
    return redirect(url_for('events'))

# Страница регистрации
@app.route('/register')
def register():
    return render_template('register.html', app_title=app_title)

@app.route('/register', methods=['POST'])
def add_user():
    user_name = request.form['name']
    user_email = request.form['email']
    user_password = request.form['password']
    user_confirm_password = request.form['confirm_password']

    # Проверяем совпадают ли пароли
    if user_password != user_confirm_password:
        # Если нет - выводим предупреждение
        return render_template('register.html', app_title=app_title, app_message='Пароли не совпадают.')

    # Проверяем, существует ли уже такой email
    if user_email == 'already_exists@mail.ru':
        return render_template('register.html', app_title=app_title, app_message='Такой email уже зарегистрирован.')

    # Всё ОК, добавляем пользователя в БД с пометкой, что почта не подтверждена
    # Переходим на страницу входа и уведомляем, что на почту отправлена ссылка для подтверждения
    return render_template('index.html', app_title=app_title, app_message='Отлично, регистрация прошла успешно! На указанную почту отправлена ссылка. Нажмите <a href="/confirm_email">сюда</a> для подтверждения.')

# Страница подтверждения почты
@app.route('/confirm_email')
def confirm_email():
    # Здесь проверяем корректность ссылки и подтверждаем почту
    # Пользователь переходит в статус зарегистрированного и авторизированного
    return render_template('confirm_email.html', app_title=app_title)

# Основное окно событий и календарей
@app.route('/events')
def events():
    events = [
        {'id': 1, 'title': 'Встреча с друзьями'},
        {'id': 2, 'title': 'День рождения'}
    ]
    calendars = [
        {'id': 'work', 'title': 'Рабочий календарь'},
        {'id': 'personal', 'title': 'Личный календарь'}
    ]
    user_name = "Вася"

    print("events:", events)
    print("calendars:", calendars)
    print("user_name:", user_name)

    # Передача данных в шаблон
    return render_template('events.html', app_title=app_title, events=events, calendars=calendars, user_name=user_name)

# Запускаем
app.run(debug=True)
