import requests
import xmltodict
from time import time

class Manager:
    def __init__(self, update_time):
        self.update_time = update_time
        self._data = {}
        self._last_update_time = 0.0

    def _update_data(self):
        pass

    def __check_update(self):
        if time() - self._last_update_time > self.update_time:
            self._update_data()

    def get_data(self, name):
        self.__check_update()
        return self._data[name]

class ValManager(Manager):
    def __init__(self, update_time):
        super().__init__(update_time)

    def _update_data(self):
        cny = None
        usd = None

        raw = requests.get("https://www.cbr-xml-daily.ru/daily_utf8.xml").text
        xmldict = xmltodict.parse(raw)['ValCurs']['Valute']

        for valcurs in xmldict:
            if valcurs['CharCode'] == "CNY":
                cny = valcurs['Value']
            elif valcurs['CharCode'] == 'USD':
                usd = valcurs['Value']

        self._data['CNY'] = cny
        self._data['USD'] = usd
        self._last_update_time = time()