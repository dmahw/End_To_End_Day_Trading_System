import UserClass
import QuoteClass
import StockClass
import calendar
import time
import dbManager

profiling = False
testing = False

class Instruction:
    def __init__(self, transactionNumber, command, username = False, stockSymbol = False, amount = False, filename = False):
        self.transactionNumber = transactionNumber
        self.command = command
        self.username = username
        self.stockSymbol = stockSymbol
        self.amount = amount
        self.filename = filename

def handler(message, quoteCache):
    print(message)
    messageSplit = message.split(",")

    transactionNumber = messageSplit[0]
    command = messageSplit[1]

    result = 1
    if profiling == True:
        import cProfile, pstats, io
        import pstats
        pr = cProfile.Profile()
        pr.enable()
    if "ADD" == command:
        username = messageSplit[2]
        amount = messageSplit[3]

        instruction = Instruction(transactionNumber, command, username, False, amount, False)
        user = UserClass.User(username, instruction)
        result = add(user, amount)


    elif "QUOTE" == command:
        username = messageSplit[2]
        stockSymbol = messageSplit[3]

        instruction = Instruction(transactionNumber, command, username, stockSymbol, False, False)
        user = UserClass.User(username, instruction)
        result = quote(user, quoteCache, stockSymbol)
    

    elif "BUY" == command:
        username = messageSplit[2]
        stockSymbol = messageSplit[3]
        amount = messageSplit[4]

        instruction = Instruction(transactionNumber, command, username, stockSymbol, amount, False)
        user = UserClass.User(username, instruction)
        result = buy(user, quoteCache, stockSymbol, amount)


    elif "COMMIT_BUY" == command:
        username = messageSplit[2]

        instruction = Instruction(transactionNumber, command, username, False, False, False)
        user = UserClass.User(username, instruction)
        result = commitBuy(user)


    elif "CANCEL_BUY" == command:
        username = messageSplit[2]

        instruction = Instruction(transactionNumber, command, username, False, False, False)
        user = UserClass.User(username, instruction)
        result = cancelBuy(user)
    

    elif "SELL" == command:
        username = messageSplit[2]
        stockSymbol = messageSplit[3]
        amount = messageSplit[4]

        instruction = Instruction(transactionNumber, command, username, stockSymbol, amount, False)
        user = UserClass.User(username, instruction)
        result = sell(user, quoteCache, stockSymbol, amount)
    

    elif "COMMIT_SELL" == command:
        username = messageSplit[2]

        instruction = Instruction(transactionNumber, command, username, False, False, False)
        user = UserClass.User(username, instruction)
        result = commitSell(user)

    elif "CANCEL_SELL" == command:
        username = messageSplit[2]

        instruction = Instruction(transactionNumber, command, username, False, False, False)
        user = UserClass.User(username, instruction)
        result = cancelSell(user)


    elif "SET_BUY_AMOUNT" == command:
        username = messageSplit[2]
        stockSymbol = messageSplit[3]
        amount = messageSplit[4]

        instruction = Instruction(transactionNumber, command, username, stockSymbol, amount, False)
        user = UserClass.User(username, instruction)
        result = setBuyAmount(user, stockSymbol, amount)


    elif "SET_BUY_TRIGGER" == command:
        username = messageSplit[2]
        stockSymbol = messageSplit[3]
        amount = messageSplit[4]

        instruction = Instruction(transactionNumber, command, username, stockSymbol, amount, False)
        user = UserClass.User(username, instruction)
        result = setBuyTrigger(user, stockSymbol, amount)


    elif "CANCEL_SET_BUY" == command:
        username = messageSplit[2]
        stockSymbol = messageSplit[3]

        instruction = Instruction(transactionNumber, command, username, stockSymbol, False, False)
        user = UserClass.User(username, instruction)
        result = cancelSetBuy(user, stockSymbol)


    elif "SET_SELL_AMOUNT" == command:
        username = messageSplit[2]
        stockSymbol = messageSplit[3]
        amount = messageSplit[4]

        instruction = Instruction(transactionNumber, command, username, stockSymbol, amount, False)
        user = UserClass.User(username, instruction)
        result = setSellAmount(user, stockSymbol, amount)


    elif "SET_SELL_TRIGGER" == command:
        username = messageSplit[2]
        stockSymbol = messageSplit[3]
        amount = messageSplit[4]

        instruction = Instruction(transactionNumber, command, username, stockSymbol, amount, False)
        user = UserClass.User(username, instruction)
        result = setSellTrigger(user, stockSymbol, amount)


    elif "CANCEL_SET_SELL" == command:
        username = messageSplit[2]
        stockSymbol = messageSplit[3]

        instruction = Instruction(transactionNumber, command, username, stockSymbol, False, False)
        user = UserClass.User(username, instruction)
        result = cancelSetSell(user, stockSymbol)


    elif "DUMPLOG" == command:
        try:
            username = messageSplit[2]
            filename = messageSplit[3]
            result = dumplog(filename, username, transactionNumber)
        except Exception as e:
            filename = messageSplit[2]
            result = dumplog(filename, "", transactionNumber)


    elif "DISPLAY_SUMMARY" == command:
        username = messageSplit[2]

        instruction = Instruction(transactionNumber, command, username, False, False, False)
        user = UserClass.User(username, instruction)
        result = displaySummary(user)

    else:
        result = 1

    if testing:
        return displaySummary(user)

    if profiling == True:
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(0.05)
        print(s.getvalue())
    return result

