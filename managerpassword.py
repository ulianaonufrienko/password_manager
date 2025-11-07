import sys
import random
import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog

con = sqlite3.connect('my_password.db') # подключение к БД
cor = con.cursor

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.create_password.clicked.connect(self.open_create_window)
        self.view_passwords.clicked.connect(self.open_view_window)

    def open_create_window(self):
        self.create_password_ = Create_password()
        # uic.loadUi('creating_password.ui',create_password_)
        self.create_password_.show()
        # открытие окна с созданием пароля

    def open_view_window(self):
        view_password_ = QDialog(self)
        uic.loadUi('viewing_password.ui', view_password_)
        view_password_.show()
        # открытие окна с просмотром существующих паролей

class Create_password(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('creating_password.ui', self)
        self.generate_password.clicked.connect(self.function_generate_password)
        # подключение функции принажатии на кнопку

    def function_generate_password(self): # функция для генирации паролей
        is_letters = self.letters.isChecked()
        is_numbers = self.numbers.isChecked()
        is_special_characters = self.special_characters.isChecked()
        # считывание видов символов(буквы,цифры,спец символы) кторые пользователь хочет использовать
        lenght = int(self.quantity.text())
        # считывание длины пароля
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        numbers = '0123456789'
        special_characters = "{}[]()*'/,_-!?"

        if is_letters == True and is_numbers == True and is_special_characters == True:
            all = letters + numbers + special_characters
            password_ = "".join(random.sample(all, lenght))
            self.final_password.setText(password_)
        elif is_letters == True and is_numbers == True and is_special_characters == False:
            letters_and_numbers = letters + numbers
            password_ = "".join(random.sample(letters_and_numbers, lenght))
            self.final_password.setText(password_)
        elif is_letters == True and is_numbers == False and is_special_characters == True:
            letters_and_special_characters = letters + special_characters
            password_ = "".join(random.sample(letters_and_special_characters, lenght))
            self.final_password.setText(password_)
        elif is_letters == False and is_numbers == True and is_special_characters == True:
            numbers_and_special_characters = numbers + special_characters
            password_ = "".join(random.sample(numbers_and_special_characters, lenght))
            self.final_password.setText(password_)
        elif is_letters == True and is_numbers == False and is_special_characters == False:
            password_ = "".join(random.sample(letters, lenght))
            self.final_password.setText(password_)
        elif is_letters == False and is_numbers == True and is_special_characters == False:
            password_ = "".join(random.sample(numbers, lenght))
            self.final_password.setText(password_)
        elif is_letters == False and is_numbers == False and is_special_characters == True:
            password_ = "".join(random.sample(special_characters, lenght))
            self.final_password.setText(password_)
        elif is_letters == False and is_numbers == False and is_special_characters == False:
            password_ = "".join(random.sample(all, lenght))
            self.final_password.setText(password_)
        # гененрация пароля по количеству символов и их типу

        con = sqlite3.connect('my_password.db')
        cur = con.cursor()
        # подключаем БД для добавления пароля
        login_ = self.login.text()
        note_ = self.note.text()
        # берем из LineEdit логин и заметку
        cur.execute("""INSERT INTO my_password(login, password, note) VALUES(login_,password_,note_) """)
        # запись пароля в бд под его логином и заметке к нему
        # тут еще надо сделать все это с типом пароля который храниться во второй таблице

class Viewing_passwords(QDialog): # окно поиска и удаления паролей
    def __init__(self):
        super().__init__()
        uic.loadUi('viewing_password.ui', self)
        self.search_password.clicked.connect(self.function_search_password)
        self.removal.clicked.connect(self.open_dialog_window())

    def function_search_password(self): # функция нахождения пароля
        con = sqlite3.connect('my_password.db')
        cur = con.cursor()
        login_1 = self.login.text()
        note_1 = self.note.text()
        # берем введеный пользователей логин и заметку

        result = cur.execute("""SELECT * FROM my_password
                            WHERE login = login_1 AND note = note_1""").fetchone()
        # записываем в result найденый пароль
        # надо тут записывать TextEdit найеный пароль

    def open_dialog_window(self):
        delete_password_ = QDialog(self)
        uic.loadUi('delete_password.ui', delete_password_)
        delete_password_.show()
        # открытие диалогового окна с уточнением надо ли удалять пароль

class Dealete_password(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('delete_password.ui', self)
        self.buttonBox.clicked.connect(self.function_delete_password())

    def function_delete_password(self):  # функция удаления найденного пароля
        login_1 = self.login.text()
        note_1 = self.note.text()
        cur.execute("""DELETE from *
        where login = login_1 AND note = note_1""")
        # тут тоже надо додлеть

def except_hook(cls,exception,treaceback):
    sys.__excepthook__(cls, exception, treaceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec())