import sys

from PyQt5.Qt import QApplication
from kernel import FirstPage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstPage.FirstPage()
    ex.show()
    sys.exit(app.exec())

"""Тестовые данные для входа и за user и за admin:
    login -> test
    password -> test
    email -> test@yandex.ru"""