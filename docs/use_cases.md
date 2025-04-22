## UML-диаграммы последовательностей

### **1. Регистрация пользователя**

@startuml
actor "Гость" as Guest
participant "Система" as System

Guest -> System: Ввод данных (имя, email, пароль)
activate System
System -> System: Проверка введённых данных
alt Данные корректны
    System -> System: Создание нового пользователя
    System -> Guest: Отправка ссылки для подтверждения на email
    System -> Guest: Сообщение о необходимости подтверждения адреса
else Данные некорректны
    System -> Guest: Отображение ошибки (например, "Пароли не совпадают" или "Email уже занят")
end
deactivate System
@enduml

---

### **2. Вход пользователя**

@startuml
actor "Гость" as Guest
participant "Система" as System

Guest -> System: Ввод email и пароля
activate System
System -> System: Проверка введённых данных
alt Учетные данные верны
    System -> Guest: Авторизация пользователя
else Ошибка в данных
    System -> Guest: Отображение ошибки (например, "Пароль не совпадает" или "Email не найден")
end
deactivate System
@enduml

---

### **3. Основное окно: отображение событий и календарей**

@startuml
actor "Зарегистрированный пользователь" as User
participant "Система" as System

User -> System: Запрос списка событий и календарей
activate System
System -> User: Отправка списка событий с кнопкой "Добавить событие"
System -> User: Отправка списка календарей с кнопкой "Добавить календарь"
alt Список событий пуст
    System -> User: Отображение сообщения (например, "Событий не найдено")
end
alt Список календарей пуст
    System -> User: Отображение сообщения (например, "Календарей не найдено")
end
deactivate System
@enduml

---

### **4. Создание календаря**

@startuml
actor "Зарегистрированный пользователь" as User
participant "Система" as System

User -> System: Нажатие на кнопку "Создать календарь"
activate System
User -> System: Ввод названия и описания календаря
System -> System: Создание календаря и привязка к пользователю (роли владельца, уровень доступа = 3)
System -> User: Подтверждение успешного создания календаря
deactivate System
@enduml

---

### **5. Добавление события**

@startuml
actor "Зарегистрированный пользователь" as User
participant "Система" as System

User -> System: Нажатие на кнопку "Добавить событие"
activate System
User -> System: Ввод данных события (название, дата, и т.д.)
User -> System: Выбор календаря (из списка с правом записи ≥ 1)
alt Календарь существует
    System -> System: Сохранение события и привязка его к выбранному календарю
    System -> User: Подтверждение сохранения события
else Календарь не существует
    System -> User: Отображение сообщения + предложение создать новый календарь
end
deactivate System
@enduml

---

### **6. "Поделиться" календарём**

@startuml
actor "Зарегистрированный пользователь" as User
participant "Система" as System

User -> System: Выбор календаря и нажатие кнопки "Поделиться"
activate System
User -> System: Ввод email другого пользователя и установка уровня доступа
System -> System: Добавление соответствующей записи в таблицу UserAccess
System -> User: Подтверждение успешного добавления доступа
deactivate System
@enduml

---

### **7. Удаление учетной записи**

@startuml
actor "Авторизованный пользователь" as User
participant "Система" as System

User -> System: Переход в раздел "Настройки" и нажатие "Удалить аккаунт"
activate System
System -> User: Запрос подтверждения удаления
User -> System: Подтверждение удаления аккаунта
System -> System: Удаление учетной записи, созданных календарей и связей доступа
System -> User: Сообщение об успешном удалении аккаунта
deactivate System
@enduml
