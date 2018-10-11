import random


class Deck:
    def __init__(self):
        self.cards = []
        self.positionInDeck = 0
        self.build()
        self.shuffle()

    def __str__(self):
        return '\nIn the deck:\n{}'.format(self.cards)

    def build(self):
        startingDeck = {Card.TYPE_ATTACK:4,
                    Card.TYPE_SKIP: 4,
                    Card.TYPE_FAVOR: 4,
                    Card.TYPE_SHUFFLE: 4,
                    Card.TYPE_SEE_THE_FUTURE: 5,
                    Card.TYPE_COLLECTABLE1:4,
                    Card.TYPE_COLLECTABLE2:4,
                    Card.TYPE_COLLECTABLE3: 4,
                    Card.TYPE_COLLECTABLE4: 4,
                    Card.TYPE_COLLECTABLE5: 4,
                    Card.TYPE_NOPE: 5,
                    Card.TYPE_DEFUSE: 0,
                    Card.TYPE_EXPLODING_KITTEN: 0}

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
    TYPE_SKIP = "Skip"
    TYPE_ATTACK = "Attack"
    TYPE_FAVOR = "Favor"
    TYPE_SHUFFLE = "Shuffle"
    TYPE_NOPE = "Nope"
    TYPE_SEE_THE_FUTURE = "See the future"
    TYPE_DEFUSE = "Defuse"
    TYPE_EXPLODING_KITTEN = "Exploding kitten"
    TYPE_COLLECTABLE1 = "Collectable1"
    TYPE_COLLECTABLE2 = "Collectable2"
    TYPE_COLLECTABLE3 = "Collectable3"
    TYPE_COLLECTABLE4 = "Collectable4"
    TYPE_COLLECTABLE5 = "Collectable5"

    def __init__(self, cardType):
        self.cardType = cardType

    def __repr__(self):
        return '{}'.format(self.cardType)

