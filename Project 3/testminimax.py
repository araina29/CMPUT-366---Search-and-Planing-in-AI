from math import inf
import random
import unittest 
from connect4 import Board

#A minimax algorithm is a recursive program written to find the best gameplay 
#that minimizes any tendency to lose a game while maximizing any opportunity to win the game.
def minimax(board,player,ply):
    return main(board,player,ply,1)

#Initialising a minmax function with 4th argument as the total number of expanded nodes there are 
def main(board, x_player, ply, total_nodes):
    """
        Function receives an instances of the Board class, the player who is to act at this state (either X or O),
        and the maximum search depth given by the variable ply.

        The function returns three values:
        1. the score of the optimal move for the player who is to act;
        2. the optimal move
        3. the total number of nodes expanded to find the optimal move
        """
	
    if(x_player == "X"):
        o_player = "O"

    else:
        o_player = "X"
	# We check if the board represents a terminal state
    if board.is_terminal() or ply == 0:
        if board.is_terminal():
			#We call the connect4 function which would give us  
					#1 if the board is winning for player 'X'
					#-1 if the board is winning for player 'O' 
					# returns 0 for a tie
            return board.game_value(), 0, total_nodes
        else:
            return 0 , 0 , total_nodes

	#For player X (Maximising player)
    if x_player=="X":

		#The estimated value we initialize
        est = -(inf)

		#So bassically we iterate over all the moves we have 
		#Inputs a board and returns an array with all the allowable moves with indexes
        for move in board.available_moves():

			#Inputs a column and a string ox and updates the board with the piece 'ox' in the desired column.
            board.perform_move(move,x_player)
			#We iterate a move on every loop call
            total_nodes+= 1
			#At every iteration we recall the minmax function to get a new score everytime.
            n_score , a , total_nodes  = main(board, o_player,ply-1,total_nodes)

            # We check that the new score is greater than our initialised value 
            if n_score > est:
                est = n_score
                column = move
			#Input a column col and removes the top checker from this column.
            board.undo_move(move)
        return est, column,total_nodes

	#For the other player O(Minimising Player)
    else:

		#The estimated value we initialize
        est = inf

		#So bassically we iterate over all the moves we have 
		#Inputs a board and returns an array with all the allowable moves with indexes
        for move in board.available_moves():

			#Inputs a column and a string ox and updates the board with the piece 'ox' in the desired column.
            board.perform_move(move, x_player)
			#We iterate a move on every loop call
            total_nodes+= 1
			#At every iteration we recall the minmax function to get a new score everytime.
            n_score , a, total_nodes  = main(board, o_player, ply - 1,total_nodes)

			# We check that the new score is less than our initialised value
            if n_score < est:
                est = n_score
                column = move
			#Input a column col and removes the top checker from this column.
            board.undo_move(move)
        return est, column, total_nodes

class TestMinMaxDepth1(unittest.TestCase):

	def test_depth1a(self):
		b = Board()
		player = b.create_board('010101')
		bestScore, bestMove, expansions = minimax(b, player, 1)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 0)

	def test_depth1b(self): 
		b = Board() 
		player = b.create_board('001122')
		bestScore, bestMove, expansions = minimax(b, player, 1)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)

	def test_depth1c(self): 
		b = Board() 
		player = b.create_board('335566')
		bestScore, bestMove, expansions = minimax(b, player, 1)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 4)

	def test_depth1d(self):
		b = Board() 
		player = b.create_board('3445655606')
		bestScore, bestMove, expansions = minimax(b, player, 1)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 6)

	def test_depth1e(self):
		b = Board() 
		player = b.create_board('34232210101')
		bestScore, bestMove, expansions = minimax(b, player, 1)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 1)

	def test_depth1f(self):
		b = Board() 
		player = b.create_board('23445655606')
		bestScore, bestMove, expansions = minimax(b, player, 1)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 6)

	def test_depth1g(self): 
		b = Board() 
		player = b.create_board('33425614156')
		bestScore, bestMove, expansions = minimax(b, player, 1)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 2)

class TestMinMaxDepth3(unittest.TestCase):

	def test_depth3a(self):
		b = Board()
		player = b.create_board('303111426551')
		bestScore, bestMove, expansions = minimax(b, player, 3)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 2)

	def test_depth3b(self): 
		b = Board() 
		player = b.create_board('23343566520605001')
		bestScore, bestMove, expansions = minimax(b, player, 3)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 6)

	def test_depth3c(self): 
		b = Board() 
		player = b.create_board('10322104046663')
		bestScore, bestMove, expansions = minimax(b, player, 3)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 0)

	def test_depth3d(self):
		b = Board() 
		player = b.create_board('00224460026466')
		bestScore, bestMove, expansions = minimax(b, player, 3)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)

	def test_depth3e(self):
		b = Board() 
		player = b.create_board('102455500041526')
		bestScore, bestMove, expansions = minimax(b, player, 3)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 1)

	def test_depth3f(self):
		b = Board() 
		player = b.create_board('01114253335255')
		bestScore, bestMove, expansions = minimax(b, player, 3)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 2)

	def test_depth3g(self): 
		b = Board() 
		player = b.create_board('0325450636643')
		bestScore, bestMove, expansions = minimax(b, player, 3)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 5)

class TestMinMaxDepth5(unittest.TestCase):
	def test_depth5a(self):
		b = Board()
		player = b.create_board('430265511116')
		bestScore, bestMove, expansions = minimax(b, player, 5)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)
		
	def test_depth5b(self):
		b = Board()
		player = b.create_board('536432111330')
		bestScore, bestMove, expansions = minimax(b, player, 5)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 5)

	def test_depth5c(self):
		b = Board()
		player = b.create_board('322411004326')
		bestScore, bestMove, expansions = minimax(b, player, 5)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)

	def test_depth5d(self):
		b = Board()
		player = b.create_board('3541226000220')
		bestScore, bestMove, expansions = minimax(b, player, 5)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 4)

	def test_depth5e(self):
		b = Board()
		player = b.create_board('43231033655')
		bestScore, bestMove, expansions = minimax(b, player, 5)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 1)

	def test_depth5f(self):
		b = Board()
		player = b.create_board('345641411335')
		bestScore, bestMove, expansions = minimax(b, player, 5)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 5)

	def test_depth5g(self):
		b = Board()
		player = b.create_board('336604464463')
		bestScore, bestMove, expansions = minimax(b, player, 5)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)		
		print(expansions)

if __name__ == '__main__':
    unittest.main()
