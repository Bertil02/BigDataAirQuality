from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import dane as pobraneDane
import DanePomiarowe
import numpy as np
import math

keys = []
tablica_sum = []
dane_wojewodztwo = []


def create_graph(self, id):
    stacja_pomiarowa_wykresy(self, id);
    rysuj_wykres(self, tablica_sum, keys, 'Zestawienie ilości elementów powietrza', 'średnie', 'elementy', keys)
    stacja_pomiarowa_na_tle_wojewodztwa(self, id);


def stacja_pomiarowa_wykresy(self, id):
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
        rysuj_wykres(self, date, value, key, nazwa1, nazwa2, nazwa1)
        tablica_values.append(value)
        tablica_keys.append(key)

        szereg_rozdzielczy(self, value)

    wykres_pudełkowy(self, tablica_values, tablica_keys)


def rysuj_wykres(self, date, value, key, nazwa1, nazwa2, group, typ='bar'):
    plt.rcParams['font.size'] = 6
    plt.subplots_adjust(left=0.1, right=0.9, top=1, bottom=0.1)

    data = {nazwa1: date, nazwa2: value}
    df1 = pd.DataFrame(data, columns=[nazwa1, nazwa2])
    figure = plt.Figure(figsize=(8, 7), dpi=100)
    ax = figure.add_subplot(111)

    self.barGraph = FigureCanvasTkAgg(figure, self.frame)
    self.barGraph.get_tk_widget().pack()

    df1 = df1[[nazwa1, nazwa2]].groupby(group).sum()
    df1.plot(kind=typ, legend=True, ax=ax)
    ax.set_title(key)  # tytuł wykresu


def rysuj_wykres_d(self, dataframe, key, nazwa1, nazwa2, group, typ='bar'):
    plt.rcParams['font.size'] = 6
    plt.subplots_adjust(left=0.1, right=0.9, top=1, bottom=0.1)

    figure = plt.Figure(figsize=(8, 7), dpi=100)
    ax = figure.add_subplot(111)

    self.barGraph = FigureCanvasTkAgg(figure, self.frame)
    self.barGraph.get_tk_widget().pack()

    if nazwa1:
        dataframe = dataframe[[nazwa1, nazwa2]].groupby(group).sum()
    dataframe.plot(kind=typ, legend=True, ax=ax)
    ax.set_title(key)


def wykres_pudełkowy(self, value, keys):

    data = value

    plt.rcParams['font.size'] = 6
    fig = plt.Figure(figsize=(8, 7), dpi=100)
    ax = fig.add_subplot(111)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    self.barGraph = FigureCanvasTkAgg(fig, self.frame)
    self.barGraph.get_tk_widget().pack()

    ax.set_title('Wykres pudełkowy dla stacji pomiarowej')

    bp = ax.boxplot(data)


def szereg_rozdzielczy(self, value):
    n = len(value)
    k = round(math.sqrt(n))

    for x in range(len(value)):
        value[x] = round(value[x], 1)

    s_min = round(min(value) - 1)
    s_max = round(max(value) + 1)

    punkty = pd.interval_range(s_min, s_max, k)

    dane_cut = pd.cut(value, punkty)
    przedzialy = pd.DataFrame(dane_cut, columns=['przedziały'])
    szereg = pd.DataFrame(przedzialy.value_counts().rename_axis('przedziały').reset_index(name='ilość'))

    rysuj_wykres_d(self, szereg, 'Szereg rodzielczy', 'przedziały', 'ilość', 'przedziały')
    czestosci_skumulowane(self, szereg, n)


def czestosci_skumulowane(self, szereg, n):
    szereg = (szereg.sort_values(by='przedziały'))
    a = szereg[['ilość']] / n * 100
    skumulowane = pd.DataFrame.cumsum(a)
    skumulowane.insert(loc=1, column='przedziały', value=szereg['przedziały'])
    rysuj_wykres_d(self, skumulowane, 'Częstości skumulowane procentowe', 'ilość', 'przedziały', 'przedziały', 'line')


