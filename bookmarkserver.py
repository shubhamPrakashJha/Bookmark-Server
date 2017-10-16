
import http.server
import requests
from urllib.parse import unquote, parse_qs

memory = {}

form = '''<!DOCTYPE html>
<title>Bookmark Server</title>
<form method="POST">
    <label>Long URI:
        <input name="longuri">
    </label>
    <br>
    <label>Short name:
        <input name="shortname">
    </label>
    <br>
    <button type="submit">Save it!</button>
</form>
<p>URIs I know about:
<pre>
{}
</pre>
'''

def CheckURI(uri, timeout=5):
    try:
        r = requests.get(uri, timeout=timeout)
        return r.status_code == 200
    except requests.RequestException:
        return False


class Shortener(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        name = unquote(self.path[1:])

        if name:
            if name in memory:
                # redirect to longuri associated to name
                self.send_response(303)
                self.send_header('Location', memory[name])
                self.end_headers()
            else:
                # if name not in dict, send 404 error
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("I don't know '{}'.".format(name).encode())
        else:
            #send the form
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # show list associated with name in the form
            known = "\n".join("{} : {}".format(key, memory[key])
                              for key in sorted(memory.keys()))
            self.wfile.write(form.format(known).encode())

    def do_POST(self):
        #decode form request body
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        # check that user fills all field before submitting
        if "longuri" not in params or "shortname" not in params:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Missing form fields!".encode())
            return

        longuri = params["longuri"][0]
        shortname = params["shortname"][0]

        if CheckURI(longuri):
            # if URI is valid!  store it under the specified name.
            memory[shortname] = longuri

            # redirect again to the form
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            # if URI is not valid. send 404 error
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(
                "Couldn't fetch URI '{}'. Sorry!".format(longuri).encode())


if __name__ == '__main__':
    # Use PORT if it's there
    port = int(os.environ.get('PORT', 8000))
    # Server address
    server_address = ('', 5000)
    #create http.server instance
    httpd = http.server.HTTPServer(server_address, Shortener)
    #run httpd server
    httpd.serve_forever()
