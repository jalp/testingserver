from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import logging

logger = logging.getLogger('test_server')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_POST(self):
        logger.debug("Client %s" % str(self.client_address))
        length = int(self.headers.getheader('content-length', 0))
        logger.debug("Content length %s " % length)
        post_data = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        for key, value in post_data.iteritems():
            logger.debug("key: %s" % key)
            logger.debug("value: %s" % value)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()


def setup():
    pass


def teardown():
    logger.debug("Closing server....(if needed)")
    httpd.server_close()


PORT = 9700
httpd = HTTPServer(("", PORT), MyHandler)


def test():
    logger.debug("Launching test...")
    httpd.handle_request()

if __name__ == "__main__":
    test()

"""
curl -X POST http://localhost:9700 -v -d @data.json -H "Content-Type: application/json"
"""