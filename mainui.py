import sys
import math
import requests
from PyQt5 import uic
from main import lst_minerals, lst_use, lst_classes, lst_class, lst_orig, lst_chem, rels, execute_query_rel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from functools import partial
from SPARQLWrapper import SPARQLWrapper, JSON

rep = 'http://LAPTOP-FRRSP1GB:7200/repositories/Mineral'
endpoint = SPARQLWrapper(rep)


def execute_query_rel(sourse_query):
    endpoint.setQuery(sourse_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    rez = []
    for result in results['results']['bindings']:
        rez.append((result['sub']['value'] + ' ', result['pName']['value'] + ' ', result['obj']['value'] + ' '))
    return rez


def execute_query(sourse_query):
    endpoint.setQuery(sourse_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    rez = []
    for result in results['results']['bindings']:
        rez.append(result['pName']['value'])
    return rez


class WelcomeWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(WelcomeWindow, self).__init__()
        uic.loadUi("mnr.ui", self)


class ClassWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(ClassWindow, self).__init__()
        uic.loadUi("cl.ui", self)
        self.pushButton_2.clicked.connect(self.add_prop_to_db)
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
        self.push_buttons[2].clicked.connect(self.show_min)
        self.push_buttons[1].clicked.connect(self.show_use)
        self.push_buttons[0].clicked.connect(self.show_classif)
        self.push_buttons[3].clicked.connect(self.show_hard)

    def show_min(self):
        self.close()
        self.window_min = MainMineralWindow()
        self.window_min.show()
        self.window_min.update()
        self.window_min.pushButton_6.clicked.connect(self.remove_min)

    def remove_min(self):
        self.window_min.close()
        self.show()

    def show_use(self):
        self.close()
        self.window_use = MainUsageWindow()
        self.window_use.show()
        self.window_use.update()

        self.window_use.pushButton_6.clicked.connect(self.remove_use)

    def remove_use(self):
        self.window_use.close()
        self.show()

    def show_classif(self):
        self.close()
        self.window_classif = MainClassificationWindow()
        self.window_classif.show()
        self.window_classif.pushButton_11.clicked.connect(self.remove_classif)

    def remove_classif(self):
        self.window_classif.close()
        self.show()

    def show_hard(self):
        self.close()
        self.window_hard = MainHardnessWindow()
        self.window_hard.show()
        self.window_hard.pushButton_6.clicked.connect(self.remove_hard)

    def remove_hard(self):
        self.window_hard.close()
        self.show()

    def add_property(self):
        text, ok = QInputDialog.getText(self, 'Input window', 'Enter new property:')
        if ok:
            print('You entered:', text)
        return text

    def add_prop_to_db(self):
        name = self.add_property()
        if name:
            query = f'''
                       PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                       PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        INSERT DATA
                        {{
                           :{name} a owl:ObjectProperty.
                        }}
                   '''
            url = rep + '/statements'
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "update": query
            }
            response = requests.post(url, headers=headers, data=data)
            if response.ok:
                print("Property added successfully!")
                self.update()
            else:
                print("Error:", response.text)


class MainMineralWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainMineralWindow, self).__init__()
        uic.loadUi("m.ui", self)
        self.pushButton_7.clicked.connect(self.add_min_to_db)
        self.query_minerals = """
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
            SELECT (strafter(str(?p), \'#\') AS ?pName)
            WHERE {
                ?p a :Minerals.
            }
        """

    def update(self):
        self.lst_minerals = list(execute_query(self.query_minerals))
        self.push_buttons = [QtWidgets.QPushButton(self.centralwidget) for i in range(len(self.lst_minerals))]
        for i in range(len(self.lst_minerals)):
            self.push_buttons[i].setGeometry(QtCore.QRect(570, 510, 131, 45))
            if i <= math.ceil(len(self.lst_minerals)/2)-1:
                self.gridLayout.addWidget(self.push_buttons[i], i, 0)
            else:
                self.gridLayout.addWidget(self.push_buttons[i], i-math.ceil(len(self.lst_minerals)/2), 1)
            font = QtGui.QFont()
            font.setFamily("Centaur")
            font.setPointSize(20)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            j = self.lst_minerals[i]
            self.push_buttons[i].setText(j)
            self.push_buttons[i].setFont(font)
            self.push_buttons[i].setStyleSheet("QPushButton{\n"
                                               "background-color: rgb(200, 177, 178);\n"
                                               "border: 2px ;\n"
                                               "border-radius: 10px;\n"
                                               "}")
            self.push_buttons[i].clicked.connect(partial(self.show_obj, j=j))
            self.push_buttons[i].setObjectName(f"pushButton{self.lst_minerals[i]}")

    def show_obj(self, j):
        self.close()
        self.window_obj = MainObjectWindow(j)
        self.window_obj.show()
        self.window_obj.pushButton_7.setText('Delete instance')
        self.window_obj.pushButton_7.clicked.connect(lambda: self.del_instance(j))
        self.window_obj.pushButton_6.clicked.connect(self.remove_obj)

    def remove_obj(self):
        self.window_obj.close()
        self.show()
        self.update()

    def add_min(self):
        text, ok = QInputDialog.getText(self, 'Input window', 'Enter name:')
        if ok:
            print('You entered:', text)
        return text

    def add_min_to_db(self):
        name = self.add_min()
        if name:
            query = f'''
                    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                    INSERT DATA {{
                        :{name} a :Minerals .
                    }}
                '''
            url = rep + '/statements'
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "update": query
            }
            response = requests.post(url, headers=headers, data=data)
            if response.ok:
                print("Mineral added successfully!")
                self.update()
            else:
                print("Error:", response.text)

    def del_instance(self, nam):
        entity_name = nam
        que = f''' 
         PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
        DELETE WHERE {{ :{entity_name} ?p ?o }}
        '''

        url = rep + '/statements'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "update": que
        }
        response = requests.post(url, headers=headers, data=data)
        if response.ok:
            print("Mineral deleted successfully!")
            # self.update()
            # button_name = "pushButton"+nam  # имя кнопки, которую нужно удалить
            # button = self.findChild(QtWidgets.QPushButton, button_name)  # поиск кнопки по имени
            # if button is not None:  # если кнопка найдена
            #     button.deleteLater()
            self.remove_obj()

        else:
            print("Error:", response.text)


class MainUsageWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainUsageWindow, self).__init__()
        uic.loadUi("m.ui", self)
        self.label_4.setText("Field of usage")
        self.pushButton_7.clicked.connect(self.add_use_to_db)
        self.query_usage = """
                    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                    SELECT (strafter(str(?p), \'#\') AS ?pName)
                    WHERE {
                        ?p a :FieldOfUsage.
                    }
                """

    def update(self):
        self.lst_use = list(execute_query(self.query_usage))
        self.push_buttons = [QtWidgets.QPushButton(self.centralwidget) for i in range(len(self.lst_use))]
        for i in range(len(self.lst_use)):
            self.push_buttons[i].setGeometry(QtCore.QRect(570, 510, 131, 45))
            if i <= math.ceil(len(self.lst_use) / 2) - 1:
                self.gridLayout.addWidget(self.push_buttons[i], i, 0)
            else:
                self.gridLayout.addWidget(self.push_buttons[i], i - math.ceil(len(self.lst_use) / 2), 1)
            font = QtGui.QFont()
            font.setFamily("Centaur")
            font.setPointSize(20)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            j = self.lst_use[i]
            self.push_buttons[i].setText(j)
            self.push_buttons[i].setFont(font)
            self.push_buttons[i].setStyleSheet("QPushButton{\n"
                                               "background-color: rgb(200, 177, 178);\n"
                                               "border: 2px ;\n"
                                               "border-radius: 10px;\n"
                                               "}")
            self.push_buttons[i].clicked.connect(partial(self.show_obj, j=j))
            self.push_buttons[i].setObjectName(f"pushButton{self.lst_use[i]}")

    def add_use(self):
        text, ok = QInputDialog.getText(self, 'Input window', 'Enter name:')
        if ok:
            print('You entered:', text)
        return text

    def add_use_to_db(self):
        name = self.add_use()
        if name:
            query = f'''
                       PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                       INSERT DATA {{
                           :{name} a :FieldOfUsage.
                       }}
                   '''
            url = rep + '/statements'
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "update": query
            }
            response = requests.post(url, headers=headers, data=data)
            if response.ok:
                print("Mineral added successfully!")
                self.update()
            else:
                print("Error:", response.text)

    def show_obj(self, j):
        self.close()
        self.window_obj = MainObjectWindow(j)
        self.window_obj.show()
        self.window_obj.pushButton_7.clicked.connect(lambda: self.del_instance(j))
        self.window_obj.pushButton_6.clicked.connect(self.remove_obj)
        self.window_obj.pushButton_7.setText('Delete instance')

    def remove_obj(self):
        self.window_obj.close()
        self.show()
        self.update()

    def del_instance(self, nam):
        entity_name = nam
        que = f''' 
           PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
          DELETE WHERE {{ :{entity_name} ?p ?o }}
          '''

        url = rep + '/statements'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "update": que
        }
        response = requests.post(url, headers=headers, data=data)
        if response.ok:
            print("Deleted successfully!")
            self.update()
            button_name = "pushButton" + nam  # имя кнопки, которую нужно удалить
            button = self.findChild(QtWidgets.QPushButton, button_name)  # поиск кнопки по имени
            if button is not None:  # если кнопка найдена
                button.deleteLater()
            self.remove_obj()

        else:
            print("Error:", response.text)


class MainHardnessWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainHardnessWindow, self).__init__()
        uic.loadUi("m.ui", self)
        self.label_4.setText("The Mohs Hardness Scale")
        self.label_4.setGeometry(220, 150, 820, 200)
        button = self.findChild(QtWidgets.QPushButton, 'pushButton_7')  # поиск кнопки по имени
        if button is not None:  # если кнопка найдена
            button.deleteLater()
        self.query_hard = """
                   PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                   SELECT (strafter(str(?p), \'#\') AS ?pName)
                   WHERE {
                       ?p a :TheMohsHardnessScale.
                   }
               """
        self.lst_hard = list(execute_query(self.query_hard))
        self.lst_hard =[str(i) for i in (sorted([int(i) for i in self.lst_hard]))]
        self.push_buttons = [QtWidgets.QPushButton(self.centralwidget) for i in range(len(self.lst_hard))]
        for i in range(len(self.lst_hard)):
            self.push_buttons[i].setGeometry(QtCore.QRect(570, 510, 131, 45))
            self.gridLayout.addWidget(self.push_buttons[i])
            font = QtGui.QFont()
            font.setFamily("Centaur")
            font.setPointSize(20)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            j = self.lst_hard[i]
            self.push_buttons[i].setText(j)
            self.push_buttons[i].setFont(font)
            self.push_buttons[i].setStyleSheet("QPushButton{\n"
                                               "background-color: rgb(200, 177, 178);\n"
                                               "border: 2px ;\n"
                                               "border-radius: 10px;\n"
                                               "}")
            self.push_buttons[i].setObjectName(f"pushButton{self.lst_hard[i]}")
            print(j)
            self.push_buttons[i].clicked.connect(partial(self.show_obj, j=j))

    def show_obj(self, j):
        self.close()
        self.window_obj = MainObjectWindow(j)
        self.window_obj.show()
        button = self.window_obj.findChild(QtWidgets.QPushButton, 'pushButton_7')  # поиск кнопки по имени
        if button is not None:  # если кнопка найдена
            button.deleteLater()
        self.window_obj.pushButton_6.clicked.connect(self.remove_obj)

    def remove_obj(self):
        self.window_obj.close()
        self.show()
        self.update()


class MainClassificationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainClassificationWindow, self).__init__()
        uic.loadUi("classif.ui", self)  # имя кнопки, которую нужно удалить
        button = self.findChild(QtWidgets.QPushButton, 'pushButton_10')  # поиск кнопки по имени
        if button is not None:  # если кнопка найдена
            button.deleteLater()
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


