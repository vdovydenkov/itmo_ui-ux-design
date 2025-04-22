from flask import Flask, render_template, request

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
    email = request.form['email']
    password = request.form['password']
    # Покажем
    return f"Email: {email}, Пароль: {password}"

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
    # Главное окно программы
    return render_template('events.html', app_title=app_title)

# Запускаем
app.run(debug=True)
