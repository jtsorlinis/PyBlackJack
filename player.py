class Player:
    playerNumCount = 0

    def __init__(self,strategy):
        self.strategy = strategy
        self.hand = []
        self.value = 0
        self.earnings = 0
        self.hasAce = False
        self.isSoft = False
        Player.playerNumCount += 1
        self.playerNum = Player.playerNumCount

    def resetHand(self):
        self.hand = []
        self.value = 0
        self.hasAce = False
        self.isSoft = False

    def win(self, table):
        self.earnings += table.betsize

    def lose(self, table):
        self.earnings -= table.betsize

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
        self.value = 0
        for card in self.hand:
            self.value += card.evaluate()
            # Check for an ace
            if card.rank == 'A':
                self.hasAce = True
                self.isSoft = True
        if self.value > 21:
            if self.hasAce:
                self.value -= 10
                self.isSoft = False
        return self.value