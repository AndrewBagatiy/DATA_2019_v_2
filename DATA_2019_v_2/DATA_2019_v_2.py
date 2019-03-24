# Проект: проект по работе со связанными данными в БД
# автор: Багатый Андрей

# Импортируем необходимые библиотеки
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import math

# Создаем класс базы данных. В нём определяем все постоянные переменные в БД
class DataBase:
    def __init__(self):
        self.sqlite_file = 'DATA_BASE_2019.db'
        self.text_field_type = 'TEXT'

        self.main_table_name = "all_tables"
        self.main_table_field = "TABLES"
        self.main_table_field_type = "TEXT PRIMARY KEY"

        self.conn = sqlite3.connect(self.sqlite_file)
        self.cursor = self.conn.cursor()

        # Создаем таблицу которая будет хратить имена других таблиц в БД. Таким образом легко обратиться к таблице

        self.cursor.execute("CREATE TABLE IF NOT EXISTS {mtn}({mtf} {mtft})"\
            .format(mtn = self.main_table_name, mtf = self.main_table_field, mtft = self.main_table_field_type))
        self.conn.commit()

        self.a = 'kek'
        self.b = 'lol'


# Создаем главный класс оконного приложения
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.create_table()


    def init_main(self):
        self.db = db
        # Создаю фрейм для хранения всех виджетов
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # добавляю картинки для кнопок
        self.open_img = tk.PhotoImage(file = "open.gif")

        self.add_img = tk.PhotoImage(file="add.gif")

        self.delete_img = tk.PhotoImage(file = "delete.gif")

        self.edit_img = tk.PhotoImage(file = "edit.gif")

        self.add_table_img = tk.PhotoImage(file = "add_table.gif")

        self.delete_table_img = tk.PhotoImage(file = "delete_table.gif")

        self.add_column_img = tk.PhotoImage(file = "add_column.gif")

        self.delete_column_img = tk.PhotoImage(file = "delete_column.gif")

        self.label_frame = tk.Frame(toolbar, bg='#d7d8e0')
        self.label_frame.pack(side=tk.LEFT)

        # строки с информацией, какая таблица открыта
        self.name_label = tk.Label(self.label_frame, text="Открыта таблица:", bg='#d7d8e0')
        self.name_label.grid(row=1, column=1)
        self.group_table_name = tk.StringVar()
        self.label_group = tk.Label(self.label_frame, textvariable=self.group_table_name, bg='#d7d8e0')
        self.label_group.config(width=20)
        self.label_group.grid(row=2, column=1)

        # кнопки

        self.btn_open_table = tk.Button(toolbar, text='Открыть таблицу',
                                     command=self.open_table, bg='#d7d8e0',
                                     bd=0,
                                     compound=tk.TOP, image=self.open_img)
        self.btn_open_table.pack(side=tk.LEFT)


        self.btn_add_table = tk.Button(toolbar, text='Добавить таблицу',
                                     command=self.open_add_table, bg='#d7d8e0',
                                     bd=0,
                                     compound=tk.TOP, image=self.add_table_img)
        self.btn_add_table.pack(side=tk.LEFT)



        self.btn_delete_table = tk.Button(toolbar, text='Удалить таблицу',
                                     command=self.delete_table, bg='#d7d8e0',
                                     bd=0, state = "disabled",
                                     compound=tk.TOP, image=self.delete_table_img)
        self.btn_delete_table.pack(side=tk.LEFT)

        self.btn_add_column = tk.Button(toolbar, text='Добавить колонку',
                                        command=self.open_add_column,
                                        bg='#d7d8e0',
                                        bd=0, state="disabled",
                                        compound=tk.TOP, image=self.add_column_img)
        self.btn_add_column.pack(side=tk.LEFT)


        self.btn_delete_column = tk.Button(toolbar, text='Удалить колонку',
                                     command=self.open_delete_column,
                                        bg='#d7d8e0',
                                     bd=0, state = "disabled",
                                     compound=tk.TOP, image=self.delete_column_img)
        self.btn_delete_column.pack(side=tk.LEFT)


        self.btn_add_record = tk.Button(toolbar, text='Добавить запись',
                                        command=self.open_add_record, bg='#d7d8e0',
                                        bd=0, state="disabled",
                                        compound=tk.TOP, image=self.add_img)
        self.btn_add_record.pack(side=tk.LEFT)


        self.btn_delete_record = tk.Button(toolbar, text='Удалить запись',
                                            bg='#d7d8e0',
                                     bd=0, state = "disabled",
                                     compound=tk.TOP, image=self.delete_img)

        self.btn_delete_record.pack(side=tk.LEFT)


        self.btn_change_record = tk.Button(toolbar, text='Изменить запись',
                                        bg='#d7d8e0', state = "disabled",
                                     bd=0,
                                     compound=tk.TOP, image=self.edit_img)
        self.btn_change_record.pack(side=tk.LEFT)

    # создаем функцию для создания начальной таблицы

    def create_table(self):

            self.X = 920
            self.Y = 400

            self.tree = ttk.Treeview(self, columns=("TEXT"), height=15, show="headings")
            self.tree.column("TEXT", width =self.X , anchor = tk.CENTER)
            self.tree.heading("TEXT", text = "Откройте или создайте таблицу!")

            self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            self.vsb.pack(side=tk.RIGHT, fill=tk.Y)

            self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
            self.hsb.pack(side=tk.BOTTOM, fill=tk.X)

            self.tree.configure(yscroll=self.vsb.set, xscroll=self.hsb.set)
            self.tree.pack(side = tk.BOTTOM, fill = tk.X)

    # функция отображения полноценной таблицы из БД
    def view_records(self, group_name):

        self.tree.destroy()
        self.hsb.destroy()
        self.vsb.destroy()

        self.tree = ttk.Treeview(self, columns=("TEXT"), height=15, show="headings")

        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.hsb.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.configure(yscroll=self.vsb.set, xscroll=self.hsb.set)

        self.db.cursor.execute("PRAGMA TABLE_INFO({})".format(group_name))

        self.columns = [column[1] for column in self.db.cursor.fetchall()]

        # print(self.columns)

        self.tree.config(columns=(self.columns),height = 15, show="headings")


        [self.tree.delete(i) for i in self.tree.get_children()]

        self.tree.bind('<<TreeviewSelect>>', self.bind_button)

        if len(self.columns) > 8:
            self.i = 115

        else:
            self.i = math.ceil(self.X / len(self.columns))

        for column in self.columns:
            self.tree.column(column, width= self.i)
            self.tree.heading(column, text = str(column))



        self.tree.pack(side = tk.BOTTOM, fill = 'x')

        self.db.cursor.execute('SELECT * FROM {tn}'.format(tn=group_name))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    # для того, чтобы не случалось ошибок, некоторые кнопки деактивируются
    # и активируются тогда, когда выполнены все условия
    def bind_button(self, a):
        self.btn_delete_record.config(state="normal")
        self.btn_change_record.config(state = "normal")
        self.btn_delete_record.bind('<Button-1>', self.delete_record)
        self.btn_change_record.bind('<Button-1>', self.open_change_record)

    # метод удаления записи в таблице
    def delete_record(self, a):
        curItem = self.tree.focus()

        self.db.cursor.execute('PRAGMA TABLE_INFO({})'.format(self.group_table_name.get()))

        self.names = [tup[1] for tup in self.db.cursor.fetchall()]

        self.values = self.tree.item(curItem, 'values')

        self.db.cursor.execute("DELETE FROM {tn} WHERE EXISTS(SELECT {cn1} FROM {tn})"
                               .format(tn = self.group_table_name.get(),
                                       cn1 = self.names[0],
                                       cn1v = self.values[0]))

        self.db.conn.commit()
        self.tree.delete(curItem)
        self.btn_delete_record.unbind('<Button-1>')
        self.btn_delete_record.config(state = "disabled")
        self.btn_change_record.config(state = "disabled")

    # Функция "Удалить таблицу"

    def delete_table(self):
        self.delete_table = self.group_table_name.get()



        self.db.cursor.execute("DELETE FROM {mtn} WHERE {mtf} = '{tn}'".format(mtn = self.db.main_table_name,
                                       mtf = self.db.main_table_field,
                                       tn = self.delete_table))

        self.db.cursor.execute("DROP TABLE IF EXISTS {tn}"
                               .format(tn=self.delete_table))

        self.db.conn.commit()
        self.btn_add_record.config(state = "disabled")
        self.btn_delete_record.config(state = "disabled")
        self.btn_change_record.config(state = "disabled")
        self.btn_delete_column.config(state = "disabled")
        self.btn_add_column.config(state = "disabled")
        self.btn_delete_table.config(state = "disabled")
        [self.tree.delete(i) for i in self.tree.get_children()]

        self.group_table_name.set('Группа удалена!')
        self.tree.destroy()
        self.hsb.destroy()
        self.vsb.destroy()
        self.create_table()

    # Для действий, которым необходимо дочернее окно создаю отдельные классы
    # Функции, которые вызывают классы дочерних окон
    def open_table(self):
        open_table()


    def open_add_table(self):
        add_table()

    def open_add_column(self):
        add_column()
    def open_add_record(self):
        add_record()

    def open_change_record(self, *args):
        change_record()

    def open_delete_column(self):
        delete_column()