def add(user, amount):
    user.updateSelfFunds()
    user.funds = float(user.funds) + float(amount)
    result = user.updateDbFunds()
    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "ADD", user.instruction.transactionNumber, "", user.username, user.funds, "", "", "", "", "", "")
    dbm.log("accountTransaction", calendar.timegm(time.gmtime()), "", "trans1", "ADD", user.instruction.transactionNumber, "ADD", user.username, user.funds, "", "", "", "", "", "")
    if result:
        return 0
    else:
        return 1

def quote(user, quoteCache, stockSymbol):
    quoteManager = QuoteClass.Quotes()
    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "QUOTE", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "", "")
    q = quoteManager.hitQuote(quoteCache, user.username, stockSymbol, user.instruction.transactionNumber)
    
    return 0

def buy(user, quoteCache, stockSymbol, amount):
    user.updateSelfFunds()
    user.updateSelfBuyStack()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "BUY", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "", "")

    quoteManager = QuoteClass.Quotes()
    q = quoteManager.getQuote(quoteCache, user.username, stockSymbol)

    if calendar.timegm(time.gmtime()) - int(q.timestamp) >= 59:
        q = quoteManager.hitQuote(quoteCache, user.username, stockSymbol, user.instruction.transactionNumber)
    
    stockQuantity = int(float(amount) / float(q.quote))
    stockValue = int(stockQuantity * float(q.quote))
    
    if (user.funds - stockValue < 0):
        print(str(user.instruction.transactionNumber) + " ERROR: Not enough funds to buy")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans1", "BUY", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "ERROR: Not enough funds to buy", "")
        return 0

    user.funds = user.funds - stockValue
    s = StockClass.Stock(user.username, stockSymbol, stockValue, stockQuantity, q.quote, q.timestamp)
    user.buyStack.append(s)

    
    dbm.log("accountTransaction", calendar.timegm(time.gmtime()), "", "trans", "BUY", user.instruction.transactionNumber, "BUY", user.username, user.funds, stockSymbol, "", "", "", "", "")
    user.updateDbFunds()
    user.updateDbUserBuyStack()
    return 0

def commitBuy(user):
    user.updateSelfBuyStack()
    user.updateSelfStocks()
    dbm = dbManager.DBM()


    if (len(user.buyStack) <= 0):
        print(str(user.instruction.transactionNumber) + " ERROR: No stocks to be commited to buy")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans1", "COMMIT_BUY", user.instruction.transactionNumber, "", user.username, "", "", "", "", "", "ERROR: No stocks to be commited to buy", "")
        return 0

    s = user.buyStack.pop()
    if calendar.timegm(time.gmtime()) - s["timestamp"] >= 59:
        print(str(user.instruction.transactionNumber) + " ERROR: Expired stock quote")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans1", "COMMIT_BUY", user.instruction.transactionNumber, "", user.username, "", "", "", "", "", "ERROR: Expired stock quote", "")
        return 0

    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "COMMIT_BUY", user.instruction.transactionNumber, "", user.username, "", s["stockSymbol"], "", "", "", "", "")

    if s["stockSymbol"] in user.stocks:
        user.stocks[s["stockSymbol"]]["quantity"] = user.stocks[s["stockSymbol"]]["quantity"] + s["quantity"]
    else:
        userStock = StockClass.UserStock(user.username, s["stockSymbol"], s["quantity"])
        user.stocks[s["stockSymbol"]] = userStock
    
    user.updateDbUserStocks()
    user.updateDbUserBuyStack()
    return 0


