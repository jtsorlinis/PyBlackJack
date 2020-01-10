from dealer import Dealer
from player import Player
from cardpile import CardPile

class Table:
    def __init__(self, numplayers, numofdecks, betsize):
        self.betsize = betsize
        self.players = []
        self.numofdecks = numofdecks
        self.cardpile = CardPile(numofdecks)
        for _ in range (0, numplayers):
            self.players.append(Player())
        self.dealer = Dealer()
        self.currentPlayer = None

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
        print(str(len(self.cardpile.cards)) + " cards left")
        self.getNewCards(60)
        self.dealRound()
        self.dealDealer()
        self.dealRound()
        self.dealDealer()
        self.postDeal()
        if(self.checkDealerNatural() == False):
            self.print()

    def getNewCards(self, mincards):
        if(len(self.cardpile.cards) < 60):
            self.cardpile = CardPile(self.numofdecks)
            self.cardpile.shuffle()
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
        print("Player " + str(self.currentPlayer.playerNum) + " splits")
        self.print()
        self.hit()

    def autoPlay(self):
        if(self.currentPlayer.canSplit() in [2,3,4,6,7]):
            if(self.dealer.upCard() in range(2,7)):
                self.split()
            else:
                self.hit()
        elif(self.currentPlayer.canSplit() in [8, 9, "A"]):
            self.split()
        elif(len(self.currentPlayer.hand) < 5):
            if(self.currentPlayer.isSoft):
                if(self.currentPlayer.value <= 17):
                    self.hit()
                elif(self.currentPlayer.value == 18 and self.dealer.upCard() not in range(2,8)):
                    self.hit()
                else:
                    self.stand()
                
            else:
                if(self.currentPlayer.value <= 11):
                    self.hit()
                elif(self.currentPlayer.value == 12 and self.dealer.upCard() not in [4,5,6]):
                    self.hit()
                elif(13 <= self.currentPlayer.value <= 16 and self.dealer.upCard() not in [2,3,4,5,6]):
                    self.hit()
                else:
                    self.stand()
        else:
            self.stand()
        
    def dealerPlay(self):
        allBusted = True
        for player in self.players:
            if player.value < 22:
                allBusted = False
        self.dealer.hideSecond = False
        self.dealer.evaluate()
        self.print()
        if(allBusted):
            print("Dealer automatically wins cause all players busted")
            self.finishRound()
        else:
            while(self.dealer.value < 17 and len(self.dealer.hand) < 5):
                print("Dealer hits")
                self.deal()
                self.dealer.evaluate()
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
            self.print()
            print("Dealer has a natural 21\n")
            self.finishRound()
            return True
        else:
            return False

    def finishRound(self):
        print("Scoring round")
        for player in self.players:
            if player.value > 21:
                player.lose(self)
                print("Player " + str(player.playerNum) + " Busts")
            elif self.dealer.value > 21:
                player.win(self)
                print("Player " + str(player.playerNum) + " Wins")
            elif player.value > self.dealer.value:
                player.win(self)
                print("Player " + str(player.playerNum) + " Wins")
            elif player.value == self.dealer.value:
                print("Player " + str(player.playerNum) + " Draws")
            else:
                player.lose(self)
                print("Player " + str(player.playerNum) + " Loses")
        for player in self.players:
            if(not player.splitFrom):
                print("Player " + str(player.playerNum) + " Earnings: " + str(player.earnings))
        print("\n")

    def print(self):
        for player in self.players:
            print(player.print())
        print(self.dealer.print())
        print("")