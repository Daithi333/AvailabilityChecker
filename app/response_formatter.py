
class ResponseFormatter:

    def construct_html(self, products):
        products_html = self._construct_products_html(products)

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

    def _construct_products_html(self, products):
        products_html = """"""
        for product in products:
            products_html += """
        <tr>
        <td>%s</td>
        <td>%s</td>
        <td><a href="%s">View</a></td>
        </tr>""" % (product['name'], product['price'], product['url'])
        return products_html

    def construct_string(self, products):
        string_response = "The following products are available:\n\n"
        for product in products:
            string_response += product['name'] + "\n" + product['price'] + "\n" + product['url'] + "\n\n"
        return string_response
