from PyQt5.QtWidgets import QWidget, QStatusBar, QInputDialog
from PyQt5 import QtWidgets
from AuthUserGUI import AuthGUI
import first_page
import sqlite3
from MainPageUsr import MainPageUsr
from MainPageAdm import MainPageAdm
from RegistrationGUI import RegistrationGUI
from random import randint
import smtplib

con = sqlite3.connect('orders.sqlite')
cur = con.cursor()


class AuthPageUsr(QWidget, AuthGUI):
    def __init__(self, adm=False):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Your Order Base')
        self.pushButton.clicked.connect(self.confirm)
        if adm:
            self.pushButton_2.close()
            self.pushButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.pushButton_2.clicked.connect(self.reg)
        self.is_adm = adm
        self.pushButton_3.clicked.connect(self.ret)

    def confirm(self):
        self.pushButton.setText('Продолжить')
        self.pushButton.setStyleSheet('color: black')
        user = 'users' if not self.is_adm else 'admins'
        if self.lineEdit.text() and self.lineEdit_2.text():
            if cur.execute(f"""SELECT * from {user}
    where (login like '{self.lineEdit.text()}' or email like '{self.lineEdit.text()}')
     and password like '{self.lineEdit_2.text()}'""").fetchall():
                self.close()
                if not self.is_adm:
                    self.Open = MainPageUsr((self.lineEdit.text(), self.lineEdit_2.text()), con)
                    self.Open.show()
                else:
                    self.Open = MainPageAdm((self.lineEdit.text(), self.lineEdit_2.text()), con)
                    self.Open.show()
            else:
                self.pushButton.setText('Данные неверны')
                self.pushButton.setStyleSheet('color: red')

    def reg(self):
        self.close()
        self.Open = Registration()
        self.Open.show()

    def ret(self):
        self.close()
        self.Open = first_page.FirstPage()
        self.Open.show()


class Registration(QWidget, RegistrationGUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.confirm)
        self.pushButton_2.clicked.connect(self.ret)
        self.setWindowTitle('Your Order Base')

    def confirm(self):
        self.pushButton.setText('Регистрация')
        self.pushButton.setStyleSheet('color: black')
        if self.lineEdit_4.text() and self.lineEdit_6.text() and self.lineEdit_5.text():
            if cur.execute(f"""SELECT * from users
    where (login like '{self.lineEdit_4.text()}' or email like '{self.lineEdit_6.text()}')""").fetchall():
                self.pushButton.setText('Логин/E-mail уже занят')
                self.pushButton.setStyleSheet('color: red')
            else:
                smtpObj = smtplib.SMTP_SSL("smtp.yandex.ru:465")
                smtpObj.login('pakhomov-sm@yandex.ru', 'Semen1610')
                code = randint(10000, 99999)
                try:
                    smtpObj.sendmail("pakhomov-sm@yandex.ru", self.lineEdit_6.text(),
                                     f"Your personal code is {code}.")
                    smtpObj.close()
                    in_code, ok_pressed = QInputDialog.getText(self, "Проверка",
                                                               "Введите код присланный на введенную почту")
                    if in_code != str(code):
                        self.pushButton.setText('Не верный код проверки')
                        self.pushButton.setStyleSheet('color: red;')
                    else:
                        cur.execute(
                            f"""INSERT into users(login, password, email)
         VALUES('{self.lineEdit_4.text()}', '{self.lineEdit_5.text()}', '{self.lineEdit_6.text()}')""")
                        con.commit()
                        self.pushButton.setText('Успешно')
                        self.pushButton.setStyleSheet('color: green')
                except smtplib.SMTPRecipientsRefused:
                    self.pushButton.setText('Почта некорректна')
                    self.pushButton.setStyleSheet('color: red;')

    def ret(self):
        self.close()
        self.Open = AuthPageUsr()
        self.Open.show()
