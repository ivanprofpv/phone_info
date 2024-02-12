## Телефонный справочник

Телефонный справочник на чистом Python с использованием SQLite3.
В качестве интерфейса используется консоль.

## Схема БД:
- id INTEGER PRIMARY KEY,
- name TEXT NOT NULL,
- patronymic TEXT NOT NULL,
- lastname TEXT NOT NULL,
- name_organization TEXT NOT NULL,
- work_phone TEXT NOT NULL,
- personal_phone TEXT NOT NULL

## Что можно сделать в приложении:

- Вывести все записи через пагинацию;
- Добавить запись;
- Отредактировать запись (по ID);
- Выполнить поиск записей по фамилии (нет ограничения по количеству записей);
- Выполнить поиск записей по фамилии и наименование организации (нет ограничения по количеству записей).

## На чем сделано:
- Python '3.10.9';
- SQLite3.