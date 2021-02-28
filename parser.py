from lxml.html import document_fromstring
import requests

class Parser:
    def __init__(self, filename, timeout):
        self.main_link = 'https://zakupki.gov.ru'
        self.filename = filename
        self.timeout = timeout

        self.session = self.init_parser()

    
    def init_parser(self) -> requests.Session:
        session = requests.session()
        session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
                           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                           'Accept': '*/*'}
        session.get(self.main_link)
        return session
    
    def 