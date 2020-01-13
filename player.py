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
        x = 0
        output = "Player " + str(self.playerNum) + ": "
        for card in self.hand:
            output += card.print() + " "
            x+=1
        for space in range(x,5):
            output += "  "
        output += "\tScore: " + str(self.value)
        if self.value > 21:
            output += " (Bust)"
        else:
            output += "       "
        output += "\tBet: " + str(self.initialBet*self.betMult)
        return output

    def evaluate(self):
        self.aces = 0
        self.value = 0
        for card in self.hand:
            self.value += card.evaluate()
            # Check for an ace
            if card.rank == 'A':
                self.aces += 1
                self.isSoft = True

        while(self.value > 21 and self.aces > 0):
                self.value -= 10
                self.aces -= 1
        
        if self.aces == 0:
            self.isSoft = False

        return self.value