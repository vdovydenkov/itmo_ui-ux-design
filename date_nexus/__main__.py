from flask import Flask, render_template, request, redirect, url_for, session, flash
from itertools import count
from datetime import date
from date_nexus.services.databaser import get_user_by_email, get_calendars_by_user_id, get_events_by_calendar

# Заголовок для всех страниц
app_title = 'DATE NEXUS'

app = Flask(__name__)
app.secret_key = '1,2,3,4,5,5.4.3.2.1' # Понятно, что так нельзя

# Индексная страница
@app.route('/')
def home():
    return render_template('index.html', app_title=app_title)

# Справка
@app.route('/help')
def help():
    return render_template('help.html', app_title=app_title)

# Прислали логин и пароль
@app.route('/login', methods=['POST'])
def login():
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
    events = []
    # Грузим все события календарей
    for calendar in calendars:
        events.extend(get_events_by_calendar(calendar.get('id')))
    # Грузим данные в сессию
    session['user'] = user
    session['calendars'] = calendars
    session['events'] = events
    print('Загрузили в сессию')
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
    # Читаем из формы
    calendar_id = request.form.get('calendar_id')
    # Если checkbox отмечен, в форме приходит selected=='1', иначе параметр отсутствует
    selected = 'selected' in request.form

    # Обновляем статус в session
    if 'calendars' in session:
        calendars = session['calendars']
        for calendar in calendars:
            if str(calendar.get('id')) == calendar_id:
                calendar['selected'] = selected
                break
        session['calendars'] = calendars  # Обновляем в сессии

    # После изменения перенаправляем обратно на страницу events
    return redirect(url_for('events'))

# Основное окно событий и календарей
@app.route('/events')
def events():
    if 'user' not in session or 'calendars' not in session:
        print('events: нет сессии.')
        # Отправляемся на страницу входа
        return render_template('index.html', app_title=app_title, app_message='Пользователь не авторизирован.')

    # Поддержка удаления через GET-параметр
    action = request.args.get('action')
    if action == 'delete':
        event_id = request.args.get('id', type=int)
        if event_id is not None and 'events' in session:
            # Берём название удаляемого события
            event_title = next(
                (
                    ev['title'] for ev in session['events']
                    if ev.get('id') == event_id
                ),
                ''  # Если не нашли название события
            )
            # удаляем из сессии
            before = len(session['events'])
            session['events'] = [
                ev for ev in session['events']
                if ev.get('id') != event_id
            ]
            after = len(session['events'])
            if after < before:
                flash(f'Событие {event_title} удалено.')
        # чтобы не повторять удаление при перезагрузке — редирект без параметров
        return redirect(url_for('events'))

    # Берём пользователя, календари и события из сессии
    user      = session.get('user')
    calendars = session.get('calendars', [])
    events    = session.get('events', [])
    if not user:
        print('Events: Пользователь не залогинен.')
        # Отправляемся на страницу входа
        return render_template('index.html', app_title=app_title, app_message='Пользователь не авторизирован.')
    print(f'Прошли проверку, user={user}')
    user_id   = user.get('id')
    user_name = user.get('name')
    selected_events = []
    # Фильтруем события из выбранных календарей.
    for calendar in calendars:
        selected_events.extend([
            event for event in events
            if calendar['id'] == event.get('calendar_id')
            and calendar.get('selected')
        ])

    print("selected_events:", selected_events)
    print("calendars:", calendars)
    print("user_name:", user_name)

    # Передача данных в шаблон
    return render_template(
        'events.html',
        app_title=app_title,
        events=selected_events,
        calendars=calendars,
        user_name=user_name
    )

# Добавление события
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if 'user' not in session:
        flash('Пользователь не авторизирован.')
        return redirect(url_for('home'))

    user = session.get('user')
    calendars = session.get('calendars', [])

    if request.method == 'POST':
        # Считываем данные из формы
        title      = request.form.get('title')
        date       = request.form.get('date')
        time       = request.form.get('time') or None
        duration   = request.form.get('duration') or None
        recurrence = request.form.get('recurrence') or None
        location   = request.form.get('location') or None
        calendar_id = request.form.get('calendar_id')

        # Валидация обязательных полей
        if not title or not date or not calendar_id:
            flash('Пожалуйста, заполните все обязательные поля.')
            return render_template(
                'add_event.html',
                app_title=app_title,
                calendars=calendars
            )

        # Подготовка словаря события
        event_data = {
            'title': title,
            'date': date,
            'time': time,
            'duration': int(duration) if duration else None,
            'recurrence_days': int(recurrence) if recurrence else None,
            'location': location,
            'calendar_id': int(calendar_id),
        }

        # Сохраняем в сессию
        session['events'].append(event_data)

        flash('Событие успешно добавлено!')
        return redirect(url_for('events'))

    # GET: показываем форму
    return render_template(
        'add_event.html',
        app_title=app_title,
        calendars=calendars
    )

# Добавление календаря
@app.route('/add_calendar', methods=['GET', 'POST'])
def add_calendar():
    if 'user' not in session:
        flash('Пользователь не авторизирован.')
        return redirect(url_for('home'))
    calendars = session.get('calendars', [])
    # Если пришла форма
    if request.method == 'POST':
        # Считываем данные
        new_title = request.form.get('title')
        # Сохраняем текущую дату
        register_at = date.today().isoformat()
        # Собираем все id
        used_ids = {calendar['id'] for calendar in calendars}
        # Берём id из множества целых, которого нет в used_ids
        new_id = next(i for i in count(0) if i not in used_ids)
        new_calendar = {
            'id': new_id,
            'title': new_title,
            'register_at': register_at,
            'selected': True
        }
        # Добавляем в список
        calendars.append(new_calendar)
        # Обновляем сессию
        session['calendars'] = calendars

        flash('Календарь добавлен!')
        return redirect(url_for('events'))

    # GET: показываем форму
    return render_template(
        'add_calendar.html',
        app_title=app_title,
        calendars=calendars
    )

# Профиль пользователя
@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    if 'user' not in session:
        flash('Пользователь не авторизирован.')
        return redirect(url_for('home'))
    user = session['user']

    if request.method == 'POST':
        # Проверяем, отправлена ли форма удаления
        if request.form.get('delete_user') == 'yes':
            # После успешного удаления:
            session.clear()
            flash('Ваш пользователь и все связанные данные удалены.')
            return redirect(url_for('home'))
    # GET: показываем форму профиля
    return render_template(
        'profile.html',
        app_title=app_title,
        user=user
    )

def main():
    app.run(debug=True, use_reloader=True)

# Запускаем
if __name__ == '__main__':
    main()