class MainObjectWindow(QtWidgets.QMainWindow):
    def __init__(self, name):
        super(MainObjectWindow, self).__init__()
        uic.loadUi("m.ui", self)
        self.label_4.setText(name)
        # button = self.findChild(QtWidgets.QPushButton, 'pushButton_7')  # поиск кнопки по имени
        # if button is not None:  # если кнопка найдена
        #     button.deleteLater()
        self.label_4.setGeometry(250, 200, 700, 100)
        self.add_relation = QtWidgets.QPushButton(self.centralwidget)
        self.add_relation.setGeometry(QtCore.QRect(1020, 390, 201, 51))
        font = QtGui.QFont()
        font.setFamily("Centaur")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.add_relation.setText('Add relation')
        self.add_relation.setFont(font)
        self.add_relation.setStyleSheet("QPushButton{\n"
                                              "background-color: rgb(200, 177, 178);\n"
                                              "border: 2px ;\n"
                                              "border-radius: 10px;\n"
                                              "}")
        self.add_relation.setObjectName(f"pushButton_add_relation")
        self.add_relation.clicked.connect(self.add_rel)
        self.name = name
        rels = f"""
              PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
              PREFIX owl: <http://www.w3.org/2002/07/owl#>
              PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
              SELECT DISTINCT (strafter(str(?p), \'#\') AS ?pName) (strafter(str(?subject), \'#\') AS ?sub) (strafter(str(?object), \'#\') AS ?obj)
              WHERE {{
             {{
                ?subject ?p ?object .
                ?p rdf:type owl:ObjectProperty .
                FILTER(?subject = :{self.name}).
              }}
              UNION
              {{
                ?subject ?p ?object .
                ?p rdf:type owl:ObjectProperty .
                FILTER(?object = :{self.name}).
              }}
              }}
        """
        rel = """
              PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
              PREFIX owl: <http://www.w3.org/2002/07/owl#>
              SELECT DISTINCT (strafter(str(?p), \'#\') AS ?pName) 
              WHERE { 
              ?p rdf:type owl:ObjectProperty.
              } 
        """
        ent = '''
         PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
              PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT (strafter(str(?p), \'#\') AS ?pName) 
        WHERE {
         ?p a owl:NamedIndividual .
        }
        '''
        self.lst_ent = list(execute_query(ent))
        self.lst_rel = list(execute_query(rel))
        lst_rels = list(execute_query_rel(rels))
        self.push_buttons = [[QtWidgets.QPushButton(self.centralwidget) for i in range(len(lst_rels[i]))] for i in
                             range(len(lst_rels))]
        for i in range(len(self.push_buttons)):
            for j in range(len(self.push_buttons[i])):
                self.push_buttons[i][j].setGeometry(QtCore.QRect(570, 510, 131, 45))
                if j == 0:
                    self.gridLayout.addWidget(self.push_buttons[i][j], i, 0)
                elif j == 1:
                    self.gridLayout.addWidget(self.push_buttons[i][j], i, 1)
                else:
                    self.gridLayout.addWidget(self.push_buttons[i][j], i, 2)
                font = QtGui.QFont()
                font.setFamily("Centaur")
                font.setPointSize(20)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                nam = lst_rels[i][j]
                self.push_buttons[i][j].setText(nam)
                self.push_buttons[i][j].setFont(font)
                self.push_buttons[i][j].setStyleSheet("QPushButton{\n"
                                                      "background-color: rgb(200, 177, 178);\n"
                                                      "border: 2px ;\n"
                                                      "border-radius: 10px;\n"
                                                      "}")
                self.push_buttons[i][j].setObjectName(f"pushButton{lst_rels[i][j]}")

    def add_rel(self):
        self.dialog = AddRelDialog(self.name, self.lst_rel, self.lst_ent)
        self.dialog.show()


class AddRelDialog(QDialog):
    def __init__(self, sub, rels, objects, parent=None):
        super().__init__(parent)
        self.sub = sub
        # Set the dialog properties
        self.setWindowTitle(sub)

        self.layout = QVBoxLayout(self)

        self.rels = rels
        # Create the label and dropdown menu for the first option
        option1_label = QLabel('Property:', self)
        self.layout.addWidget(option1_label)
        self.option1_select = QComboBox(self)
        self.option1_select.addItems(self.rels)
        self.layout.addWidget(self.option1_select)
        self.objects = objects
        # Create the label and dropdown menu for the second option
        option2_label = QLabel('Instanse2:', self)
        self.layout.addWidget(option2_label)
        self.option2_select = QComboBox(self)
        self.option2_select.addItems(self.objects)
        self.layout.addWidget(self.option2_select)

        # Create the OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def get_options(self):
        return self.sub, self.option1_select.currentText(), self.option2_select.currentText()


class Controller:

    def __init__(self):
        pass

    def show_welcome(self):
        self.window = WelcomeWindow()
        self.window.pushButton.clicked.connect(self.show_classes)
        self.window.show()

    def show_classes(self):
        self.window.close()
        self.window_cl = ClassWindow()
        self.window_cl.show()


    #     if count == 0:
    #         self.window.close()
    #     if count == 1:
    #         self.window_min.close()
    #     if count == 2:
    #         self.window_us.close()
    #     if count == 3:
    #         self.window_classif.close()
    #     self.window_cl.show()
    #
    # def show_minerals(self):
    #     self.window_min = MainMineralWindow()
    #     self.window_min.pushButton_6.clicked.connect(partial(self.show_classes, count=1))
    #     self.window_min.pushButton_6.clicked.connect(partial(self.show_classes, count=1))
    #     self.window_cl.close()
    #     self.window_min.show()
    #
    # def show_classification(self):
    #     self.window_classif = MainClassificationWindow()
    #     self.window_classif.pushButton_11.clicked.connect(partial(self.show_classes, count=3))
    #     self.window_cl.close()
    #     self.window_classif.show()
    #
    # def show_usage(self):
    #     self.window_us = MainUsageWindow()
    #     self.window_us.pushButton_6.clicked.connect(partial(self.show_classes, count=2))
    #     self.window_cl.close()
    #     self.window_us.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_welcome()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
