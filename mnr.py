from PyQt5 import QtCore, QtGui, QtWidgets
from cl import StartMenu
import sys


class WelcomeWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1261, 841)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-20, 0, 1261, 841))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../Users/maria/Downloads/mnrl.FmiML.jpg"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(460, 360, 351, 91))
        font = QtGui.QFont()
        font.setFamily("Felix Titling")
        font.setPointSize(35)
        self.label_2.setFont(font)
        self.label_2.setLineWidth(20)
        self.label_2.setMidLineWidth(20)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(540, 430, 241, 51))
        font = QtGui.QFont()
        font.setFamily("Centaur")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(570, 510, 131, 45))
        font = QtGui.QFont()
        font.setFamily("Centaur")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
                                      "background-color: rgb(200, 177, 178);\n"
                                      "border: 2px ;\n"
                                      "border-radius: 10px;\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1261, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.go_win1)
        self.pushButton.show()

        # self.pushButton.clicked.connect(self.show_window_1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    # def show_window_1(self):
    #     #self.window = QtWidgets.QMainWindow()
    #     self.w1 = StartMenu()
    #     self.w1.setupUi(MainWindow)
    #     #self.window.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Minerals"))
        self.label_3.setText(_translate("MainWindow", "Get a better understanding"))
        self.pushButton.setText(_translate("MainWindow", "Begin"))

#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = WelcomeWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
