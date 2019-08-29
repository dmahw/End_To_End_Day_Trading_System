import time
import multiprocessing
import transactionHandler
import trigger

import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading

quoteCache = 0

class S(BaseHTTPRequestHandler):
    def _set_response(self, data="Okies"):
        self.send_response(200, data)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/x-www-form-urlencoded')
        self.end_headers()

    def do_HEAD(self):
        self._set_response()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        global quoteCache
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        data = newMessage(post_data.decode("utf-8"), quoteCache)
        self._set_response(str(data))

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass
    

def newMessage(receiveMessage, quoteCache):
    try:
        receiveMessagePair = receiveMessage.split(",", 3)
        
        instruction = {}
        for pair in receiveMessagePair:
            key, value = pair.split(":")
            instruction[key] = value

        result = transactionHandler.handler(instruction["message"], quoteCache)
        return result
    except Exception as e:
        print(e)
    

def buyTrigger(quoteCache):
    trigger.buyTrigger(quoteCache)

def sellTrigger(quoteCache):
    trigger.sellTrigger(quoteCache)


def main():
    if sys.argv[1]:
        address = str(sys.argv[1])
    else:
        address = '127.0.0.1'

    if sys.argv[2]:
        port = int(sys.argv[2])
    else:
        port = 8080
    server_address = (address, port)

    with multiprocessing.Manager() as manager:
        global quoteCache 
        quoteCache = manager.dict()

        buyTriggerProcess = multiprocessing.Process(target = buyTrigger, args = (quoteCache,))
        sellTriggerProcess = multiprocessing.Process(target = sellTrigger, args = (quoteCache,))
        buyTriggerProcess.start()
        sellTriggerProcess.start()

        print("server is listening on address port: " + str(address) + " " + str(port))
        server = ThreadingSimpleServer((address, port), S)
        server.serve_forever()

main()