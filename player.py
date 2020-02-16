class Player:

    playerNumCount = 0
    maxSplits = 10

    def __init__(self, table=None, split=None):
        self.hand = []
        self.value = 0
        self.earnings = 0
        self.aces = 0
        self.is_soft = False
        self.split_count = 0
        self.is_done = False
        self.split_from = split
        self.bet_mult = 1
        self.has_natural = 0
        self.table = table

        if table:
            self.initial_bet = self.table.betsize

        if split:
            self.hand = [split.hand[1]]
            self.split_count = split.split_count + 1
            self.player_num = str(split.player_num) + "S"
            self.initial_bet = split.initial_bet
        else:
            Player.playerNumCount += 1
            self.player_num = Player.playerNumCount

    def double(self):
        self.bet_mult = 2

    def reset_hand(self):
        self.hand = []
        self.value = 0
        self.aces = 0
        self.is_soft = False
        self.split_count = 0
        self.is_done = False
        self.bet_mult = 1
        self.has_natural = 0
        self.initial_bet = self.table.betsize

    def can_split(self):
        if (
                len(self.hand) == 2
                and (self.hand[0].rank == self.hand[1].rank)
                and self.split_count < Player.maxSplits
        ):
            return self.hand[0].value
        return 0

    def win(self, mult=1):
        if self.split_from:
            self.split_from.win(mult)
        else:
            self.earnings += self.initial_bet * self.bet_mult * mult
            self.table.casino_earnings -= self.initial_bet * self.bet_mult * mult

    def lose(self):
        if self.split_from:
            self.split_from.lose()
        else:
            self.earnings -= self.initial_bet * self.bet_mult
            self.table.casino_earnings += self.initial_bet * self.bet_mult

    def print(self):
        output = "Player " + str(self.player_num) + ": "
        for card in self.hand:
            output += card.print() + " "
        for _ in range(len(self.hand), 5):
            output += "  "
        output += "\tScore: " + str(self.value)
        if self.value > 21:
            output += " (Bust)"
        else:
            output += "       "
        if self.player_num != "D":
            output += "\tBet: " + str(self.initial_bet * self.bet_mult)
        return output

    def evaluate(self):
        aces = 0
        value = 0
        for card in self.hand:
            value += card.value
            # Check for an ace
            if card.is_ace:
                aces += 1
                is_soft = True

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        if aces == 0:
            is_soft = False

        self.value = value
        self.aces = aces
        self.is_soft = is_soft

        return self.value
