from enum import Enum

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.faceDown = False

    def print(self):
        if (self.faceDown):
            return "X"
        else:
            return str(self.rank)
    
    def evaluate(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return self.rank
    
    def count(self):
        if self.rank in [10, "J", "Q", "K", "A"]:
            return -1
        elif self.rank in [7,8,9]:
            return 0
        elif self.rank in [2,3,4,5,6]:
            return 1
        else:
            print("erored with " + str(self.rank))
            exit()
        