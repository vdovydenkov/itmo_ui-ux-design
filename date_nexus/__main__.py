from flask import Flask, render_template, request, redirect, url_for
from date_nexus.services.databaser import get_user_by_email, get_calendars_by_user_id, get_events_by_calendar

# Заголовок для всех страниц
app_title = 'DATE NEXUS'
# Псевдосессия
pseudo_session = None

app = Flask(__name__)

# Индексная страница
@app.route('/')
def home():
    return render_template('index.html', app_title=app_title)

# Прислали логин и пароль
@app.route('/login', methods=['POST'])
def login():
    global pseudo_session 

    user_email = request.form['email']
    user_password = request.form['password']
    # Проверяем пользователя
    if user_email != 'ok@mail.ru':
        # Аутентификация не прошла
        return render_template('index.html', app_title=app_title, app_message='Такой email не зарегистрирован.')

    # Аутентификация прошла успешно
    user = get_user_by_email('ok@mail.ru')
    user_id = user.get('id')
    print(f'Авторизовались: user_id={user_id}, user_email={user_email}')
    # Грузим данные
    calendars = get_calendars_by_user_id(user_id)
    print(f'Получили календари: calendars={calendars}')
    if not pseudo_session:
        pseudo_session = {}
    # Грузим данные в сессию
    pseudo_session['user'] = user
    pseudo_session['calendars'] = calendars
    print(f'Загрузили в сессию: pseudo_session={pseudo_session}')
    # Переходим к основному окну событий и календарей
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

# Переключение флажка календаря
@app.route('/toggle_calendar', methods=['POST'])
def toggle_calendar():
    global pseudo_session

    # Читаем из формы
    calendar_id = request.form.get('calendar_id')
    # Если checkbox отмечен, в форме приходит selected=='1', иначе параметр отсутствует
    selected = 'selected' in request.form

    # Обновляем статус в pseudo_session
    if pseudo_session and 'calendars' in pseudo_session:
        for calendar in pseudo_session['calendars']:
            if str(calendar.get('id')) == calendar_id:
                calendar['selected'] = selected
                break

    # После изменения перенаправляем обратно на страницу events
    return redirect(url_for('events'))

# Основное окно событий и календарей
@app.route('/events')
def events():
    if not pseudo_session:
        print('events: нет сессии.')
        # Отправляемся на страницу входа
        return render_template('index.html', app_title=app_title, app_message='Пользователь не авторизирован.')
    # Берём пользователя и календари из сессии
    user = pseudo_session['user']
    calendars = pseudo_session['calendars']
    if not user:
        print('Events: Пользователь не залогинен.')
        # Отправляемся на страницу входа
        return render_template('index.html', app_title=app_title, app_message='Пользователь не авторизирован.')
    print(f'Прошли проверку, user={user}')
    user_id = user.get('id')
    user_name = user.get('name')
    events = []
    for calendar in calendars:
        # Если календарь не выбран
        if not calendar.get('selected'):
            continue
        # Получаем события календаря
        calendar_events = get_events_by_calendar(calendar['id'])
        print(f'Events: Получили события календаря: calendar_events={calendar_events}')
        for event in calendar_events:
            # Добавляем событие в общий список
            events.append(event)

    print("events:", events)
    print("calendars:", calendars)
    print("user_name:", user_name)

    # Передача данных в шаблон
    return render_template('events.html', app_title=app_title, events=events, calendars=calendars, user_name=user_name)

# Запускаем
if __name__ == '__main__':
    app.run(debug=True)

