from player import Player


class Dealer(Player):
    def __init__(self):
        Player.__init__(self)
        self.hand = []
        self.playerNum = "D"
        self.value = 0

    def resetHand(self):
        self.hand = []
        self.value = 0

    def upCard(self):
        return self.hand[0].evaluate()
