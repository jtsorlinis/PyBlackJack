from player import Player

class Dealer(Player):
    def __init__(self):
        self.hand = []
        self.playerNum = "D"
        self.hideSecond = True
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
        if self.hideSecond and len(self.hand) == 2:
            output += self.hand[0].print()
            output += ' X'
        else:
            for card in self.hand:
                output += card.print() + " "
            output += "\tScore: "
            if self.value < 22:
                output += str(self.value)
            else:
                output += "Bust (" + str(self.value) + ")"
        return output