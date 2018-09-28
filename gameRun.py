import random


class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def __str__(self):
        return '\nIn the deck:\n{}'.format(self.cards)

    def build(self):
        startingDeck = {'Attack':4,
                    'Skip': 4,
                    'Favor': 4,
                    'Shuffle': 4,
                    'See the future': 5,
                    'Collectable1':4,
                    'Collectable2':4,
                    'Collectable3': 4,
                    'Collectable4': 4,
                    'Collectable5': 4,
                    'Nope': 5,
                    'Defuse': 0,
                    'Exploding kitten': 0}

        for key, value in startingDeck.items():
            self.addCard(key, value)

    def shuffle(self):
        n = len(self.cards)-1
        for _ in range(1000):
            i = random.randint(0, n)
            j = random.randint(0, n)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        print("It's the popular game called Exploding Kitten, written in Python.\n")
        print('The deck has been shuffled')

    def addCard(self, cardtype, num = 1):
        for _ in range(num):
            n = max(len(self.cards) - 1, 1)
            k = random.randint(0, n)
            self.cards.insert(k, str(Card(cardtype)))

class Trash:
    def __init__(self):
        self.cards = []

class Card:
    def __init__(self, cardType):
        self.cardType = cardType

    def __repr__(self):
        return '{}'.format(self.cardType)

class Player:
    numOfPlayer = 0
    def __init__(self, name):
        self.name = name
        self.hand = ['Defuse']
        type(self).numOfPlayer += 1
        self.attacked = 0

    def __del__(self):
        type(self).numOfPlayer -= 1

    def __repr__(self):
        return "{}'s hand: {}".format(self.name, self.hand)

    def drawCard(self, deck: Deck, num = 1):
        for _ in range(num):
            self.hand.append(deck.cards[0])
            del deck.cards[0]

    def playCard(self,trash: Trash, cardname):
        if cardname in self.hand:
            self.hand.remove(cardname)
            trash.cards.append(cardname)
            print('{} played a {}!'.format(self.name, cardname))
        else:
            print('{} has no {} to play'.format(self.name, cardname))

    def takeBackCardToTheDeck(self, deck: Deck, cardname, deckIndex = 0):
        self.hand.remove(cardname)
        deck.cards.insert(deckIndex, cardname)

    def shuffleHand(self):
        n = len(self.hand) - 1
        for _ in range(1000):
            i = random.randint(0, n)
            j = random.randint(0, n)
            self.hand[i], self.hand[j] = self.hand[j], self.hand[i]

    def giveOneCardToAnotherPlayer(self, anotherPlayer, cardname):
        if cardname in self.hand:
            self.hand.remove(cardname)
            anotherPlayer.hand.append(cardname)
            print('{} given a {} to {}!'.format(self.name, cardname, anotherPlayer.name))
        else:
            print('{} has no {} to give'.format(self.name, cardname))

