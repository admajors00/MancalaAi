import sys
import Main
import time
import random


# Mancala Rules
# The board consists of two rows of 6 holes and a moncala on each side
# In each hole there are 4 marblesto start off with
# A play in done by taking the marblesout of a hole and dropping one marblein each successing
#   hole in a clockwise direction
# Each player has a  side and moncala and must start their tunr from one of the 6 holes on their side
# If a player passes over their own mancala they drop a marble in, when coming to the opposing player's
#    moncala they skip it
# If a player's last marbleis placed in their own moncala then they get another turn
# If a player's last marbleis placed in an empty hole on their own side, that marblealong with any on the oppsite side of
#   the board are placed in the player's moncala, unless there are no marbleson the opposite side the
#   no pieces are collected
# A players score is determined by how many marblesare in thei moncala at the end of the game
# the game ends when there are no pieces left on one side of the board, the reaming pieces on the other side go to that player.


# A Mancala board look like
#  0   1   2   3   4   5   6   7
#  _   _   _   _   _   _   _   _
# |0|  _   _   _   _   _   _  |0|
# |_| |4| |4| |4| |4| |4| |4| |_|
#
#      13  12  11  10  9   8
# | | |4| |4| |4| |4| |4| |4| | |

# numbers are the amount of marbles in each spot
# index starts at the left players home and goes clockwise

class Game:
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        # Game_modes are single player, two-palyer, and AI,
        self.board = [0, 4, 4, 4, 4, 4, 4, 0
            , 4, 4, 4, 4, 4, 4]
        self.player = 1

        # format: player one[min, max, moncala] player two[min, max, moncala]
        #                       ^
        #                    starting moves
        self.player_sides = [[1, 6, 7], [8, 13, 0]]

    def play(self):
        print("===============================\n===============================\n===============================\n\nNEW GAME")
        if self.number_of_players != 0:
            print_board(self.board)
        has_won = False
        turns = 0
        while not has_won:
            # This alternates players
            if turns % 2 == 0:
                self.player = 1
                opponent = 2
                player_hole = 7
            elif turns % 2 == 1:
                self.player = 2
                opponent = 1
                player_hole = 0
            #print("play() player", self.player)
            move = self.request_move()
            # print(move)
            marbles = self.board[move]
            self.board[move] = 0

            while marbles > 0:
                # print("Position: ", move, "\n Marbles: ", marbles, "\n Marbles in hole: ", self.board[move])
                move += 1
                if move > 13:
                    move = 0
                if move == self.player_sides[opponent - 1][2]:
                    move += 1

                self.board[move] += 1
                marbles -= 1
                if marbles == 0:
                    if (self.board[move] == 1 and self.player_sides[self.player - 1][0] <= move <=
                            self.player_sides[self.player - 1][1] and find_adjacent_hole(move) > 0):
                        self.board[player_hole] += self.board[move] + self.board[find_adjacent_hole(move)]
                        self.board[find_adjacent_hole(move)] = 0
                        self.board[move] = 0

            # this adds 1 to turns so that turns will come out even again and will be the player's turn again
            if move == self.player_sides[self.player - 1][2]:
                turns += 1
            if self.number_of_players != 0:
                print_board(self.board)
            turns += 1
            n = 0
            for i in range(1, 7):
                n += self.board[i]
            if n == 0:
                has_won = True
            m = 0
            for i in range(8, 14):
                m += self.board[i]
            if n == 0 or m == 0:
                has_won = True

        print("Donezzoses1")

    def request_move(self):
        if self.number_of_players == 1:
            move = 0
            let_pass = False
            while not let_pass:
                if self.player == 1:
                    p = "Player 1"
                    let_pass = False
                    move = int(input("%s which position do you want to start from? : " % (p)))

                if self.player == 2:
                    move = Main.get_ai_move(self.board, self.player_sides, self.player)
                    print("Thinking...")
                    time.sleep(1)
                    print("Computers move : ", move)
                if self.player != 1 and self.player != 2:
                    print("WTF!?!?!")

                try:
                    if move == 0 or move == 7 or move > 13:
                        print("You can't do that!")
                    elif self.board[move] == 0:
                        print("You can't do that!")
                    if self.player_sides[self.player - 1][0] <= move <= self.player_sides[self.player - 1][1]:
                        return move
                    else:
                        print("You must choose a hole from your side!")
                except ValueError:
                    print("ERROR Entry must be a number")

        if self.number_of_players == 2:
            move = 0
            print("player : ", self.player)
            if self.player == 1:
                p = "Player1"
            if self.player == 2:
                p = "Player2"
            if self.player != 1 and self.player != 2:
                print("WTF!?!?!")
            let_pass = False

            while not let_pass:
                try:
                    move = int(input("%s which position do you want to start from? : " % (p)))
                    if move == 0 or move == 7 or move > 13:
                        print("You can't do that!")
                    elif self.board[move] == 0:
                        print("You can't do that!")
                    if self.player_sides[self.player - 1][0] <= move <= self.player_sides[self.player - 1][1]:
                        return move
                    else:
                        print("You must choose a hole from your side!")
                except ValueError:
                    print("ERROR Entry must be a number")

        if self.number_of_players == 0:
            move = Main.train_ai_network(self.board, self.player)
            #print("YOOOO\n", self.board, "\nYOOOO\n")

            try:
                if move == 0 or move == 7 or move > 13:
                    move = random.randint(self.player_sides[self.player - 1][0], self.player_sides[self.player - 1][1])
                elif self.board[move] == 0:
                    print("empty")
                    move = random.randint(self.player_sides[self.player - 1][0], self.player_sides[self.player - 1][1])
                if self.player_sides[self.player - 1][0] <= move <= self.player_sides[self.player - 1][1]:
                    return move
                else:
                    print("You must choose a hole from your side!")
            except ValueError:
                print("ERROR Entry must be a number")
            return move


