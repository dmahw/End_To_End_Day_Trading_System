def Stock(username, stockSymbol, value = False, quantity = False, quote = False, timestamp = False):
    stock = {
        "username": username,
        "stockSymbol": stockSymbol,
        "value": value,
        "quantity": quantity,
        "quote": quote,
        "timestamp": timestamp
    }
    return stock

def UserStock(username, stockSymbol, quantity = False):
    userStock = {
        "username": username,
        "stockSymbol": stockSymbol,
        "quantity": quantity,
    }
    return userStock

def AmountStock(username, stockSymbol, transactionNumber, value = False, trigger = False, timestamp = False):
    amountStock = {
        "username": username,
        "stockSymbol": stockSymbol,
        "value": value,
        "trigger": trigger,
        "timestamp": timestamp,
        "transactionNumber" : transactionNumber
    }
    return amountStock

global dbLock
        