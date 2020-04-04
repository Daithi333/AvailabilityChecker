import urllib.request as request

from bs4 import BeautifulSoup


class HtmlExtractor:

    def scrape_html(self, urls):
        soup_list = []
        for url in urls:
            response = request.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            soup_list.append(soup)
        return soup_list

    def get_products_tesco(self, soup_list):
        products = []
        for soup in soup_list:
            panels = soup.find_all('li', {'class': 'product-list--list-item'})
            for panel in panels:
                product = self._extract_products_tesco(panel)
                if product is not None:
                    products.append(product)
        return products

    def _extract_products_tesco(self, panel):
        price = panel.find('div', {'class': 'price-per-sellable-unit'}) or None
        if price is None:
            return
        price = price.get_text().strip()
        name = panel.find('h3').get_text().strip()
        image = panel.find('img', {'class': 'product-image'})['src']
        url = 'https://www.tesco.com/' + panel.find('h3').find('a')['href']
        # info = panel.find('div', {'class': 'product-info-message'}).get_text().strip()

        product = {
            'name': name,
            'image': image,
            'price': price,
            'url': url
        }
        return product
