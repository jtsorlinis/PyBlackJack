from player import Player


class Dealer(Player):
    def __init__(self):
        Player.__init__(self)
        self.hand = []
        self.player_num = "D"
        self.value = 0

    def reset_hand(self):
        self.hand = []
        self.value = 0

    def up_card(self):
        return self.hand[0].value
