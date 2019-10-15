import The_Game
import Network
import random
import pickle
import os

bot_1 = Network.Network([14, 10, 6], [1, 6, 7], [8, 13, 0], 1, .001)
bot_2 = Network.Network([14, 10, 6], [8, 13, 0], [1, 6, 7], 2, .001)

if __name__ == '__main__':
    number_of_players = int(input("Enter number of players: "))
    if number_of_players == 0:
        load_nets = input("Would you like to 'load' or 'save' a network?\n"
                          "Type 'load' to load a network set\n"
                          "     'save' to train a network then save the nets\n"
                          "     'n' for neither and run the program\n"
                          "     : ")

        if load_nets == "load":
            folder_name = input("Type the folder name and press enter\n"
                            "     : ")
            bot_1.load_weights(folder_name)
            bot_2.load_weights(folder_name)


        if load_nets == 'save':
            folder_name = input("Type a name for the folder and press enter\n"
                                "     : ")
            bot_1.save_folder_name(folder_name)
            bot_2.save_folder_name(folder_name)
            bot_1.init_network()
            bot_2.init_network()

        if load_nets == "n":
            bot_1.init_network()
            bot_2.init_network()

        num_iterations = input("How many iterations do you want to execute?\n"
                               "     : ")
        for i in range(0, int(num_iterations)+1):
            new_game = The_Game.Game(number_of_players)
            new_game.play()
            print(i)

        if load_nets != "n":
            bot_1.save()
            bot_2.save()
            print("\n Networks saved!\n")
        print("Done!")
        print("Bot_1 number of wins : ", bot_1.wins, " losses : ", bot_1.losses, "\n"
              "Bot_2 number of wins : ", bot_2.wins, " losses : ", bot_2.losses, "\n",)

    if number_of_players == 1:
        AI_opponent_f = input("Enter the folder of the network you want to play against.\n"
                            "     : ")
        bot_1.load_weights(AI_opponent_f)
        new_game = The_Game.Game(number_of_players)
        new_game.play()

    if number_of_players == 2:
        new_game = The_Game.Game(number_of_players)
        new_game.play()

def train_ai_network(board, player):
    if player == 1:
        move = bot_1.eval(board)

    if player == 2:
        move = bot_2.eval(board) + 8
    print(move)
    return move

def get_ai_move(board, player_sides, player):
    # bot_1.eval(board)
    move = bot_1.eval(board) + 8
    print("Get_AI_Move: ", board)
    return move