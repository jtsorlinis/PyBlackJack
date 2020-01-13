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
        self.casinoEarnings = 0
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
        if(self.checkDealerNatural()):
            self.finishRound()
        else:
            self.checkPlayerNatural()
            if(self.verbose):
                self.print()
            self.autoPlay()
            

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

    def hit(self):
        if(self.verbose == 1):
            print("Player " + str(self.currentPlayer.playerNum) + " hits")
        self.deal()
        self.currentPlayer.evaluate()

    def stand(self):
        if (self.verbose):
            if (self.currentPlayer.value <= 21):
                print("Player " + str(self.currentPlayer.playerNum) + " stands")
        self.currentPlayer.isDone = True

    def split(self):
        splitPlayer = Player(self.currentPlayer)
        self.players.insert(self.players.index(self.currentPlayer)+1, splitPlayer)
        self.currentPlayer.hand.pop()
        self.currentPlayer.evaluate()
        splitPlayer.evaluate()
        if(self.verbose == 1):
            print("Player " + str(self.currentPlayer.playerNum) + " splits")
            self.print()
        
    
    def double(self):
        if (self.currentPlayer.betMult == 1 and len(self.currentPlayer.hand) == 2):
            self.currentPlayer.double()
            if(self.verbose == 1):
                print("Player " + str(self.currentPlayer.playerNum) + " doubles")
            self.hit()
            self.stand()
        else:
            self.hit()

    def playHard(self):
        tempval = self.currentPlayer.value
        for x in self.stratHard:
            if(x[0] == str(tempval)):
                if(self.verbose == 2):
                    print("Strategy: Hard\tPlayer " + str(self.currentPlayer.playerNum) + " has: " + str(tempval) + "\tDealer has: " + str(self.dealer.upCard()) + "\tAction: " + str(x[self.stratHard[0].index(str(self.dealer.upCard()))]))
                return x[self.stratHard[0].index(str(self.dealer.upCard()))]

    def playSoft(self):
        tempval = self.currentPlayer.value
        for x in self.stratSoft:
            if(x[0] == str(tempval)):
                if(self.verbose == 2):
                    print("Strategy: Soft\tPlayer " + str(self.currentPlayer.playerNum) + " has: " + str(tempval) + "\tDealer has: " + str(self.dealer.upCard()) + "\tAction: " + str(x[self.stratSoft[0].index(str(self.dealer.upCard()))]))
                return x[self.stratSoft[0].index(str(self.dealer.upCard()))]

    def playSplit(self):
        for x in self.stratSplits:
            if(x[0] == str(self.currentPlayer.canSplit())):
                if(self.verbose == 2):
                    print("Strategy: Split\tPlayer " + str(self.currentPlayer.playerNum) + " has pair of: " + str(self.currentPlayer.canSplit()) + "\tDealer has: " + str(self.dealer.upCard()) + "\tAction: " + str(x[self.stratSplits[0].index(str(self.dealer.upCard()))]))
                return x[self.stratSplits[0].index(str(self.dealer.upCard()))]

    def autoPlay(self):
        # temp strategy
        # while(len(self.currentPlayer.hand) < 5 and self.currentPlayer.value < 17):
        #     self.hit()

        # Actual strategy
        while(not self.currentPlayer.isDone):
            if(len(self.currentPlayer.hand) == 1):
                if(self.verbose == 1):
                    print("Player " + str(self.currentPlayer.playerNum) + " gets 2nd card after splitting")
                self.deal()
                self.currentPlayer.evaluate()

            if(len(self.currentPlayer.hand) < 5 and self.currentPlayer.value < 21):
                if(self.currentPlayer.canSplit() and self.currentPlayer.canSplit() not in [5, 10, "J", "Q", "K"]):
                    self.do(self.playSplit())
                elif(self.currentPlayer.isSoft):
                    self.do(self.playSoft())
                else:
                    self.do(self.playHard())
            else:
                self.stand()
        self.nextPlayer()
    
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
            print("errored")
            print(action)
            exit()
        if(self.verbose):
            self.print()

    def dealerPlay(self):
        allBusted = True
        for player in self.players:
            if player.value < 22:
                allBusted = False
        self.dealer.hideSecond = False
        self.dealer.evaluate()
        if(self.verbose):
            print("Dealer's turn")
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

    def checkPlayerNatural(self):
        for player in self.players:
            if(player.value == 21):
                player.hasNatural = 1

    def checkDealerNatural(self):
        if (self.dealer.evaluate() == 21):
            self.dealer.hideSecond = False
            if(self.verbose):
                self.print()
                print("Dealer has a natural 21\n")
            return True
        else:
            return False

    def finishRound(self):
        if(self.verbose):
            print("Scoring round")
        for player in self.players:
            if player.hasNatural:
                player.win(self, 1.5)
                if(self.verbose):  
                    print("Player " + str(player.playerNum) + " wins x" + str(1.5*player.betMult) + " with a natural 21")
            elif player.value > 21:
                player.lose(self)
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Busts x" + str(player.betMult))
            elif self.dealer.value > 21:
                player.win(self)
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Wins x" + str(player.betMult))
            elif player.value > self.dealer.value:
                player.win(self)
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Wins x" + str(player.betMult))
            elif player.value == self.dealer.value:
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Draws")
            else:
                player.lose(self)
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Loses x" + str(player.betMult))
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