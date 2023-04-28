import sys
import math
import requests
from PyQt5 import uic
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
        self.pushButton_3.clicked.connect(self.del_prop_from_db)
        self.pushButton_4.clicked.connect(self.add_rel_to_db)
        self.pushButton_5.clicked.connect(self.del_rel_from_db)
        self.pushButton_6.clicked.connect(self.add_class_to_db)
        self.pushButton_7.clicked.connect(self.del_class_from_db)
        self.pushButton_8.clicked.connect(self.query)
        self.pushButton_9.clicked.connect(self.show_rels)
        self.query = '''
        SELECT DISTINCT (strafter(str(?class), \'#\') AS ?pName) WHERE {
          ?class a owl:Class .
          FILTER NOT EXISTS { ?class rdfs:subClassOf ?superclass }
        }
        '''

    def update(self):
        lst_classes = list(execute_query(self.query))
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

    def add_prop_to_db(self):
        self.property_edit1 = QLineEdit()
        self.property_edit_sub1 = QLineEdit()
        self.property_edit_sub2 = QLineEdit()
        property_name, ok = QInputDialog.getText(self, 'Добавить новое свойство', 'Введите название свойства:')
        if ok and property_name:
            self.property_edit1.setText(property_name)
            domain_uri, ok = QInputDialog.getText(self, 'Добавить новое свойство', 'Введите URI класса домена:')
            if ok and domain_uri:
                self.property_edit_sub1.setText(domain_uri)
                range_uri, ok = QInputDialog.getText(self, 'Добавить новое свойство', 'Введите URI класса диапазона:')
                if ok and range_uri:
                    self.property_edit_sub2.setText(range_uri)
                    property_uri = self.property_edit1.text()
                    domain_uri = self.property_edit_sub1.text()
                    range_uri = self.property_edit_sub2.text()
                else:
                    return
        # Check if class_uri exists in the ontology
        check_query = f"""
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX :<http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>

                            ASK {{
                                :{domain_uri} rdf:type owl:Class .
                            }}
                            """

        url = rep
        headers = {"Accept": "application/sparql-results+json"}
        data = {"query": check_query}

        response = requests.post(url, headers=headers, data=data)

        # Check the response to see if superclass_name exists in the ontology
        superclass_exists = response.json()['boolean']
        if not superclass_exists:
            print("Error: class_name for domain not found")
            self.result_browser.clear()
            self.result_browser.insertPlainText("Error: class_name for domain not found")
            return

        # Check if class_uri exists in the ontology
        check_query1 = f"""
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>

                        ASK {{
                            :{range_uri} rdf:type owl:Class .
                        }}
                        """

        url = rep
        headers = {"Accept": "application/sparql-results+json"}
        data = {"query": check_query1}

        response = requests.post(url, headers=headers, data=data)

        # Check the response to see if superclass_name exists in the ontology
        superclass_exists = response.json()['boolean']
        if not superclass_exists:
            print("Error: class_name for range not found")
            self.result_browser.clear()
            self.result_browser.insertPlainText("Error: class_name for range not found")
            return
        # Set up the query
        query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>

                INSERT DATA {:%s
                    rdf:type owl:ObjectProperty ;
                    rdfs:domain :%s ;
                    rdfs:range :%s .}
                """ % (property_uri, domain_uri, range_uri)

        # Set up the request
        url = rep
        headers = {"Content-Type": "application/sparql-update"}
        data = query

        # Send the request
        response = requests.post(url, headers=headers, data=data)

        # Check the response
        if response.ok:
            print("Property added successfully!")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText('Property added successfully')
        else:
            print("Error:", response.text)
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error:" + response.text)

    def del_prop_from_db(self):
        pr, ok = QInputDialog.getText(self, 'Удалить свойство:', 'Введите название свойства:')
        self.delete_property_edit = QLineEdit()
        if ok and pr:
            self.delete_property_edit.setText(pr)
        else:
            return
        property = self.delete_property_edit.text()
        # Check if class_uri exists in the ontology
        check_query = f"""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>

                ASK {{
                    :{property} rdf:type owl:ObjectProperty .
                }}
                """

        url = rep
        headers = {"Accept": "application/sparql-results+json"}
        data = {"query": check_query}

        response = requests.post(url, headers=headers, data=data)

        # Check the response to see if superclass_name exists in the ontology
        superclass_exists = response.json()['boolean']
        if not superclass_exists:
            print("Error: property not found")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error: property not found")
            return
        # Set up the query
        query = """
                           PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                           PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                           PREFIX owl: <http://www.w3.org/2002/07/owl#>

                           DELETE { ?s :%s ?o }
                                    WHERE {
                                      ?s :%s ?o .
                                    };
                           """ % (property, property)

        # Set up the request
        url = rep
        headers = {"Content-Type": "application/sparql-update"}
        data = query

        # Send the request
        response = requests.post(url, headers=headers, data=data)

        # Check the response
        if response.ok:
            print("Property removed successfully!")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText('Property removed successfully')
        else:
            print("Error:", response.text)
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error:" + response.text)
        # Set up the query
        query = """
                           PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                           PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                           PREFIX owl: <http://www.w3.org/2002/07/owl#>

                           DELETE {
                                      ?s ?p ?o .
                                    }
                                    WHERE {
                                      ?s rdf:type owl:ObjectProperty .
                                      ?s rdfs:subClassOf* :%s .
                                      ?s ?p ?o .
                                    }
                           """ % property

        # Set up the request
        url = rep
        headers = {"Content-Type": "application/sparql-update"}
        data = query

        # Send the request
        response = requests.post(url, headers=headers, data=data)

        # Check the response
        if response.ok:
            print("Property removed successfully!")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText('Property removed successfully')
        else:
            print("Error:", response.text)
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error:" + response.text)

    def add_rel_to_db(self):
        self.ind1 = QLineEdit()
        self.property = QLineEdit()
        self.ind2 = QLineEdit()
        ind_name1, ok = QInputDialog.getText(self, 'Добавить свойство', 'Введите первый экземпляр:')
        if ok and ind_name1:
            self.ind1.setText(ind_name1)
            property, ok = QInputDialog.getText(self, 'Добавить свойство', 'Введите свойство:')
            if ok and property:
                self.property.setText(property)
                ind_name2, ok = QInputDialog.getText(self, 'Добавить свойство', 'Введите второй экземпляр:')
                if ok and ind_name2:
                    self.ind2.setText(ind_name2)
                    ind_1 = self.ind1.text()
                    property = self.property.text()
                    ind_2 = self.ind2.text()
                else:
                    return
        else:
            return

        if ind_1.__eq__(ind_2):
            print("Error: equal names")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error: equal names")
            return

        check_query = f"""
                                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>

                                ASK {{
                                    :{property} rdf:type owl:ObjectProperty .
                                }}
                                """

        url = rep
        headers = {"Accept": "application/sparql-results+json"}
        data = {"query": check_query}

        response = requests.post(url, headers=headers, data=data)

        # Check the response to see if superclass_name exists in the ontology
        superclass_exists = response.json()['boolean']
        if not superclass_exists:
            print("Error: property not found")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error: property not found")
            return
        check_query1 = f"""
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>

                        ASK {{
                            :{ind_1} rdf:type owl:NamedIndividual .
                        }}
                        """

        url1 = rep
        headers1 = {"Accept": "application/sparql-results+json"}
        data1 = {"query": check_query1}

        response = requests.post(url1, headers=headers1, data=data1)

        # Check the response to see if superclass_name exists in the ontology
        superclass_exists1 = response.json()['boolean']
        if not superclass_exists1:
            print("Error: first individual not found")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error:first individual not found")
            return
        check_query2 = f"""
                                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>

                                ASK {{
                                    :{ind_2} rdf:type owl:NamedIndividual .
                                }}
                                """
        url2 = rep
        headers2 = {"Accept": "application/sparql-results+json"}
        data2 = {"query": check_query2}

        response = requests.post(url2, headers=headers2, data=data2)

        # Check the response to see if superclass_name exists in the ontology
        superclass_exists2 = response.json()['boolean']
        if not superclass_exists2:
            print("Error: second individual not found")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error:second individual not found")
            return
        query = """
                    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                    INSERT DATA {{
                        :{} :{} :{}
                    }}
                """.format(ind_1, property, ind_2)

        # Set up the request
        url = rep
        headers = {"Content-Type": "application/sparql-update"}
        data = query

        # Send the request
        response = requests.post(url, headers=headers, data=data)

        # Check the response
        if response.ok:
            print("Property to individual added successfully!")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText('Property to individual added successfully')
        else:
            print("Error:", response.text)
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error:" + response.text)

    def del_rel_from_db(self):
        self.delete_property_edit12 = QLineEdit()
        self.delete_property_edit_sub12 = QLineEdit()
        self.delete_property_edit_sub22 = QLineEdit()
        property_name, ok = QInputDialog.getText(self, 'Удалить свойство', 'Введите название свойства:')
        if ok and property_name:
            self.delete_property_edit12.setText(property_name)
            instance1, ok = QInputDialog.getText(self, 'Удалить свойство', 'Введите первый экземпляр:')
            if ok and instance1:
                self.delete_property_edit_sub12.setText(instance1)
                instance2, ok = QInputDialog.getText(self, 'Удалить свойство', 'Введите второй экземпляр:')
                if ok and instance2:
                    self.delete_property_edit_sub22.setText(instance2)
                    property = self.delete_property_edit12.text()
                    ind_1 = self.delete_property_edit_sub12.text()
                    ind_2 = self.delete_property_edit_sub22.text()
                else:
                    return
            else:
                return
        else:
            return

        if ind_1.__eq__(ind_2):
            print("Error: equal names")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error: equal names")
            return
        check_query = f"""
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>

                        ASK {{
                            :{property} rdf:type owl:ObjectProperty .
                        }}
                        """

        url = rep
        headers = {"Accept": "application/sparql-results+json"}
        data = {"query": check_query}

        response = requests.post(url, headers=headers, data=data)

        # Check the response to see if superclass_name exists in the ontology
        superclass_exists = response.json()['boolean']
        if not superclass_exists:
            print("Error: property not found")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error: property not found")
            return
        check_query1 = f"""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>

                ASK {{
                    :{ind_1} rdf:type owl:NamedIndividual .
                }}
                """

        url1 = rep
        headers1 = {"Accept": "application/sparql-results+json"}
        data1 = {"query": check_query1}

        response = requests.post(url1, headers=headers1, data=data1)

        # Check the response to see if superclass_name exists in the ontology
        superclass_exists1 = response.json()['boolean']
        if not superclass_exists1:
            print("Error: first individual not found")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error:first individual not found")
            return
        check_query2 = f"""
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>

                        ASK {{
                            :{ind_2} rdf:type owl:NamedIndividual .
                        }}
                        """
        url2 = rep
        headers2 = {"Accept": "application/sparql-results+json"}
        data2 = {"query": check_query2}

        response = requests.post(url2, headers=headers2, data=data2)

        # Check the response to see if superclass_name exists in the ontology
        superclass_exists2 = response.json()['boolean']
        if not superclass_exists2:
            print("Error: second individual not found")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error:second individual not found")
            return
        query = """
                    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                    DELETE {
                            :%s :%s :%s .
                            }
                    WHERE {
                            :%s :%s :%s .
                            }
                """ % (ind_1, property, ind_2, ind_1, property, ind_2)

        # Set up the request
        url = rep
        headers = {"Content-Type": "application/sparql-update"}
        data = query

        # Send the request
        response = requests.post(url, headers=headers, data=data)

        # Check the response
        if response.ok:
            print("Property to individual deleted successfully!")
            self.textBrowser.clear()
            self.textBrowser.insertPlainText('Property to individual deleted successfully')
        else:
            print("Error:", response.text)
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error:" + response.text)

    def add_class_to_db(self):
        class_name, ok = QInputDialog.getText(self, 'Добавить новый класс', 'Введите название класса:')
        if ok and class_name:
            superclass_name, ok = QInputDialog.getText(self, 'Добавить суперкласс',
                                                       'Введите название суперкласса (оставьте пустым, если нет):')
            if ok:
                if superclass_name:
                    query = f"""
                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                        INSERT DATA {{
                            :{class_name} rdf:type owl:Class ;
                                          rdfs:subClassOf :{superclass_name} .
                        }}
                    """
                else:
                    query = f"""
                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                        INSERT DATA {{
                            :{class_name} rdf:type owl:Class .
                        }}
                    """
                # Set up the request to add the class to the ontology
                url = rep+ "/statements"
                headers = {"Content-Type": "application/sparql-update"}
                data = query

                # Send the request
                response = requests.post(url, headers=headers, data=data)

                # Check the response
                if response.ok:
                    print("Class added successfully!")
                    self.textBrowser.clear()
                    self.textBrowser.insertPlainText('Class added successfully')
                else:
                    print("Error:", response.text)
                    self.textBrowser.clear()
                    self.textBrowser.insertPlainText("Error:" + response.text)
        else:
            return

    def del_class_from_db(self):
        class_name, ok = QInputDialog.getText(self, 'Удалить класс', 'Введите название класса:')
        if ok and class_name:
            # Составляем запрос для удаления класса из базы данных
            query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                    DELETE {
                        :%s ?p ?o .
                        ?s ?p :%s .
                    }
                    WHERE {
                        OPTIONAL {:%s ?p ?o .}
                        OPTIONAL {?s ?p :%s .}
                    }
                    """ % (class_name, class_name, class_name, class_name)

            # Отправляем запрос на удаление класса в базе данных
            url = rep+"/statements"
            headers = {"Content-Type": "application/sparql-update"}
            data = query
            response = requests.post(url, headers=headers, data=data)

            # Проверяем ответ на запрос
            if response.ok:
                print("Class deleted successfully!")
                self.textBrowser.clear()
                self.textBrowser.insertPlainText('Class deleted successfully')
            else:
                print("Error:", response.text)
                self.textBrowser.clear()
                self.textBrowser.insertPlainText("Error:" + response.text)
        else:
            return

    def query(self):
        query_str = self.lineEdit.text()

        # Check if the query string is empty
        if not query_str:
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("No SPARQL query inserted")
            return

        # Construct the full SPARQL query with the query string
        sparql_query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
                %s
            """ % query_str

        # Create a SPARQLWrapper object and set the endpoint URL
        endpoint = SPARQLWrapper(rep)

        # Set the SPARQL query
        endpoint.setQuery(sparql_query)

        # Set the return format to JSON
        endpoint.setReturnFormat(JSON)

        # Execute the query and convert the results to JSON
        results = endpoint.query().convert()

        # Clear the textBrowser before inserting new results
        self.textBrowser.clear()

        # Display the results in the textBrowser
        for result in results['results']['bindings']:
            for var in result:
                self.textBrowser.insertPlainText(var + ': ' + result[var]['value'] + '\n')
            self.textBrowser.insertPlainText('\n')

    def show_rels(self):
        rel = """
              PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
              PREFIX owl: <http://www.w3.org/2002/07/owl#>
              SELECT DISTINCT (strafter(str(?p), \'#\') AS ?pName) 
              WHERE { 
              ?p rdf:type owl:ObjectProperty.
              } 
        """
        lst_rel = list(execute_query(rel))
        self.textBrowser.clear()
        for i in lst_rel:
            self.textBrowser.insertPlainText(i + '\n')


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
        self.window_obj.pushButton_7.clicked.connect(self.remove_obj)
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
        if button is not None:
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
        query_classification = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
            SELECT (strafter(str(?p), \'#\') AS ?pName)
            WHERE {
                ?p rdfs:subClassOf :Classification .
                FILTER EXISTS { ?e rdfs:subClassOf ?p }
            }
        """
        lst_class = list(execute_query(query_classification))
        query_chem = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
            SELECT (strafter(str(?p), \'#\') AS ?pName)
            WHERE {
                ?p rdfs:subClassOf :ByChemicalComposition .
            }
        """

        lst_chem = list(execute_query(query_chem))

        query_orig = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
            SELECT (strafter(str(?p), \'#\') AS ?pName)
            WHERE {
                ?p rdfs:subClassOf :ByFormOfOrigin .
            }
        """

        lst_orig = list(execute_query(query_orig))

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
        self.label_4.setGeometry(250, 200, 700, 100)
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
        self.window_cl.update()
        self.window_cl.pushButton_10.clicked.connect(self.updating)

    def updating(self):
        self.window_cl.close()
        self.window_cl = ClassWindow()
        self.window_cl.show()
        self.window_cl.update()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_welcome()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