def stacja_pomiarowa_na_tle_wojewodztwa(self, id):
    dane_wojewodztwo.clear()
    id_stacji_danego_wojewodztwa = []
    stanowiska_pomiarowe = []
    keys = []
    klucze = []

    # wyszukiwanie z jakiego województwa jest stacja pomiarowa
    for x in range(len(pobraneDane.lista_stacji_pomiarowych)):
        if pobraneDane.lista_stacji_pomiarowych[x].id_stacji == id:
            wojewodztwo = pobraneDane.lista_stacji_pomiarowych[x].wojewodztwo
            print(wojewodztwo)

    # wyszukiwanie wszystkich stacji z danego województwa
    for x in range(len(pobraneDane.lista_stacji_pomiarowych)):
        if pobraneDane.lista_stacji_pomiarowych[x].wojewodztwo == wojewodztwo:
            id_stacji_danego_wojewodztwa.append(pobraneDane.lista_stacji_pomiarowych[x].id_stacji)

    # wyszukiwania stanowisk pomiarowych z danego województwa
    for x in range(len(id_stacji_danego_wojewodztwa)):
        stanowiska_pomiarowe.append(pobraneDane.stanowiska_pomiarowe(self, id_stacji_danego_wojewodztwa[x]))

    stanowiska_pomiarowe = sum(stanowiska_pomiarowe, [])

    for x in range(len(stanowiska_pomiarowe)):
        dane_wojewodztwo.append(pobraneDane.dane_pomiarowe(self, stanowiska_pomiarowe[x]))
        if dane_wojewodztwo[x][0] not in keys:  # jeśli wśród tablicy kluczy nie ma klucza
            keys.append(dane_wojewodztwo[x][0])  # dodaje klucze czyli no2 co2 itd

    for x in range(len(keys)):  # dla każdego z kluczy
        klucze.append(DanePomiarowe.DanePomiarowe(keys[x], [],
                                                  []))  # dodaje do tablicy obiekt DatePomiarowe z danym kluczem a reszta danych jest pusta?

    for x in range(len(dane_wojewodztwo)):  # dla każdego stanowiska
        for y in range(len(keys)):  # dla każdego klucza
            if dane_wojewodztwo[x][0] == klucze[y].key:  # gdzie klucz w województwie jest równy kluczowi w obiekcie klucze
                klucze[y].data.append(dane_wojewodztwo[x][1])  # dodawane są wszystkie daty
                klucze[y].value.append(dane_wojewodztwo[x][2])  # i wszystkie values

    stacja_vs_wojewodztwo(self, klucze)

    return klucze


def stacja_vs_wojewodztwo(self, klucze):
    srednie_wojewodztwo = []
    elementy = []

    for x in range(len(klucze)):
        srednie_wojewodztwo.append(sum(klucze[x].value, []))
        dlugosc = len(srednie_wojewodztwo[x])
        srednie_wojewodztwo[x] = sum(map(float, srednie_wojewodztwo[x])) / dlugosc
        srednie_wojewodztwo[x] = round(srednie_wojewodztwo[x],1)
        elementy.append(klucze[x].key)

    for x in range(len(tablica_sum)):
        tablica_sum[x] = round(tablica_sum[x], 1)

    # jeśli na danej stacji pomiarowej nie było pomiarów niektórych elementów powietrza to ich wartość będzie wynosiła 0
    for x in range(len(elementy)):
        if elementy[x] not in keys:
            keys.append(elementy[x])
            tablica_sum.append(0)

    x = np.arange(len(elementy))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, srednie_wojewodztwo, width, label='województwo')
    rects2 = ax.bar(x + width / 2, tablica_sum, width, label='stacja pomiarowa')

    ax.set_ylabel('Wartości')
    ax.set_title('Porównanie: stacja - województwo')
    ax.set_xticks(x, elementy)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    self.barGraph = FigureCanvasTkAgg(fig, self.frame)
    self.barGraph.get_tk_widget().pack()


def wszystkie_stacje(self):
    wszystkie_stacje_pomiarowe = pobraneDane.stacje_pomiarowe(self)
    id_stanowisk = wszystkie_stacje_pomiarowe[1]
    ilosc_stacji = len(wszystkie_stacje_pomiarowe[1])

    wszystkie_stanowiska_pomiarowe = []
    wszystkie_dane_pomiarowe = []

    for x in range(ilosc_stacji):
        wszystkie_stanowiska_pomiarowe.append(pobraneDane.stanowiska_pomiarowe(self, id_stanowisk[x]))

    wszystkie_stanowiska_pomiarowe_tablica = sum(wszystkie_stanowiska_pomiarowe, [])
    wszystkie_stanowiska_pomiarowe_tablica_dlugosc = len(wszystkie_stanowiska_pomiarowe_tablica)

    for x in range(wszystkie_stanowiska_pomiarowe_tablica_dlugosc):
        wszystkie_dane_pomiarowe.append(pobraneDane.dane_pomiarowe(self, wszystkie_stanowiska_pomiarowe_tablica[x]))

    print(wszystkie_dane_pomiarowe)
