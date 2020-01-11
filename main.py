from card import Card
from deck import Deck
from player import Player
from table import Table
from cardpile import CardPile
import time

rounds = 100000
verbose = 0

table1 = Table(5,8,10,verbose)
table1.cardpile.shuffle()

x=0
start = time.perf_counter()
while(x<rounds):
    if(verbose):
        print("Round " + str(x))
    table1.startRound()
    table1.autoPlay()
    x+=1

for player in table1.players:
    if(not player.splitFrom):
        print("Player " + str(player.playerNum) + " earnings: " + str(player.earnings) + "\t\tWin percentage: " + str(50+(player.earnings/rounds*5)))

print("Casino earnings: " + str(table1.casinoEarnings))

end = time.perf_counter()
duration = end - start
print ("Played " + str(x) + " rounds in " + format(duration, ".2f") + " seconds")