# класс "Открыть таблицу"
class open_table(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.open_table_window()

    # создаю дочернее окно

    def open_table_window(self):
        self.title('Открыть группу')
        self.geometry("+450+200")
        self.resizable(False, False)
        self.label_group_name = tk.Label(self, text="Введите название группы: ").\
            grid(column=1, row=1)

        # На случай, если будет создано много таблиц, к списку таблиц добавляю поисковую строку
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.update_list)


        self.entry_group_open = ttk.Entry(self, textvariable = self.search_var).\
            grid(column = 2, row = 1)

        self.listbox = tk.Listbox(self)
        self.listbox.bind('<Double-ButtonRelease-1>', self.open_table)
        self.listbox.grid(row = 2,column = 1, columnspan = 2, sticky = "WE" )
        self.scroll = tk.Scrollbar(self, orient="vertical",
                                   command=self.listbox.yview)
        self.scroll.grid(row = 2, column = 2, sticky = "NSE")
        self.listbox.configure(yscrollcommand=self.scroll.set)


        self.lbox_list = list()

        self.db.cursor.execute('SELECT * FROM {mtn}'.\
                               format(mtn=self.db.main_table_name))
        self.rows = self.db.cursor.fetchall()
        for row in self.rows:
            for value in row:
                self.listbox.insert('end', value)
                self.lbox_list.append(value)




        self.grab_set()
        self.focus_set()

    # функция для поиска в списке существующих таблицк

    def update_list(self, *args):
        search_term = self.search_var.get()
        self.listbox.delete(0, "end")
        for item in self.lbox_list:
            if search_term.lower() in item.lower():
                    self.listbox.insert('end', item)

    # функция открытия таблицы. Вызывает функцию отображения таблицы, которая была выбрана в списке

    def open_table(self, *args):

        self.app = app

        index = self.listbox.curselection()[0]
        self.selection = self.listbox.get(index)

        self.app.group_table_name.set(self.selection)

        self.db.cursor.execute('PRAGMA TABLE_INFO({})'.format(self.selection))

        names = [tup[1] for tup in self.db.cursor.fetchall()]
        if len(names) > 1:
            self.app.btn_delete_column.config(state = "normal")
        else:
            self.app.btn_delete_column.config(state="disabled")
        self.app.btn_add_record.config(state = "normal")
        self.app.btn_add_column.config(state = "normal")
        self.app.btn_delete_table.config(state = "normal")
        self.destroy()
        self.app.view_records(self.selection)


