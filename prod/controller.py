from prod.alert import Alert
from prod.file_reader import FileReader
from prod.htm_handler import HtmlHandler


class Controller:

    def __init__(self):
        self.file_reader = FileReader('search_urls.txt')
        self.html_handler = HtmlHandler()
        self.alert = Alert()

    def process(self):
        try:
            return self._processing_steps()
        except Exception as e:
            print(str(e))
            return str(e)

    def _processing_steps(self):
        urls = self.file_reader.read_lines()
        soup_list = self.html_handler.scrape_html(urls)
        products = self.html_handler.get_products(soup_list)
        formatted_response = self._format_response(products)
        return self.alert.send(formatted_response)

    def _format_response(self, products):
        formatted_response = "The following products are available:\n\n"
        for product in products:
            formatted_response += product['name'] + "\n" + product['price'] + "\n" + product['url'] + "\n\n"
        return formatted_response
