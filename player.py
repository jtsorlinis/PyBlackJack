class Player:
    playerNumCount = 0
    maxSplits = 10

    def __init__(self,table,split=None):
        self.hand = []
        self.value = 0
        self.earnings = 0
        self.aces = 0
        self.isSoft = False
        self.splitCount = 0
        self.isDone = False
        self.splitFrom = split
        self.betMult = 1
        self.hasNatural = 0
        self.table = table
        self.initialBet = self.table.betsize

        if(split):
            self.hand = [split.hand[1]]
            self.splitCount = split.splitCount + 1
            self.playerNum = str(split.playerNum) + "S"
            self.initialBet = split.initialBet
        else:
            Player.playerNumCount += 1
            self.playerNum = Player.playerNumCount

    def double(self):
        self.betMult = 2

    def resetHand(self):
        self.hand = []
        self.value = 0
        self.aces = 0
        self.isSoft = False
        self.splitCount = 0
        self.isDone = False
        self.betMult = 1
        self.hasNatural = 0
        self.initialBet = self.table.betsize

    def canSplit(self):
        if(len(self.hand) == 2 and (self.hand[0].rank == self.hand[1].rank) and self.splitCount < Player.maxSplits):
            return self.hand[0].rank
        else:
            return False

    def win(self, mult=1):
        if(self.splitFrom):
            self.splitFrom.win(mult)
        else:
            self.earnings += (self.initialBet * self.betMult * mult)
            self.table.casinoEarnings -= (self.initialBet * self.betMult * mult)

    def lose(self):
        if(self.splitFrom):
            self.splitFrom.lose()
        else:
            self.earnings -= (self.initialBet * self.betMult)
            self.table.casinoEarnings += (self.initialBet * self.betMult)

    def print(self):
        output = "Player " + str(self.playerNum) + ": "
        for card in self.hand:
            output += card.print() + " "
        for _ in range(len(self.hand),5):
            output += "  "
        output += "\tScore: " + str(self.value)
        if self.value > 21:
            output += " (Bust)"
        else:
            output += "       "
        if(self.playerNum != "D"):
            output += "\tBet: " + str(self.initialBet*self.betMult)
        return output

    def evaluate(self):
        aces = 0
        value = 0
        for card in self.hand:
            value += card.value
            # Check for an ace
            if card.isAce:
                aces += 1
                isSoft = True

        while(value > 21 and aces > 0):
                value -= 10
                aces -= 1
        
        if aces == 0:
            isSoft = False

        self.value = value
        self.aces = aces
        self.isSoft = isSoft

        return self.value