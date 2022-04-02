import requests
import StacjePomiarowe
from datetime import datetime

lista_stacji_pomiarowych = []


def stacje_pomiarowe(self):
    path = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"
    response = requests.get(path)
    json = response.json()

    nazwa_stacji = []
    id_stacji = []
    miasto = []
    wojewodztwo = []
    commune = []

    for x in json:
        nazwa_stacji.append((x['stationName']))
        id_stacji.append((x['id']))
        miasto.append(x['city'])

    for x in miasto:
        commune.append((x['commune']))

    for x in commune:
        wojewodztwo.append(x['provinceName'])

    for x in range(len(id_stacji)):
        lista_stacji_pomiarowych.append(StacjePomiarowe.StacjePomiarowe(id_stacji[x], nazwa_stacji[x], wojewodztwo[x]))

    stanowiska_pomiarowe(self, id_stacji[0])
    return nazwa_stacji, id_stacji


def stanowiska_pomiarowe(self, id_stacji):
    id_stanowiska = []

    path = "https://api.gios.gov.pl/pjp-api/rest/station/sensors/" + str(id_stacji)
    response = requests.get(path)
    json = response.json()

    for x in json:
        id_stanowiska.append((x['id']))

    return id_stanowiska


def dane_pomiarowe(self, id_stanowiska):

    path = "https://api.gios.gov.pl/pjp-api/rest/data/getData/" + str(id_stanowiska)
    response = requests.get(path)
    json = response.json()

    values = json["values"]
    key = json["key"]
    date = []
    value = []

    for x in values:
        if x["value"] is not None:
            date_time_obj = datetime.strptime(x["date"], '%Y-%m-%d %H:%M:%S')

            date.append(date_time_obj)
            value.append(x["value"])

    return key, date, value


def index_jakosci(self, id):
    path = "https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/" + str(id)
    response = requests.get(path)
    json = response.json()

    level = json['stIndexLevel']

    return level['indexLevelName']
