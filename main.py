import sqlite3

def create_db(cursor: sqlite3.Cursor):
    """
    Создаем таблицу с проверкой на то, существует она или нет.
    :param cursor:
    :return:
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cards (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    patronymic TEXT NOT NULL,
    lastname TEXT NOT NULL,
    name_organization TEXT NOT NULL,
    work_phone TEXT NOT NULL,
    personal_phone TEXT NOT NULL
    )
    ''')

def get_card(cursor: sqlite3.Cursor, page_point=2):
    """
    Функция для вывода записей через пагинацию (2 записи на страницу с шагом 1)
    :param cursor:
    :param page_point:
    :return:
    """
    page_num = 1
    offset = 0

    while True:
        cursor.execute('SELECT * FROM Cards LIMIT ? OFFSET ?', (page_point, offset))
        cards = cursor.fetchall()

        if not cards:
            print("Нет записей на странице")
            break

        print(f"Страница {page_num}")
        for card in cards:
            print(card)

        user_input = input("Нажмите Enter для продолжения или 'Выход' для выхода: ")
        if user_input.lower() == "Выход":
            break

        page_num += 1
        offset += page_point

def add_card(cursor: sqlite3.Cursor, name: str, patronymic: str,
             lastname: str, name_organization: str,
             work_phone: str, personal_phone: str):
    """
    Функция для добавления новой записи в БД.
    :param cursor:
    :param name:
    :param patronymic:
    :param lastname:
    :param name_organization:
    :param work_phone:
    :param personal_phone:
    :return:
    """
    # Добавление записи в базу данных с использованием параметров запроса
    cursor.execute('''
        INSERT INTO Cards (name, patronymic, lastname, name_organization, work_phone, personal_phone)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, patronymic, lastname, name_organization, work_phone, personal_phone))

    print("Запись добавлена")


def edit_card(cursor: sqlite3.Cursor, card_id: int):
    """
    Функция для редактирования ранее созданной записи.
    При редактировании необходимо вводить заново все поля.
    :param cursor:
    :param card_id:
    :return:
    """

    # Получаем запись по введенному ID
    cursor.execute('SELECT * FROM Cards WHERE id = ?', (card_id,))
    card = cursor.fetchone()

    if card:
        name = input("Введите новое имя: ")
        patronymic = input("Введите новое отчество: ")
        lastname = input("Введите новую фамилию: ")
        name_organization = input("Введите новое название организации: ")
        work_phone = input("Введите новый рабочий номер: ")
        personal_phone = input("Введите новый личный номер: ")

        # Обновление записи в базе данных
        cursor.execute('''
            UPDATE Cards SET 
            name = ?,
            patronymic = ?,
            lastname = ?,
            name_organization = ?,
            work_phone = ?,
            personal_phone = ?
            WHERE id = ?
            ''', (name, patronymic, lastname, name_organization, work_phone, personal_phone, card_id))

        print("Запись обновлена")
    else:
        print("Запись с указанным ID не найдена")


def search_card_for_lastname(cursor: sqlite3.Cursor, lastname: str):
    """
    Функция для поиска и вывода записи по фамилии.
    :param cursor:
    :param lastname:
    :return:
    """
    cursor.execute('SELECT * FROM Cards WHERE lastname = ?', (lastname,))
    results = cursor.fetchall()

    for lastname in results:
        print(lastname)


def search_card_for_lastname_and_organization(cursor: sqlite3.Cursor, lastname: str, name_organization: str) -> None:
    """
    Функция для поиска и вывода записи по фамилии и наименованию организации.
    :param cursor:
    :param lastname:
    :param name_organization:
    :return:
    """
    cursor.execute('SELECT * FROM Cards WHERE lastname = ? and name_organization = ?', (lastname, name_organization,))
    results = cursor.fetchall()

    for part in results:
        print(part)

def menu():
    """
    Цикл для выбора меню и последующая передача параметров в функции в зависимости
    от выбранного пункта
    :return:
    """
    # Создаем подключение к базе данных (будет создан файл database.db)
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()

        # Создаем БД
        create_db(cursor)

        while True:
            print("Выберите нужный пункт и введите цифру пункта:")
            print("1. Показать все записи")
            print("2. Добавить запись")
            print("3. Отредактировать запись")
            print("4. Найти запись по фамилии")
            print("5. Найти запись по фамилии и организации")
            print("0. Выход")
            choice = input("Введите номер строки: ")

            if choice == "1":
                get_card(cursor)
            elif choice == "2":
                name = input("Введите имя: ")
                patronymic = input("Введите отчество: ")
                lastname = input("Введите фамилию: ")
                name_organization = input("Введите название организации: ")
                work_phone = input("Введите рабочий номер: ")
                personal_phone = input("Введите личный номер: ")
                add_card(cursor, name, patronymic, lastname, name_organization, work_phone, personal_phone)
            elif choice == "3":
                card_id = int(input("Введите ID записи для редактирования: "))
                edit_card(cursor, card_id)
            elif choice == "4":
                lastname = input("Введите фамилию: ")
                search_card_for_lastname(cursor, lastname)
            elif choice == "5":
                lastname = input("Введите фамилию: ")
                name_organization = input("Введите орагнизацию: ")
                search_card_for_lastname_and_organization(cursor, lastname, name_organization)
            elif choice == "0":
                break
            else:
                print("Ошибка. Попробуйте еще раз.")

            # Сохраняем изменения и закрываем соединение
    connection.commit()

    connection.close()

if __name__ == "__main__":
    menu()

