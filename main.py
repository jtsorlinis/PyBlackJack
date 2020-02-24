import time
import sys
from table import Table

def main():

    players = 5
    decks = 8
    bet_size = 10
    min_cards = 40

    rounds = 1000000
    verbose = 0

    if len(sys.argv) == 2:
        rounds = int(sys.argv[1])

    if verbose and rounds > 100:
        sys.stdout = open("output.txt", "w")

    table1 = Table(players, decks, bet_size, min_cards, verbose)
    table1.cardpile.shuffle()

    start_time = time.perf_counter()
    for _x in range(0, rounds):
        if verbose:
            print("Round " + str(_x + 1))
        if not verbose and rounds > 1000 and _x % (rounds / 100) == 0:
            print("\tProgress: " + str(int(_x * 100 / rounds)), end="%\r")
        table1.start_round()
        table1.check_earnings()

    for player in table1.players:
        if not player.split_from:
            print(
                "Player "
                + str(player.player_num)
                + " earnings: "
                + str(player.earnings)
                + "\t\tWin percentage: "
                + str(50 + (player.earnings / (rounds * bet_size) * 50))
            )
    print("Casino earnings: " + str(table1.casino_earnings))

    print(
        "Played "
        + str(_x + 1)
        + " rounds in "
        + format(time.perf_counter() - start_time, ".2f")
        + " seconds"
    )

if __name__ == "__main__":
    main()
