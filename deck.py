from card import Card
import random

suits = ["Clubs", "Hearts", "Spades", "Diamonds"]
ranks = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]

class Deck:

    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank,suit))

    def print(self):
        string = ""
        for card in self.cards:
            string += str(card.print() + "\n")
        return string

    def getCards(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)