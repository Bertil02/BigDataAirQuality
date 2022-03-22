import tkinter
from tkinter import *
from tkinter import ttk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame


class GUI:
    def __init__(self, master):

        self.myFrame = Frame(master)
        self.myFrame.pack()
        self.table = NONE
        self.tableScrollView = NONE

        # taby do GUI
        tabControl = ttk.Notebook(master)
        self.tableTab = ttk.Frame(tabControl)
        self.graphTab = ttk.Frame(tabControl)
        self.machineLearningTab = ttk.Frame(tabControl)
        tabControl.add(self.tableTab, text='Tabele')
        tabControl.add(self.graphTab, text='Wykresy')
        tabControl.add(self.machineLearningTab, text='Uczenie maszynowe')
        tabControl.pack(expand=1, fill="both")

        # część do tabu z tabelą
        self.tableTitle = Label(self.tableTab, text="", font=(None, 20))
        self.tableTitle. place(relx=.5, y=200, anchor=CENTER)
        label = Label(self.tableTab, text="Wybierz tabelę", font=(None, 20)).place(relx=.5, y=65, anchor=CENTER)
        # options menu na wybranie odpowiedniej tabeli
        tables = ["Stacje pomiarowe", "Stanowiska pomiarowe", "Dane pomiarowe", "Indeks jakości powietrza"]
        tkvar = StringVar(master)
        tkvar.set(tables[0])
        chooseTable = tkinter.OptionMenu(self.tableTab, tkvar, *tables, command=self.get_data)
        chooseTable.pack(pady=100)

        # część do tabu z wykresami

        # przycisk do tworzenia wykresów
        self.tableTitle = Label(self.graphTab, text="", font=(None, 17))
        self.tableTitle.place(relx=.5, y=200, anchor=CENTER)
        label = Label(self.graphTab, text="Wybierz stację pomiarową", font=(None, 20)).place(relx=.5, y=65, anchor=CENTER)
        tkvar = StringVar(master)

        stacjePomiarowe = self.stacje_pomiarowe();
        tkvar.set(stacjePomiarowe[0][0]) # tutaj stacje pomiarowe
        chooseTable = tkinter.OptionMenu(self.graphTab, tkvar, *stacjePomiarowe[0], command=self.stanowiska_pomiarowe)
        chooseTable.pack(pady=100)
        #createGraphBtn = Button(self.graphTab, text="Stwórz wykres", command=self.stacje_pomiarowe()).place(relx=.5, y=65,
                #                                                                                      anchor=CENTER)

    #pobiera nazwy stacji pomiarowych
    def stacje_pomiarowe(self):
        nazwy_stacji = []
        id_stacji = []
        response = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/findAll")
        json = response.json()
        for x in json:
            nazwy_stacji.append((x['stationName']))
            id_stacji.append((x['id']))
        return nazwy_stacji,id_stacji


    #pobiera stanowiska pomiarowe dla id danej stacji pomiarowej
    def stanowiska_pomiarowe(self, selection):

        self.tableTitle.configure(text=selection)
        print(selection)

        lista_stacji = self.stacje_pomiarowe();
        ilosc_stacji = len(lista_stacji[0]);

        for x in range(ilosc_stacji):
            if lista_stacji[0][x] == selection:
                id = lista_stacji[1][x]

        path = "https://api.gios.gov.pl/pjp-api/rest/station/sensors/" + str(id)
        response = requests.get(path)
        json = response.json()

        id_stanowiska = []

        for x in json:
            id_stanowiska.append((x['id']))
        self.create_graph(id_stanowiska)

    # metoda na pobranie danych z odpowiedniego api i ustawienie ich do tabeli
    def get_data(self, selection):

        if self.table != NONE:
            self.delete_table()

        self.tableTitle.configure(text=selection)
        # słownik zawierający nazwy tabel wraz z odpowiednimi api
        tables = {"Stacje pomiarowe": "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
                  "Stanowiska pomiarowe": "https://api.gios.gov.pl/pjp-api/rest/station/sensors/14",
                  "Dane pomiarowe": "https://api.gios.gov.pl/pjp-api/rest/data/getData/92",
                  "Indeks jakości powietrza": "https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/52"}

        # pobieranie danych z odpowiedniego api i wywołanie funkcji na tworzenie tabel z tych danych
        for key in tables:
            if key == selection:
                response = requests.get(tables[key])
                json = response.json()
                if type(json) is list:
                    jsonKeys = json[0]
                else:
                    jsonKeys = json
                self.create_table(jsonKeys, json)

    # metoda na stworzenie tabeli z danymi
    def create_table(self, jsonKeys, json):

        i = 0
        # dodanie ilości kolumn w tabeli
        columns = list(range(0, len(jsonKeys)))

        # tworzenie tabeli
        self.table = ttk.Treeview(self.tableTab, columns=columns, show='headings', height=30)

        # dodanie nazw kolumn do tabeli
        for key in jsonKeys:
            self.table.heading("#" + str(i + 1), text=key)
            i += 1

        # dodanie danych do tabeli
        if type(json) is list:
            for row in json:
                self.table.insert("", END, values=(list(row.values())))
        else:
            self.table.insert("", END, values=(list(json.values())))
        self.table.pack(side=BOTTOM)

        # dodanie scroll horyzontalny do tabeli
        self.tableScrollView = Scrollbar(self.tableTab, orient='horizontal')
        self.tableScrollView.pack(side=BOTTOM, fill='x')
        self.tableScrollView.config(command=self.table.xview)
        self.table.configure(xscrollcommand=self.tableScrollView.set)

    # metoda na usunięcie tabeli z danymi
    def delete_table(self):
        self.table.destroy()
        self.tableScrollView.destroy()

    # metoda na stworzenie wykresu (tu macie przykładowe wykresy na których możecie się wzorować)
    def create_graph(self, dane):

        ilosc = len(dane);
        i = 0;

        for x in range(ilosc):
            i = i + 1;
            id = str(dane[x])
            path = "https://api.gios.gov.pl/pjp-api/rest/data/getData/" + id;
            response = requests.get(path);
            json = response.json()

            values = json["values"]
            key = json["key"]
            date = []
            value = []

            for x in values:
                date.append(x["date"])
                value.append(x["value"])

            d1 = {'Date' : date, 'Value' : value}
            df1 = DataFrame(d1, columns=['Date', 'Value'])

            figure1 = plt.Figure(figsize=(4, 3), dpi=100)
            ax1 = figure1.add_subplot(111)
            bar1 = FigureCanvasTkAgg(figure1, self.graphTab)
            bar1.get_tk_widget().pack(side=BOTTOM)
            df1 = df1[['Date', 'Value']].groupby('Date').sum()
            df1.plot(kind='bar', legend=True, ax=ax1)
            ax1.set_title(key)

            # figure2 = plt.Figure(figsize=(4, 2), dpi=100)
            # ax2 = figure2.add_subplot(111)
            # line2 = FigureCanvasTkAgg(figure2, self.graphTab)
            # line2.get_tk_widget().pack(side=LEFT)
            # df2 = df1[['Date', 'Value']].groupby('Date').sum()
            # df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
            # ax2.set_title('Year Vs. Unemployment Rate')

            # figure3 = plt.Figure(figsize=(5, 4), dpi=100)
            # ax3 = figure3.add_subplot(111)
            # ax3.scatter(df3['Interest_Rate'], df3['Stock_Index_Price'], color='g')
            # scatter3 = FigureCanvasTkAgg(figure3, self.graphTab)
            # scatter3.get_tk_widget().pack(side=LEFT)
            # ax3.legend(['Stock_Index_Price'])
            # ax3.set_xlabel('Interest Rate')
            # ax3.set_title('Interest Rate Vs. Stock Index Price')

        # przykadowe dane do wykresów
        # data1 = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
        #          'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]
        #          }
        # df1 = DataFrame(data1, columns=['Country', 'GDP_Per_Capita'])
        #
        # data2 = {'Year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
        #          'Unemployment_Rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
        #          }
        # df2 = DataFrame(data2, columns=['Year', 'Unemployment_Rate'])
        #
        # data3 = {'Interest_Rate': [5, 5.5, 6, 5.5, 5.25, 6.5, 7, 8, 7.5, 8.5],
        #          'Stock_Index_Price': [1500, 1520, 1525, 1523, 1515, 1540, 1545, 1560, 1555, 1565]
        #          }
        # df3 = DataFrame(data3, columns=['Interest_Rate', 'Stock_Index_Price'])

        # przykładowe wykresy
        # figure1 = plt.Figure(figsize=(4, 3), dpi=100)
        # ax1 = figure1.add_subplot(111)
        # bar1 = FigureCanvasTkAgg(figure1, self.graphTab)
        # bar1.get_tk_widget().pack(side=LEFT)
        # df1 = df1[['XD', 'XDD']].groupby('XD').sum()
        # df1.plot(kind='bar', legend=True, ax=ax1)
        # ax1.set_title('XDDD')

        # figure2 = plt.Figure(figsize=(5, 4), dpi=100)
        # ax2 = figure2.add_subplot(111)
        # line2 = FigureCanvasTkAgg(figure2, self.graphTab)
        # line2.get_tk_widget().pack(side=LEFT)
        # df2 = df2[['Year', 'Unemployment_Rate']].groupby('Year').sum()
        # df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
        # ax2.set_title('Year Vs. Unemployment Rate')
        #
        # figure3 = plt.Figure(figsize=(5, 4), dpi=100)
        # ax3 = figure3.add_subplot(111)
        # ax3.scatter(df3['Interest_Rate'], df3['Stock_Index_Price'], color='g')
        # scatter3 = FigureCanvasTkAgg(figure3, self.graphTab)
        # scatter3.get_tk_widget().pack(side=LEFT)
        # ax3.legend(['Stock_Index_Price'])
        # ax3.set_xlabel('Interest Rate')
        # ax3.set_title('Interest Rate Vs. Stock Index Price')


def main():
    window = Tk()
    window.title('Big data i hurtownie danych')
    window.geometry('1660x900')
    e = GUI(window)
    window.mainloop()


if __name__ == "__main__":
    main()