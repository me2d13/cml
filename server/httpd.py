import http.server
import socketserver
import re
import config
import log
import traceback


logger = log.create_logger(__name__)

def make_handler(broker):
    class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            path_pattern = re.compile("/cmd/([0-9]+)", re.IGNORECASE)
            # Sending an '200 OK' response
            self.send_response(200)

            # Setting the header
            self.send_header("Content-type", "text/html")

            # Whenever using 'send_header', you also have to call 'end_headers'
            self.end_headers()

            match = path_pattern.match(self.path)
            if match:
                command = match.group(1)
                logger.debug("Recognized httpd command %s", command)
                try:
                    broker.on_command(command)
                    result = 'Command executed'
                except:
                    traceback.print_exc()
                    result = 'Command recognized but failed'
            else:
                logger.warning("Unexpected path {}, cannot be parsed".format(self.path))
                result = 'Unsupported path, provide /cmd/number'
            html = f"<html><head></head><body>{result}</body></html>"
            self.wfile.write(bytes(html, "utf8"))
            return
    return MyHttpRequestHandler

def start_httpd(broker):
    with socketserver.TCPServer(("", config.HTTPD_PORT), make_handler(broker)) as httpd:
        logger.debug("Server started at localhost:" + str(config.HTTPD_PORT))
        httpd.serve_forever()