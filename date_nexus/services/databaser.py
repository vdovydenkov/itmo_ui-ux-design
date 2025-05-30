# date_nexus\services\databaser.py

def get_user_by_email(email: str) -> dict:
    '''Возвращает пользователя по заданному email.'''
    if email.lower() == 'ok@mail.ru':
        return {
            'id': 0,
            'name': 'Василий Пуговков',    
            'email': 'ok@mail.ru'
        }
    else:
        return None

def get_calendars_by_user_id(user_id: int) -> list[dict]:
    '''Возвращает список словарей с календарями по id пользователя.'''
    calendars = [
        {
            'id': 0,
            'title': 'Рабочий календарь',
            'register_at': '2025-02-23',
            'selected': True
        },
        {
            'id': 1,
            'title': 'Личный календарь',
            'register_at': '2025-03-08',
            'selected': True}
    ]

    if user_id == 0:
        return calendars
    else:
        return None

def get_user_access(user_id: int, calendar_id: int) -> int:
    '''Возвращает уровень доступа по id пользователя и id календаря.'''
    if user_id == 0:
        if calendar_id == 0: # рабочий календарь, доступ "только чтение"
            return 0
        elif calendar_id == 1: # Личный календарь, доступ "владелец"
            return 3
    return None

def get_events_by_calendar(calendar_id: int) -> list[dict]:
    '''Возвращает список событий по id календаря.'''
    personal_events = [
        {
            'id': 0,
            'title': 'Поход в кино',
            'date': '2025-05-11',
            'time': '19:00',
            'duration': 120,
            'location': 'Кинотеатр Аврора',
            'calendar_id': 1,
        },
        {
            'id': 1,
            'title': 'Встреча с друзьями',
            'date': '2025-05-13',
            'time': '18:30',
            'recurrence': 7,
            'location': 'Кафе на углу',
            'calendar_id': 1,
        },
        {
            'id': 2,
            'title': 'Прогулка в парке',
            'date': '2025-05-15',
            'time': '17:00',
            'duration': 90,
            'calendar_id': 1,
        }
    ]

    work_events = [
        {
            'id': 3,
            'title': 'Совещание отдела',
            'date': '2025-05-09',
            'time': '10:00',
            'duration': 60,
            'recurrence': 1,
            'location': 'Зал переговоров',
            'calendar_id': 0,
        },
        {
            'id': 4,
            'title': 'Презентация проекта',
            'date': '2025-05-14',
            'time': '14:00',
            'duration': 45,
            'location': 'Конференц-зал',
            'calendar_id': 0,
        },
        {
            'id': 5,
            'title': 'Отчет перед руководством',
            'date': '2025-05-20',
            'time': '09:00',
            'duration': 30,
            'calendar_id': 0,
        }
    ]
    if calendar_id == 0:
        return work_events
    elif calendar_id == 1:
        return personal_events
    else:
        return []