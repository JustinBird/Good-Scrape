from http.server import BaseHTTPRequestHandler, HTTPServer
import goodscrape
from jinja2 import Environment, FileSystemLoader
from urllib.parse import urlparse, parse_qsl
from math import ceil

hostName = "localhost"
serverPort = 8080

class FxGoodReadsHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.goodreads_base_url = "https://goodreads.com"
        self.environment = Environment(loader=FileSystemLoader(""))
        self.book_template = self.environment.get_template("book.template")
        self.oembed_book_template = self.environment.get_template("oembed_book.template")
        super().__init__(*args, **kwargs)

    def jinja_render_book(self, book: goodscrape.GRBook):
        vars = {
            "url": f'{self.goodreads_base_url}{self.path}',
            "title": book.get_title(),
            "author": book.get_author(),
            "cover_image": book.get_cover_image(),
            "description": book.get_description(),
            "average": book.get_average_rating(),
            "stars": "⭐" * round(float(book.get_average_rating())),
            "ratings": book.get_num_ratings(),
            "reviews": book.get_num_reviews(),
        }
        content = self.book_template.render(vars)
        return content

    def jinja_render_oembed_book(self):
        print("Handling oembed book!")
        print(self.path)
        parsed_url = urlparse(self.path)
        qs = parse_qsl(parsed_url.query)
        content = self.oembed_book_template.render(qs)
        return content

    def do_GET(self):
        print(self.command)
        print(self.path)
        if self.path.startswith('/book/'):
            book = goodscrape.GRBook(f'{self.goodreads_base_url}{self.path}')
            print(book.get_author)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(self.jinja_render_book(book), "utf-8"))
        elif self.path.startswith('/oembed'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(self.jinja_render_oembed_book(), "utf-8"))
        else:
            self.send_response(404)

if __name__ == "__main__":

    webServer = HTTPServer((hostName, serverPort), FxGoodReadsHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")