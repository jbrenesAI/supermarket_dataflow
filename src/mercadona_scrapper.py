from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import random


class MercadonaScrapper:
    login_url = 'https://www.telecompra.mercadona.es/ns/entrada.php?js=1'
    credentials = {
        'username': 'biec.jdrzm22@pihey.com',
        'password': '****'
    }
    product_ids = []
    search_url = 'https://www.telecompra.mercadona.es/lista.php?busc_ref=%s&posicion_actual=%s'

    def __init__(self):
        self.products = None
        self.search_term = 'a'
        self.item = 0
        self.names = []
        self.price_desc = []
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.login()

    def login(self):
        self.driver.get(self.login_url)
        for key, val in self.credentials.items():
            self.driver.find_element(By.ID, value=key).send_keys(val)

        time.sleep(20)

    def get_products(self):
        self.products = {}

        print("Starting to scrap mercadona data")
        tic = time.time()

        self.search_products()
        self.scrap_product_list()

        toc = time.time()

        print(f"Scrapping took {toc - tic} ms")
        print(f"{len(self.names)} products read")
        return self.products

    def search_products(self, search_term='a'):
        self.search_term = search_term
        self.driver.get(self.search_url % (self.search_term, self.item))

    def scrap_product_list(self):
        current_products_len = len(self.names)
        self.parse_elements()

        while current_products_len < len(self.names):
            current_products_len = len(self.names)

            self.next_page()
            self.reload_on_ban()
            self.parse_elements()

            if random.random() > .65:
                time.sleep(5)

    def next_page(self):
        self.item = self.item + 20
        self.driver.get(self.search_url % (self.search_term, self.item))

    def reload_on_ban(self):
        if 'The requested URL was rejected.' in self.driver.find_element(By.TAG_NAME, 'body').text:
            url = self.driver.current_url
            self.login()
            self.driver.get(url)

    def parse_elements(self):
        print(self.driver.current_url)

        for tr in self.find_css_elements('tr:not(.tablacabecera)'):
            product, _, price_col, *_ = tr.find_elements(By.TAG_NAME, 'td')
            self.names.append(product.text)
            self.price_desc.append(price_col.text)

            print(product.text, price_col.text)
            self.products['product_name'] = self.names
            self.products['price_desc'] = self.price_desc

    def find_css_elements(self, css):
        try:
            return self.driver.find_elements(By.CSS_SELECTOR, css)
        except NoSuchElementException:
            return []

    def __del__(self):
        try:
            self.driver.close()
        except:
            pass
