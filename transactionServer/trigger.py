import QuoteClass
import dbManager
import time
import calendar

def buyTrigger(quoteCache):
    dbm = dbManager.DBM()
    quotes = QuoteClass.Quotes()

    while(True):
        for userRow in dbm.getAllBuyTriggers():
            username = userRow["username"]
            buyTriggers = userRow["buyTriggers"]

            for stockSymbol, buyTrigger in buyTriggers.items():
                if float(buyTrigger["value"]) <= 0 or buyTrigger["value"] == False:
                    continue

                if float(buyTrigger["trigger"]) <= 0 or buyTrigger["trigger"] == False:
                    continue
                
                q = quotes.hitQuote(quoteCache, username, buyTrigger["stockSymbol"], buyTrigger["transactionNumber"])

                if float(q.quote) >= float(buyTrigger["trigger"]):
                    continue
                
                stockQuantityToBuy = int(float(buyTrigger["value"]) / float(q.quote))
                stockValueToBuy = float(stockQuantityToBuy) * float(q.quote)
                change = float(buyTrigger["value"]) - stockValueToBuy

                dbm.log("systemEvent", calendar.timegm(time.gmtime()), "", "buyTrigger", "SET_BUY_TRIGGER", buyTrigger["transactionNumber"], "", username, "", buyTrigger["stockSymbol"], "", "", "", "", "")

                dbm.updateUserFundsSpecific(username, change)
                dbm.updateUserStockSpecific(username, buyTrigger["stockSymbol"], stockQuantityToBuy)
                dbm.updateUserBuyTriggerSpecific(username, buyTrigger["stockSymbol"])
        time.sleep(59)

def sellTrigger(quoteCache):
    dbm = dbManager.DBM()
    quotes = QuoteClass.Quotes()

    while(True):
        for userRow in dbm.getAllSellTriggers():
            username = userRow["username"]
            sellTriggers = userRow["sellTriggers"]

            for stockSymbol, sellTrigger in sellTriggers.items():
                if float(sellTrigger["value"]) <= 0 or sellTrigger["value"] == False:
                    continue
                
                if float(sellTrigger["trigger"]) <= 0 or sellTrigger["trigger"] == False:
                    continue

                q = quotes.hitQuote(quoteCache, username, sellTrigger["stockSymbol"], sellTrigger["transactionNumber"])

                if float(q.quote) <= float(sellTrigger["trigger"]):
                    continue

                fakeStockQuantityToSell = int(float(sellTrigger["value"]) / float(sellTrigger["trigger"]))
                
                stockQuantityToSell = int(float(sellTrigger["value"]) / float(q.quote))
                change = fakeStockQuantityToSell - stockQuantityToSell
                stockValueToSell = float(stockQuantityToSell) * float(q.quote)

                dbm.log("systemEvent", calendar.timegm(time.gmtime()), "", "sellTrigger", "SET_SELL_TRIGGER", sellTrigger["transactionNumber"], "", username, "", sellTrigger["stockSymbol"], "", "", "", "", "")

                dbm.updateUserFundsSpecific(username, stockValueToSell)
                dbm.updateUserStockSpecific(username, sellTrigger["stockSymbol"], change)
                dbm.updateUserSellTriggerSpecific(username, sellTrigger["stockSymbol"])
        time.sleep(59)
            
