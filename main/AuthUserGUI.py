from PyQt5 import QtCore, QtGui, QtWidgets


class AuthGUI(object):
    def setupUi(self, auth_page_usr):
        auth_page_usr.setObjectName("auth_page_usr")
        auth_page_usr.resize(965, 665)
        self.gridLayout = QtWidgets.QGridLayout(auth_page_usr)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, 150, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(auth_page_usr)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(auth_page_usr)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(500, 16777215))
        self.lineEdit_2.setStyleSheet("")
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setFrame(True)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_2.setDragEnabled(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 150, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(auth_page_usr)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(auth_page_usr)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QtCore.QSize(500, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(auth_page_usr)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.label_4 = QtWidgets.QLabel(auth_page_usr)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton = QtWidgets.QPushButton(auth_page_usr)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(auth_page_usr)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 3)

        self.retranslateUi(auth_page_usr)
        QtCore.QMetaObject.connectSlotsByName(auth_page_usr)

    def retranslateUi(self, auth_page_usr):
        _translate = QtCore.QCoreApplication.translate
        auth_page_usr.setWindowTitle(_translate("auth_page_usr", "Form"))
        self.label_2.setText(_translate("auth_page_usr", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Пароль</span></p></body></html>"))
        self.lineEdit_2.setPlaceholderText(_translate("auth_page_usr", "Ваш пароль от учетной записи"))
        self.label.setText(_translate("auth_page_usr", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Логин/Email</span></p></body></html>"))
        self.lineEdit.setPlaceholderText(_translate("auth_page_usr", "Ваш логин/email учетной записи"))
        self.pushButton_3.setText(_translate("auth_page_usr", "<-"))
        self.label_4.setToolTip(_translate("auth_page_usr", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Авторизация</span></p></body></html>"))
        self.label_4.setText(_translate("auth_page_usr", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Авторизация</span></p></body></html>"))
        self.pushButton.setText(_translate("auth_page_usr", "Продолжить"))
        self.pushButton_2.setText(_translate("auth_page_usr", "Регистрация"))