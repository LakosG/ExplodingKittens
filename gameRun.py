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
        self.deck = Deck()
        self.trash = Trash()

    def createPlayers(self):
        pass


    def gameStart(self):
        print("It's the popular game called Exploding Kitten, written in Python.\n")

        intro = input("Enter names (2-5 players) separated by comma (, ): ")
        #intro = 'évi, gergő, béla'
        playersNames = intro.split(', ')
        numOfPlayers = len(playersNames)
        assert numOfPlayers > 1 and numOfPlayers < 6, "Please add min. 2 players and max. 5. You added {} player".format(numOfPlayers)

        players = [Player(i) for i in playersNames]

        for key, value in enumerate(players):
            players[key].drawCard(self.deck, 4)

        self.deck.addCard('Exploding kitten', Player.numOfPlayer - 1)
        self.deck.addCard('Defuse', 1)

        for key, value in enumerate(players):
            players[key].shuffleHand()
            print(players[key])

        print(self.deck)

        c = 0
        while len(players) > 1:
            if c > (len(players) - 1):
                c = 0
            print("\nIt's {}'s turn!".format(players[c].name))
            print(players[c])
            while True:
                action = input("Play a card by name or end your turn with Enter: ")
                #action = ''
                if action == '':
                    players[c].drawCard(self.deck)
                    print("{} drawed a card.".format(players[c].name))
                    if players[c].hand[-1] == 'Exploding kitten' and 'Defuse' in players[c].hand:
                        print("Exploding kitten!\n{} Defused the bomb!".format(players[c].name))
                        players[c].playCard(self.trash, 'Defuse')
                        deckindex = int(input('Where do you want to take the card? (0 = top of the deck / {} = last card): '.format(len(self.deck.cards))) or '0')
                        #deckindex = 0
                        players[c].takeBackCardToTheDeck(self.deck, 'Exploding kitten', deckindex)
                    elif players[c].hand[-1] == 'Exploding kitten' and 'Defuse' not in players[c].hand:
                        print("Exploding kitten! - BOOM!\n{} exploded".format(players[c].name))
                        del players[c]
                        c += 1
                        break
                    print(players[c])
                    print('\nTurn has ended!')
                    if players[c].attacked == 0:
                        c += 1
                    else:
                        players[c].attacked = 0
                    break
                elif action in players[c].hand:
                    players[c].playCard(self.trash, action)
                    whoNope = input('Anybody to Nope this action? Type a name or hit Enter: ')
                    if whoNope in [players[_].name for _ in range(len(players))] and 'Nope' in players[[x.name for x in players].index(whoNope)].hand:
                        players[[_.name for _ in players].index(whoNope)].playCard(self.trash, 'Nope')
                        #ide kell még, hogy lehessen Nope-olni a Nope-ot
                    else:
                        print('Nobody played Nope.') if whoNope == '' else print('{} has no Nope to play'.format(whoNope))

                        if action == 'Attack':
                            c += 1
                            if c > (len(players) - 1):
                                c = 0
                            print('Turn has been skipped!\n{} has been attacked.(2 turns)'.format(players[c].name))
                            players[c].attacked = 1
                            break
                        elif action == 'Skip':
                            print('\nTurn has been skipped!')
                            if players[c].attacked == 0:
                                c += 1
                            else:
                                players[c].attacked = 0
                            break
                        elif action == 'Favor':
                            favorGiver = input('Name a player who give you a favor: ')
                            cardToFavor = input('{}! do a favor for {}, please!\nName a card from your hand:{}: '.format(favorGiver, players[c].name, players[[x.name for x in players].index(favorGiver)].hand))
                            players[[x.name for x in players].index(favorGiver)].giveOneCardToAnotherPlayer(players[c], cardToFavor)
                        elif action == 'Shuffle':
                            self.deck.shuffle()
                        elif action == 'See the future':
                            print('The next 3 card will be:\n{}\n{}\n{}'.format(self.deck.cards[0], self.deck.cards[1], self.deck.cards[2]))
                        elif action == 'Nope':
                            print('Nothing to {}, sorry!'.format(action)) #ToDo Nope-olni a Nope-ot
                        elif action == 'Defuse':
                            print('Nothing to {}, sorry!'.format(action))
                        #elif action == 'Collectable1':
                            #favorGiver = input('Name a player who give you a favor: ')
                            #cardToFavor = input('{}! do a favor for {}, please!\nName a card from your hand:{}: '.format(favorGiver, players[c].name, players[[x.name for x in players].index(favorGiver)].hand))
                            #players[[x.name for x in players].index(favorGiver)].giveOneCardToAnotherPlayer(players[c], cardToFavor)
                else:
                    print('No card like this!')
        print("\n{} won the game!\nCongratulations!".format(players[0].name))

#---

mygame = Game()
mygame.gameStart()