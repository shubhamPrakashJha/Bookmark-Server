
import http.server
import requests
from urllib.parse import unquote, parse_qs

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Shortener)
    httpd.serve_forever()
