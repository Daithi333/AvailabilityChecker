import urllib.request as request

from bs4 import BeautifulSoup


class HtmlHandler:

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
                product = self._extract_product_info(panel)
                if product is not None:
                    products.append(product)
        return products

    def _extract_product_info(self, panel):
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

    def format_results(self, products):
        products_html = self._format_products(products)

        html_response = """\
        <html>
        <head>
        </head>
        <body>
        <h2>The following products are available:</h2>
        <table>
        <tr>
        <th>Product</th>
        <th>Price</th>
        <th>Link</th>
        </tr>%s
        </table>
        </body>
        </html>
        """ % products_html
        return html_response

    def _format_products(self, products):
        products_html = """"""
        for product in products:
            products_html += """
        <tr>
        <td>%s</td>
        <td>%s</td>
        <td><a href="%s">View</a></td>
        </tr>""" % (product['name'], product['price'], product['url'])
        return products_html
