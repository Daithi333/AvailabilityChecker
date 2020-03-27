import urllib.request as request

from bs4 import BeautifulSoup


class HtmlHandler:

    def __init__(self, urls):
        self.urls = urls

    def scrape_html(self, urls):
        soup_list = []
        for url in urls:
            response = request.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            soup_list.append(soup)
        return soup_list


    def get_products(self, soup_list):
        products = []
        for soup in soup_list:
            panels = soup.find_all('li', {'class': 'product-list--list-item'})
            for panel in panels:
                name = panel.find('h3').get_text().strip()
                image = panel.find('img', {'class': 'product-image'})
                info = panel.find('div', {'class': 'product-info-message'}).get_text().strip()

                product = {
                    'name': name,
                    'url': image['src'],
                    'info': info
                }
                products.append(product)
        return products
