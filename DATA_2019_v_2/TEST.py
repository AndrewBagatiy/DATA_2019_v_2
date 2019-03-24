import sqlite3

# Тестирование всех запросов и транзакций, которые используются в приложении

class DataBase:
    def __init__(self):
        self.sqlite_file = "DATA_BASE_2019_TEST.db"
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cursor = self.conn.cursor()

# удаление таблицы, если ранее уже запускались тесты,
# чтобы протестировать все транзакции и запросы снова.

        self.cursor.execute("DROP TABLE IF EXISTS test")
        self.conn.commit()


def add_table_test():
    # создание тестовой таблцицы "test" с колонкой "testCol" и типом "testCol"
    db.cursor.execute("CREATE TABLE IF NOT EXISTS test (testCol TEXT)")
    db.conn.commit()
    # извлекаем имя таблицы для проверки наличия таблицы в базе
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name = 'test'")
    select = db.cursor.fetchone()
    print(select[0])
    # если начальное название совпадает с полученным, значит таблица добавлена в базу
    assert 'test' == select[0], "Название таблицы должно совпадать с запросом"

def add_column_test():
    # добавляем колонку с названием "SecondTestCol"
    db.cursor.execute("ALTER TABLE test ADD COLUMN 'SecondTestCol' TEXT")
    db.conn.commit()
    # извлекаем имена колонок из таблицы и вносим их в список
    db.cursor.execute('PRAGMA TABLE_INFO(test)')
    cols = [tup[1] for tup in db.cursor.fetchall()]
    # новая колонка всегда находится в конце списка
    print(cols[-1])
    assert 'SecondTestCol' == cols[-1], "Название колонки должно совпадать с запросом"

def add_record_test():
    # добавляем запись 'row1col1', 'row2col2' в колонки "testCol", "SecondTestCol" в таблицу "test"
    db.cursor.execute("INSERT INTO test (testCol, SecondTestCol) VALUES ('row1col1', 'row2col2')")
    db.conn.commit()
    # извлекаем всё из таблицы
    db.cursor.execute("SELECT * FROM test")
    rows = db.cursor.fetchall()
    # сравним первую запись в первой колонке с предпологаемым значением
    print(rows[0][0])
    assert  'row1col1' == rows[0][0], "Название строки должна совпалать с запросом"

def change_record_test():
    # изменим значение в первой строке первой колонки с 'row1col1' на 'newRow'
    db.cursor.execute("UPDATE test SET testCol = ('newRow') WHERE testCol = ('row1col1') OR testCol IS NULL")
    db.conn.commit()
    # сравниваем полученное значение с предпологаемым
    db.cursor.execute("SELECT * FROM test")
    rows = db.cursor.fetchall()
    print(rows[0][0])
    assert  'newRow' == rows[0][0], "Название новой строки должна совпалать с запросом"


def del_column_test():
    # удаляем колонку из таблицы
    # 1. Получаем значения таблиц в список
    db.cursor.execute('PRAGMA TABLE_INFO(test)')
    cols = [tup[1] for tup in db.cursor.fetchall()]
    # 2. Удаляем имя колонки из списка
    cols.remove("SecondTestCol")
    # 3. Переименовываем таблицу
    db.cursor.execute("ALTER TABLE test RENAME TO test_old")
    # 4. Создаем новую таблицу со старым названием
    db.cursor.execute("CREATE TABLE test (testCol TEXT)")
    # 5. Копируем все данные из старой таблицы в новую кроме удаленной колонки
    db.cursor.execute("INSERT INTO test (testCol) SELECT testCol FROM test_old")
    # 6. Удаляем старую таблицу
    db.cursor.execute("DROP TABLE test_old")
    db.conn.commit()
    # 7. проверяем оставшиеся колонки в таблице
    db.cursor.execute('PRAGMA TABLE_INFO(test)')
    cols = [tup[1] for tup in db.cursor.fetchall()]
    print(cols[0])
    assert 'testCol' == cols[0], 'Название последней колонки должно совпадать с запросом'

def delete_table_test():
    # удаляем таблицу из базы
    db.cursor.execute("DROP TABLE test")
    # проверяем наличие таблицы в базе, если ничего не найдено - значит таблица удалена
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name = 'test'")
    select = db.cursor.fetchone()
    print(select)
    assert  select == None, "Название таблицы должно совпадать с запросом"

if __name__ == '__main__':
    # Вызов всех методов
    db = DataBase()
    add_table_test()
    print("таблица добавлена в базу")
    add_column_test()
    print("добавлена колонка в таблицу")
    add_record_test()
    print("добавлена запись в таблицу")
    change_record_test()
    print("изменена запись в таблице")
    del_column_test()
    print("удалена колонка в таблице")
    delete_table_test()
    print("удалена таблица")

