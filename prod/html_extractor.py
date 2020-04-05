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
        print(len(soup_list) + ' soup entries retrieved')
        return soup_list

    def get_products_tesco(self, soup_list):
        """
        Tesco urls are search results with multiple products in a list
        """
        products = []
        for soup in soup_list:
            panels = soup.find_all('li', {'class': 'product-list--list-item'})
            for panel in panels:
                product = self._extract_product_info_tesco(panel)
                if product is not None:
                    products.append(product)
        return products

    def _extract_product_info_tesco(self, panel):
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

    def get_products_amazon(self, soup_list):
        """
        Amazon Pantry urls are for single products
        """
        products = []
        for soup in soup_list:
            panel = soup.find('div', {'id': 'ppd'})
            product = self._extract_product_info_amazon(panel)
            if product is not None:
                products.append(product)
        return products

    def _extract_product_info_amazon(self, panel):
        price = panel.find('span', {'id': 'priceblock_ourprice'}).get_text().strip() or None
        if price is None:
            return
        name = panel.find('div', {'id': 'title_feature_div'}).get_text().strip()
        image_container = panel.find('div', {'id': 'main-image-container'})
        image = image_container.find('img')['src']

        product = {
            'name': name,
            'image': image,
            'price': price,
            'url': None
        }
        print(product)
        return product
