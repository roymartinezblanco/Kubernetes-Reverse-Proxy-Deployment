from http.server import BaseHTTPRequestHandler,HTTPServer
import argparse, os, random, sys, requests, logging,urllib3, yaml, json

hostname = 'roymartinez.dev'
logger = logging.getLogger("proxy-Log")
urllib3.disable_warnings()
config = None
n = -1
origins = []

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

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
   

    def do_GET(self, body=True):

            try:
                url = 'https://{}{}'.format(hostname, self.path)

                incommingHost = dict(self.headers.items())['Host']
                service = findService("load-balancer")
                o = origins[balanceOrigin()]
               
                self.server= ""
                self.server_version = ""
                self.sys_version = ""
                
                endpoint="http://{}:{}{}".format(o['address'],o['port'],self.path)
                
               
                http = requests.Session()
                resp = http.get(endpoint, verify=False)
        
            
                
                       
                self.send_response_only(resp.status_code)
                self.send_header("APP Server","{}-{}".format(o['name'],o['address']))
                for k,v in resp.headers.items():
            
                    self.send_header(k,v)
                self.end_headers()
                             
                self.wfile.write(resp.text.encode())
                self.wfile.flush() #actually send the response if not already done.
                self.close_connection= 1
                logger.error("{} - {} - {} ".format(self.address_string(),self.requestline,200))
            except Exception as e:

                self.log_error("Request got ab error out: %r", e)
                logger.error("{} - {} - {} ".format(self.address_string(),self.requestline,200))
                self.close_connection = 1



def startServer():
    server_address = (config['proxy']['listen']['address'], config['proxy']['listen']['port'])

    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    logger.info('http proxy server is running')
    httpd.serve_forever()
    return

def findService(service:str):
    for s in config['proxy']['services']:
        if s['name'] == service:
            return s
    return None

def getOrigins(service:dict):
    
    for s in service['hosts']:
        origins.append(s)
##roundRobin
def balanceOrigin():
    global n
    n += 1
    return (n % len(origins))

def load_proxy_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    configure_error_logging()
    config= load_proxy_config("config.yaml")
    service = findService("load-balancer")
    getOrigins(service)


    startServer()

