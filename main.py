import tkinter
from tkinter import *
from tkinter import ttk
import requests
import analiza
import dane as pobraneDane
import uczenieMaszynowe


class GUI:
    def __init__(self, master):

        self.myFrame = Frame(master)
        self.myFrame.pack()
        self.table = None
        self.tableScrollView = None
        self.barGraph = None

        # taby do GUI
        tabControl = ttk.Notebook(master)
        self.tableTab = ttk.Frame(tabControl)
        self.graphTab = ttk.Frame(tabControl)
        self.machineLearningTab = ttk.Frame(tabControl)
        tabControl.add(self.tableTab, text='Tabele')
        tabControl.add(self.graphTab, text='Wykresy')
        tabControl.add(self.machineLearningTab, text='Uczenie maszynowe')
        tabControl.pack(expand=True, fill="both")

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

        # machineLearning
        self.MLTitle = Label(self.machineLearningTab, text="Wybierz stację pomiarową", font=(None, 20))
        self.MLTitle.place(relx=.5, y=50, anchor=CENTER)
        stacje = self.stacje_pomiarowe()  # pobieranie nazw stacji pomiarowych
        mlvar = StringVar(master)
        mlvar.set(stacje[0][0])  # stacje pomiarowe
        mlChooseStation = tkinter.OptionMenu(self.machineLearningTab, mlvar, *stacje[0], command=self.machine_learning)
        mlChooseStation.pack(pady=100)

        #ramka wykresów
        self. mlCanvas = Canvas(self.machineLearningTab)
        self. mlFrame = Frame(self.mlCanvas)
        self.mlVsb = Scrollbar(self.machineLearningTab, orient="vertical", command=self.mlCanvas.yview)
        self.mlCanvas.configure(yscrollcommand=self.mlVsb.set)
        self.mlVsb.pack(side="right", fill="y", expand=0)
        self.mlCanvas.pack(fill="both", expand=1)
        self.mlCanvas.create_window((940,0), window=self.mlFrame,anchor=CENTER, tags="self.mlFrame", width=1000)
        self.mlFrame.bind("<Configure>",self.onFrameConfigure)

        self.mlGraphTitle = Label(self.mlFrame, text="", font=(None,17))
        self.mlGraphTitle.place(relx=.3, y=180, anchor=CENTER)
        self.mlIndex = Label(self.mlFrame, text="", font=(None,17))
        self.mlIndex.place(relx=.3, y=210, anchor=CENTER)




        # część do tabu z wykresami
        # miejsce w którym udało się zaimplementować scrollowanie
        self.canvas = Canvas(self.graphTab)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(self.graphTab, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y", expand=0)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.create_window((840, 0), window=self.frame, anchor=CENTER,
                                  tags="self.frame", width=1000)
        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.graphTitle = Label(self.frame, text="", font=(None, 17))
        self.graphTitle.place(relx=.3, y=180, anchor=CENTER)
        self.index = Label(self.frame, text="", font=(None, 17))
        self.index.place(relx=.3, y=210, anchor=CENTER)

        label = Label(self.frame, text="Wybierz stację pomiarową", font=(None, 20)).place(relx=.3, y=65, anchor=CENTER)
        tkvar = StringVar(master)

        stacjePomiarowe = self.stacje_pomiarowe() #pobieranie nazw stacji pomiarowych
        tkvar.set(stacjePomiarowe[0][0]) #stacje pomiarowe
        chooseTable = tkinter.OptionMenu(self.frame, tkvar, *stacjePomiarowe[0], command=self.stanowiska_pomiarowe)
        chooseTable.pack(pady=100)
        # chooseTable.grid(column=1, row=0)


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #pobiera nazwy stacji pomiarowych
    def stacje_pomiarowe(self):
        return pobraneDane.stacje_pomiarowe(self)

    #pobiera stanowiska pomiarowe dla id danej stacji pomiarowej
    def stanowiska_pomiarowe(self, selection):

        self.graphTitle.configure(text=selection)
        print(selection)

        for x in range(len(pobraneDane.lista_stacji_pomiarowych)):
            if pobraneDane.lista_stacji_pomiarowych[x].nazwa_stacji == selection:
                id = pobraneDane.lista_stacji_pomiarowych[x].id_stacji

        index_jakosci = pobraneDane.index_jakosci(self, id)
        text = "Index jakości powietrza: " + str(index_jakosci)
        self.index.configure(text=text)
        analiza.create_graph(self, id)

    def machine_learning(self, selection):
        print(selection)
        self.graphTitle.configure(text=selection)

        for x in range(len(pobraneDane.lista_stacji_pomiarowych)):
            if pobraneDane.lista_stacji_pomiarowych[x].nazwa_stacji == selection:
                id = pobraneDane.lista_stacji_pomiarowych[x].id_stacji

        uczenieMaszynowe.makeGraphs(self,id)

    # metoda na pobranie danych z odpowiedniego api i ustawienie ich do tabeli
    def get_data(self, selection):

        if self.table is not None:
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

    def delete_graph(self):
        self.barGraph.get_tk_widget().destroy()
        self.barGraph = None

def main():
    window = Tk()
    window.title('Big data i hurtownie danych')
    window.geometry('1660x900')
    e = GUI(window)
    window.mainloop()


if __name__ == "__main__":
    main()
