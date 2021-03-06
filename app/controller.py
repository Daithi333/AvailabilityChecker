from app.alert import Alert
from app.file_reader import FileReader
from app.html_extractor import HtmlExtractor
from app.response_formatter import ResponseFormatter


class Controller:

    def __init__(self):
        self.file_reader = FileReader('search_urls.txt')
        self.html_extractor = HtmlExtractor()
        self.response_formatter = ResponseFormatter()
        self.alert = Alert()

    def process(self):
        try:
            return self._processing_steps()
        except Exception as e:
            print(str(e))
            return str(e)

    def _processing_steps(self):
        urls = self.file_reader.read_lines()
        soup_list = self.html_extractor.scrape_html(urls)
        products = self.html_extractor.get_products_tesco(soup_list)
        formatted_response = self.response_formatter.construct_string(products)
        return self.alert.send(formatted_response)
