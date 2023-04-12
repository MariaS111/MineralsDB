import sys
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets, QtGui
from mnr import WelcomeWindow
from m import MainWindowMinerals
from cl import StartMenu
from main import lst_minerals, lst_use, lst_classes, lst_class, lst_orig, lst_chem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from functools import partial


class WelcomeWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(WelcomeWindow, self).__init__()
        uic.loadUi("mnr.ui", self)

    # def switch(self):
    #     self.switch_window.emit()


class ClassWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ClassWindow, self).__init__()
        uic.loadUi("cl.ui", self)
        self.push_buttons = [QtWidgets.QPushButton(self.centralwidget) for i in range(len(lst_classes))]
        for i in range(len(lst_classes)):
            self.push_buttons[i].setGeometry(QtCore.QRect(570, 510, 131, 45))
            self.gridLayout_2.addWidget(self.push_buttons[i], 1, i)
            font = QtGui.QFont()
            font.setFamily("Centaur")
            font.setPointSize(20)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            j = lst_classes[i]
            self.push_buttons[i].setText(j)
            self.push_buttons[i].setFont(font)
            self.push_buttons[i].setStyleSheet("QPushButton{\n"
                                               "background-color: rgb(200, 177, 178);\n"
                                               "border: 2px ;\n"
                                               "border-radius: 10px;\n"
                                               "}")
            self.push_buttons[i].setObjectName(f"pushButton{i}")


class MainMineralWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainMineralWindow, self).__init__()
        uic.loadUi("m.ui", self)
        self.push_buttons = [QtWidgets.QPushButton(self.centralwidget) for i in range(len(lst_minerals))]
        for i in range(len(lst_minerals)):
            self.push_buttons[i].setGeometry(QtCore.QRect(570, 510, 131, 45))
            if i <= 7:
                self.gridLayout.addWidget(self.push_buttons[i], i, 0)
            else:
                self.gridLayout.addWidget(self.push_buttons[i], i - 8, 1)
            font = QtGui.QFont()
            font.setFamily("Centaur")
            font.setPointSize(20)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            j = lst_minerals[i]
            self.push_buttons[i].setText(j)
            self.push_buttons[i].setFont(font)
            self.push_buttons[i].setStyleSheet("QPushButton{\n"
                                               "background-color: rgb(200, 177, 178);\n"
                                               "border: 2px ;\n"
                                               "border-radius: 10px;\n"
                                               "}")
            self.push_buttons[i].setObjectName(f"pushButton{lst_minerals[i]}")

    #     self.pushButton_3.clicked.connect(self.switch_min_list)
    #
    # def switch_min_list(self):
    #     self.switch_window.emit()


class MainUsageWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainUsageWindow, self).__init__()
        uic.loadUi("m.ui", self)
        self.label_4.setText("Field of usage")
        self.push_buttons = [QtWidgets.QPushButton(self.centralwidget) for i in range(len(lst_use))]
        for i in range(len(lst_use)):
            self.push_buttons[i].setGeometry(QtCore.QRect(570, 510, 131, 45))
            self.gridLayout.addWidget(self.push_buttons[i])
            font = QtGui.QFont()
            font.setFamily("Centaur")
            font.setPointSize(20)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            j = lst_use[i]
            self.push_buttons[i].setText(j)
            self.push_buttons[i].setFont(font)
            self.push_buttons[i].setStyleSheet("QPushButton{\n"
                                               "background-color: rgb(200, 177, 178);\n"
                                               "border: 2px ;\n"
                                               "border-radius: 10px;\n"
                                               "}")
            self.push_buttons[i].setObjectName(f"pushButton{lst_use[i]}")


class MainClassificationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainClassificationWindow, self).__init__()
        uic.loadUi("classif.ui", self)
        self.push_buttons_1 = [QtWidgets.QPushButton(self.centralwidget) for i in range(len(lst_class))]
        self.push_buttons_2 = [QtWidgets.QPushButton(self.centralwidget) for i in range(len(lst_chem))]
        self.push_buttons_3 = [QtWidgets.QPushButton(self.centralwidget) for i in range(len(lst_orig))]
        for i in range(len(lst_class)):
            self.push_buttons_1[i].setGeometry(QtCore.QRect(570, 510, 131, 45))
            self.gridLayout.addWidget(self.push_buttons_1[i], 0, i)
            font = QtGui.QFont()
            font.setFamily("Centaur")
            font.setPointSize(20)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            j = lst_class[i]
            self.push_buttons_1[i].setText(j)
            self.push_buttons_1[i].setFont(font)
            self.push_buttons_1[i].setStyleSheet("QPushButton{\n"
                                               "background-color: rgb(200, 177, 178);\n"
                                               "border: 2px ;\n"
                                               "border-radius: 10px;\n"
                                               "}")
            self.push_buttons_1[i].setObjectName(f"pushButton{j}")
        for i in range(len(lst_chem)):
            self.push_buttons_2[i].setGeometry(QtCore.QRect(570, 510, 131, 45))
            self.gridLayout_2.addWidget(self.push_buttons_2[i])
            font = QtGui.QFont()
            font.setFamily("Centaur")
            font.setPointSize(20)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            j = lst_chem[i]
            self.push_buttons_2[i].setText(j)
            self.push_buttons_2[i].setFont(font)
            self.push_buttons_2[i].setStyleSheet("QPushButton{\n"
                                               "background-color: rgb(200, 177, 178);\n"
                                               "border: 2px ;\n"
                                               "border-radius: 10px;\n"
                                               "}")
            self.push_buttons_2[i].setObjectName(f"pushButton{j}")
        for i in range(len(lst_orig)):
            self.push_buttons_3[i].setGeometry(QtCore.QRect(570, 510, 131, 45))
            self.gridLayout_3.addWidget(self.push_buttons_3[i])
            font = QtGui.QFont()
            font.setFamily("Centaur")
            font.setPointSize(20)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            j = lst_orig[i]
            self.push_buttons_3[i].setText(j)
            self.push_buttons_3[i].setFont(font)
            self.push_buttons_3[i].setStyleSheet("QPushButton{\n"
                                               "background-color: rgb(200, 177, 178);\n"
                                               "border: 2px ;\n"
                                               "border-radius: 10px;\n"
                                               "}")
            self.push_buttons_3[i].setObjectName(f"pushButton{j}")


class Controller:

    def __init__(self):
        pass

    def show_welcome(self):
        self.window = WelcomeWindow()
        self.window.pushButton.clicked.connect(partial(self.show_classes, count=0))
        self.window.show()

    def show_classes(self, count):
        self.window_cl = ClassWindow()
        self.window_cl.push_buttons[2].clicked.connect(self.show_minerals)
        self.window_cl.push_buttons[1].clicked.connect(self.show_usage)
        self.window_cl.push_buttons[0].clicked.connect(self.show_classification)
        if count == 0:
            self.window.close()
        if count == 1:
            self.window_min.close()
        if count == 2:
            self.window_us.close()
        if count == 3:
            self.window_classif.close()
        self.window_cl.show()

    def show_minerals(self):
        self.window_min = MainMineralWindow()
        self.window_min.pushButton_6.clicked.connect(partial(self.show_classes, count=1))
        self.window_cl.close()
        self.window_min.show()

    def show_classification(self):
        self.window_classif = MainClassificationWindow()
        self.window_classif.pushButton_11.clicked.connect(partial(self.show_classes, count=3))
        self.window_cl.close()
        self.window_classif.show()

    # def show_classes_1(self):
    #     self.window_cl_1 = ClassWindow()
    #     self.window_cl_1.push_buttons[2].clicked.connect(self.show_minerals)
    #     self.window_cl_1.push_buttons[1].clicked.connect(self.show_usage)
    #     self.window_min.close()
    #     self.window_cl_1.show()

    def show_usage(self):
        self.window_us = MainUsageWindow()
        self.window_us.pushButton_6.clicked.connect(partial(self.show_classes, count=2))
        self.window_cl.close()
        self.window_us.show()
    #
    # def show_classes_2(self):
    #     self.window_cl_2 = ClassWindow()
    #     self.window_cl_2.push_buttons[2].clicked.connect(self.show_minerals)
    #     self.window_cl_2.push_buttons[1].clicked.connect(self.show_usage)
    #     self.window_us.close()
    #     self.window_cl_2.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_welcome()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
