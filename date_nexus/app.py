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
    # Посмотрим
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
        return render_template('register.html', app_title=app_title, app_message='<p>Пароли не совпадают.</p>')

    return f'Имя {user_name}, Почта: {user_email}, Пароль: {user_password}, Повтор: {user_confirm_password}'

# Запускаем
app.run(debug=True)
