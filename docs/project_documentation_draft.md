﻿# **Проектная документация**
# **Программного обеспечения "Календарь"**

## **Введение**

Цель проекта — разработать веб-приложение для управления личными календарями, с возможностью создания и удаления событий.
Приложение должно обеспечивать регистрацию пользователей, создание и удаление учетных записей, создание и редактирование календарей и событий, поддержку повторяющихся событий и хранения метаданных (время, локация и т.д.). Данные пользователей защищаются через хеширование паролей.

---

## **Функциональные требования**

### 1. **Управление пользователями**
- Регистрация новых пользователей с указанием имени, email и пароля.
- Удаление учетной записи пользователя.
- Аутентификация и авторизация по email и паролю.
- Хеширование пароля перед хранением.
- Отображение информации профиля (имя, email, дата регистрации).

### 2. **Календари**
- Создание календарей.
- Удаление календарей, созданных пользователем.
- Отображение списка календарей.
- Автоматическая установка даты создания календаря.

### 3. **События**
- Создание событий с указанием:
  - Названия (обязательно);
  - Даты (обязательно);
  - Времени (необязательно);
  - Продолжительности (необязательно);
  - Периодичности (число дней до повторения);
  - Локации (необязательно).
- Удаление событий.
- Привязка события к календарю.
- Отображение событий календаря.

### 5. **Связи между сущностями**
- Пользователь может быть участником неограниченного числа календарей.
- Событие может принадлежать только одному календарю.
- Пользователь-календарь — связь через таблицу прав доступа.
- Календарь-событие — связь один-ко-многим.

### 6. **Безопасность и ограничения**
- Уникальность email-адреса.
- Проверка прав доступа перед операциями с календарями и событиями.
- Валидация всех входных данных.

---

## **Сценарии использования**

### **1. Регистрация пользователя**
- **Актор:** Гость
- **Условие:** Пользователь не зарегистрирован
- **Основной поток:**
  1. Пользователь вводит имя, email и пароль.
  2. Система проверяет данные.
  3. Система создаёт нового пользователя.
  4. На указанную почту отправляется ссылка с подтверждением.
  5. Отображается информация о необходимости подтвердить адрес.
- **Альтернативные потоки:**
  1. Повторный пароль не совпал с первичным — отображается ошибка.
  2. Email уже занят — отображается ошибка.

---

### **2. Вход пользователя**
- **Актор:** Гость
- **Условие:** Пользователь зарегистрирован
- **Основной поток:**
  1. Пользователь вводит email и пароль.
  2. Система проверяет данные.
  3. Система авторизует пользователя.
- **Альтернативные потоки:**
  1. Пароль не совпал — отображается ошибка.
  2. Такой Email не зарегистрирован — отображается ошибка.

---

### **3. Основное окно: отображение событий и календарей**
- **Актор:** Зарегистрированный пользователь
- **Условие:** Пользователь авторизован
- **Основной поток:**
  1. Отображается список событий и кнопка "Добавить событие".
  2. Отображается список календарей и кнопка "Добавить календарь".
- **Альтернативный поток:**
  1. Если список событий пуст — отображается сообщение.
  2. Если список календарей пуст — отображается сообщение.

---

### **4. Создание календаря**
- **Актор:** Зарегистрированный пользователь
- **Условие:** Пользователь авторизован
- **Основной поток:**
  1. Пользователь нажимает "Создать календарь".
  2. Вводит название.
  3. Система создаёт календарь, связывая его с пользователем как владельцем.

---

### **5. Добавление события**
- **Актор:** Зарегистрированный пользователь
- **Условие:** Пользователь авторизован
- **Основной поток:**
  1. Пользователь нажимает "Добавить событие".
  2. Вводит данные (название, дата и т.д.).
  3. Выбирает календарь: отображаются календари, к которым пользователь имеет права записи.
  4. Система сохраняет событие и связывает с календарем.
- **Альтернативный поток:**
  1. Если календаря не существует: отображается сообщение и появляется форма создания нового календаря.
  
---

### **6. Удаление учетной записи**
- **Актор:** Авторизованный пользователь
- **Основной поток:**
  1. Пользователь переходит на вкладку "Профиль" и нажимает на кнопку "Удалить аккаунт".
  2. Система подтверждает действие.
  3. Пользователь подтверждает.
  4. Система удаляет пользователя и его созданные календари и связи доступа.

