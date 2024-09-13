from http.server import BaseHTTPRequestHandler, HTTPServer
import goodscrape
from jinja2 import Environment, FileSystemLoader

hostName = "localhost"
serverPort = 8080

class FxGoodReadsHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        print("TEST")
        self.goodreads_base_url = "https://goodreads.com"
        self.environment = Environment(loader=FileSystemLoader(""))
        self.template = self.environment.get_template("book.template")
        super().__init__(*args, **kwargs)

    def jinja_render_book(self, book: goodscrape.GRBook):
        vars = {
            "url": f'{self.goodreads_base_url}{self.path}',
            "author": book.get_author(),
            "cover_image": book.get_cover_image(),
            "description": book.get_description(),
        }
        content = self.template.render(vars)
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