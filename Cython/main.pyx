from card import Card
from deck import Deck
from player import Player
from table import Table
from cardpile import CardPile
import time
import sys
import random

cdef int players,decks,betsize,mincards, rounds, verbose

players = 5
decks = 8
betsize = 10
mincards = 40

rounds = 1000000
verbose = 0

if(len(sys.argv) == 2):
    rounds = int(sys.argv[1])

if(verbose and rounds > 100):
    sys.stdout = open('output.txt', 'w')

table1 = Table(players,decks,betsize, mincards,verbose)
table1.cardpile.shuffle()

start = time.perf_counter()
for x in range(0,rounds):
    if(verbose):
        print("Round " + str(x+1))
    if(not verbose and rounds>1000 and x % (rounds/100) == 0):
        print("\tProgress: " + str(int(x/rounds*100)),end="%\r")
    table1.startRound()
    table1.checkEarnings()

for player in table1.players:
    if(not player.splitFrom):
        print("Player " + str(player.playerNum) + " earnings: " + str(player.earnings) + "\t\tWin percentage: " + str(50+(player.earnings/(rounds*betsize)*50)))
print("Casino earnings: " + str(table1.casinoEarnings))

end = time.perf_counter()
duration = end - start
print ("Played " + str(x+1) + " rounds in " + format(duration, ".2f") + " seconds")