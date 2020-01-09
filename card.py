from enum import Enum

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def print(self):
        return str(self.rank)
    
    def evaluate(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return self.rank