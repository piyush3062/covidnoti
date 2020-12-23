import json
from functools import partial
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic.uiparser import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
import matplotlib.pyplot as plt
import numpy as np
import requests
from plyer import notification


def notifyme(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon='icon.ico',
        timeout=10
    )


def getdata(url):
    r = requests.get(url)
    return r.text


data = getdata('https://api.covidindiatracker.com/state_data.json')

import pandas as pd

pd.set_option('display.max_columns', 50)  # display columns
df = pd.read_json(data)
df.to_csv("covid.csv")
ot = pd.read_csv(r'covid.csv', usecols=['state', 'active', 'confirmed', 'recovered', 'deaths'])

data1 = getdata('https://api.covidindiatracker.com/total.json')
n1 = json.loads(data1)
message1 = "Active: " + str(n1['active']) + "\nConfirmed: " + str(n1['confirmed']) + "\nRecovered: " + str(
    n1['recovered']) + "\nDeaths: " + str(n1['deaths'])
notifyme("India case update", message1)
n = ot[ot.state == 'Chhattisgarh']
active = int(n['active'])
confirmed = int(n['confirmed'])
recovered = int(n['recovered'])
deaths = int(n['deaths'])
message = "Active: " + str(active) + "\nConfirmed: " + str(confirmed) + "\nRecovered: " + str(
    recovered) + "\nDeaths: " + str(deaths)
notifyme("Chhattisgarh case update", message)


# time.sleep(180)

