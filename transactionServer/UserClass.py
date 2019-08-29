import dbManager

class User:
    def __init__(self, username, instruction, funds = False, buyStack = False, sellStack = False, stocks = False, buyTriggers = False, sellTriggers = False):
        self.username = username
        self.funds = funds
        self.buyStack = buyStack
        self.sellStack = sellStack
        self.stocks = stocks
        self.instruction = instruction
        self.buyTriggers = buyTriggers
        self.sellTriggers = sellTriggers

    # def __del__(self):
    #     self.updateDB()

    def updateSelfFunds(self):
        dbm = dbManager.DBM()
        userInfo = dbm.getUserInfo(self.username)
        if userInfo == None:
            self.funds = 0
        else:
            self.funds = userInfo["funds"]
        return 0

    def updateSelfBuyStack(self):
        dbm = dbManager.DBM()
        userBuyStack = dbm.getUserBuyStack(self.username)
        if userBuyStack == None:
            self.buyStack = []
        else:
            self.buyStack = userBuyStack["buyStack"]
        return 0

    def updateSelfStocks(self):
        dbm = dbManager.DBM()
        userStocks = dbm.getUserStocks(self.username)
        if userStocks == None:
            self.stocks = {}
        else:
            self.stocks = userStocks["stocks"]
        return 0
    
    def updateSelfSellStack(self):
        dbm = dbManager.DBM()
        userSellStack = dbm.getUserSellStack(self.username)
        if userSellStack == None:
            self.sellStack = []
        else:
            self.sellStack = userSellStack["sellStack"]
        return 0

    def updateSelfBuyTriggers(self):
        dbm = dbManager.DBM()
        userBuyTriggers = dbm.getUserBuyTriggers(self.username)
        if userBuyTriggers == None:
            self.buyTriggers = {}
        else:
            self.buyTriggers = userBuyTriggers["buyTriggers"]
        return 0

    def updateSelfSellTriggers(self):
        dbm = dbManager.DBM()
        userSellTriggers = dbm.getUserSellTriggers(self.username)
        if userSellTriggers == None:
            self.sellTriggers = {}
        else:
            self.sellTriggers = userSellTriggers["sellTriggers"]
        return 0



    def updateDbFunds(self):
        dbm = dbManager.DBM()
        return dbm.updateUserFunds(self.username, self.funds)
        
    def updateDbUserBuyStack(self):
        dbm = dbManager.DBM()
        return dbm.updateUserBuyStack(self.username, self.buyStack)

    def updateDbUserStocks(self):
        dbm = dbManager.DBM()
        return dbm.updateUserStocks(self.username, self.stocks)

    def updateDbUserSellStack(self):
        dbm = dbManager.DBM()
        return dbm.updateUserSellStack(self.username, self.sellStack)

    def updateDbUserBuyTriggers(self):
        dbm = dbManager.DBM()
        return dbm.updateUserBuyTriggers(self.username, self.buyTriggers)

    def updateDbUserSellTriggers(self):
        dbm = dbManager.DBM()
        return dbm.updateUserSellTriggers(self.username, self.sellTriggers)

    