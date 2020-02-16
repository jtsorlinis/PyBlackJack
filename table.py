import sys
from dealer import Dealer
from player import Player
from cardpile import CardPile
import strategies


class Table:
    def __init__(self, numplayers, numofdecks, betsize, mincards, verbose=False):
        self.verbose = verbose
        self.betsize = betsize
        self.players = []
        self.numofdecks = numofdecks
        self.cardpile = CardPile(numofdecks)
        self.mincards = mincards
        for _ in range(0, numplayers):
            self.players.append(Player(self))
        self.dealer = Dealer()
        self.current_player = 0
        self.casino_earnings = 0
        self.running_count = 0
        self.true_count = 0
        self.strat_hard = strategies.array_to_dict(strategies.STRAT_HARD)
        self.strat_soft = strategies.array_to_dict(strategies.STRAT_SOFT)
        self.strat_split = strategies.array_to_dict(strategies.STRAT_SPLIT)

    def deal_round(self):
        for player in self.players:
            self.deal()
            player.evaluate()
            self.current_player += 1
        self.current_player = 0

    def pre_deal(self):
        for player in self.players:
            self.select_bet(player)

    # check count and bet accordingly
    def select_bet(self, player):
        if int(self.true_count) >= 2:
            player.initial_bet = self.betsize * (int(self.true_count - 1) * 1.25)

    def deal_dealer(self, face_down=False):
        card = self.cardpile.cards.pop()
        card.face_down = face_down
        self.dealer.hand.append(card)
        if not face_down:
            self.running_count += card.count

    def start_round(self):
        self.clear()
        self.update_count()
        if self.verbose:
            print(str(len(self.cardpile.cards)) + " cards left")
            print(
                "Running count is: "
                + str(self.running_count)
                + "\tTrue count is: "
                + str(int(self.true_count))
            )
        self.get_new_cards()
        self.pre_deal()
        self.deal_round()
        self.deal_dealer()
        self.deal_round()
        self.deal_dealer(True)
        self.current_player = 0
        if self.check_dealer_natural():
            self.finish_round()
        else:
            self.check_player_natural()
            if self.verbose:
                self.print()
            self.auto_play()

    def get_new_cards(self):
        if len(self.cardpile.cards) < self.mincards:
            self.cardpile.refresh()
            self.cardpile.shuffle()
            self.true_count = 0
            self.running_count = 0
            if self.verbose:
                print(
                    "Got "
                    + str(self.numofdecks)
                    + " new decks as number of cards is below "
                    + str(self.mincards)
                )

    def clear(self):
        for player in self.players[:]:
            player.reset_hand()
            if player.split_from:
                self.players.remove(player)
        self.dealer.reset_hand()
        self.current_player = 0

    def deal(self):
        card = self.cardpile.cards.pop()
        self.players[self.current_player].hand.append(card)
        self.running_count += card.count

    def update_count(self):
        self.true_count = self.running_count / (len(self.cardpile.cards) / 52)
        # print(self.running_count)

    def hit(self):
        if self.verbose == 1:
            print(
                "Player " + str(self.players[self.current_player].player_num) + " hits"
            )
        self.deal()
        self.players[self.current_player].evaluate()

    def stand(self):
        if self.verbose:
            if self.players[self.current_player].value <= 21:
                print(
                    "Player "
                    + str(self.players[self.current_player].player_num)
                    + " stands"
                )
        self.players[self.current_player].is_done = True

    def split(self):
        split_player = Player(self, self.players[self.current_player])
        self.players[self.current_player].hand.pop()
        self.players.insert(self.current_player + 1, split_player)
        self.players[self.current_player].evaluate()
        self.players[self.current_player + 1].evaluate()
        if self.verbose == 1:
            print(
                "Player " + str(self.players[self.current_player].player_num) + " splits"
            )

    def split_aces(self):
        if self.verbose == 1:
            print(
                "Player "
                + str(self.players[self.current_player].player_num)
                + " splits aces"
            )
        split_player = Player(self, self.players[self.current_player])
        self.players[self.current_player].hand.pop()
        self.players.insert(self.current_player + 1, split_player)
        self.deal()
        self.players[self.current_player].evaluate()
        self.stand()
        self.current_player += 1
        self.deal()
        self.players[self.current_player].evaluate()
        self.stand()
        if self.verbose == 1:
            self.print()

    def double(self):
        if (
                self.players[self.current_player].bet_mult == 1
                and len(self.players[self.current_player].hand) == 2
        ):
            self.players[self.current_player].double()
            if self.verbose == 1:
                print(
                    "Player "
                    + str(self.players[self.current_player].player_num)
                    + " doubles"
                )
            self.hit()
            self.stand()
        else:
            self.hit()

    def auto_play(self):
        # # temp strategy
        # while(len(self.players[self.current_player].hand)
        # < 5 and self.players[self.current_player].value < 17):
        #     self.hit()

        # Actual strategy
        currplayer = self.players[self.current_player]
        dealerupcard = self.dealer.up_card()

        while not currplayer.is_done:
            if len(currplayer.hand) == 1:
                if self.verbose == 1:
                    print(
                        "Player "
                        + str(currplayer.player_num)
                        + " gets 2nd card after splitting"
                    )
                self.deal()
                currplayer.evaluate()

            if len(currplayer.hand) < 5 and currplayer.value < 21:
                split_player_val = currplayer.can_split()
                if split_player_val == 11:
                    self.split_aces()
                elif split_player_val != 0 and split_player_val not in (5, 10):
                    self.do_(
                        strategies.get_action(
                            split_player_val, dealerupcard, self.strat_split
                        )
                    )
                elif currplayer.is_soft:
                    self.do_(
                        strategies.get_action(
                            currplayer.value, dealerupcard, self.strat_soft
                        )
                    )
                else:
                    self.do_(
                        strategies.get_action(
                            currplayer.value, dealerupcard, self.strat_hard
                        )
                    )
            else:
                self.stand()
        self.next_player()

    def do_(self, action):
        if action == "H":
            self.hit()
        elif action == "S":
            self.stand()
        elif action == "D":
            self.double()
        elif action == "P":
            self.split()
        else:
            print("errored")
            print(action)
            sys.exit()
        if self.verbose:
            self.print()

    def dealer_play(self):
        all_busted = True
        for player in self.players:
            if player.value < 22:
                all_busted = False
                break
        self.dealer.hand[1].face_down = False
        self.running_count += self.dealer.hand[1].count
        self.dealer.evaluate()
        if self.verbose:
            print("Dealer's turn")
            self.print()
        if all_busted:
            if self.verbose:
                print("Dealer automatically wins cause all players busted")
            self.finish_round()
        else:
            while self.dealer.value < 17 and len(self.dealer.hand) < 5:
                if self.verbose:
                    print("Dealer hits")
                self.deal_dealer()
                self.dealer.evaluate()
                if self.verbose:
                    self.print()
            self.finish_round()

    def next_player(self):
        if self.current_player < len(self.players) - 1:
            self.current_player += 1
            self.auto_play()
        else:
            self.dealer_play()

    def check_player_natural(self):
        for player in self.players:
            if player.value == 21 and len(player.hand) == 2 and not player.split_from:
                player.has_natural = 1

    def check_dealer_natural(self):
        if self.dealer.evaluate() == 21:
            self.dealer.hand[1].face_down = False
            self.running_count += self.dealer.hand[1].count
            if self.verbose:
                self.print()
                print("Dealer has a natural 21\n")
            return True
        return False

    def check_earnings(self):
        check = 0
        for player in self.players:
            check += player.earnings
        if check * -1 != self.casino_earnings:
            print("NO MATCH")
            sys.exit()

    def finish_round(self):
        if self.verbose:
            print("Scoring round")
        for player in self.players:
            if player.has_natural:
                player.win(1.5)
                if self.verbose:
                    print(
                        "Player "
                        + str(player.player_num)
                        + " wins "
                        + str(1.5 * player.bet_mult * player.initial_bet)
                        + " with a natural 21"
                    )
            elif player.value > 21:
                player.lose()
                if self.verbose:
                    print(
                        "Player "
                        + str(player.player_num)
                        + " Busts and loses "
                        + str(player.bet_mult * player.initial_bet)
                    )
            elif self.dealer.value > 21 or player.value > self.dealer.value:
                player.win()
                if self.verbose:
                    print(
                        "Player "
                        + str(player.player_num)
                        + " Wins "
                        + str(player.bet_mult * player.initial_bet)
                    )
            elif player.value == self.dealer.value:
                if self.verbose:
                    print("Player " + str(player.player_num) + " Draws")
            else:
                player.lose()
                if self.verbose:
                    print(
                        "Player "
                        + str(player.player_num)
                        + " Loses "
                        + str(player.bet_mult * player.initial_bet)
                    )
        if self.verbose:
            for player in self.players:
                if not player.split_from:
                    print(
                        "Player "
                        + str(player.player_num)
                        + " Earnings: "
                        + str(player.earnings)
                    )
            print("\n")

    def print(self):
        for player in self.players:
            print(player.print())
        print(self.dealer.print())
        print("")
