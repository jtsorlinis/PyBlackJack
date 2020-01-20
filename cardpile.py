from deck import Deck
import random

class CardPile:
    def __init__(self,numofdecks):
        self.cards = []
        for _ in range(0,numofdecks):
            self.cards += Deck().cards

    def print(self):
        string = ""
        for card in self.cards:
            string += str(card.print() + "\n")
        return string

    def shuffle(self):
        random.shuffle(self.cards)