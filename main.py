from card import Card
from deck import Deck
from player import Player
from table import Table
from cardpile import CardPile

table1 = Table(5,8,10)
table1.cardpile.shuffle()

rounds = 100

x=0
while(x<rounds):
    print("Round " + str(x))
    table1.startRound()
    table1.autoPlay()
    x+=1

for player in table1.players:
    if(not player.splitFrom):
        print("Player " + str(player.playerNum) + " win percentage: " + str(50+(player.earnings/rounds*5)))