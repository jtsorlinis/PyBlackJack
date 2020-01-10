from dealer import Dealer
from player import Player
from cardpile import CardPile
import utils

class Table:
    def __init__(self, numplayers, numofdecks, betsize, verbose=False):
        self.verbose = verbose
        self.betsize = betsize
        self.players = []
        self.numofdecks = numofdecks
        self.cardpile = CardPile(numofdecks)
        for _ in range (0, numplayers):
            self.players.append(Player())
        self.dealer = Dealer()
        self.currentPlayer = None
        self.stratHard = utils.readArray('strategyHard.txt')
        self.stratSoft = utils.readArray('strategySoft.txt')
        self.stratSplits = utils.readArray('strategySplits.txt')

    def dealRound(self):
        for player in self.players:
            self.currentPlayer = player
            self.deal()
    
    def postDeal(self):
        self.currentPlayer = self.players[0]
        for player in self.players:
                player.evaluate()

    def dealDealer(self):
        self.currentPlayer = self.dealer
        self.deal()

    def startRound(self):
        self.clear()
        if(self.verbose):
            print(str(len(self.cardpile.cards)) + " cards left")
        self.getNewCards(60)
        self.dealRound()
        self.dealDealer()
        self.dealRound()
        self.dealDealer()
        self.postDeal()
        if(self.checkDealerNatural() == False):
            if(self.verbose):
                self.print()

    def getNewCards(self, mincards):
        if(len(self.cardpile.cards) < 60):
            self.cardpile = CardPile(self.numofdecks)
            self.cardpile.shuffle()
            if(self.verbose):
                print("Got " + str(self.numofdecks) + " new decks as number of cards is below " + str(mincards))

    def clear(self):
        for player in self.players:
            if (player.splitFrom):
                self.players.remove(player)
            else:
                player.resetHand()
        self.dealer.resetHand()

    def deal(self):
        card = self.cardpile.cards.pop()
        self.currentPlayer.hand.append(card)

    def play(self):
        if (self.currentPlayer.value < 21):
            if len(self.currentPlayer.hand) < 5:
                inp = input("Player" + str(self.currentPlayer.playerNum) + "\n1. Hit\n2. Stay\nChoose an option:")
                if inp == "1":
                    print("")
                    self.deal()
                    self.currentPlayer.evaluate()
                    self.print()
                    self.play()
                if inp == "2":
                    self.print()
                    self.nextPlayer()
        else:
            self.nextPlayer()

    def hit(self):
        if(self.verbose):
            print("Player " + str(self.currentPlayer.playerNum) + " hits")
        self.deal()
        self.currentPlayer.evaluate()
        self.autoPlay()

    def stand(self):
        self.nextPlayer()

    def split(self):
        splitPlayer = Player(self.currentPlayer)
        self.players.insert(self.players.index(self.currentPlayer)+1, splitPlayer)
        self.currentPlayer.hand.pop()
        self.currentPlayer.isSplit = True
        self.currentPlayer.evaluate()
        splitPlayer.evaluate()
        if(self.verbose):
            print("Player " + str(self.currentPlayer.playerNum) + " splits")
            self.print()
        self.hit()
    
    def double(self):
        if (self.currentPlayer.betMult == 1):
            self.currentPlayer.double()
            if(self.verbose):
                print("Player " + str(self.currentPlayer.playerNum) + " doubles")
        self.hit()

    def autoPlay(self):
        if(len(self.currentPlayer.hand) < 5):
            row = self.currentPlayer.value
            column = str(self.dealer.upCard())
            if(self.currentPlayer.canSplit() and self.currentPlayer.canSplit() not in [5, 10, "J", "Q", "K"]):
                for x in self.stratSplits:
                    if(x[0] == str(self.currentPlayer.canSplit())):
                        self.do(x[self.stratSplits[0].index(column)])
                        break
            elif(self.currentPlayer.isSoft):
                if (row > 19):
                    row = 19
                if (row < 13):
                    row = 13
                for x in self.stratSoft:
                    if(x[0] == str(row)):
                        self.do(x[self.stratSoft[0].index(column)])
            else:
                if (row > 17):
                    row = 17
                if (row < 8):
                    row = 8
                for x in self.stratHard:
                    if(x[0] == str(row)):
                        self.do(x[self.stratHard[0].index(column)])
        else:
            self.stand()
    
    def do(self, action):
        if action == 'H':
            self.hit()
        elif action == 'S':
            self.stand()
        elif action == 'D':
            self.double()
        elif action == 'P':
            self.split()
        else:
            exit()

    def dealerPlay(self):
        allBusted = True
        for player in self.players:
            if player.value < 22:
                allBusted = False
        self.dealer.hideSecond = False
        self.dealer.evaluate()
        if(self.verbose):
            self.print()
        if(allBusted):
            if(self.verbose):
                print("Dealer automatically wins cause all players busted")
            self.finishRound()
        else:
            while(self.dealer.value < 17 and len(self.dealer.hand) < 5):
                if(self.verbose):
                    print("Dealer hits")
                self.deal()
                self.dealer.evaluate()
                if(self.verbose):
                    self.print()
            self.finishRound()

    def nextPlayer(self):
        if (self.currentPlayer != self.dealer and self.players.index(self.currentPlayer) < len(self.players)-1):
            self.currentPlayer = self.players[self.players.index(self.currentPlayer)+1]
            self.autoPlay() 
        else:
            self.currentPlayer = self.dealer
            self.dealerPlay()

    def checkDealerNatural(self):
        if (self.dealer.evaluate() == 21):
            self.dealer.hideSecond = False
            if(self.verbose):
                self.print()
                print("Dealer has a natural 21\n")
            self.finishRound()
            return True
        else:
            return False

    def finishRound(self):
        if(self.verbose):
            print("Scoring round")
        for player in self.players:
            if player.value > 21:
                player.lose(self)
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Busts")
            elif self.dealer.value > 21:
                player.win(self)
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Wins")
            elif player.value > self.dealer.value:
                player.win(self)
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Wins")
            elif player.value == self.dealer.value:
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Draws")
            else:
                player.lose(self)
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Loses")
        for player in self.players:
            if(not player.splitFrom):
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Earnings: " + str(player.earnings))
        if(self.verbose):
            print("\n")

    def print(self):
        for player in self.players:
            print(player.print())
        print(self.dealer.print())
        print("")