from enum import Enum

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.faceDown = False
        self.isAce = True if self.rank == "A" else False
        self.value = self.evaluate()
        self.count = self.countCard()
        

    def print(self):
        if (self.faceDown):
            return "X"
        else:
            return str(self.rank)
    
    def evaluate(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.isAce:
            return 11
        else:
            return self.rank
    
    def countCard(self):
        if self.rank in [10, "J", "Q", "K", "A"]:
            return -1
        elif self.rank in [7,8,9]:
            return 0
        else:
            return 1
        