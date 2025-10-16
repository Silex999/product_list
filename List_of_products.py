from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

list_products = {
    1: ['Наименование: Хлеб', 'Описание: Пшеничный', 'Цена: 20'],
    2: ['Наименование: Вода', 'Описание: Негазированная', 'Цена: 45'],
    3: ['Наименование: Колбаса', 'Описание: Молочная', 'Цена: 150'],
    4: ['Наименование: Молоко', 'Описание: Обезжиреное', 'Цена: 120'],
}

response_start = '''
<html>
<head>
    <style>
    body {background-color: #0f1015; color: #fff; font-family: Arial, sans-serif;}
    a {font-size: 16px; text-decoration: none; color: #d1d1d1; text-decoration: none; transition: all 200ms ease-in-out 0s;}
    a:hover {opacity: 0.9;}
    li {list-style-type: none;}
    .product:hover { text-decoration: none; transition: all 200ms ease-in-out 0s; opacity: 0.9; width: 400px;}
    .product {display: flex;padding: 20px;transition: all 200ms ease-in-out 0s;background-color: #1b1d25; width: 15%; margin-bottom: 10px; border-radius: 10px;}
    .product_full {display: flex; flex-direction: column; padding: 20px;background-color: #1b1d25;width: 30%; margin-bottom: 10px; border-radius: 10px; margin-left: 30px;}
    p {color: #fff;}
    h1 {color: #fff;}
    h2 {color: #fff;}
    h3 {color: #fff;}
    .link_main {margin-left: 40px;}
    </style>
    <meta charset="UTF-8">  
    <title>Список продуктов</title>
</head>
<body>
'''

response_end = '''
</body>
</html>
'''

class MySiteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.products()
        elif parsed.path == "/product":
            query = parse_qs(parsed.query)
            self.product_detail(query)
        else:
            self.response(404)

    def index(self, **kwargs):
        self.response(200)
        self.render(self.render('<h1>Main page</h1>'))

    def products(self, **kwargs):
        list_products_in_html = ''
        for i in range(len(list_products)):
            prod_id = i + 1
            title = list_products[prod_id][0]
            list_products_in_html += (
                f"<li>"
                f"<div class='product'><a href=\"/product?id={prod_id}\"><h3>{title}</h3></a></div>"
                f"</li>"
            )

        list_products_in_html = "<ul>" + list_products_in_html + "</ul>"
        self.response(200)
        self.render(self.render(list_products_in_html))

    def product_detail(self, query, **kwargs):
        prod_id_raw = query.get('id', [])
        prod_id = None
        if prod_id_raw:
            prod_id = int(prod_id_raw[0])
        else:
            prod_id = None

        if prod_id in list_products:
            name, description, price = list_products[prod_id]
            content = (
                f"<div class='product_full'>"
                f"<h2>{name}</h2>"
                f"<p>{description}</p>"
                f"<p>{price}</p>"
                f"</div>"
                f"<div><a class='link_main' href='/'>Вернуться назад</a></div>"
            )
            self.response(200)
            self.render(self.render(content))
        else:
            self.response(404)
            self.render(self.render('<h1>Product not found</h1><p>Такого товара не существует.</p>'))

    def response(self, code: int):
        self.send_response(code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def render(self, content: str):
        self.wfile.write(response_start.encode('utf-8'))
        self.wfile.write(content.encode('utf-8'))
        self.wfile.write(response_end.encode('utf-8'))

def run(http_server=HTTPServer, handler=BaseHTTPRequestHandler):
    httpd = http_server(('', 8000), handler)
    httpd.serve_forever()

if __name__ == '__main__':
    print('start server')
    run(HTTPServer, MySiteHandler)
