import random
from IPython.display import clear_output
coin_value = 10
max_players = 3
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':0}

#Functions


def choice(m):
    #general function of when u need user input of "question?(Y/N)"
    choice = 'wrong'
    while choice not in ['Y','y','N','n']:
        choice = input(m)
        if choice not in ['Y','y','N','n']:
            clear_output()
            print("Sorry, please choose a valid option")
    if choice.upper() == 'Y':
        return True
    else:
        return False
    
    
def coin_store(name):
    #Sets the number of coins for the specified player (the coins they want to buy not how many they want to bet)
    clear_output()
    print(f"{name} Let's get you some coins!\n")
    print(f'Every coin is worth {coin_value}$, you can exchange your coins at the end of the game')
    while True:
        try:
            money = int(input("How much do you want to exchange? ")) 
        except: 
            clear_output()
            print("Sorry that's not a valid number, please try again")
        else:
            if money%10 != 0 or money <= 0:
                clear_output()
                print("Sorry, you can only buy by multiples of ten")
            else:
                clear_output()
                print("Now its time to set the gamble for the game!")
                coins = int(money/10)
                #Sets the coins the player wants to use for their turn (important for doubling down or splitting) 
                while True:
                    try:
                        print(f'{name} you have {coins} coins worth {money}$!') 
                        gcoins = int(input("How many coins do you want to bet?:"))
                    except:
                        clear_output()
                        print("Sorry That's not a valid number, please try again")
                    else: 
                        clear_output()
                        if coins < gcoins or gcoins <= 0:
                            print("Sorry that's more coins than what you have")
                        else:
                            clear_output()
                            break
                #Confirm ammount for players
                print(f'{name} you have {coins} coins worth {money}$ and have betted {gcoins} coins for this round!') 
                end = choice("Do you want to continue?(Y/N)") 
                if end:
                    clear_output()
                    coins -= gcoins
                    break
                else:
                    clear_output()

    return [coins, gcoins]

def ask_for_as_value():
    #Returns the choice of the player for the value of an as (1 or 11)
    print(f" You have an As in  your deck!!")
    while True:
        try:
            choice = int(input("Choose its value(1/11):"))
        except: 
            clear_output()
            print("Sorry that's not a valid number, please try again")
        else:
            if choice not in [1,11]:
                clear_output()
                print("Sorry thats not a valid choice!")
            else:
                break
    return choice

def print_table():
    #prints on screen updated table 
    toprint = ''
    print("Deck of dealer:")
    if dealer_scard:
        for i in range(len(dealer_cards)):
            toprint += ' | ' + dealer_cards[i].rank + ' of ' + dealer_cards[i].suit + ' | '
        print(toprint)
    else:
        print(' | ' + dealer_cards[0].rank + ' of ' + dealer_cards[0].suit + ' | ')
    #printing players
    toprint = '\n'
    for i in range(len(players.all_players)):
        toprint += 'Deck of ' + players.all_players[i].name + ':\n'
        for y in range(len(players_cards[i])):
            toprint += ' | ' + players_cards[i][y].rank + ' of ' + players_cards[i][y].suit + ' | '
        toprint += '\n\n'
    
    print(toprint)
        
def sum_cards(i):
    c = 0
    for x in range(len(players_cards[i])):
        c += players_cards[i][x].value
    players.all_players[i].sum = c

#Objects

class Card:
    #single card object
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

class Player:
    def __init__(self, name, coins, gcoins):
        self.name = name
        self.coins = coins
        self.money = coins * coin_value
        self.sum = 0 #its the sum value of the player cards
        self.status = '' #can be bust or natural or stand
        self.gcoins = gcoins #The coins that the player is going to use on the game 

    def add_coins(self, new_coins):
        self.coins = self.coins + new_coins
        self.money = self.coins * coin_value
        
    def remove_coins(self, new_coins):
        self.coins = self.coins - new_coins
        self.money = self.coins * coin_value

    def __str__(self):
        return f'{self.name} you have {self.coins} coins worth {self.money}$!'
        