class Player:
    numOfPlayer = 0
    def __init__(self, name):
        self.name = name
        self.hand = [Card.TYPE_DEFUSE]
        type(self).numOfPlayer += 1
        self.attacked = 0
        self.action = ''

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

        self.deck.addCard(Card.TYPE_EXPLODING_KITTEN, Player.numOfPlayer - 1)
        self.deck.addCard(Card.TYPE_DEFUSE, 1)

        for key, value in enumerate(self.players):
            self.players[key].shuffleHand()
            print(self.players[key])

    def gameStart(self):
        self.deck = Deck()
        self.trash = Trash()
        self.createPlayers()
        print(self.deck)

    def turnCounterStep(self):
        if self.players[self.turnCounter].attacked == 0:
            self.turnCounter += 1
        else:
            self.players[self.turnCounter].attacked = 0

    def attack(self):
        self.turnCounter += 1
        if self.turnCounter > (len(self.players) - 1):
            self.turnCounter = 0
        print('Turn has been skipped!\n{} has been attacked.(2 turns)'.format(self.players[self.turnCounter].name))
        self.players[self.turnCounter].attacked = 1

    def skip(self):
        print('\nTurn has been skipped!')
        self.turnCounterStep()

    def favor(self):
        favorGiver = input('Name a player who give you a favor: ')
        cardToFavor = input('{}! do a favor for {}, please!\nName a card from your hand:{}: '.format(favorGiver, self.players[self.turnCounter].name, self.players[[x.name for x in self.players].index(favorGiver)].hand))
        self.players[[x.name for x in self.players].index(favorGiver)].giveOneCardToAnotherPlayer(self.players[self.turnCounter], cardToFavor)

    def nopeAction(self):
        whoNope = input('Anybody to Nope this action? Type a name or hit Enter: ')
        if whoNope in [self.players[_].name for _ in range(len(self.players))] and Card.TYPE_NOPE in self.players[
            [x.name for x in self.players].index(whoNope)].hand:
            self.players[[_.name for _ in self.players].index(whoNope)].playCard(self.trash, Card.TYPE_NOPE)
            # Nope to Nope is not working
        else:
            print('Nobody played Nope.') if whoNope == '' else print('{} has no Nope to play'.format(whoNope))

    def defuseBomb(self):
        print("Exploding kitten!\n{} Defused the bomb!".format(self.players[self.turnCounter].name))
        self.players[self.turnCounter].playCard(self.trash, 'Defuse')
        self.deck.positionInDeck = int(
            input('Where do you want to take the card? (0 = top of the deck / {} = last card): '.format(
                len(self.deck.cards))) or '0')
        # self.deck.positionInDeck = 0
        self.players[self.turnCounter].takeBackCardToTheDeck(self.deck, Card.TYPE_EXPLODING_KITTEN,
                                                             self.deck.positionInDeck)
    def explodePlayer(self):
        print("Exploding kitten! - BOOM!\n{} exploded".format(self.players[self.turnCounter].name))
        del self.players[self.turnCounter]
        self.turnCounter += 1

    def turnCircle(self):
        while len(self.players) > 1:
            if self.turnCounter > (len(self.players) - 1):
                self.turnCounter = 0
            print("\nIt's {}'s turn!".format(self.players[self.turnCounter].name))
            print(self.players[self.turnCounter])
            self.playerTurn()
        print("\n{} won the game!\nCongratulations!".format(self.players[0].name))

    def playerTurn(self):
       while True:
            self.players[self.turnCounter].action = input("Play a card by name or end your turn with Enter: ")
            if self.players[self.turnCounter].action == '': #end the turn by Enter
                self.players[self.turnCounter].drawCard(self.deck)
                print("{} drawn a card.".format(self.players[self.turnCounter].name))
                if self.players[self.turnCounter].hand[-1] == Card.TYPE_EXPLODING_KITTEN and Card.TYPE_DEFUSE in self.players[self.turnCounter].hand:
                    self.defuseBomb()
                elif self.players[self.turnCounter].hand[-1] == Card.TYPE_EXPLODING_KITTEN and Card.TYPE_DEFUSE not in self.players[
                    self.turnCounter].hand:
                    self.explodePlayer()
                    break
                print(self.players[self.turnCounter])
                print('\nTurn has ended!')
                self.turnCounterStep()
                break
            elif self.players[self.turnCounter].action in self.players[self.turnCounter].hand:
                self.players[self.turnCounter].playCard(self.trash, self.players[self.turnCounter].action)
                self.nopeAction()
                if self.players[self.turnCounter].action == Card.TYPE_ATTACK:
                    self.attack()
                    break
                elif self.players[self.turnCounter].action == Card.TYPE_SKIP:
                    self.skip()
                    break
                elif self.players[self.turnCounter].action == Card.TYPE_FAVOR:
                    self.favor()
                elif self.players[self.turnCounter].action == Card.TYPE_SHUFFLE:
                    self.deck.shuffle()
                elif self.players[self.turnCounter].action == Card.TYPE_SEE_THE_FUTURE:
                    print('The next 3 card will be:\n{}\n{}\n{}'.format(self.deck.cards[0], self.deck.cards[1],
                                                                            self.deck.cards[2]))
                elif self.players[self.turnCounter].action == Card.TYPE_NOPE:
                    print('Nothing to {}, sorry!'.format(self.players[self.turnCounter].action))  # Nope to nope is not working
                elif self.players[self.turnCounter].action == Card.TYPE_DEFUSE:
                    print('Nothing to {}, sorry!'.format(self.players[self.turnCounter].action))

                # elif self.players[self.turnCounter].action == 'Card.TYPE.COLLECTABLE1':
                    # favorGiver = input('Name a player who give you a favor: ')
                    # cardToFavor = input('{}! do a favor for {}, please!\nName a card from your hand:{}: '.format(favorGiver, self.players[self.turnCounter].name, self.players[[x.name for x in self.players].index(favorGiver)].hand))
                    # self.players[[x.name for x in self.players].index(favorGiver)].giveOneCardToAnotherPlayer(self.players[self.turnCounter], cardToFavor)
            else:
                print('No card like this!')

#---

mygame = Game()
mygame.gameStart()
mygame.turnCircle()
