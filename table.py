from dealer import Dealer
from player import Player
from cardpile import CardPile
import utils

class Table:
    def __init__(self, numplayers, numofdecks, betsize, mincards, verbose=False):
        self.verbose = verbose
        self.betsize = betsize
        self.players = []
        self.numofdecks = numofdecks
        self.cardpile = CardPile(numofdecks)
        self.mincards = mincards
        for _ in range (0, numplayers):
            self.players.append(Player(self))
        self.dealer = Dealer()
        self.currentPlayer = None
        self.casinoEarnings = 0
        self.runningCount = 0
        self.trueCount = 0
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
            self.selectBet(player)
                   
    # check count and bet accordingly
    def selectBet(self, player):
        if(int(self.trueCount) >= 2):
                player.initialBet = self.betsize * (int(self.trueCount-1))

    def dealDealer(self,faceDown=False):
        self.currentPlayer = self.dealer
        self.deal(faceDown)

    def startRound(self):
        self.clear()
        if(self.verbose):
            print(str(len(self.cardpile.cards)) + " cards left")
        self.getNewCards()
        self.dealRound()
        self.dealDealer()
        self.dealRound()
        self.dealDealer(True)
        self.postDeal()
        if(self.verbose):
            print("Running count is: " + str(self.runningCount) +"\tTrue count is: " + str(int(self.trueCount)))
        if(self.checkDealerNatural()):
            self.finishRound()
        else:
            self.checkPlayerNatural()
            if(self.verbose):
                self.print()
            self.autoPlay()
            

    def getNewCards(self):
        if(len(self.cardpile.cards) < self.mincards):
            self.cardpile = CardPile(self.numofdecks)
            self.cardpile.shuffle()
            self.trueCount = 0
            self.runningCount = 0
            if(self.verbose):
                print("Got " + str(self.numofdecks) + " new decks as number of cards is below " + str(self.mincards))

    def clear(self):
        for player in self.players:
            if (player.splitFrom):
                self.players.remove(player)
        for player in self.players:
            player.resetHand()
        self.dealer.resetHand()

    def deal(self, faceDown=False):
        card = self.cardpile.cards.pop()
        self.currentPlayer.hand.append(card)
        card.faceDown = faceDown
        self.updateCount(card)
    
    def updateCount(self, card):
        self.runningCount += card.count()
        self.trueCount = self.runningCount/(len(self.cardpile.cards)/52)
        # print(self.runningCount)

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
        splitPlayer = Player(self,self.currentPlayer)
        self.players.insert(self.players.index(self.currentPlayer)+1, splitPlayer)
        self.currentPlayer.hand.pop()
        self.currentPlayer.evaluate()
        splitPlayer.evaluate()
        if(self.verbose == 1):
            print("Player " + str(self.currentPlayer.playerNum) + " splits")
    
    def splitAces(self):
        if(self.verbose == 1):
            print("Player " + str(self.currentPlayer.playerNum) + " splits aces")
        splitPlayer = Player(self,self.currentPlayer)
        self.players.insert(self.players.index(self.currentPlayer)+1, splitPlayer)
        self.currentPlayer.hand.pop()
        self.deal()
        self.currentPlayer.evaluate()
        self.stand()
        self.currentPlayer = splitPlayer
        self.deal()
        self.currentPlayer.evaluate()
        self.stand()
        if(self.verbose == 1):
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
        # # temp strategy
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
                if(self.currentPlayer.canSplit() == 'A'):
                    self.splitAces()
                elif(self.currentPlayer.canSplit() and self.currentPlayer.canSplit() not in [5, 10, "J", "Q", "K"]):
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
        self.dealer.hand[1].faceDown = False
        self.updateCount(self.dealer.hand[1])
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
            if(player.value == 21 and len(player.hand) == 2 and not player.splitFrom):
                player.hasNatural = 1

    def checkDealerNatural(self):
        if (self.dealer.evaluate() == 21):
            self.dealer.hand[1].faceDown = False
            self.updateCount(self.dealer.hand[1])
            if(self.verbose):
                self.print()
                print("Dealer has a natural 21\n")
            return True
        else:
            return False

    def checkEarnings(self):
        check = 0
        for player in self.players:
            check += player.earnings
        if (check*-1 != self.casinoEarnings):
            print("NO MATCH")
            exit()

    def finishRound(self):
        if(self.verbose):
            print("Scoring round")
        for player in self.players:
            if player.hasNatural:
                player.win(1.5)
                if(self.verbose):  
                    print("Player " + str(player.playerNum) + " wins " + str(1.5*player.betMult*player.initialBet) + " with a natural 21")
            elif player.value > 21:
                player.lose()
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Busts and loses " + str(player.betMult*player.initialBet))
            elif self.dealer.value > 21:
                player.win()
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Wins " + str(player.betMult*player.initialBet))
            elif player.value > self.dealer.value:
                player.win()
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Wins " + str(player.betMult*player.initialBet))
            elif player.value == self.dealer.value:
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Draws")
            else:
                player.lose()
                if(self.verbose):
                    print("Player " + str(player.playerNum) + " Loses " + str(player.betMult*player.initialBet))
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