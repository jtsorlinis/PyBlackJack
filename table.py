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
        self.currentPlayer = 0
        self.casinoEarnings = 0
        self.runningCount = 0
        self.trueCount = 0
        self.stratHard = utils.fileToDict('strategyHard.txt')
        self.stratSoft = utils.fileToDict('strategySoft.txt')
        self.stratSplits = utils.fileToDict('strategySplits.txt')

    def dealRound(self):
        for player in self.players:
            self.deal()
            player.evaluate()
            self.currentPlayer+=1
        self.currentPlayer = 0

    def preDeal(self):
        for player in self.players:
            self.selectBet(player)
              
    # check count and bet accordingly
    def selectBet(self, player):
        if(int(self.trueCount) >= 2):
                player.initialBet = self.betsize * (int(self.trueCount-1) * 1.25)

    def dealDealer(self,faceDown=False):
        card = self.cardpile.cards.pop()
        card.faceDown = faceDown
        self.dealer.hand.append(card)
        if(not faceDown):
            self.runningCount += card.count

    def startRound(self):
        self.clear()
        self.updateCount()
        if(self.verbose):
            print(str(len(self.cardpile.cards)) + " cards left")
            print("Running count is: " + str(self.runningCount) +"\tTrue count is: " + str(int(self.trueCount)))
        self.getNewCards()
        self.preDeal()
        self.dealRound()
        self.dealDealer()
        self.dealRound()
        self.dealDealer(True)
        self.currentPlayer = 0
        if(self.checkDealerNatural()):
            self.finishRound()
        else:
            self.checkPlayerNatural()
            if(self.verbose):
                self.print()
            self.autoPlay()
            

    def getNewCards(self):
        if(len(self.cardpile.cards) < self.mincards):
            self.cardpile.refresh()
            self.cardpile.shuffle()
            self.trueCount = 0
            self.runningCount = 0
            if(self.verbose):
                print("Got " + str(self.numofdecks) + " new decks as number of cards is below " + str(self.mincards))

    def clear(self):
        for player in self.players[:]:
            player.resetHand()
            if (player.splitFrom):
                self.players.remove(player)     
        self.dealer.resetHand()
        self.currentPlayer = 0

    def deal(self):
        card = self.cardpile.cards.pop()
        self.players[self.currentPlayer].hand.append(card)
        self.runningCount += card.count
        
    def updateCount(self):
        self.trueCount = self.runningCount/(len(self.cardpile.cards)/52)
        # print(self.runningCount)

    def hit(self):
        if(self.verbose == 1):
            print("Player " + str(self.players[self.currentPlayer].playerNum) + " hits")
        self.deal()
        self.players[self.currentPlayer].evaluate()

    def stand(self):
        if (self.verbose):
            if (self.players[self.currentPlayer].value <= 21):
                print("Player " + str(self.players[self.currentPlayer].playerNum) + " stands")
        self.players[self.currentPlayer].isDone = True

    def split(self):
        splitPlayer = Player(self,self.players[self.currentPlayer])
        self.players[self.currentPlayer].hand.pop()
        self.players.insert(self.currentPlayer+1, splitPlayer)
        self.players[self.currentPlayer].evaluate()
        self.players[self.currentPlayer+1].evaluate()
        if(self.verbose == 1):
            print("Player " + str(self.players[self.currentPlayer].playerNum) + " splits")
    
    def splitAces(self):
        if(self.verbose == 1):
            print("Player " + str(self.players[self.currentPlayer].playerNum) + " splits aces")
        splitPlayer = Player(self,self.players[self.currentPlayer])
        self.players[self.currentPlayer].hand.pop()
        self.players.insert(self.currentPlayer+1, splitPlayer)
        self.deal()
        self.players[self.currentPlayer].evaluate()
        self.stand()
        self.currentPlayer+=1
        self.deal()
        self.players[self.currentPlayer].evaluate()
        self.stand()
        if(self.verbose == 1):
            self.print()
    
    def double(self):
        if (self.players[self.currentPlayer].betMult == 1 and len(self.players[self.currentPlayer].hand) == 2):
            self.players[self.currentPlayer].double()
            if(self.verbose == 1):
                print("Player " + str(self.players[self.currentPlayer].playerNum) + " doubles")
            self.hit()
            self.stand()
        else:
            self.hit()

    def autoPlay(self):
        # # temp strategy
        # while(len(self.players[self.currentPlayer].hand) < 5 and self.players[self.currentPlayer].value < 17):
        #     self.hit()

        # Actual strategy
        currplayer = self.players[self.currentPlayer]
        dealerupcard = self.dealer.upCard()
        
        while(not currplayer.isDone):
            
            if(len(currplayer.hand) == 1):
                if(self.verbose == 1):
                    print("Player " + str(currplayer.playerNum) + " gets 2nd card after splitting")
                self.deal()
                currplayer.evaluate()

            if(len(currplayer.hand) < 5 and currplayer.value < 21):
                splitPlayerVal = currplayer.canSplit()
                if(splitPlayerVal == 11):
                    self.splitAces()
                elif(splitPlayerVal != 0 and (splitPlayerVal != 5 and splitPlayerVal != 10)):
                    self.do(utils.getAction(splitPlayerVal,dealerupcard,self.stratSplits))
                elif(currplayer.isSoft):
                    self.do(utils.getAction(currplayer.value,dealerupcard,self.stratSoft))
                else:
                    self.do(utils.getAction(currplayer.value,dealerupcard,self.stratHard))
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
                break
        self.dealer.hand[1].faceDown = False
        self.runningCount += self.dealer.hand[1].count
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
                self.dealDealer()
                self.dealer.evaluate()
                if(self.verbose):
                    self.print()
            self.finishRound()

    def nextPlayer(self):
        if (self.currentPlayer < len(self.players)-1):
            self.currentPlayer += 1
            self.autoPlay() 
        else:
            self.dealerPlay()

    def checkPlayerNatural(self):
        for player in self.players:
            if(player.value == 21 and len(player.hand) == 2 and not player.splitFrom):
                player.hasNatural = 1

    def checkDealerNatural(self):
        if (self.dealer.evaluate() == 21):
            self.dealer.hand[1].faceDown = False
            self.runningCount += self.dealer.hand[1].count
            if(self.verbose):
                self.print()
                print("Dealer has a natural 21\n")
            return True
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
        if(self.verbose):
            for player in self.players:
                if(not player.splitFrom):
                    print("Player " + str(player.playerNum) + " Earnings: " + str(player.earnings))
            print("\n")

    def print(self):
        for player in self.players:
            print(player.print())
        print(self.dealer.print())
        print("")