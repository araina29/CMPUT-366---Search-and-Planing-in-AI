# Motivation for starter code: https://www.cs.hmc.edu/twiki/bin/view/CS5Fall2016/Connect4Ply
# Name: Justin Stevens
# Problem description: Connect 4 Board and AI

from math import inf 

class Board:
    def __init__(self, width=7, height=6):
        """Initialize a Connect 4 Board with a specific width and height"""
        self.width = width
        self.height = height
        self.board = [self.width*[' '] for i in range(self.height)] 
        self.lastRow = None 
        self.lastCol = None 
        self.lastPlayer = None

    def __repr__(self):
        """Prints a representation of the Connect4 Board."""
        # Start with the empty string 
        board_str = "" 

        for row in range(self.height):
            # Initialize each row with a | 
            board_str += "|" 
            for col in range(self.width):
                board_str += self.board[row][col]+"|"
            board_str += "\n" 
        # Line of dashes 
        board_str += "-"*(self.width*2+1)+"\n" 
        for col in range(self.width):
            # Column numbers at the bottom 
            board_str += " "+str(col) 
        return board_str


    def available_moves(self): 
        """Inputs a board and returns an array with all the allowable moves with indexes"""
        allowableMoves = []
        for col in range(self.width):
            if self.allows_move(col):
                allowableMoves.append(col)
        return allowableMoves
    
    def allows_move(self, col):
        """Input a column and returns True if one can place a piece
            into this column."""
        # If the column isn't within the allowed range return False 
        if col not in range(self.width): 
            return False
        else:
            # Check to see if the top column is empty or not 
            if self.board[0][col]==' ':  
                return True
            else:
                return False 
    def perform_move(self, col, ox):
        """Inputs a column and a string ox and updates the board 
            with the piece 'ox' in the desired column"""
        #Decrement from the bottom row to the top row 
        for row in range(self.height-1, -1, -1):
            # If the location is empty 
            if self.board[row][col] == ' ': 
                self.board[row][col] = ox
                self.lastRow = row 
                self.lastCol = col
                self.lastPlayer = ox 
                return 
            
    def create_board(self, moveString):
        """ Accepts a string of columns and places
            alternating checkers in those columns,
            starting with 'X'.
            
            For example, call b.create_board('012345')
            to see 'X's and 'O's alternate on the
            bottom row, or b.create_board('000000') to
            see them alternate in the left column.

            moveString must be a string of integers
        """
        # Start by playing 'X'
        nextCh = 'X'   
        for colDigit in moveString:
            col = int(colDigit)
            # If the move is valid 
            if 0 <= col < self.width:
                self.perform_move(col, nextCh)
            # Switch to the other player's move
            if nextCh == 'X':
                nextCh = 'O'
            else:
                nextCh = 'X'
        return nextCh
    
    def undo_move(self, col):
        """Input a column col and removes the top checker from this column."""
        # Go from the top down 
        for row in range(self.height): 
            if self.board[row][col] != ' ': #If it is not empty
                self.board[row][col] = ' ' #Make it empty
                return 

    def is_terminal(self):
        """
        Returns True if the board represents a terminal state; False otherwise
        """
        return self.has_winner() or self.is_draw()

    def has_winner(self):
        """Input a boards and returns True if the board is a winning position
            and False otherwise."""

        row = self.lastRow 
        col = self.lastCol
        ox = self.lastPlayer 

        # No moves made on the board so far
        if(not row):
            return False 
        # Checks to see if there is a horizontal win
        for c in range(max(0, col-3), min(self.width-3, col+1)):
            if self.board[row][c]+self.board[row][c+1]+self.board[row][c+2]+self.board[row][c+3] == ox*4:
                    return True
        # Checks to see if there is a vertical win
        if row<self.height-3: 
            if self.board[row][col]+self.board[row+1][col]+self.board[row+2][col]+self.board[row+3][col] == ox*4:
                return True
        # Checks to see if there is a win on the upper right diagonal 
        for i in range(4):
            r = row-i
            c = col-i
            # Loop through all possible winning locations and see if they're valid 
            if 0<=r<self.height-3 and 0<=c<self.width-3: 
                if self.board[r][c]+self.board[r+1][c+1]+self.board[r+2][c+2]+self.board[r+3][c+3]==ox*4:
                    return True
        # Checks to see if there is a win on the upper left diagonal
        for i in range(4): 
            r = row-i
            c = col+i
            # Loop through all possible winning locations and see if they're valid 
            if 0<=r<self.height-3 and 3<=c<self.width: 
                if self.board[r][c]+self.board[r+1][c-1]+self.board[r+2][c-2]+self.board[r+3][c-3]==ox*4:
                    return True       
        return False

    def is_draw(self):
        """ Returns whether or not the current position is a draw"""
        return(not self.available_moves())
    
    def get_player_move(self, ox):
        """Input a player's checker piece and gets a move for them"""
        while True:
            #continually does this until the user enters a valid move
            try:
                col_move=int(input(ox+"'s choice ")) #tries to make the move an integer 
            except ValueError:
                continue
            if self.allows_move(col_move): #if it is a valid move 
                return col_move #return that move
            
    def print_congrats(self):
        """Prints out who won the game and the final game board"""

        print(self.lastPlayer, " wins -- Congratulations!")
        print(self)
    
    def host_game(self, ox = 'X'):
        """Hosts a game which can be played between two players"""
        print("Welcome to Connect Four!\n")
        gameOver = False
        moves = ''
        while not gameOver: 
            # Print current board position 
            print(self) 
            # Get the move an add it to the board 
            col_move = self.get_player_move(ox) 
            self.perform_move(col_move, ox)  
            moves += str(col_move)
            #print(moves)
            if(self.winsFor()):
                gameOver = True
            # Change player 
            if(ox == 'X'): 
                ox='O'
            else:
                ox='X'
        self.print_congrats()
        return moves

    def game_value(self):
        """
        This method assumes that the board represents a terminal state of the game.
        Returns 1 if the board is winning for player 'X' returns -1 if the board is winning for player 'O' returns 0 if neither
        """
        if self.has_winner(): #If the board is a win for self 
            if (self.lastPlayer == 'X'):
                return 1
            else:
                return -1 
        elif self.is_draw(): # If the board is a draw 
            return 0

