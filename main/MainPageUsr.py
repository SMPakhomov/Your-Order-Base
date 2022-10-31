import smtplib
import random
from UsersMainPageGUI import UsrMainPageGUI
from PyQt5.QtWidgets import QWidget, QInputDialog, QTableWidgetItem
import AuthPageUsr

COMB = {'Все': '', 'Название': 'title', 'Откуда': '_from', 'Куда': '_to', 'Продавец': 'seller',
        'Было отправлено': 'sent', 'Прибудет': 'arrival', 'Цена': 'price', 'Состояние': 'stage'}


class MainPageUsr(QWidget, UsrMainPageGUI):
    def __init__(self, inf, con):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Your Order Base')
        self.con = con
        self.cur = con.cursor()
        self.pushButton.clicked.connect(self.redact)
        self.login, self.email, self.password = self.cur.execute(f"""SELECT login, email, password from users
    where (login like '{inf[0]}' or email like '{inf[0]}')
     and password like '{inf[1]}'""").fetchone()
        self.lineEdit_2.setPlaceholderText(self.login)
        self.lineEdit.setPlaceholderText(self.password)
        self.lineEdit_3.setPlaceholderText(self.email)
        self.pushButton_2.clicked.connect(self.my_purchase)
        self.pushButton_3.clicked.connect(self.orders_search)
        self.lineEdit_5.setEnabled(False)
        self.comboBox.currentIndexChanged.connect(self.cmbchange)
        self.filter = ''
        self.pushButton_4.clicked.connect(self.help)
        self.pushButton_5.clicked.connect(self.ret)

    def redact(self):
        self.lineEdit_2.setStyleSheet('color:black')
        self.lineEdit_3.setStyleSheet('color:black')
        if not self.lineEdit.text() or not self.lineEdit_2.text() or not self.lineEdit_3.text():
            self.pushButton.setText('Заполните все поля!')
            self.pushButton.setStyleSheet('color:red;')
        elif self.cur.execute(f"""SELECT * from users where login like '{self.lineEdit_2.text()}'""").fetchone() \
                and self.login != self.lineEdit_2.text():
            self.lineEdit_2.setText('')
            self.lineEdit_2.setPlaceholderText('Данный логин уже занят')
            self.lineEdit_2.setStyleSheet('color:red;')
        elif self.cur.execute(f"""SELECT * from users where email like '{self.lineEdit_3.text()}'""").fetchone() \
                and self.email != self.lineEdit_3.text():
            self.lineEdit_3.setText('')
            self.lineEdit_3.setPlaceholderText('Данная почта уже используется')
            self.lineEdit_3.setStyleSheet('color:red;')
        else:
            smtpObj = smtplib.SMTP_SSL("smtp.yandex.ru:465")
            smtpObj.login('pakhomov-sm@yandex.ru', 'Semen1610')
            code = random.randint(10000, 99999)
            try:
                smtpObj.sendmail("pakhomov-sm@yandex.ru", self.lineEdit_3.text(),
                                 f"Your personal code is {code}.")
                smtpObj.close()
                in_code, ok_pressed = QInputDialog.getText(self, "Проверка",
                                                           "Введите код присланный на введенную почту")
                if in_code != str(code):
                    self.lineEdit_3.setText('')
                    self.lineEdit_3.setPlaceholderText('Не верный код проверки')
                    self.lineEdit_3.setStyleSheet('color: red;')
                else:
                    self.con.execute(f"""UPDATE users
                     SET login = '{self.lineEdit_2.text()}', email = '{self.lineEdit_3.text()}',
                      password = '{self.lineEdit.text()}'
                        where login like '{self.login}'""")
                    self.pushButton.setText("Успешно!")
                    self.pushButton.setStyleSheet('color: green;')
                    self.con.commit()
                    self.login = self.lineEdit_2.text()
                    self.email = self.lineEdit_3.text()
                    self.password = self.lineEdit.text()
            except smtplib.SMTPRecipientsRefused:
                self.lineEdit_3.setText('')
                self.lineEdit_3.setPlaceholderText('Не корректная почта')
                self.lineEdit_3.setStyleSheet('color:red;')

    def cmbchange(self):
        self.filter = COMB[self.comboBox.currentText()]
        if self.filter:
            self.lineEdit_5.setEnabled(True)
        else:
            self.lineEdit_5.setEnabled(False)

    def my_purchase(self):
        if self.filter != '':
            res = self.cur.execute(
                f"""SELECT * from orders
                where buyer in (select id from users where login like '{self.login}')
                 and {self.filter} like '{self.lineEdit_5.text()}'""").fetchall()
        else:
            res = self.cur.execute(
                f"""SELECT *
                  from orders where buyer in (select id from users where login like '{self.login}')""").fetchall()
        if not res:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return 0
        res = list(map(lambda x: x[:-1], res))
        self.pretty_result(res)
        self.print_res(res)

    def pretty_result(self, res):
        for i in range(len(res)):
            res[i] = list(res[i])
            res[i][-2] = self.cur.execute(f"""select title from stages where id = {res[i][-2]}""").fetchone()[0]
            res[i][-1] = self.cur.execute(f"""select title from sellers where id = {res[i][-1]}""").fetchone()[0]

    def orders_search(self):
        try:
            order_id = self.lineEdit_4.text()
            self.pushButton_3.setText('Обновить')
            self.pushButton_3.setStyleSheet('color: black')
            order_info = self.cur.execute(f"""select * from orders where id = '{order_id}'""").fetchone()
            order_info = [list(map(str, order_info))]
            order_info[0] = order_info[0][1:-1]
            if order_info:
                self.pretty_result(order_info)
                order_info = order_info[0]
                self.label_8.setText(order_info[0])
                self.label_11.setText(order_info[1])
                self.label_21.setText(order_info[2])
                self.label_23.setText(order_info[3])
                self.label_15.setText(order_info[4])
                self.label_19.setText(order_info[7])
                self.label_16.setText(order_info[6] + '.')
                self.label_13.setText(order_info[5])
        except Exception:
            self.pushButton_3.setText('Введите корректный id')
            self.pushButton_3.setStyleSheet('color: red')

    def print_res(self, res):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Откуда', 'Куда', 'Отправлено', 'Прибудет', 'Цена',
             'Состояние', 'Продавец'])
        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def help(self):
        smtpObj = smtplib.SMTP_SSL("smtp.yandex.ru:465")
        smtpObj.login('pakhomov-sm@yandex.ru', 'Semen1610')
        smtpObj.sendmail('pakhomov-sm@yandex.ru', 'sem.pakhomov2007@yandex.ru',
                         self.textEdit_2.toPlainText() + f' Login: {self.login}; Email: {self.email};')
        self.textEdit_2.setText('')
        self.pushButton_4.setText('Успешно!')
        self.pushButton_4.setStyleSheet('color: green')
        smtpObj.close()

    def ret(self):
        self.close()
        self.Open = AuthPageUsr.AuthPageUsr()
        self.Open.show()