class Game:
    def __init__(self):
        self.numOfPlayers = 0
        self.playersNames = ''
        self.players = []
        self.turnCounter = 0

    def createPlayers(self):
        intro = input("Enter names (2-5 players) separated by comma (, ): ")
        # intro = 'évi, gergő, béla'
        self.playersNames = intro.split(', ')
        self.numOfPlayers = len(self.playersNames)
        assert self.numOfPlayers > 1 and self.numOfPlayers < 6, "Please add min. 2 players and max. 5. You added {} player".format(
            self.numOfPlayers)

        self.players = [Player(i) for i in self.playersNames]

        for key, value in enumerate(self.players):
            self.players[key].drawCard(self.deck, 4)

        self.deck.addCard('Exploding kitten', Player.numOfPlayer - 1)
        self.deck.addCard('Defuse', 1)

        for key, value in enumerate(self.players):
            self.players[key].shuffleHand()
            print(self.players[key])

    def gameStart(self):
        self.deck = Deck()
        self.trash = Trash()
        self.createPlayers()
        print(self.deck)

    def attack(self):
        self.turnCounter += 1
        if self.turnCounter > (len(self.players) - 1):
            self.turnCounter = 0
        print('Turn has been skipped!\n{} has been attacked.(2 turns)'.format(self.players[self.turnCounter].name))
        self.players[self.turnCounter].attacked = 1

    def skip(self):
        print('\nTurn has been skipped!')
        if self.players[self.turnCounter].attacked == 0:
            self.turnCounter += 1
        else:
            self.players[self.turnCounter].attacked = 0

    def favor(self):
        favorGiver = input('Name a player who give you a favor: ')
        cardToFavor = input('{}! do a favor for {}, please!\nName a card from your hand:{}: '.format(favorGiver, self.players[self.turnCounter].name, self.players[[x.name for x in self.players].index(favorGiver)].hand))
        self.players[[x.name for x in self.players].index(favorGiver)].giveOneCardToAnotherPlayer(self.players[self.turnCounter], cardToFavor)

    def turnCircle(self):
        while len(self.players) > 1:
            if self.turnCounter > (len(self.players) - 1):
                self.turnCounter = 0
            print("\nIt's {}'s turn!".format(self.players[self.turnCounter].name))
            print(self.players[self.turnCounter])
            while True:
                action = input("Play a card by name or end your turn with Enter: ")
                #action = ''
                if action == '':
                    self.players[self.turnCounter].drawCard(self.deck)
                    print("{} drawed a card.".format(self.players[self.turnCounter].name))
                    if self.players[self.turnCounter].hand[-1] == 'Exploding kitten' and 'Defuse' in self.players[self.turnCounter].hand:
                        print("Exploding kitten!\n{} Defused the bomb!".format(self.players[self.turnCounter].name))
                        self.players[self.turnCounter].playCard(self.trash, 'Defuse')
                        deckindex = int(input('Where do you want to take the card? (0 = top of the deck / {} = last card): '.format(len(self.deck.cards))) or '0')
                        #deckindex = 0
                        self.players[self.turnCounter].takeBackCardToTheDeck(self.deck, 'Exploding kitten', deckindex)
                    elif self.players[self.turnCounter].hand[-1] == 'Exploding kitten' and 'Defuse' not in self.players[self.turnCounter].hand:
                        print("Exploding kitten! - BOOM!\n{} exploded".format(self.players[self.turnCounter].name))
                        del self.players[self.turnCounter]
                        self.turnCounter += 1
                        break
                    print(self.players[self.turnCounter])
                    print('\nTurn has ended!')
                    if self.players[self.turnCounter].attacked == 0:
                        self.turnCounter += 1
                    else:
                        self.players[self.turnCounter].attacked = 0
                    break
                elif action in self.players[self.turnCounter].hand:
                    self.players[self.turnCounter].playCard(self.trash, action)
                    whoNope = input('Anybody to Nope this action? Type a name or hit Enter: ')
                    if whoNope in [self.players[_].name for _ in range(len(self.players))] and 'Nope' in self.players[[x.name for x in self.players].index(whoNope)].hand:
                        self.players[[_.name for _ in self.players].index(whoNope)].playCard(self.trash, 'Nope')
                        #Nope to Nope is not working
                    else:
                        print('Nobody played Nope.') if whoNope == '' else print('{} has no Nope to play'.format(whoNope))
                        if action == 'Attack':
                            self.attack()
                            break
                        elif action == 'Skip':
                            self.skip()
                            break
                        elif action == 'Favor':
                            self.favor()
                        elif action == 'Shuffle':
                            self.deck.shuffle()
                        elif action == 'See the future':
                            print('The next 3 card will be:\n{}\n{}\n{}'.format(self.deck.cards[0], self.deck.cards[1], self.deck.cards[2]))
                        elif action == 'Nope':
                            print('Nothing to {}, sorry!'.format(action)) #Nope to nope is not working
                        elif action == 'Defuse':
                            print('Nothing to {}, sorry!'.format(action))
                        #elif action == 'Collectable1':
                            #favorGiver = input('Name a player who give you a favor: ')
                            #cardToFavor = input('{}! do a favor for {}, please!\nName a card from your hand:{}: '.format(favorGiver, self.players[self.turnCounter].name, self.players[[x.name for x in self.players].index(favorGiver)].hand))
                            #self.players[[x.name for x in self.players].index(favorGiver)].giveOneCardToAnotherPlayer(self.players[self.turnCounter], cardToFavor)
                else:
                    print('No card like this!')
        print("\n{} won the game!\nCongratulations!".format(self.players[0].name))

#---

mygame = Game()
mygame.gameStart()
mygame.turnCircle()