def print_board(board):
    board_print = " \
       ""  0  1   2   3   4   5   6  \n"" \
       "" _   _   _   _   _   _   _   _ \n"" \
       ""| | |%s| |%s| |%s| |%s| |%s| |%s| | |\n"" \
       ""|%s|  _   _   _   _   _   _  |%s|\n"" \
       ""|_| |%s| |%s| |%s| |%s| |%s| |%s| |_|\n\n"" \
       ""     13  12  11  10  9  8   7\n" \
                  "===============================  """ % (
                      board[1], board[2], board[3],
                      board[4], board[5], board[6], board[0], board[7],
                      board[13], board[12], board[11],
                      board[10], board[9], board[8])
    print(board_print)


def eval_move(board, move, player):
    turns = 0
    has_won = False
    has_lost = False
    empty = False
    second_turn = False
    player_sides = [[1, 6, 7], [8, 13, 0]]
    player_hole = player_sides[player-1][2]
    if player == 1:
        opponent = 2
    else:
        opponent = 1
    if board[move] == 0:
        empty = True
        return [board, has_won, empty, second_turn, has_lost]
    marbles = board[move]
    board[move] = 0
    while marbles > 0:
        # print("Position: ", move, "\n Marbles: ", marbles, "\n Marbles in hole: ", self.board[move])
        move += 1
        if move > 13:
            move = 0
        if move == player_sides[opponent - 1][2]:
            move += 1
        board[move] += 1
        marbles -= 1
        if (marbles == 0):
            if (board[move] == 1 and player_sides[player - 1][0] <= move <=
                    player_sides[player - 1][1] and find_adjacent_hole(move) > 0):
                board[player_hole] += board[move] + board[find_adjacent_hole(move)]
                board[find_adjacent_hole(move)] = 0
                board[move] = 0

    # this adds 1 to turns so that turns will come out even again and will be the player's turn again
    if move == player_sides[player - 1][2]:
        turns += 1
        second_turn = True
    turns += 1
    n = 0
    for i in range(1, 7):
        n += board[i]
    m = 0
    for i in range(8, 14):
        m += board[i]
    if n == 0 or m==0 :

        if board[player_sides[player-1][2]] > board[player_sides[opponent-1][2]]:
            has_won = True
        else:
            has_lost = True

    return[board, has_won, empty, second_turn, has_lost]


def find_adjacent_hole(position):
    adjacent = 14 - position
    return adjacent