def cancelBuy(user):
    user.updateSelfFunds()
    user.updateSelfBuyStack()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "CANCEL_BUY", user.instruction.transactionNumber, "", user.username, user.funds, "", "", "", "", "", "")

    if (len(user.buyStack) <= 0):
        print(str(user.instruction.transactionNumber) + " ERROR: No stocks to cancel")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans1", "CANCEL_BUY", user.instruction.transactionNumber, "", user.username, user.funds, "", "", "", "", "ERROR: No stocks to cancel", "")
        return 0

    s = user.buyStack.pop()

    user.funds = user.funds + s["value"]

    dbm.log("accountTransaction", calendar.timegm(time.gmtime()), "", "trans", "CANCEL_BUY", user.instruction.transactionNumber, "CANCEL_BUY", user.username, user.funds, "", "", "", "", "", )

    user.updateDbUserBuyStack()
    user.updateDbFunds()
    return 0

def sell(user, quoteCache, stockSymbol, amount):
    user.updateSelfFunds()
    user.updateSelfSellStack()
    user.updateSelfStocks()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "SELL", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "", "")

    quoteManager = QuoteClass.Quotes()
    q = quoteManager.getQuote(quoteCache, user.username, stockSymbol)

    if calendar.timegm(time.gmtime()) - int(q.timestamp) >= 59:
        q = quoteManager.hitQuote(quoteCache, user.username, stockSymbol, user.instruction.transactionNumber)
    

    if not stockSymbol in user.stocks:
        print(str(user.instruction.transactionNumber) + " ERROR: User doesn't have stock")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "SELL", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "ERROR: User doesn't have stock", "")
        return 0

    stockQuantity = int(float(amount) / float(q.quote))
    stockValue = int(stockQuantity * float(q.quote))

    if user.stocks[stockSymbol]["quantity"] - stockQuantity <= 0:
        print(str(user.instruction.transactionNumber) + " ERROR: User doesn't have enough stock amount")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "SELL", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "ERROR: User doesn't have enough stock amount", "")
        return 0
        
    user.stocks[stockSymbol]["quantity"] = user.stocks[stockSymbol]["quantity"] - stockQuantity

    s = StockClass.Stock(user.username, stockSymbol, stockValue, stockQuantity, q.quote, q.timestamp)
    user.sellStack.append(s)

    dbm.log("accountTransaction", calendar.timegm(time.gmtime()), "", "trans", "SELL", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "", "")

    user.updateDbUserStocks()
    user.updateDbUserSellStack()
    user.updateDbFunds()
    return 0

def commitSell(user):
    user.updateSelfFunds()
    user.updateSelfSellStack()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "COMMIT_SELL", user.instruction.transactionNumber, "", user.username, user.funds, "", "", "", "", "", "")

    if (len(user.sellStack) <= 0):
        print(str(user.instruction.transactionNumber) + " ERROR: No stocks to be commited to sell")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "COMMIT_SELL", user.instruction.transactionNumber, "", user.username, user.funds, "", "", "", "", "ERROR: No stocks to be commited to sell", "")
        return 0

    s = user.sellStack.pop()
    if calendar.timegm(time.gmtime()) - s["timestamp"] >= 59:
        print(str(user.instruction.transactionNumber) + " ERROR: Expired stock quote")
        return 0
    
    user.funds = user.funds + s["value"]
    
    dbm.log("accountTransaction", calendar.timegm(time.gmtime()), "", "trans1", "COMMIT_SELL", user.instruction.transactionNumber, "COMMIT_SELL", user.username, user.funds, "", "", "", "", "", "")


    user.updateDbUserSellStack()
    user.updateDbFunds()
    return 0

def cancelSell(user):
    user.updateSelfSellStack()
    user.updateSelfStocks()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "CANCEL_SELL", user.instruction.transactionNumber, "", user.username, "", "", "", "", "", "", "")

    if (len(user.sellStack) <= 0):
        print(str(user.instruction.transactionNumber) + " ERROR: No sells to cancel")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "CANCEL_SELL", user.instruction.transactionNumber, "", user.username, "", "", "", "", "", "ERROR: No sells to cancel", "")
        return 0
    s = user.sellStack.pop()
    
    user.stocks[s["stockSymbol"]]["quantity"] = user.stocks[s["stockSymbol"]]["quantity"] + s["quantity"]

    user.updateDbUserStocks()
    user.updateDbUserSellStack()
    return 0

