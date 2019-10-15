from http.server import BaseHTTPRequestHandler,HTTPServer
import  logging, json, os, datetime


logger = logging.getLogger("app-log")


def configure_error_logging():
    logger.setLevel(logging.DEBUG)
    # Format for our loglines
    formatter = logging.Formatter("[%(asctime)s] - %(name)s - %(levelname)s - %(message)s")
    # Setup console logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    directory = "/tmp/proxy/"
    if not os.path.exists(directory):
        os.makedirs(directory)


    LOG_FILENAME = directory+"event.log"
    print(LOG_FILENAME)
    # Setup file logging as well
    fh = logging.FileHandler(LOG_FILENAME)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

class HTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_GET(self, body=True):
            sent = False
            try:
                self.server= ""
                self.server_version = "APP Server"
                self.sys_version = ""
                #Mon, 18 Jul 2016 02:36:04 GMT
                self.send_response_only(200)
                self.send_header('Server','Jeju')
                
                x = datetime.datetime.now()
                self.send_header('Date',x.strftime("%c"))
                self.send_header('Content-type','application/json')
                body = {"message":"you got this!"}
                self.send_header('Content-Length',len(json.dumps(body).encode()))

                self.end_headers()
                
                self.wfile.write(json.dumps(body).encode())
                sent = True
                
                self.wfile.flush() #actually send the response if not already done.
                self.close_connection= 1
                logger.debug("{} - {} - {} ".format(self.address_string(),self.requestline,200))
            except Exception as e:
                self.log_error("Request got ab error out: %r", e)
                logger.error("{} - {} - {} ".format(self.address_string(),self.requestline,200))
                self.close_connection = 1
                return
                


def startServer():
    port = 8000
    #ip = '127.0.0.1'
    ip = '0.0.0.0'
    configure_error_logging()
    logger.info('http app server is running')

    httpd = HTTPServer((ip,port), HTTPRequestHandler)
    httpd.serve_forever()
    return
if __name__ == '__main__':
       startServer()

