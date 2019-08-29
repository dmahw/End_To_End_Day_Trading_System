import calendar
import time
import dbManager
import socket

testing = False

class Quote:
    def __init__(self, quote, stockSymbol, userid, timestamp, cryptokey):
        self.stockSymbol = stockSymbol
        self.quote = quote
        self.userid = userid
        self.cryptokey = cryptokey
        self.timestamp = timestamp

    def print(self):
        print(str(self.stockSymbol) + "," + str(self.quote) + "," + str(self.userid) + "," + str(self.cryptokey) + "," + str(self.timestamp))
 

class Quotes:
    def hitQuote(self, quoteCache, userid, stockSymbol, transactionNumber):
        dbm = dbManager.DBM()
        dummy = True

        if dummy == True:
            if stockSymbol in quoteCache:
                quote = quoteCache[stockSymbol]
                if calendar.timegm(time.gmtime()) - int(quote.timestamp) >= 59:
                    time.sleep(1)
                    if testing:
                        newQuote = Quote(10.00, stockSymbol, userid, 9999999999, "abcdefghijklmnopqrstuvwxyz" )
                    else:
                        newQuote = Quote(10.00, stockSymbol, userid, calendar.timegm(time.gmtime()), "abcdefghijklmnopqrstuvwxyz" )
                    quoteCache[stockSymbol] = newQuote
                    dbm.log("quoteServer", calendar.timegm(time.gmtime()), newQuote.timestamp, "trans1", "QUOTE", transactionNumber, "", newQuote.userid, "", stockSymbol, newQuote.quote, newQuote.cryptokey, "", "", "")
                    return newQuote
                else:
                    dbm.log("quoteServer", calendar.timegm(time.gmtime()), quote.timestamp, "trans1", "QUOTE", transactionNumber, "", quote.userid, "", stockSymbol, quote.quote, quote.cryptokey, "", "", "")
                    return quote
            else:
                time.sleep(2)
                if testing:
                    newQuote = Quote(10.00, stockSymbol, userid, 9999999999, "abcdefghijklmnopqrstuvwxyz" )
                else:
                    newQuote = Quote(10.00, stockSymbol, userid, calendar.timegm(time.gmtime()), "abcdefghijklmnopqrstuvwxyz" )
                quoteCache[stockSymbol] = newQuote
                dbm.log("quoteServer", calendar.timegm(time.gmtime()), newQuote.timestamp, "trans1", "QUOTE", transactionNumber, "", newQuote.userid, "", stockSymbol, newQuote.quote, newQuote.cryptokey, "", "", "")
                return newQuote
        else:
            if stockSymbol in quoteCache:
                quote = quoteCache[stockSymbol]
                if (calendar.timegm(time.gmtime()) - int(quote.timestamp) <= 59):
                    dbm.log("systemEvent", calendar.timegm(time.gmtime()), quote.timestamp, "trans1", "QUOTE", transactionNumber, "", quote.userid, "", stockSymbol, quote.quote, quote.cryptokey, "", "", "")
                    return quote
            host = "quoteserve.seng.uvic.ca"
            port = 4449

            sendMessage = stockSymbol + "," + userid + "\r"
            sendMessage = sendMessage.encode()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(sendMessage)

            receiveMessage = s.recv(1024).decode()
            resp = receiveMessage.split(",")
            newQuote = Quote(resp[0], resp[1], resp[2], int(resp[3]), resp[4].split("\n")[0])
            quoteCache[stockSymbol] = newQuote

            dbm.log("quoteServer", calendar.timegm(time.gmtime()), newQuote.timestamp, "trans1", "QUOTE", transactionNumber, "", newQuote.userid, "", stockSymbol, newQuote.quote, newQuote.cryptokey, "", "", "")
            return newQuote


    def getQuote(self, quoteCache, userid, stockSymbol):
        if stockSymbol in quoteCache:
            return quoteCache[stockSymbol]
        else:
            newQuote = Quote(False, stockSymbol, userid, -1, "abcdefghijklmnopqrstuvwxyz")
            quoteCache[stockSymbol] = newQuote

            return newQuote
