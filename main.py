import time
import sys
from table import Table

PLAYERS = 5
DECKS = 8
BET_SIZE = 10
MIN_CARDS = 40

ROUNDS = 1000000
VERBOSE = 0

if len(sys.argv) == 2:
    ROUNDS = int(sys.argv[1])

if VERBOSE and ROUNDS > 100:
    sys.stdout = open("output.txt", "w")

T = Table(PLAYERS, DECKS, BET_SIZE, MIN_CARDS, VERBOSE)
T.cardpile.shuffle()

START_TIME = time.perf_counter()
for x in range(0, ROUNDS):
    if VERBOSE:
        print("Round " + str(x + 1))
    if not VERBOSE and ROUNDS > 1000 and x % (ROUNDS / 100) == 0:
        print("\tProgress: " + str(int(x * 100 / ROUNDS)), end="%\r")
    T.start_round()
    T.check_earnings()

for player in T.players:
    if not player.split_from:
        print(
            "Player "
            + str(player.player_num)
            + " earnings: "
            + str(player.earnings)
            + "\t\tWin percentage: "
            + str(50 + (player.earnings / (ROUNDS * BET_SIZE) * 50))
        )
print("Casino earnings: " + str(T.casino_earnings))

print(
    "Played "
    + str(x + 1)
    + " rounds in "
    + format(time.perf_counter() - START_TIME, ".2f")
    + " seconds"
)
