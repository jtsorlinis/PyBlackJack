class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.face_down = False
        self.is_ace = self.rank == "A"
        self.value = self.evaluate()
        self.count = self.count_card()

    def print(self):
        if self.face_down:
            return "X"
        return str(self.rank)

    def evaluate(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        if self.is_ace:
            return 11
        return self.rank

    def count_card(self):
        if self.rank in [10, "J", "Q", "K", "A"]:
            return -1
        if self.rank in [7, 8, 9]:
            return 0
        return 1