dict1 = {
  "2days": 2,
  "1 week": 7,
  "1 month": 30
}
class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Covid-19 Prediction and Analysis")

        # setting geometry
        self.setGeometry(250, 100, 1400, 800)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    def UiComponents(self):

        self.label_title = QLabel("COVID-19 Prediction and Analysis", self)

        # setting geometry
        self.label_title.setGeometry(400, 10, 700, 100)
        self.label_title.setFont(QFont('Times', 30))
        # setting alignment to the text
        self.label_title.setAlignment(Qt.AlignCenter)

        self.label_state = QLabel("State's data", self)

        # setting geometry
        self.label_state.setGeometry(1000, 130, 200, 50)
        self.label_state.setFont(QFont('Times', 18))
        # setting alignment to the text
        self.label_state.setAlignment(Qt.AlignCenter)

        self.label_india = QLabel("Total India data", self)

        # setting geometry
        self.label_india.setGeometry(300, 130, 200, 50)
        self.label_india.setFont(QFont('Times', 18))
        # setting alignment to the text
        self.label_india.setAlignment(Qt.AlignCenter)

        # creating a combo box widget
        self.combo_box = QComboBox(self)

        # setting geometry to combo box
        self.combo_box.setGeometry(1000, 200, 250, 50)

        # setting font
        self.combo_box.setFont(QFont('Times', 14))

        l = list(ot['state'])
        # adding items to combo box
        for i in l:
            self.combo_box.addItem(i)

            # adding action to the combo box
        self.combo_box.activated.connect(self.get_cases)

        self.label_total = QLabel("Total Cases ", self)

        # setting geometry
        self.label_total.setGeometry(1000, 300, 250, 50)
        self.label_total.setFont(QFont('Times', 14))
        # setting alignment to the text
        self.label_total.setAlignment(Qt.AlignCenter)

        # adding border to the label
        self.label_total.setStyleSheet("border : 2px solid black;")

        # creating label to show the total cases
        self.label_active = QLabel("Active Cases ", self)

        self.label_active.setFont(QFont('Times', 14))
        # setting geometry
        self.label_active.setGeometry(1000, 400, 250, 50)

        # setting alignment to the text
        self.label_active.setAlignment(Qt.AlignCenter)

        # adding border to the label
        self.label_active.setStyleSheet("border : 2px solid black;")

        # creating label to show the recovered cases
        self.label_reco = QLabel("Recovered Cases ", self)

        self.label_reco.setFont(QFont('Times', 14))
        # setting geometry
        self.label_reco.setGeometry(1000, 500, 250, 50)

        # setting alignment to the text
        self.label_reco.setAlignment(Qt.AlignCenter)

        # adding border
        self.label_reco.setStyleSheet("border : 2px solid black;")

        # creating label to show death cases
        self.label_death = QLabel("Total Deaths ", self)

        self.label_death.setFont(QFont('Times', 14))
        # setting geometry
        self.label_death.setGeometry(1000, 600, 250, 50)

        # setting alignment to the text
        self.label_death.setAlignment(Qt.AlignCenter)

        # adding border to the label
        self.label_death.setStyleSheet("border : 2px solid black;")

        button = QPushButton('Show graph', self)
        button.setGeometry(1000, 700, 250, 50)
        button.setFont(QFont('Times', 14))
        button.setStyleSheet(
            "QPushButton::pressed"
            "{"
            "background-color : grey;"
            "}")

        button.clicked.connect(self.state_graph)

        button1 = QPushButton('Predict Cases', self)

        button1.setGeometry(150, 480, 250, 50)
        button1.setFont(QFont('Times', 14))
        button1.setStyleSheet(
            "QPushButton::pressed"
            "{"
            "background-color : grey;"
            "}")
        button1.clicked.connect(self.on_click)

        self.label_pred = QLabel("Predicted Cases : ", self)

        # setting geometry
        self.label_pred.setGeometry(430, 480, 310, 50)
        self.label_pred.setFont(QFont('Times', 14))
        # setting alignment to the text
        self.label_pred.setAlignment(Qt.AlignCenter)

        button2 = QPushButton('Show India graph', self)
        button2.setGeometry(150, 600, 250, 50)
        button2.setFont(QFont('Times', 14))
        button2.setStyleSheet(
            "QPushButton::pressed"
            "{"
            "background-color : grey;"
            "}")
        button2.clicked.connect(self.india_graph)

        self.label_total1 = QLabel("Total Cases ", self)

        # setting geometry
        self.label_total1.setGeometry(100, 230, 280, 70)
        self.label_total1.setFont(QFont('Times', 14))
        # setting alignment to the text
        self.label_total1.setAlignment(Qt.AlignCenter)

        # adding border to the label
        self.label_total1.setStyleSheet("border : 2px solid black;")

        # creating label to show the total cases
        self.label_active1 = QLabel("Active Cases ", self)

        self.label_active1.setFont(QFont('Times', 14))
        # setting geometry
        self.label_active1.setGeometry(450, 230, 280, 70)

        # setting alignment to the text
        self.label_active1.setAlignment(Qt.AlignCenter)

        # adding border to the label
        self.label_active1.setStyleSheet("border : 2px solid black;")

        # creating label to show the recovered cases
        self.label_reco1 = QLabel("Recovered Cases ", self)

        self.label_reco1.setFont(QFont('Times', 14))
        # setting geometry
        self.label_reco1.setGeometry(100, 350, 280, 70)

        # setting alignment to the text
        self.label_reco1.setAlignment(Qt.AlignCenter)

        # adding border
        self.label_reco1.setStyleSheet("border : 2px solid black;")

        # creating label to show death cases
        self.label_death1 = QLabel("Total Deaths ", self)

        self.label_death1.setFont(QFont('Times', 14))
        # setting geometry
        self.label_death1.setGeometry(450, 350, 280, 70)

        # setting alignment to the text
        self.label_death1.setAlignment(Qt.AlignCenter)

        # adding border to the label
        self.label_death1.setStyleSheet("border : 2px solid black;")

        self.label_total1.setText("Total Cases : " + str(n1['confirmed']))
        self.label_active1.setText("Active Cases : " + str(n1['active']))
        self.label_reco1.setText("Recovered Cases : " + str(n1['recovered']))
        self.label_death1.setText("Total Deaths : " + str(n1['deaths']))

    @pyqtSlot()
    def on_click(self):
        items = ("2 Days", "1 Week", "1 Month")
        l=(2,7,30)
        item, okPressed = QInputDialog.getItem(self, "Get Days", "Predict After:", items, 0, False)
        if okPressed and item:
            print(item)
            import pandas as pd
            import numpy as np
            from sklearn.preprocessing import PolynomialFeatures
            from sklearn import linear_model

            ###LOAD DATA###
            header = ['Days', 'Date', 'Cases']
            data = pd.read_csv("india_covid.csv", sep=',', names=header)

            x = np.array(data['Days']).reshape(-1, 1)
            y = np.array(data['Cases']).reshape(-1, 1)

            pf = PolynomialFeatures(degree=7)
            x = pf.fit_transform(x)
            pf.fit(x, y)

            model = linear_model.LinearRegression()
            model.fit(x, y)
            accuracy = model.score(x, y)
            # print(accuracy)

            i=items.index(item)
            days=l[i]
            prediction = (model.predict(pf.fit_transform([[244 + days]])))
            item=int(prediction)
            print(item)
            self.label_pred.setText("Predicted Cases : " + str(item)+" cases")
    def india_graph(self):

        import matplotlib.pyplot as plt
       
        import csv
        date = []
        cases = []
        with open('india_covid.csv', 'r') as inFile:
            fileReader = csv.reader(inFile)
            interval = 0
            for row in fileReader:
                if interval % 10 == 0:
                    date.append(row[1])
                    cases.append(row[2])
                interval += 1

        print(date)
        print(cases)
        plt.title("Total Covid-19 Cases In India", fontsize=18)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Number Of Cases", fontsize=12)
        plt.plot(date, cases)
        plt.xticks(rotation=60)
        plt.tick_params(labelsize=6)
        plt.grid()
        plt.show()

    def state_graph(self):
        index1 = self.combo_box.currentIndex()
        # print(index)
        f1 = ot.iloc[index1]
        # getting data
        state = str(f1['state'])

        fname = state + ".csv"
        header = ['Days', 'Sno', 'Date', 'Time', 'State/UnionTerritory', 'ConfirmedIndianNational',
                  'ConfirmedForeignNational', 'Cured', 'Deaths', 'Confirmed']
        data = pd.read_csv(fname, sep=',', names=header)

        x1 = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300]

        x = np.array(data['Days']).reshape(-1, 1)
        y = np.array(data['Confirmed']).reshape(-1, 1)
        plt.xlabel("Day", labelpad=10)
        plt.ylabel("Cases")
        plt.title(f'COVID CASES IN {state}.')
        plt.grid()
        plt.xticks(x1)
        plt.text(0, 20000, "30 JAN 2020 - Day 1")
        plt.plot(x, y, '-r')
        plt.show()

    def get_cases(self):

        # getting index
        index = self.combo_box.currentIndex()
        # print(index)
        f = ot.iloc[index]
        print(f)
        # getting data
        state = str(f['state'])
        total = str(f['confirmed'])
        active = str(f['active'])
        recovered = str(f['recovered'])
        deaths = str(f['deaths'])

        # show data through labels
        self.label_total.setText("Total Cases : " + total)
        self.label_active.setText("Active Cases : " + active)
        self.label_reco.setText("Recovered Cases : " + recovered)
        self.label_death.setText("Total Deaths : " + deaths)

    # create pyqt5 app


App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

window.show()

# start the app
sys.exit(App.exec())
