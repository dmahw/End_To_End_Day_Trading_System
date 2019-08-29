import unittest
import transactionHandler
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import multiprocessing
import json



class TestStringMethods(unittest.TestCase):
    def test(self):
        resDump = str(transactionHandler.handler("1,ADD,David,5000", quoteCache))
        expected = {
            "username": "David",
            "funds": 5000.0,
            "stocks": {},
            "buyStack": [],
            "sellStack": [],
            "buyTriggers": {},
            "sellTriggers": {}
        }
        self.assertEqual(resDump, (json.dumps(expected)))

    def test2(self):
        resDump = transactionHandler.handler("1,ADD,David,5000", quoteCache)
        expected = {
            "username": "David",
            "funds": 10000.0,
            "stocks": {},
            "buyStack": [],
            "sellStack": [],
            "buyTriggers": {},
            "sellTriggers": {}
        }
        self.assertEqual(resDump, (json.dumps(expected)))

    def test3(self):
        resDump = transactionHandler.handler("1,BUY,David,S,50", quoteCache)
        expected = {
            "username": "David",
            "funds": 9950.0,
            "stocks": {},
            "buyStack": [
                {
                "username": "David",
                "stockSymbol": "S",
                "value": 50,
                "quantity": 5,
                "quote": 10.0,
                "timestamp": 9999999999
            }
            ],
            "sellStack": [],
            "buyTriggers": {},
            "sellTriggers": {}
        }
        self.assertEqual(resDump, (json.dumps(expected)))

    def test4(self):
        resDump = transactionHandler.handler("1,COMMIT_BUY,David", quoteCache)
        expected = {
            "username": "David",
            "funds": 9950.0,
            "stocks": {
                "S": {
                    "username": "David",
                    "stockSymbol": "S",
                    "quantity": 5
                }
            },
            "buyStack": [],
            "sellStack": [],
            "buyTriggers": {},
            "sellTriggers": {}
        }
        self.assertEqual(resDump, (json.dumps(expected)))
    
    def test5(self):
        resDump = transactionHandler.handler("1,SELL,David,S,20", quoteCache)
        expected = {
            "username": "David",
            "funds": 9950.0,
            "stocks": {
                "S": {
                    "username": "David",
                    "stockSymbol": "S",
                    "quantity": 3
                }
            },
            "buyStack": [],
            "sellStack": [
                {
                    "username": "David",
                    "stockSymbol": "S",
                    "value": 20,
                    "quantity": 2,
                    "quote": 10.0,
                    "timestamp": 9999999999
                }
            ],
            "buyTriggers": {},
            "sellTriggers": {}
        }
        self.assertEqual(resDump, (json.dumps(expected)))

    def test6(self):
        resDump = transactionHandler.handler("1,CANCEL_SELL,David", quoteCache)
        expected = {
            "username": "David",
            "funds": 9950.0,
            "stocks": {
                "S": {
                    "username": "David",
                    "stockSymbol": "S",
                    "quantity": 5
                }
            },
            "buyStack": [],
            "sellStack": [],
            "buyTriggers": {},
            "sellTriggers": {}
        }
        self.assertEqual(resDump, (json.dumps(expected)))

    def test7(self):
        resDump = transactionHandler.handler("1,SELL,David,S,20", quoteCache)
        expected = {
            "username": "David",
            "funds": 9950.0,
            "stocks": {
                "S": {
                    "username": "David",
                    "stockSymbol": "S",
                    "quantity": 3
                }
            },
            "buyStack": [],
            "sellStack": [
                {
                    "username": "David",
                    "stockSymbol": "S",
                    "value": 20,
                    "quantity": 2,
                    "quote": 10.0,
                    "timestamp": 9999999999
                }
            ],
            "buyTriggers": {},
            "sellTriggers": {}
        }
        self.assertEqual(resDump, (json.dumps(expected)))

    def test8(self):
        resDump = transactionHandler.handler("1,COMMIT_SELL,David", quoteCache)
        expected = {
            "username": "David",
            "funds": 9970.0,
            "stocks": {
                "S": {
                    "username": "David",
                    "stockSymbol": "S",
                    "quantity": 3
                }
            },
            "buyStack": [],
            "sellStack": [],
            "buyTriggers": {},
            "sellTriggers": {}
        }
        self.assertEqual(resDump, (json.dumps(expected)))

    def test9(self):
        resDump = transactionHandler.handler("1,ADD,David,-5000", quoteCache)
        expected = {
            "username": "David",
            "funds": 9970.0,
            "stocks": {
                "S": {
                    "username": "David",
                    "stockSymbol": "S",
                    "quantity": 3
                }
            },
            "buyStack": [],
            "sellStack": [],
            "buyTriggers": {},
            "sellTriggers": {}
        }
        self.assertEqual(resDump, (json.dumps(expected)))

with multiprocessing.Manager() as manager:
    global quoteCache 
    quoteCache = manager.dict()

    if __name__ == '__main__':
        unittest.main()