def setBuyAmount(user, stockSymbol, amount):
    user.updateSelfFunds()
    user.updateSelfBuyTriggers()
    user.updateSelfStocks()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "SET_BUY_AMOUNT", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "", "")

    if float(user.funds) - float(amount) <= 0:
        print(str(user.instruction.transactionNumber) + " ERROR: Not enough funds")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "SET_BUY_AMOUNT", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "ERROR: Not enough funds", "")
        return 0

    if stockSymbol in user.buyTriggers:
        amountStock = user.buyTriggers[stockSymbol]
    else:
        amountStock = StockClass.AmountStock(user.username, stockSymbol, user.instruction.transactionNumber, 0, False, False)
    
    if not stockSymbol in user.stocks:
        userStock = StockClass.UserStock(user.username, stockSymbol, 0)
        user.stocks[stockSymbol] = userStock

    amountStock["value"] = float(amountStock["value"]) + float(amount)
    amountStock["timestamp"] = calendar.timegm(time.gmtime())
    amountStock["transactionNumber"] = user.instruction.transactionNumber
    user.buyTriggers[stockSymbol] = amountStock
    user.funds = float(user.funds) - float(amount)

    dbm.log("accountTransaction", calendar.timegm(time.gmtime()), "", "trans", "SET_BUY_AMOUNT", user.instruction.transactionNumber, "SET_BUY_AMOUNT", user.username, user.funds, "", "", "", "", "", "")

    user.updateDbUserStocks()
    user.updateDbUserBuyTriggers()
    user.updateDbFunds()

    return 0

def setBuyTrigger(user, stockSymbol, amount):
    user.updateSelfBuyTriggers()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "SET_BUY_TRIGGER", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "", "")

    if not stockSymbol in user.buyTriggers:
        print(str(user.instruction.transactionNumber) + " ERROR: Must set buy amount first")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "SET_BUY_TRIGGER", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "ERROR: Must set buy amount first", "")
        return 0

    amountStock = user.buyTriggers[stockSymbol]

    if amountStock["value"] <= 0:
        print(str(user.instruction.transactionNumber) + " ERROR: Must set buy amount first")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "SET_BUY_TRIGGER", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "ERROR: Must set buy amount first", "")
        return 0
    
    amountStock["trigger"] = amount
    amountStock["transactionNumber"] = user.instruction.transactionNumber
    user.buyTriggers[stockSymbol] = amountStock

    user.updateDbUserBuyTriggers()
    return 0

def cancelSetBuy(user, stockSymbol):
    user.updateSelfFunds()
    user.updateSelfBuyTriggers()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "CANCEL_SET_BUY", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "", "")

    if not stockSymbol in user.buyTriggers:
        print(str(user.instruction.transactionNumber) + " ERROR: No trigger set")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "CANCEL_SET_BUY", user.instruction.transactionNumber, "", user.username, user.funds, stockSymbol, "", "", "", "ERROR: No trigger set", "")
        return 0

    amountStock = user.buyTriggers[stockSymbol]
    user.funds = user.funds + amountStock["value"]
    amountStock["value"] = False
    amountStock["trigger"] = False
    amountStock["timestamp"] = calendar.timegm(time.gmtime())
    amountStock["transactionNumber"] = user.instruction.transactionNumber
    user.buyTriggers[stockSymbol] = amountStock

    dbm.log("accountTransaction", calendar.timegm(time.gmtime()), "", "trans", "CANCEL_SET_BUY", user.instruction.transactionNumber, "CANCEL_SET_BUY", user.username, user.funds, "", "", "", "", "", "")

    user.updateDbUserBuyTriggers()
    user.updateDbFunds()
    return 0

def setSellTrigger(user, stockSymbol, amount):
    user.updateSelfSellTriggers()
    user.updateSelfStocks()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "SET_SELL_TRIGGER", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "", "")

    if not stockSymbol in user.sellTriggers:
        print(str(user.instruction.transactionNumber) + " ERROR: Must set buy amount first")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "SET_SELL_TRIGGER", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "ERROR: Must set buy amount first", "")
        return 0

    amountStock = user.sellTriggers[stockSymbol]

    if amountStock["value"] <= 0:
        print(str(user.instruction.transactionNumber) + " ERROR: Must set buy amount first")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "SET_SELL_TRIGGER", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "ERROR: Must set buy amount first", "")
        return 0
    if float(amount) <= 0:
        return 0
    
    amountStock["trigger"] = float(amount)
    amountStock["transactionNumber"] = user.instruction.transactionNumber
    
    fakeStockQuantityToSell = int( float(amountStock["value"]) / float(amountStock["trigger"]) )

    userStock = user.stocks[stockSymbol]

    if userStock["quantity"] - fakeStockQuantityToSell <= 0:
        print(str(user.instruction.transactionNumber) + " ERROR: Not enough stock")
        amountStock["trigger"] = False
        amountStock["value"] = False
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "SET_SELL_TRIGGER", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "ERROR: Not enough stock", "")
        return 0

    userStock["quantity"] = userStock["quantity"] - fakeStockQuantityToSell
    amountStock["timestamp"] = calendar.timegm(time.gmtime())

    user.sellTriggers[stockSymbol] = amountStock
    user.stocks[stockSymbol] = userStock
    user.updateDbUserStocks()
    user.updateDbUserSellTriggers()
    return 0

