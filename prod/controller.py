from prod.alert import Alert
from prod.file_reader import FileReader
from prod.htm_handler import HtmlHandler


class Controller:

    def __init__(self):
        self.file_reader = FileReader('search_urls.txt')
        self.urls = self.file_reader.urls
        self.html_handler = HtmlHandler(self.urls)
        self.alert = Alert()

    def process(self):
        try:
            soup_list = self.html_handler.scrape_html(self.urls)
            products = self.html_handler.get_products(soup_list)
            return self.alert.send("Below products are in stock:\n" + str(products))
        except Exception as e:
            print(str(e))
            return e
