from typing import List

from urllib3 import Timeout, PoolManager, Retry
from urllib3.exceptions import HTTPError, NewConnectionError

from bs4 import BeautifulSoup


class HtmlExtractor:

    def __init__(self):
        self.retry = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        self.http = PoolManager(retries=self.retry)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }

    def scrape_html(self, urls: List[str]):
        soup_list = []
        for url in urls:
            print(f'Scraping html from {url}')
            try:
                response = self.http.request(
                    'GET',
                    url,
                    headers=self.headers,
                    timeout=Timeout(connect=1.0, read=2.0)
                )
                html = response.data.decode('utf-8')

            except (HTTPError, NewConnectionError, Exception) as e:
                print(f'Failed to scrape url {url}: {type(e).__name__} - {str(e)}')
                continue

            soup = BeautifulSoup(html, 'html.parser')
            soup_list.append(soup)

        print('%s soup entries retrieved' % len(soup_list))
        return soup_list

    def get_products_tesco(self, soup_list: List[BeautifulSoup]):
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
        image = panel.find('img', {'class': 'product-image'})['app']
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
        image = image_container.find('img')['app']

        product = {
            'name': name,
            'image': image,
            'price': price,
            'url': None
        }
        print(product)
        return product
