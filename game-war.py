#Global variables 
import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}

class Card:
    #creates a card object and prints what card is it
    def __init__(self, suit, rank):
        self.suit = suit    
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    #Creates a deck using a list of cards(objects) and has a Shuffle function 
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))
                #note that all the elements of this list will be able to use the functions of the card class
    
    def shuffle(self):
        #Random.shuffle does not return anything
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        return self.all_cards.pop()

"""
new_deck = Deck()
note that  print(new_deck.all_cards will print the memory location of all the elements of the list.
to be able to print it like before:
new_card = new_deck.all_cards[0]  to print them all use a for loop
for x in new_deck.all_cards:
    print(x)"""

class Player():
    #This class gives cards to a player and also removes the top card of the hand of the player(0 index)
    def __init__(self):
        self.cards = []

    def add_card(self, new_cards):
        #we will make sure that when you want to add more than one you do it with a list
        if type(new_cards) == type([]):
            self.cards.extend(new_cards)
            #if we use the append method we would have a nested list so we use extend to fuse the two lists together, the new cards will be at the "bottom"
        else:
            self.cards.append(new_cards)

    def remove_card(self):
        return self.cards.pop(0)

#START OF GAME LOGIC
player_one = Player()
player_two = Player()
deck = Deck()
deck.shuffle()
#Give the card to the players 
for x in range(26):
    player_one.add_card(deck.deal_one())
    player_two.add_card(deck.deal_one())

#start of while loop- turns
round_num = 0
game_on = True
while game_on:
    #Check if win
    if len(player_one.cards) == 0:
        print("Player One out of cards! Game Over")
        print("Player Two Wins!")
        game_on = False
        break
        
    
    if len(player_one.cards) == 0:
        print("Player One out of cards! Game Over")
        print("Player Two Wins!")
        break
    
    #Reset board and puts cards on "table" to compare
    player_one_cards = []
    player_one_cards.append(player_one.remove_card())
    player_two_cards = []
    player_two_cards.append(player_two.remove_card())

    #comparing the cards on "table"
    compare = True
    while compare: #this needs to be on a loop in case there's a tie
        round_num += 1
        print(f"Round {round_num}:")
        print("  Player one       Player Two")
        print(f"{player_one_cards[-1]} vs {player_two_cards[-1]}") 
        #comparing
        if player_one_cards[-1].value > player_two_cards[-1].value:
            #adding both players cards to the deck of player one
            player_one.add_card(player_one_cards)
            player_one.add_card(player_two_cards)
            print("\nPlayer one takes this round!\n\n")
            break

        elif player_one_cards[-1].value < player_two_cards[-1].value:
            #adding both players cards to the deck of player two
            player_two.add_card(player_one_cards)
            player_two.add_card(player_two_cards)
            print("\nPlayer two takes this round!\n\n")
            break
        
        else:
            print("\n WAR! \n")
            #check to see if player has enough cards for war (draw 5 cards)
            if len(player_one.cards) < 5:
                print("Player One unable to play war! Game Over at War")
                print("Player Two Wins! Player One Loses!")
                game_on = False
                break

            elif len(player_two.cards) < 5:
                print("Player Two unable to play war! Game Over at War")
                print("Player One Wins! Player Two Loses!")
                game_on = False
                break

            else:
                for num in range(5):
                    player_one_cards.append(player_one.remove_card())
                    player_two_cards.append(player_two.remove_card())


        