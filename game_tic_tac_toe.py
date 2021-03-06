from tkinter import *
from functools import partial
import random

class GameWindow:
    def __init__(self, number_of_players, players, onclose=None):
        self.number_of_players = number_of_players
        self.players = players
        self.onclose = onclose

        self.count_turns = 0
        self.disable_numbers_x = set()
        self.disable_numbers_o = set()

        # The first time that someone plays goes directly to the board
        # This code sorts out who will be starting the game
        random.shuffle(self.players)
        self.player_x = self.players[0]
        self.player_o = self.players[1]
        
        # WINDOW: Game 
        self.top = Toplevel()
        self.top.title('tic-tac-toe')
        # width*height
        self.top.geometry("700x350")

        # when closing the top window with x, it will run the function to_settings.
        # same as when the button back to settings is clicked.
        # protocol() --- Registers a callback function for the given protocol. 
        # The name argument is typically one of “WM_DELETE_WINDOW” (the window is about to be deleted)
        self.top.protocol("WM_DELETE_WINDOW", self.to_settings)

        self.message_label4 = StringVar()
        
        label1 = Label(self.top, text='Tic-tac-toe',font='Helvetic 16 bold italic')
        back_button = Button(self.top, text="Back to settings",
                padx=5, pady=5, command=self.to_settings)
        label2 = Label(self.top, text=f"{self.players[0]} vs. {self.players[1]}",
                fg = '#1b1c5e', font='Helvetic 12',
                borderwidth=2, relief="groove", padx= 5, pady=5)
        #TO DO --- make the vr. bold
        label3 = Label(self.top, text="Let's Play")
        label4 = Label(self.top, textvariable=self.message_label4, font='TkDefaultFont 10')
        self.message_label4.set(f"it's your turn {self.player_x}")

        #Game frame
        Game_frame = Frame(self.top)
       
        self.game_btns = []
        for i in range(9):
            game_btn = Button(Game_frame, text=' ',
                            command=partial(self.click_number, i),
                            font=('Helvetica', 20), width=3)
            game_btn.grid(row=i//3, column=i%3)
            self.game_btns.append(game_btn)
        
        self.orig_color = game_btn.cget("background")
        # orig_color is SystemButtonFace

        #Play again button
        play_again_btn = Button(self.top, text="Play again",
                         padx= 5, pady=5, command=self.play_again)
        
        #layout
        label1.grid(row=0, column=0, columnspan=2, padx=80, pady=(10,0))
        label2.grid(row=1, column=0, columnspan=2, padx=80)
        label3.grid(row=2, column=0, columnspan=2, padx=80)
        label4.grid(row=3, column=0, columnspan=2, padx=80)
        Game_frame.grid(row=4, column=0, columnspan=2, padx=80)
        play_again_btn.grid(row=5, column=0, padx= 5, pady=(5,0), sticky=E)
        back_button.grid(row=5, column=1, padx=5, pady=(5,0), sticky=W)
        
    def to_settings(self):
        '''destroys the game window and activate the choices 
        on the setting window '''
        # when the user goes back to the setting 
        # the buttons on the game settings should be 
        # back to active (normal).
        self.top.destroy()
        if self.onclose:
            # the onclose() is calling the function enable_all from 
            # class MainWindow, used in the constructor
            # of the gameWindow object.
            self.onclose()

    def play_again(self):
        ''' Gets the game started. It resets all values stored during the last game,
        defines which player plays first'''
        # turn counter is reset to cero
        self.count_turns = 0

        # sets are reset to empty
        self.disable_numbers_x = set()
        self.disable_numbers_o = set()

        # buttons of the board games are reset, so that they are available to the
        # players, with no text and in their original color
        for i in range(9):
            if self.game_btns[i]['state'] == 'disabled':
                self.game_btns[i].config(state="normal", text=" ", bg=self.orig_color)
        # choose randomly the player that starts
        # applies for 1 player and 2 player choice
        random.shuffle(self.players)
        self.player_x = self.players[0]
        self.player_o = self.players[1] 

        self.message_label4.set(f"it's your turn {self.player_x}")

    def click_number(self, i):
        '''Places an X or an O over the pressed button of the game and disable this 
        button. Checks if there is a winner using the function player_won() or 
        if there is no more possible moves. Once a player has won, it dissables
        all the buttons on the board game. It changes the label to display who's next,
        if somebody has won or if the result is a tie.
        This functions is called by pressing any button on the board game

        Parameter:
        i(int): is the number referening the position of the button in the game board
        '''

        if self.count_turns % 2 == 0:
            current_player = self.player_x
            self.game_btns[i].config(state="disabled", text='X')
            next_player = self.player_o
            self.disable_numbers_x.add(i)
            self.check_disable = self.disable_numbers_x

        else:
            current_player = self.player_o
            self.game_btns[i].config(state="disabled", text='O')
            next_player = self.player_x
            self.disable_numbers_o.add(i)
            self.check_disable = self.disable_numbers_o
        
        self.count_turns += 1

        if self.player_won(self.check_disable):
            self.message_label4.set(f"{current_player} won!! :) ")

            # this code disable left over buttons after winning
            for i in range(9):
                if self.game_btns[i]['state'] == 'normal':
                    self.game_btns[i].config(state="disabled", text=" ")
        elif self.count_turns == 9:
             self.message_label4.set(f"It is a tie")
        else:
             self.message_label4.set(f"Your turn {next_player}")

    def player_won(self, check_disable):
        '''Checks if the last player to make a move has won, when a player has won 
        the buttons with the winning three in a row will turn to a color blue

        Parameter:
        check_disable(set): collected moves of the last player to make a move
        Returns:
        (bool): True if the player won or False if no player has won
        '''
        win_combinations = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8},
                        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
                        {2, 4, 6}, {0, 4, 8}]
        for win_set in win_combinations:
            if win_set.issubset(self.check_disable):
                for elem in win_set:
                    self.game_btns[elem]['bg'] = '#CCFFFF'
                return True

        return False

# if __name__ == "__main__": 