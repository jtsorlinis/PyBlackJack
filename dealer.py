from player import Player

class Dealer(Player):
    def __init__(self):
        self.hand = []
        self.playerNum = "D"
        self.value = 0
        self.hasAce = False
        self.isSoft = False

    def resetHand(self):
        self.hand = []
        self.value = 0
        self.hasAce = False
        self.hideSecond = True

    def upCard(self):
        return self.hand[0].evaluate()

    def print(self):
        output = "Player " + str(self.playerNum) + ": "
        for card in self.hand:
            output += card.print() + " "
        for _ in range(len(self.hand),5):
            output += "  "
        output += "\tScore: " + str(self.value)
        if self.value > 21:
            output += " (Bust)"
        return output