def setSellAmount(user, stockSymbol, amount):
    user.updateSelfSellTriggers()
    user.updateSelfStocks()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "SET_SELL_AMOUNT", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "", "")
    
    if not stockSymbol in user.stocks:
        print(str(user.instruction.transactionNumber) + " ERROR: Not enough specified stock")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "SET_SELL_AMOUNT", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "ERROR: Not enough specified stock", "")
        return 0
    
    if stockSymbol in user.sellTriggers:
        amountStock = user.sellTriggers[stockSymbol]
    else:
        amountStock = StockClass.AmountStock(user.username, stockSymbol, user.instruction.transactionNumber, 0, False, False)
     
    amountStock["value"] = float(amountStock["value"]) + float(amount)
    amountStock["timestamp"] = calendar.timegm(time.gmtime())
    amountStock["transactionNumber"] = user.instruction.transactionNumber
    user.sellTriggers[stockSymbol] = amountStock

    user.updateDbUserStocks()
    user.updateDbUserSellTriggers()
    setSellTrigger(user, stockSymbol, amountStock["trigger"])
    return 0

def cancelSetSell(user, stockSymbol):
    user.updateSelfStocks()
    user.updateSelfSellTriggers()

    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans1", "CANCEL_SET_SELL", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "", "")

    if not stockSymbol in user.sellTriggers:
        print(str(user.instruction.transactionNumber) + " ERROR: No trigger set")
        dbm.log("errorEvent", calendar.timegm(time.gmtime()), "", "trans", "CANCEL_SET_SELL", user.instruction.transactionNumber, "", user.username, "", stockSymbol, "", "", "", "ERROR: No trigger set", "")
        return 0

    amountStock = user.sellTriggers[stockSymbol]
    userStock = user.stocks[stockSymbol]

    if float(amountStock["trigger"]) <= 0:
        return 0
    refundStockQuantity = int(float(amountStock["value"]) / float(amountStock["trigger"]))
    userStock["quantity"]  = int(userStock["quantity"]) + refundStockQuantity
    amountStock["value"] = False
    amountStock["trigger"] = False
    amountStock["timestamp"] = calendar.timegm(time.gmtime())
    amountStock["transactionNumber"] = user.instruction.transactionNumber

    user.stocks[stockSymbol] = userStock
    user.sellTriggers[stockSymbol] = amountStock

    user.updateDbUserSellTriggers()
    user.updateDbUserStocks()
    return 0

def dumplog(filename, username, transactionNumber):
    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans", "DUMPLOG", transactionNumber, "", username, "", "", "", "", filename, "", "")
    dbm.exportLog(filename, username)
    return 0

def displaySummary(user):
    dbm = dbManager.DBM()
    dbm.log("userCommand", calendar.timegm(time.gmtime()), "", "trans", "DISPLAY_SUMMARY", user.instruction.transactionNumber, "", user.username, "", "", "", "", "", "", "")
    logResults = dbm.getLogs(user.username)

    user.updateSelfFunds()
    user.updateSelfStocks()
    user.updateSelfBuyStack()
    user.updateSelfSellStack()
    user.updateSelfBuyTriggers()
    user.updateSelfSellTriggers()

    if testing:
        import json
        someObj = {
            "username": user.username,
            "funds": user.funds,
            "stocks": user.stocks,
            "buyStack": user.buyStack,
            "sellStack": user.sellStack,
            "buyTriggers": user.buyTriggers,
            "sellTriggers": user.sellTriggers,
        }
        return json.dumps(someObj)
    else:
        import json
        someObj = {
            "username": user.username,
            "funds": user.funds,
            "stocks": user.stocks,
            "buyStack": user.buyStack,
            "sellStack": user.sellStack,
            "buyTriggers": user.buyTriggers,
            "sellTriggers": user.sellTriggers,
            "logs": logResults
        }
        return json.dumps(someObj)
