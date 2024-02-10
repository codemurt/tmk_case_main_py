import requests
import xmltodict
from time import time

from bs4 import BeautifulSoup

class Manager:
    def __init__(self, update_time):
        self.update_time = update_time
        self._data = {}
        self._last_update_time = 0.0
        self._update_data()

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

class MetalManager(Manager):
    def __init__(self, update_time):
        super().__init__(update_time)

    def _update_data(self):
        cast_iron = None
        steel = None

        page_cast_iron = requests.get('https://www.metaltorg.ru/metal_catalog/metallurgicheskoye_syrye_i_polufabrikaty/chugun/chugun_peredelnyi/')

        soup = BeautifulSoup(page_cast_iron.text, "html.parser")

        elem = soup.find_all('td', string='Чугун передельный, exw, внутр. цены России, без НДС, $/т')

        next_td_tag = elem[0].findNext('td')
        cast_iron_value = float(next_td_tag.text.replace(',', '.'))
        self._data['IRN'] = cast_iron_value

        page_steel = requests.get('https://www.metaltorg.ru/metal_catalog/listovoi_prokat/list_rulon_bez_pokrytiya/goryachekatanaya_rulonnaya_stal/')

        soup_steel = BeautifulSoup(page_steel.text, "html.parser")

        elem_steel = soup_steel.find_all('td', string='Г/к рулонная сталь, ShFE, фев. 2024 поставка в ближайший месяц, $/т')

        next_td_tag_steel = elem_steel[0].findNext('td')
        steel_value = float(next_td_tag_steel.text.replace(',', '.'))
        self._data['STL'] = steel_value

        self._last_update_time = time()