# класс добавления таблицы

class add_table(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.add_table_window()

    # окно добавления таблицы

    def add_table_window(self):
        self.title('Добавить группу')
        self.geometry("+450+300")
        self.resizable(False, False)
        self.label_group_name = ttk.Label(self, text="Введите название группы: ", width = 40).\
            grid(column=1, row=1)

        self.group_table_name = tk.StringVar()

        self.entry_group_name = ttk.Entry(self, textvariable = self.group_table_name).\
            grid(column = 1, row = 2, sticky = "we")\




        self.btn_add = ttk.Button(self, text="Добавить",
                                  command=self.add_table).grid(column=1,
                                                               row=3 ,
                                                               sticky= "we")




        self.grab_set()
        self.focus_set()

    # функция добавления принимает введеные значения из ENTRY.
    # Если значение не состоит только из букв и цифр -
    # возвращает ошибку о неправильности ввода
    def add_table(self):

        # таблица в sqlite3 не может быть пустой, нужна хотя бы одна колонка

        self.group_name = self.group_table_name.get()

        if self.group_name.isalnum():

            self.empty_col_field = 'Empty'
            try:
                self.db.cursor.execute("""INSERT INTO {mtn} ({mtf})
                 VALUES ("{tn}")""".format(mtn = self.db.main_table_name,
                                           mtf = self.db.main_table_field,
                                           tn = self.group_name))

                self.db.cursor.execute("""CREATE TABLE IF NOT EXISTS {tn} ({ecf} {txtft})"""\
                                   .format(tn=self.group_name,
                                           ecf=self.empty_col_field,
                                           txtft=self.db.text_field_type))
            except sqlite3.IntegrityError:
                print("Table allready exists!")
                messagebox.showerror("Ошибка!", "Таблица уже существует!")

            self.app = app
            self.app.btn_add_record.config(state = "normal")
            self.app.btn_delete_table.config(state = "normal")
            self.app.btn_add_column.config(state = "normal")
            self.app.view_records(self.group_name)
            self.app.group_table_name.set(self.group_name)
            self.db.conn.commit()
        else:
            messagebox.showerror("Ошибка!", "Неверный ввод!")
            self.destroy()
        self.destroy()


# класс добавления колонки.

class add_column(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.add_column_window()
        # создаем окно
    def add_column_window(self):
        self.title('Добавить группу')
        self.geometry("+450+300")
        self.resizable(False, False)
        self.label_group_name = ttk.Label(self,
                                          text="Введите название колонки: ",
                                          width=40, justify = tk.CENTER ). \
            grid(column=1, columnspan = 2,  row=1, sticky="we" )

        self.group_column_name = tk.StringVar()

        self.entry_group_name = ttk.Entry(self, textvariable=self.group_column_name).\
            grid(column=1, columnspan = 2,  row=2, sticky="we")




        self.btn_add = ttk.Button(self,
                                  text="Добавить",
                                  command=self.add_column).grid(column=1,
                                                                columnspan = 2,
                                                               row=5,
                                                               sticky="we")

        self.grab_set()
        self.focus_set()

    # функция добавления колонки

    def add_column(self):

        self.app = app

        self.col_name = self.group_column_name.get()

        # если имя колонки не состоит только из букв и цифр - возвращает ошибку
        if self.col_name.isalnum():

            self.db.cursor.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {type}".
                                   format(tn= self.app.group_table_name.get(),
                                          cn=self.col_name,
                                          type = self.db.text_field_type))

            self.db.conn.commit()
            self.app.view_records(self.app.group_table_name.get())

            self.app.btn_delete_column.config(state = "normal")
        else:
            messagebox.showerror("Ошибка!", "Неверный ввод!")
        self.destroy()


# класс удаления колонки
# Поскольку в sqlite нельзя удалить колонку как таблицу, ряд или запись,
# выполняется последовательность:
class delete_column(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.delete_column_window()
    def delete_column_window(self):
        self.app = app
        self.title('Удалить колонку')
        self.geometry("+450+300")
        self.resizable(False, False)
        self.label_group_name = ttk.Label(self, text="Выберите колонку: ", width=40). \
            grid(column=1, row=1)

        # извлекаеются названия всех колонок
        self.db.cursor.execute('PRAGMA TABLE_INFO({tn})'.format(tn = self.app.group_table_name.get()))

        self.names = [tup[1] for tup in self.db.cursor.fetchall()]

        # названия помещаются в выпадающий список для выбора удаляемой колонки
        self.combobox_column = ttk.Combobox(self, state="readonly", values=self.names)
        self.combobox_column.current(0)
        self.combobox_column.grid(column=1, row=2, sticky="we")

        self.btn_add = ttk.Button(self, text="Удалить",
                                  command=self.delete_column).grid(column=1,
                                                               row=3,
                                                               sticky="we")

        self.grab_set()
        self.focus_set()

    def delete_column(self):

        # выбранная колонка удаляется из списка

        self.names.remove(self.combobox_column.get())

        # переименовывается текущая таблица
        self.db.cursor.execute("""ALTER TABLE {tn} RENAME TO {tn}_old;"""
                               .format(tn = self.app.group_table_name.get()))
        # создается новая таблица с прежним названием и вносится первая по списку колонка
        self.db.cursor.execute("""CREATE TABLE {tn} ({colf} {colft})"""
                               .format(tn = self.app.group_table_name.get(),
                                       colft = self.db.text_field_type,
                                       colf = self.names[0]))

        # далее в цикле вносятся все остальные колонки, если они есть
        for name in self.names[1:]:
                self.db.cursor.executescript("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
                                       .format(tn = self.app.group_table_name.get(),
                                               cn = name,
                                               ct = self.db.text_field_type))
        # переносятся все данные из старой таблицы в новую кроме удаленной колонки
        self.db.cursor.execute("INSERT INTO {tn}({cols}) SELECT {cols} FROM {tn}_old  "
                               .format(tn=self.app.group_table_name.get(),
                                       cols = ', '.join(self.names)))
        # удаляется старая колонка
        self.db.cursor.execute("DROP TABLE {tn}_old"\
                               .format(tn = self.app.group_table_name.get()))

        self.db.conn.commit()

        if len(self.names) > 1:
            self.app.btn_delete_column.config(state = "normal")
        else:
            self.app.btn_delete_column.config(state="disabled")
        self.db.conn.commit()
        self.app.view_records(self.app.group_table_name.get())
        self.destroy()

# класс добавление записи, принимает значения из ввода и вностит их в базу, если
# они состоят из цифр и букв. Иначе возвращает ошибку

class add_record(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.add_record_window()


    def add_record_window(self):
        self.title('Добавить запись')
        self.geometry('+450+300')
        self.resizable(False, False)
        #
        self.app = app

        self.db.cursor.execute('PRAGMA TABLE_INFO({})'.format(self.app.group_table_name.get()))

        names = [tup[1] for tup in self.db.cursor.fetchall()]

        self.vars_list = list()


        i = 0
        for row in names:
            self.vars_list.append('var' + str(i))
            self.vars_list[i] = tk.StringVar()
            self.vars_list[i].set('')
            ttk.Label(self, text=row).grid(column=1)

            ttk.Entry(self, textvariable=self.vars_list[i]).grid(row = i, column=2)
            i += 1

        self.btn_add = ttk.Button(self, text="Добавить",
                                  command=self.add_record).grid(row = i, column=1, columnspan = 2,sticky = "we")



        self.grab_set()
        self.focus_set()


    def add_record(self):

        self.app = app

        self.new_vars_list = list()

        # если введенные данные состоят из букв и цифр, тогда данные вносятся, иначе появляется ошибка
        check = False
        k = 0
        for var in self.vars_list:
            if var.get().isalnum():
                check = True
            else:
                check = False
            k+=1

        if check == True:
            del check

            self.db.cursor.execute('PRAGMA TABLE_INFO({})'.
                                   format(self.app.group_table_name.get()))

            self.names= [tup[1] for tup in self.db.cursor.fetchall()]


            self.db.cursor.execute("""INSERT INTO {tn} ({cn}) VALUES ("{var}")""" \
                                   .format(tn=self.app.group_table_name.get(), cn=self.names[0],
                                           var=self.vars_list[0].get()))


            i = 1
            while i < len(self.names):
                self.db.cursor.execute("""UPDATE {tn} SET {cn} = ("{var}") WHERE {cn1} = ("{cn1v}") """ \
                                       .format(tn=self.app.group_table_name.get(),
                                               cn=self.names[i],
                                               var=self.vars_list[i].get(),
                                               cn1 = self.names[0],
                                               cn1v = self.vars_list[0].get()))
                i+=1

            self.db.conn.commit()
            self.app = app
            self.app.view_records(self.app.group_table_name.get())
        else:
            messagebox.showerror("Ошибка!","Неверный ввод!")
            self.destroy()

        self.destroy()



# класс изменения записи, изменяет значения выбранной строки в таблице.

class change_record(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.change_record_window()


    def change_record_window(self):
        self.title('Добавить запись')
        self.geometry('+450+300')
        self.resizable(False, False)

        self.app = app

        curItem = self.app.tree.focus()

        # получаем текущие значения строки
        self.values = self.app.tree.item(curItem, 'values')

        # получаем названия колонок для создания окна ввода
        self.db.cursor.execute('PRAGMA TABLE_INFO({})'.format(self.app.group_table_name.get()))

        self.names = [tup[1] for tup in self.db.cursor.fetchall()]

        self.vars_list = list()

        i = 0
        for row in self.names:
            self.vars_list.append('var' + str(i))
            self.vars_list[i] = tk.StringVar()

            ttk.Label(self, text=row).grid(row=i, column=1)

            ttk.Entry(self, textvariable=self.vars_list[i]).grid(row=i, column=2)

            self.vars_list[i].set(self.values[i])


            i += 1

        self.btn_add = ttk.Button(self, text="Изменить",
                                  command = self.change_record).grid(column=1, columnspan=2, sticky="we")

        self.grab_set()
        self.focus_set()

    def change_record(self):

        self.db.cursor.execute('PRAGMA TABLE_INFO({})'.format(self.app.group_table_name.get()))

        self.names = [tup[1] for tup in self.db.cursor.fetchall()]

        # если новые данные не проходят проверку ввода - появляется ошибка
        check = False
        k = 0
        for var in self.vars_list:
            if var.get().isalnum():
                check = True
            else:
                check = False
            k += 1

        if check == True:

            self.db.cursor.execute("""UPDATE {tn} SET {cn} = ("{var}") WHERE {cn} = ("{old_var}") OR {cn} IS NULL"""  \
                                   .format(tn=self.app.group_table_name.get(), cn=self.names[0],
                                           var=self.vars_list[0].get(), old_var = self.values[0]))

            i = 1
            while i < len(self.names):
                self.db.cursor.execute("""UPDATE {tn} SET ({cn}) = ("{var}") WHERE {cn1} = ('{cn1v}') OR {cn} IS NULL"""\
                        .format(tn = self.app.group_table_name.get(),
                                var = self.vars_list[i].get(),
                                cn = self.names[i],
                                cn1 = self.names[0],
                                cn1v = self.vars_list[0].get()))
                i+=1


            self.db.conn.commit()

            self.app = app
            self.app.view_records(self.app.group_table_name.get())

            self.app.btn_change_record.config(state = "disabled")
            self.app.btn_delete_record.config(state = "disabled")

        else:
            messagebox.showerror("Ошибка!", "Неверный ввод!")
            self.destroy()

        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    db = DataBase()
    app = Main(root)
    app.pack()
    root.title("DATA_BASE_2019")
    root.geometry("940x400+300+200")
    root.resizable(False, False)
    root.mainloop()
