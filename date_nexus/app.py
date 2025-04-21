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

# Запускаем
app.run(debug=True)
