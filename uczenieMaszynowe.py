from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import dane as pobraneDane
import DanePomiarowe
import numpy as np
from sklearn.linear_model import LinearRegression
import math

keys = []
tablica_sum = []
dane_wojewodztwo = []


def create_graph(self, id):
    makeGraphs(self, id);
    # rysuj_wykres(self, tablica_sum, keys, 'Zestawienie ilości elementów powietrza', 'średnie', 'elementy', keys)
    # stacja_pomiarowa_na_tle_wojewodztwa(self, id);

def drawGraph(self,input):
    print(input)


def makeGraphs(self, id):
    keys.clear()
    tablica_sum.clear()
    tablica_values = []
    tablica_keys = []

    id_stacji_pomiarowych = pobraneDane.stanowiska_pomiarowe(self, id)

    for x in range(len(id_stacji_pomiarowych)):
        id = str(id_stacji_pomiarowych[x])
        pobrane = pobraneDane.dane_pomiarowe(self, id)

        key = pobrane[0]
        date = pobrane[1]
        value = pobrane[2]

        keys.append(key)
        tablica_sum.append(sum(map(float, value)) / len(date))

        nazwa1 = 'Data'
        nazwa2 = 'Wartość'
        tablica_values.append(value)
        tablica_keys.append(key)

    splitAirQualityData(self, tablica_values, tablica_keys)



def splitAirQualityData(self,values, keys):
    for label in range(len(keys)):
        linearRegression(self, values[label])


def linearRegression(self,values):
    indexes = np.arange(len(values))
    ones = np.ones(len(values))
    X = np.stack((ones, values), axis=1)
    gradLin = LinearRegression()
    gradLin.fit(X, indexes)
    res = gradLin.predict(X)
    #res = np.stack((indexes,res), axis=1)

    #rysowanie wykresów
    plt.rcParams['font.size'] = 6
    plt.subplots_adjust(left=0.1, right=0.9, top=1, bottom=0.1)

    dataSet = {"Pomiar" : indexes, "Wartość" : res}
    dfML = pd.DataFrame(dataSet,columns=["Pomiar","Wartość"])
    print(dfML)

    fig = plt.figure(figsize=(8,7), dpi =100)

    ax = fig.add_subplot(111)
    chart_type = FigureCanvasTkAgg(fig, self.mlFrame)
    chart_type.get_tk_widget().pack()
    dfML.plot(kind="scatter", x = indexes, y = res, legend=True, ax = ax )





