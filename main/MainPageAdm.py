import smtplib
import sqlite3

from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QTableWidgetItem
from AdmMainPageGUI import AdmMainPageGUI
from random import randint
import AuthPageUsr

COMB = {'Все': '', 'Название': 'title', 'Откуда': '_from', 'Куда': '_to', 'Продавец': 'seller',
        'Было отправлено': 'sent', 'Прибудет': 'arrival', 'Цена': 'price', 'Состояние': 'stage', 'Покупатель': 'buyer',
        'Login': 'login', 'E-mail': 'email'}


class MainPageAdm(QWidget, AdmMainPageGUI):
    def __init__(self, inf, con):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Your Order Base')
        self.con = con
        self.cur = con.cursor()
        self.pushButton_7.clicked.connect(self.redact)
        id, self.login, self.email, self.password, self.first_name, self.last_name, self.company \
            = self.cur.execute(f"""SELECT * from admins
            where (login like '{inf[0]}' or email like '{inf[0]}')
             and password like '{inf[1]}'""").fetchone()
        self.company = self.cur.execute(f"""SELECT title from sellers where id = {self.company}""").fetchone()[0]
        self.lineEdit_14.setPlaceholderText(self.login)
        self.lineEdit_15.setPlaceholderText(self.password)
        self.lineEdit_18.setPlaceholderText(self.email)
        self.lineEdit_13.setPlaceholderText(self.first_name)
        self.lineEdit_16.setPlaceholderText(self.last_name)
        self.lineEdit_17.setPlaceholderText(self.company)
        self.lineEdit_13.setEnabled(False)
        self.lineEdit_16.setEnabled(False)
        self.lineEdit_17.setEnabled(False)
        self.lineEdit_5.setEnabled(False)
        self.comboBox.currentIndexChanged.connect(self.CMBchange)
        self.filter = ''
        self.pushButton_2.clicked.connect(self.purchase)
        self.pushButton_4.clicked.connect(self.db_redact)
        self.pushButton_3.clicked.connect(self.purchase_id)
        self.pushButton.clicked.connect(self.db_redact_order)
        self.id_order_now = ''
        self.pushButton_5.clicked.connect(self.red)
        self.ids_order_now = []

    def redact(self):
        self.lineEdit_14.setStyleSheet('color:black')
        self.lineEdit_18.setStyleSheet('color:black')
        self.pushButton_7.setText('Обновить данные')
        self.pushButton_7.setStyleSheet('color:black')
        if not self.lineEdit_15.text() or not self.lineEdit_14.text() or not self.lineEdit_18.text():
            self.pushButton_7.setText('Заполните все поля!')
            self.pushButton_7.setStyleSheet('color:red;')
        elif self.cur.execute(f"""SELECT * from admins where login like '{self.lineEdit_14.text()}'""").fetchone() \
                and self.login != self.lineEdit_14.text():
            self.lineEdit_14.setText('')
            self.lineEdit_14.setPlaceholderText('Данный логин уже занят')
            self.lineEdit_14.setStyleSheet('color:red;')
        elif self.cur.execute(f"""SELECT * from admins where email like '{self.lineEdit_18.text()}'""").fetchone() \
                and self.email != self.lineEdit_18.text():
            self.lineEdit_18.setText('')
            self.lineEdit_18.setPlaceholderText('Данная почта уже используется')
            self.lineEdit_18.setStyleSheet('color:red;')
        else:
            smtpObj = smtplib.SMTP_SSL("smtp.yandex.ru:465")
            smtpObj.login('pakhomov-sm@yandex.ru', 'Semen1610')
            code = randint(10000, 99999)
            try:
                smtpObj.sendmail("pakhomov-sm@yandex.ru", self.lineEdit_18.text(),
                                 f"Your personal code is {code}.")
                smtpObj.close()
                in_code, ok_pressed = QInputDialog.getText(self, "Проверка",
                                                           "Введите код присланный на введенную почту")
                if in_code != str(code):
                    self.lineEdit_18.setText('')
                    self.lineEdit_18.setPlaceholderText('Не верный код проверки')
                    self.lineEdit_18.setStyleSheet('color: red')
                else:
                    self.login = self.lineEdit_14.text()
                    self.email = self.lineEdit_18.text()
                    self.password = self.lineEdit_15.text()
                    self.con.execute(f"""UPDATE admins
                             SET login = '{self.lineEdit_14.text()}', email = '{self.lineEdit_18.text()}',
                              password = '{self.lineEdit_15.text()}'
                                where login like '{self.login}'""")
                    self.pushButton_7.setText("Успешно!")
                    self.pushButton_7.setStyleSheet('color: green;')
                    self.con.commit()
            except smtplib.SMTPRecipientsRefused:
                self.lineEdit_18.setText('')
                self.lineEdit_18.setPlaceholderText('Не корректная почта')
                self.lineEdit_18.setStyleSheet('color: red')

    def CMBchange(self):
        self.filter = COMB[self.comboBox.currentText()]
        if self.filter:
            self.lineEdit_5.setEnabled(True)
        else:
            self.lineEdit_5.setEnabled(False)

    def CMBchange2(self):
        self.usrfilter = COMB[self.comboBox_2.currentText()]
        if self.filter:
            self.lineEdit_12.setEnabled(True)
        else:
            self.lineEdit_12.setEnabled(False)

    def purchase(self):
        self.pushButton_2.setText('Обновить')
        self.pushButton_2.setStyleSheet('color: black')
        if self.filter != '':
            try:
                res = self.cur.execute(
                    f"""SELECT * from orders
                    where {self.filter} like '{self.lineEdit_5.text()}'
                     and seller in (select id from sellers where title like '{self.company}')""").fetchall()
            except Exception:
                self.pushButton_2.setText('Не верные данные')
                self.pushButton_2.setStyleSheet('color: red')
        else:
            res = self.cur.execute(
                f"""SELECT *
                  from orders where seller in (select id from sellers where title like '{self.company}')""").fetchall()
        if not res:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return 0
        self.pretty_result_to_table(res)
        self.print_res(res)

    def pretty_result_to_table(self, res):
        for i in range(len(res)):
            res[i] = list(res[i])
            res[i][-3] = self.cur.execute(f"""select title from stages where id = {res[i][-3]}""").fetchone()[0]
            res[i][-2] = self.cur.execute(f"""select title from sellers where id = {res[i][-2]}""").fetchone()[0]
            res[i][-1] = self.cur.execute(f"""select login from users where id = {res[i][-1]}""").fetchone()[0]

    def print_res(self, res):
        self.ids_order_now = []
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Откуда', 'Куда', 'Отправлено', 'Прибудет', 'Цена',
             'Состояние', 'Продавец', 'Покупатель'])
        for i, row in enumerate(res):
            self.ids_order_now.append(row[0])
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def pretty_result_from_table(self, res):
        for i in range(len(res)):
            res[i] = list(res[i])
            res[i][-3] = self.cur.execute(f"""select id from stages where title like '{res[i][-3]}'""").fetchone()[0]
            res[i][-2] = self.cur.execute(f"""select id from sellers where title like '{res[i][-2]}'""").fetchone()[0]
            res[i][-1] = self.cur.execute(f"""select id from users where login like '{res[i][-1]}'""").fetchone()[0]

    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Вы уверенны?")
        msgBox.setText('Прежние данные будет не вернуть!')
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return msgBox.exec() == QMessageBox.Ok

    def db_redact(self):
        res = []
        if self.showDialog():
            for i in range(self.tableWidget.rowCount()):
                res.append([])
                for j in range(self.tableWidget.columnCount()):
                    res[i].append(self.tableWidget.item(i, j).text())
            try:
                self.pretty_result_from_table(res)
                for i in range(len(res)):
                    self.cur.execute(
                        f"""UPDATE orders set title = '{res[i][1]}', _from = '{res[i][2]}', _to = '{res[i][3]}',
                         sent = '{res[i][4]}', arrival = '{res[i][5]}', price = '{res[i][6]}', stage = {res[i][7]},
                        seller = {res[i][8]}, buyer = {res[i][9]} where id = {self.ids_order_now[i]}""")
                self.con.commit()
                self.pushButton_4.setStyleSheet('color: green')
                self.pushButton_4.setText('Успешно!')
            except TypeError:
                self.pushButton_4.setStyleSheet('color: red')
                self.pushButton_4.setText('Данные не корректы!')

    def purchase_id(self):
        self.pushButton_3.setText('Обновить')
        self.pushButton_3.setStyleSheet('color: black')
        self.pushButton.setStyleSheet('color: black')
        self.pushButton.setText('Сохранить')
        try:
            res = self.cur.execute(
                f"""select * from orders where id = {self.lineEdit_4.text()} and seller in 
                (select id from sellers where title = '{self.company}')""").fetchone()
            if res:
                res = [res[1:]]
                self.pretty_result_to_table(res)
                res = list(map(str, res[0]))
                self.lineEdit_11.setText(res[0])
                self.lineEdit_10.setText(res[1])
                self.lineEdit_9.setText(res[2])
                self.lineEdit_8.setText(res[3])
                self.lineEdit_7.setText(res[4])
                self.lineEdit_6.setText(res[5])
                self.lineEdit_3.setText(res[6])
                self.lineEdit_2.setText(res[7])
                self.lineEdit.setText(res[8])
                self.id_order_now = self.lineEdit_4.text()
            else:
                self.pushButton_3.setText("Этот id не найден или не принадлежит вашей компании")
                self.pushButton_3.setStyleSheet('color: red')
        except sqlite3.OperationalError or TypeError:
            self.pushButton_3.setText('id не корректен')
            self.pushButton_3.setStyleSheet('color: red')

    def db_redact_order(self):
        self.pushButton_3.setText('Обновить')
        self.pushButton_3.setStyleSheet('color: black')
        self.pushButton.setStyleSheet('color: black')
        self.pushButton.setText('Сохранить')
        if self.id_order_now:
            if self.showDialog():
                res = [
                    [self.lineEdit_11.text(), self.lineEdit_10.text(), self.lineEdit_9.text(), self.lineEdit_8.text(),
                     self.lineEdit_7.text(), self.lineEdit_6.text(), self.lineEdit_3.text(), self.lineEdit_2.text(),
                     self.lineEdit.text()]]
                try:
                    self.pretty_result_from_table(res)
                    for i in range(len(res)):
                        self.cur.execute(f"""UPDATE orders
                            set title = '{res[i][0]}', _from = '{res[i][1]}', _to = '{res[i][2]}',
                             sent = '{res[i][3]}', arrival = '{res[i][4]}', price = '{res[i][5]}', stage = {res[i][6]},
                            seller = {res[i][7]}, buyer = {res[i][8]} where id = {self.id_order_now}""")
                        self.con.commit()
                        self.pushButton.setStyleSheet('color: green')
                        self.pushButton.setText('Успешно!')
                except TypeError:
                    self.pushButton.setStyleSheet('color: red')
                    self.pushButton.setText('Данные не корректы!')

    def red(self):
        self.close()
        self.Open = AuthPageUsr.AuthPageUsr(True)
        self.Open.show()
