import pymongo
import sys

class DBM:
    def __init__(self, addr = "127.0.0.1", port = 27017):
        if len(sys.argv) >= 3:
            if sys.argv[3]:
                addr = str(sys.argv[3])
            else:
                addr = "127.0.0.1"

            if sys.argv[4]:
                port = int(sys.argv[4])
            else:
                port = 27017
        self.client = pymongo.MongoClient(addr, port)
        self.db = self.client["dayTradingDb"]


    def getUserInfo(self, username):
        self.db = self.client["dayTradingDbUserInfo"]
        col = self.db["userInfo"]
        result = col.find_one({"username": username})
        return result

    def insertUserInfo(self, username, funds):
        self.db = self.client["dayTradingDbUserInfo"]
        col = self.db["userInfo"]
        newDoc = { "username": username, "funds": funds }
        result = col.insert_one(newDoc)
        return result

    def updateUserFunds(self, username, funds):
        self.db = self.client["dayTradingDbUserInfo"]
        col = self.db["userInfo"]
        query = { "username": username }
        newValue = { "$set": { "funds": funds } }
        result = col.update_one(query, newValue)

        if result.matched_count > 0:
            return result
        else:
            return self.insertUserInfo(username, funds)



    def getUserBuyStack(self, username):
        self.db = self.client["dayTradingDbUserBuyStack"]
        col = self.db["userBuyStack"]
        result = col.find_one({"username": username})
        return result

    def insertUserBuyStack(self, username, buyStack):
        self.db = self.client["dayTradingDbUserBuyStack"]
        col = self.db["userBuyStack"]
        newDoc = { "username": username, "buyStack": buyStack }
        result = col.insert_one(newDoc)
        return result

    def updateUserBuyStack(self, username, buyStack):
        self.db = self.client["dayTradingDbUserBuyStack"]
        col = self.db["userBuyStack"]
        query = { "username": username }
        newValue = { "$set": { "buyStack": buyStack } }
        result = col.update_one(query, newValue)

        if result.matched_count > 0:
            return result
        else:
            return self.insertUserBuyStack(username, buyStack)



    def getUserSellStack(self, username):
        self.db = self.client["dayTradingDbUserSellStack"]
        col = self.db["userSellStack"]
        result = col.find_one({"username": username})
        return result

    def insertUserSellStack(self, username, sellStack):
        self.db = self.client["dayTradingDbUserSellStack"]
        col = self.db["userSellStack"]
        newDoc = { "username": username, "sellStack": sellStack }
        result = col.insert_one(newDoc)
        return result

    def updateUserSellStack(self, username, sellStack):
        self.db = self.client["dayTradingDbUserSellStack"]
        col = self.db["userSellStack"]
        query = { "username": username }
        newValue = { "$set": { "sellStack": sellStack } }
        result = col.update_one(query, newValue)

        if result.matched_count > 0:
            return result
        else:
            return self.insertUserSellStack(username, sellStack)

    

    def getUserStocks(self, username):
        self.db = self.client["dayTradingDbUserStocks"]
        col = self.db["userStocks"]
        result = col.find_one({"username": username})
        return result

    def insertUserStocks(self, username, stocks):
        self.db = self.client["dayTradingDbUserStocks"]
        col = self.db["userStocks"]
        newDoc = { "username": username, "stocks": stocks }
        result = col.insert_one(newDoc)
        return result

    def updateUserStocks(self, username, stocks):
        self.db = self.client["dayTradingDbUserStocks"]
        col = self.db["userStocks"]
        query = { "username": username }
        newValue = { "$set": { "stocks": stocks } }
        result = col.update_one(query, newValue)

        if result.matched_count > 0:
            return result
        else:
            return self.insertUserStocks(username, stocks)

    


    def getUserBuyTriggers(self, username):
        self.db = self.client["dayTradingDbUserBuyTriggers"]
        col = self.db["userBuyTriggers"]
        result = col.find_one({"username": username})
        return result

    def insertUserBuyTriggers(self, username, buyTriggers):
        self.db = self.client["dayTradingDbUserBuyTriggers"]
        col = self.db["userBuyTriggers"]
        newDoc = { "username": username, "buyTriggers": buyTriggers }
        result = col.insert_one(newDoc)
        return result

    def updateUserBuyTriggers(self, username, buyTriggers):
        self.db = self.client["dayTradingDbUserBuyTriggers"]
        col = self.db["userBuyTriggers"]
        query = { "username": username }
        newValue = { "$set": { "buyTriggers": buyTriggers } }
        result = col.update_one(query, newValue)

        if result.matched_count > 0:
            return result
        else:
            return self.insertUserBuyTriggers(username, buyTriggers)



    def getUserSellTriggers(self, username):
        self.db = self.client["dayTradingDbUserSellTriggers"]
        col = self.db["userSellTriggers"]
        result = col.find_one({"username": username})
        return result

    def insertUserSellTriggers(self, username, sellTriggers):
        self.db = self.client["dayTradingDbUserSellTriggers"]
        col = self.db["userSellTriggers"]
        newDoc = { "username": username, "sellTriggers": sellTriggers }
        result = col.insert_one(newDoc)
        return result

    def updateUserSellTriggers(self, username, sellTriggers):
        self.db = self.client["dayTradingDbUserSellTriggers"]
        col = self.db["userSellTriggers"]
        query = { "username": username }
        newValue = { "$set": { "sellTriggers": sellTriggers } }
        result = col.update_one(query, newValue)

        if result.matched_count > 0:
            return result
        else:
            return self.insertUserSellTriggers(username, sellTriggers)


    def getAllBuyTriggers(self):
        self.db = self.client["dayTradingDbUserBuyTriggers"]
        col = self.db["userBuyTriggers"]
        result = col.find()
        return result
    
    def updateUserFundsSpecific(self, username, difference):
        self.db = self.client["dayTradingDbUserInfo"]
        col = self.db["userInfo"]
        query = { "username": username }
        newValue = { "$inc": { "funds": difference } }
        result = col.update_one(query, newValue)
        return result
    
    def updateUserStockSpecific(self, username, stockSymbol, difference):
        self.db = self.client["dayTradingDbUserStocks"]
        col = self.db["userStocks"]
        query = { "username": username }
        newValue = { "$inc": { "stocks." + stockSymbol + ".quantity": difference } }
        result = col.update_one(query, newValue)

    def updateUserBuyTriggerSpecific(self, username, stockSymbol):
        self.db = self.client["dayTradingDbUserBuyTriggers"]
        col = self.db["userBuyTriggers"]
        query = { "username": username }
        newValue = { "$set": { "buyTriggers." + stockSymbol + ".value": 0 } }
        result = col.update_one(query, newValue)
        newValue = { "$set": { "buyTriggers." + stockSymbol + ".trigger": 0 } }
        result = col.update_one(query, newValue)


    def getAllSellTriggers(self):
        self.db = self.client["dayTradingDbUserSellTriggers"]
        col = self.db["userSellTriggers"]
        result = col.find()
        return result

    def updateUserSellTriggerSpecific(self, username, stockSymbol):
        self.db = self.client["dayTradingDbUserSellTriggers"]
        col = self.db["userSellTriggers"]
        query = { "username": username }
        newValue = { "$set": { "sellTriggers." + stockSymbol + ".value": 0 } }
        result = col.update_one(query, newValue)
        newValue = { "$set": { "sellTriggers." + stockSymbol + ".trigger": 0 } }
        result = col.update_one(query, newValue)


    def log(self, msgType = "", timestamp = "", quoteServerTime = "", server = "", command = "", transactionNum = "", action = "", username = "", funds = "", stockSymbol = "", price = "", cryptoKey = "", filename = "", errorMessage = "", debugMessage = ""):
        logMessage = {
            "msgType": msgType,
            "timestamp": timestamp,
            "quoteServerTime": quoteServerTime,
            "server": server,
            "command": command,
            "transactionNum": transactionNum,
            "action": action,
            "username": username,
            "funds": funds,
            "stockSymbol": stockSymbol,
            "price": price,
            "cryptoKey": cryptoKey,
            "filename": filename,
            "errorMessage": errorMessage,
            "debugMessage": debugMessage
        }
        col = self.db["logs"]
        result = col.insert_one(logMessage)
        return result
    
    def exportLog(self, filename, username = False):
        col = self.db["logs"]
        if not username:
            result = col.find()
        else:
            result = col.find({ "username": username })
                
        outputFile = open(filename, "w")
        outputFile.write("<?xml version=\"1.0\"?>\n<log>\n\n")
        for msg in result:
            msg["timestamp"] = msg["timestamp"] * 1000
            if str(msg["msgType"]) == "userCommand":
                outputFile.write("<" + str(msg["msgType"]) + ">\n") 
                outputFile.write("\t<timestamp>" + str(msg["timestamp"]) + "</timestamp>\n")
                outputFile.write("\t<server>" + str(msg["server"]) + "</server>\n")
                outputFile.write("\t<transactionNum>" + str(msg["transactionNum"]) + "</transactionNum>\n")
                outputFile.write("\t<command>" + str(msg["command"]) + "</command>\n")
                if not str(msg["username"]) == "": outputFile.write("\t<username>" + str(msg["username"]) + "</username>\n")
                if not str(msg["stockSymbol"]) == "": outputFile.write("\t<stockSymbol>" + str(msg["stockSymbol"]) + "</stockSymbol>\n")
                if not str(msg["filename"]) == "": outputFile.write("\t<filename>" + str(msg["filename"]) + "</filename>\n")
                if not str(msg["funds"]) == "": outputFile.write("\t<funds>" + str(msg["funds"]) + "</funds>\n")
                outputFile.write("</" + str(msg["msgType"]) + ">\n")

            elif str(msg["msgType"]) == "quoteServer":
                outputFile.write("<" + str(msg["msgType"]) + ">\n") 
                outputFile.write("\t<timestamp>" + str(msg["timestamp"]) + "</timestamp>\n")
                outputFile.write("\t<server>" + str(msg["server"]) + "</server>\n")
                outputFile.write("\t<transactionNum>" + str(msg["transactionNum"]) + "</transactionNum>\n")
                outputFile.write("\t<price>" + str(msg["price"]) + "</price>\n")
                outputFile.write("\t<stockSymbol>" + str(msg["stockSymbol"]) + "</stockSymbol>\n")
                outputFile.write("\t<username>" + str(msg["username"]) + "</username>\n")
                outputFile.write("\t<quoteServerTime>" + str(msg["quoteServerTime"]) + "</quoteServerTime>\n")
                outputFile.write("\t<cryptokey>" + str(msg["cryptoKey"]) + "</cryptokey>\n")
                outputFile.write("</" + str(msg["msgType"]) + ">\n")

            elif str(msg["msgType"]) == "accountTransaction":
                outputFile.write("<" + str(msg["msgType"]) + ">\n") 
                outputFile.write("\t<timestamp>" + str(msg["timestamp"]) + "</timestamp>\n")
                outputFile.write("\t<server>" + str(msg["server"]) + "</server>\n")
                outputFile.write("\t<transactionNum>" + str(msg["transactionNum"]) + "</transactionNum>\n")
                outputFile.write("\t<action>" + str(msg["action"]) + "</action>\n")
                outputFile.write("\t<username>" + str(msg["username"]) + "</username>\n")
                outputFile.write("\t<funds>" + str(msg["funds"]) + "</funds>\n")
                outputFile.write("</" + str(msg["msgType"]) + ">\n")


            elif str(msg["msgType"]) == "systemEvent":
                outputFile.write("<" + str(msg["msgType"]) + ">\n") 
                outputFile.write("\t<timestamp>" + str(msg["timestamp"]) + "</timestamp>\n")
                outputFile.write("\t<server>" + str(msg["server"]) + "</server>\n")
                outputFile.write("\t<transactionNum>" + str(msg["transactionNum"]) + "</transactionNum>\n")
                outputFile.write("\t<command>" + str(msg["command"]) + "</command>\n")
                if not str(msg["username"]) == "": outputFile.write("\t<username>" + str(msg["username"]) + "</username>\n")
                if not str(msg["stockSymbol"]) == "": outputFile.write("\t<stockSymbol>" + str(msg["stockSymbol"]) + "</stockSymbol>\n")
                if not str(msg["filename"]) == "": outputFile.write("\t<filename>" + str(msg["filename"]) + "</filename>\n")
                if not str(msg["funds"]) == "": outputFile.write("\t<funds>" + str(msg["funds"]) + "</funds>\n")
                outputFile.write("</" + str(msg["msgType"]) + ">\n")

            elif str(msg["msgType"]) == "errorEvent":
                outputFile.write("<" + str(msg["msgType"]) + ">\n") 
                outputFile.write("\t<timestamp>" + str(msg["timestamp"]) + "</timestamp>\n")
                outputFile.write("\t<server>" + str(msg["server"]) + "</server>\n")
                outputFile.write("\t<transactionNum>" + str(msg["transactionNum"]) + "</transactionNum>\n")
                outputFile.write("\t<command>" + str(msg["command"]) + "</command>\n")
                if not str(msg["username"]) == "": outputFile.write("\t<username>" + str(msg["username"]) + "</username>\n")
                if not str(msg["stockSymbol"]) == "": outputFile.write("\t<stockSymbol>" + str(msg["stockSymbol"]) + "</stockSymbol>\n")
                if not str(msg["filename"]) == "": outputFile.write("\t<filename>" + str(msg["filename"]) + "</filename>\n")
                if not str(msg["funds"]) == "": outputFile.write("\t<funds>" + str(msg["funds"]) + "</funds>\n")
                if not str(msg["errorMessage"]) == "": outputFile.write("\t<errorMessage>" + str(msg["errorMessage"]) + "</errorMessage>\n")
                outputFile.write("</" + str(msg["msgType"]) + ">\n")

            elif str(msg["msgType"]) == "debugEvent":
                outputFile.write("<" + str(msg["msgType"]) + ">\n") 
                outputFile.write("\t<timestamp>" + str(msg["timestamp"]) + "</timestamp>\n")
                outputFile.write("\t<server>" + str(msg["server"]) + "</server>\n")
                outputFile.write("\t<transactionNum>" + str(msg["transactionNum"]) + "</transactionNum>\n")
                outputFile.write("\t<command>" + str(msg["command"]) + "</command>\n")
                if not str(msg["username"]) == "": outputFile.write("\t<username>" + str(msg["username"]) + "</username>\n")
                if not str(msg["stockSymbol"]) == "": outputFile.write("\t<stockSymbol>" + str(msg["stockSymbol"]) + "</stockSymbol>\n")
                if not str(msg["filename"]) == "": outputFile.write("\t<filename>" + str(msg["filename"]) + "</filename>\n")
                if not str(msg["funds"]) == "": outputFile.write("\t<funds>" + str(msg["funds"]) + "</funds>\n")
                if not str(msg["debugMessage"]) == "": outputFile.write("\t<debugMessage>" + str(msg["debugMessage"]) + "</debugMessage>\n")
                outputFile.write("</" + str(msg["msgType"]) + ">\n")

        outputFile.write("\n</log>")
        outputFile.close()
        return result

    def getLogs(self, username):
        col = self.db["logs"]
        result = col.find({"$and":[ {"username":username}, {"msgType":"userCommand"}]})
        data = []
        for msg in result.sort([("timestamp", -1), ("transactionNum", -1)]).limit(10):
            simpleLog = {
                "timestamp": msg["timestamp"],
                "command": msg["command"],
                "transactionNumber": msg["transactionNum"],
                "username": msg["username"],
                "stockSymbol": msg["stockSymbol"],
                "funds": msg["funds"]
            }
            data.append(simpleLog)
        return data
