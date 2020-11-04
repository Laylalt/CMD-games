#do u want to play again? 
def play_again():
    choice = 'wrong'
    while choice not in ['Y','y','N','n']:
        choice = input("Do you want to keep playing?(Y/N) ")
        if choice not in ['Y','y','N','n']:
            print("-----"*5)
            print("Sorry, please choose a valid option")
    if choice.upper() == 'Y':
        return True
    else:
        return False
    
#plater 1 choose symbol
def choose():
    players = {'p1': 'N', 'p2': 'N'}
    symbol = 'Wrong'
    while symbol not in ['x', 'X', 'O', 'o']:
        print("Player 1:")
        symbol = input('Do you want to be X or O? ')
        if symbol not in ['x', 'X', 'o', 'O']:
            print("-----"*5)
            print("sorry that's not a valid option :(")
    print("-----"*5)
    players['p1'] = symbol.upper()
    if players['p1'] == 'X':
        players['p2'] = 'O'
    else:
        players['p2'] = 'X'
    return players
    
#print board
def print_board(game_list): #print board
    print("     |     |")
    print(f'   {game_list[0]} |  {game_list[1]}  | {game_list[2]} ')
    print("     |     |")
    print("------------------")
    print("     |     |")
    print(f'   {game_list[3]} |  {game_list[4]}  | {game_list[5]} ')
    print("     |     |")
    print("------------------")
    print("     |     |")
    print(f'   {game_list[6]} |  {game_list[7]}  | {game_list[8]} ')
    print("     |     |")

#check if board is full
def check_full(game_list): #False not full,  True full
    checker = True
    for n in game_list:
        if n in [1,2,3,4,5,6,7,8,9]:
            checker = False
            break
        else: 
            pass
    return checker
#check for win
def check_win(game_list):
    index = [0,3,6]
    for i in index:
        if game_list[i] == game_list[i+1] == game_list[i+2]:
            return True
    index = [0,1,2]
    for i in index:
        if game_list[i] == game_list[i+3] == game_list[i+6]:
            return True
    if game_list[0] == game_list[4] == game_list[8]:
        return True
    if game_list[2] == game_list[4] == game_list[6]:
        return True
    return False

#check if user input when selecting spot is correct
def check_pos(game_list,turn): 
    print_board(game_list)
    pos = 'Wrong'
    while pos not in ['1','2','3','4','5','6','7','8','9']:
        print(f'Player {turn} it is your turn!')
        pos = input("Choose your position: ")
        if pos not in ['1','2','3','4','5','6','7','8','9']:
            print("-----"*5)
            print_board(game_list)
            print("sorry that's not a  valid option")
    print("-----"*5)
    pos = int(pos) - 1
    while game_list[pos] in ['X', 'O']:
        print_board(game_list)
        print("sorry that position is already taken")
        pos = input("Choose your position: ")
        if pos not in ['1','2','3','4','5','6','7','8','9']:
            print("-----"*5)
            print_board(game_list)
            print("sorry that's not a  valid option")
        print("-----"*5)
        pos = int(pos) - 1
    return pos

#update symbol in board
def update(game_list, pos, symbol ): 
    game_list[pos] = symbol
    return game_list

#main--------------------------------
game_on = True
turn = 1
game_list = [1,2,3,4,5,6,7,8,9]
#first player chooses symbol
players = choose()
while game_on == True:
    if turn % 2 == 0:
        symbol = players['p2']
        player = 2
    else:
        symbol = players['p1']
        player = 1
    pos = check_pos(game_list, player )
    game_list = update(game_list, pos, symbol)
    if check_full(game_list) or check_win(game_list) :
        print_board(game_list)
        if check_win(game_list):
            print(f'Congratulations Player {player}!! You Win')
        else:
            print("It's a Tie!!")
        turn = 1
        game_list = [1,2,3,4,5,6,7,8,9]
        game_on = play_again()
        if game_on:
            print("-----"*5)
            players = choose()
    else:
        turn += 1