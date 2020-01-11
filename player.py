class Player:
    playerNumCount = 0

    def __init__(self,split=None):
        self.hand = []
        self.value = 0
        self.earnings = 0
        self.aces = 0
        self.isSoft = False
        self.isSplit = False
        self.splitFrom = split
        self.betMult = 1
        self.hasNatural = 0

        if(split):
            self.hand = [split.hand[1]]
            self.playerNum = str(split.playerNum) + "S"
            self.isSplit = True
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
        self.isSplit = False
        self.betMult = 1
        self.hasNatural = 0

    def canSplit(self):
        if(len(self.hand) == 2 and (self.hand[0].rank == self.hand[1].rank) and self.isSplit == False):
            return self.hand[0].rank
        else:
            return False

    def win(self, table, mult=1):
        if(self.splitFrom):
            self.splitFrom.earnings += (table.betsize * self.betMult * mult)
        else:
            self.earnings += (table.betsize * self.betMult * mult)
        table.casinoEarnings -= (table.betsize * self.betMult * mult)

    def lose(self, table):
        if(self.splitFrom):
            self.splitFrom.earnings -= (table.betsize * self.betMult)
        else:
            self.earnings -= (table.betsize * self.betMult)
        table.casinoEarnings += (table.betsize * self.betMult)

    def print(self):
        output = "Player " + str(self.playerNum) + ": "
        for card in self.hand:
            output += card.print() + " "
        output += "\tScore: "
        if self.value < 22:
            output += str(self.value)
        else:
            output += "Bust (" + str(self.value) + ")"
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