class Players:
    def __init__(self):
        self.all_players = []
        
    def set_players(self):
        #getting number of players
        print(f"The maximum number of players is {max_players}")
        while True:
            try:
                num = int(input("How many players? ")) 
            except: 
                clear_output()
                print("Sorry that's not a valid number, please try again")
            else:
                if num not in range(1,4):
                    clear_output()
                    print(f"Sorry, There can only be {max_players} players")
                else:
                    break
        #getting the names of the players
        for i in range(num):
            clear_output()
            name = input(f"Player {i+1} What's your name? ")
            set_coins = coin_store(name) #getting coins 
            self.all_players.append(Player(name, set_coins[0], set_coins[1]))

#Game logic

game_on = True 
while game_on:

#creating neccesary objects for the game
players = Players() 
players.set_players() 
deck = Deck()
deck.shuffle()
players_cards = [] #will hold nested lists of the two cards of every player, we will identify the player by index
dealer_cards = []
dealer_scard = False #will tell the print_table function when to print the remaining card of dealer

#setting table of players
for i in range(len(players.all_players)):
    card_holder = []
    for y in range(2):
        card_holder.append(deck.deal_one())
    players_cards.append(card_holder)

#setting table of dealer
for i in range(2):
    dealer_cards.append(deck.deal_one())

#Starting game 
print("Let's Start!")
for i in range(len(players.all_players)):    
    clear_output()
    print_table()
    print(f"{players.all_players[i].name} It's your turn: \n\n")
    sum_cards(i)
    #check for a natural at the begining 
    if players.all_players[i].sum == 10:
        players.all_players[i].status = 'natural'
        print("\n\nCongratulations! You have a BlackJack!! :D")
        print("Please wait for the end of the game")

    else:
        #check if first card is an as and ask value
        if players_cards[i][0].value == 0:
            choice = ask_for_as_value()
            players_cards[i][0].value = choice
        #start turn
        turn = True
        while turn:
            clear_output()
            print_table()
            print(f"{players.all_players[i].name} It's your turn: \n\n")
            #check for As in new card and ask value
            if players_cards[i][-1].value == 0:
                choice = ask_for_as_value()
                clear_output()
                print_table()
                print(f"{players.all_players[i].name} It's your turn: \n\n")
                players_cards[i][-1].value = choice
            #sum the values of the cards of the i player
            sum_cards(i) 
            #check for natural/blackjack
            if players.all_players[i].sum == 21:
                players.all_players[i].status = 'natural'
                print("Congratulations! You have a BlackJack!! :D")
                print("Please wait for the end of the game")
                break #END OF WHILE TURN ON
            #check for bust
            elif players.all_players[i].sum > 21: 
                players.all_players[i].status = 'bust'
                print("You Busted! :(")
                print("Please wait for the end of the game")
                break #END OF WHILE TURN ON
            else:
                #printing menu
                print("1. Hit")
                print("2.Stand")
                #check if double down possible
                if players.all_players[i].coins >= (players.all_players[i].gcoins*2):
                    print("3.Double down")
                    options_list = [1,2,3]
                else:
                    options_list = [1,2]
                #grab choice 
                while True:
                    try:
                        case = int(input("Pick an option: ")) 
                    except: 
                        print("Sorry that's not a valid number, please try again")
                    else:
                        if case not in options_list:
                            print("Sorry thats not a valid choice!")
                        else:
                            break
                #now user has picked 
                if case == 1:
                    #Hit
                    players_cards[i].append(deck.deal_one())
                elif case == 2:
                    #Stand
                    players.all_players[i].status = 'stand'
                    break #END OF WHILE TURN ON
                elif case == 3:
                    #double down
                    new_gcoins = players.all_players[i].gcoins*2
                    players.all_players[i].gcoins = new_gcoins
                    new_coins = players.all_players[i].coins - new_gcoins
                    players.all_players[i].coins = new_coins
                    players_cards[i].append(deck.deal_one())
                    sum_cards(i) 
                    if players.all_players[i].sum == 21:
                        players.all_players[i].status = 'natural'
                    elif players.all_players[i].sum > 21:
                        players.all_players[i].status = 'bust'
                    else:
                        players.all_players[i].status = 'stand'
                    break #End of while turn on
        #while  turn on level

#End of players turns (end of for)
#check dealers deck and compare, give money
clear_output()
dealer_scard = False
print_table()
#game finished, ask if play again
game_on = choice("Do you want to play again?(Y/N)")
clear_output()
#end of while game on
