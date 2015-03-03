import sys
import random
import signal
import copy
infinity=999999999
depth=0
#Timer handler, helper function

class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))
		

class Player45:
	
	def __init__(self):
		pass
	def getCells(self,temp_board,temp_block,old_move,flag):
#		while(1):
#			pass
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
		return cells
	
	# checks whether the board is completely filled or not if complete returns 0 else return -1
	def checkComplete(self,board,block_no):
		id1=block_no/3
		id2=block_no%3
		for i in xrange(id1*3,id1*3+3):
			for j in xrange(id2*3,id2*3+3):
				if(board[i][j] == '-'):
					return -1
		return 0

	# checks whether the character provided is same in all 3 cells in board
	def check(self,board,char,a,b,c):
		if(board[a[0]][a[1]]==char and board[b[0]][b[1]]==char and board[c[0]][c[1]]==char):
			return True	

	# checks whether the game is won by rows or columns or diagonals
	def checkAll(self,state,char,block_no):
		id1=block_no/3
		id2=block_no%3
		id1=id1*3
		id2=id2*3
		# 0 1 2 row
		if(self.check(state,char,(id1,id2),(id1,id2+1),(id1,id2+2))):
			return True
		# 3 4 5 row
		if(self.check(state,char,(id1+1,id2),(id1+1,id2+1),(id1+1,id2+2))):
			return True
		# 6 7 8 row
		if(self.check(state,char,(id1+2,id2),(id1+2,id2+1),(id1+2,id2+2))):
			return True
		# 0 3 6 col
		if(self.check(state,char,(id1,id2),(id1+1,id2),(id1+2,id2))):
			return True
		# 1 4 7 col
		if(self.check(state,char,(id1,id2+1),(id1+1,id2+1),(id1+2,id2+1))):
			return True
		# 2 5 8 col
		if(self.check(state,char,(id1,id2+2),(id1+1,id2+2),(id1+2,id2+2))):
			return True
		# 0 4 8 dia
		if(self.check(state,char,(id1,id2),(id1+1,id2+1),(id1+2,id2+2))):
			return True
		# 2 4 6 dia
		if(self.check(state,char,(id1,id2+2),(id1+1,id2+1),(id1+2,id2))):
			return True

	# returns utility value if game in a block is completed(utility for block)
	def terminalNode(self,state,block_no,flag):
		global depth
		if(flag=='x'):
			if(self.checkAll(state,'o',block_no)):
				return depth-10
			elif(self.checkAll(state,'x',block_no)):
				return 10-depth
			else:
			 	# if game is complete and draw returns 0
		 		if(self.checkComplete(state,block_no)==0):
	 				return 0
				else:
			  		return -1
		elif(flag=='o'):
			if(self.checkAll(state,'o',block_no)):
				return 10-depth
			elif(self.checkAll(state,'x',block_no)):
				return depth-10
			else:
			 	# if game is complete and draw returns 0
		 		if(self.checkComplete(state,block_no)==0):
	 				return 0
				else:
			  		return -1
	
	# converts cells to block_numbers(ex: 4 4 cell will be in block_no 4)
	def CellsToBlock(self,available_moves):
		available_blocks=[]
		for i in available_moves:
			row=i[0]
			col=i[1]
			block_no=(row/3)*3+col/3
			if block_no not in available_blocks:
				available_blocks.append(block_no)
		return available_blocks

	# returns all available cells in current block
	def getPositions(self,temp_board,block_no):
		available_positions=[]
		id1=block_no/3
		id2=block_no%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if(temp_board[i][j]=='-'):
					available_positions.append((i,j))
		return available_positions

	# returns Utility for Complete Board
	def getUtility(self,block,flag):
		utility=0
		if(flag=='x'):
			flag_negation='o'
		elif(flag=='o'):
			flag_negation='x'
		for i in xrange(0,9):
			if(block[i]==flag or block[i]==flag_negation or block[i]=='d'):
				# corner positions for board
				if(i%2==0 and i!=4):
					if(block[i]==flag):
						utility+=3*100
					elif(block[i]==flag_negation):
						utility+=3*-100
					elif(block[i]=='d'):
						utility+=0
				# center position takes highest utility because it is the best move for any block
				elif(i==4):
					if(block[i]==flag):
						utility+=5*100
					elif(block[i]==flag_negation):
						utility+=5*-100
					elif(block[i]=='d'):
						utility+=0
				# edge center takes list utility
				else:
				  	if(block[i]==flag):
						utility+=1*100
					elif(block[i]==flag_negation):
						utility+=1*-100
					elif(block[i]=='d'):
						utility+=0
		return utility

	# returns Utility for current block by looking at current position
	def alternateUtility(self,board,block_no,flag):
		utility=0
		if(flag=='x'):
			flag_negation='o'
		elif(flag=='o'):
			flag_negation='x'
		id1=block_no/3
		id2=block_no%3
		id1=id1*3
		id2=id2*3
		position={}
		position[0]=board[id1+0][id2+0]
		position[1]=board[id1+0][id2+1]
		position[2]=board[id1+0][id2+2]
		position[3]=board[id1+1][id2+0]
		position[4]=board[id1+1][id2+1]
		position[5]=board[id1+1][id2+2]
		position[6]=board[id1+2][id2+0]
		position[7]=board[id1+2][id2+1]
		position[8]=board[id1+2][id2+2]
		# possible winning positions in a block
		Three_in_a_row=[[position[0],position[1],position[2]],
				[position[3],position[4],position[5]],
				[position[6],position[7],position[8]],
				[position[0],position[3],position[6]],
				[position[1],position[4],position[7]],
				[position[2],position[5],position[8]],
				[position[0],position[4],position[8]],
				[position[2],position[4],position[6]]]
		Heuristic_Array=[[0,-10,-100,-1000],
				 [10,0,0,0],
				 [100,0,0,0],
				 [1000,0,0,0]]
		# for loop is for checking number of x's and number of o's in possible winning positions(ex: in row:0 1 2 if number of x's are 2 and number of o's are 0 then heuristic returns 100
		for i in xrange(8):
			ply=0
			opp=0
			for j in xrange(3):
				place=Three_in_a_row[i][j]
				if(place==flag):
					ply+=1
				elif(place==flag_negation):
					opp+=1
			utility+=Heuristic_Array[ply][opp]
		return utility

	# returns utility of current block by using alpha-beta pruning
	def getblockUtility(self,board,block,block_no,flag):
		index={}
		# board_states and block_states are like stack to store current states of board and block
		board_states=[]
		block_states=[]
		if(flag=='x'):
			flag_negation='o'
		elif(flag=='o'):
			flag_negation='x'
		def max_value(board,block,alpha,beta,flag,flag_negation):
			global depth
			checkGame=self.terminalNode(board,block_no,flag)
			if(checkGame == 10-depth or checkGame == depth-10 or checkGame == 0):
				utility=self.getUtility(block,flag)
				return checkGame+utility
			v=-infinity
			# returns available_moves in present block
			available_moves=self.getPositions(board,block_no)
			for i in available_moves:
				depth+=1
				# push current state of board and block in stack before updating with move
				board_states.append(copy.deepcopy(board))
				block_states.append(copy.deepcopy(block))
				update_lists(board,block,i,flag)
				new_vertex=min_value(board,block,alpha,beta,flag,flag_negation)
				if(len(board_states)==1):
					index[i]=new_vertex
				v=max(v,new_vertex)
				# pop states of board and block
				board=board_states.pop()
				block=block_states.pop()
				depth-=1
				alpha=max(alpha,v)
				if(beta<alpha):
					break
			return v

		def min_value(board,block,alpha,beta,flag,flag_negation):
			global depth
			checkGame=self.terminalNode(board,block_no,flag)
			if(checkGame==10-depth or checkGame==depth-10 or checkGame==0):
				utility=self.getUtility(block,flag)
				return checkGame+utility
			v=infinity
			available_moves=self.getPositions(board,block_no)
			for i in available_moves:
				depth+=1
				board_states.append(copy.deepcopy(board))
				block_states.append(copy.deepcopy(block))
				update_lists(board,block,i,flag_negation)
				v=min(v,max_value(board,block,alpha,beta,flag,flag_negation))
				board=board_states.pop()
				block=block_states.pop()
				depth-=1
				beta=min(beta,v)
				if(beta<alpha):
					break
			return v
		alpha=-infinity
		beta=infinity
		max_value(board,block,alpha,beta,flag,flag_negation)
		return index

	# move for our turn
	def move(self,temp_board,temp_block,old_move,flag):
		# index variable is used to store utilities of all possible moves and we select move which has maximum utility from those possible moves
		index={}
		# cell positions to block number convertion
		available_moves=self.getCells(temp_board,temp_block,old_move,flag)
		# get available blocks by using available_cells
		available_blocks=self.CellsToBlock(available_moves)
		# if number of available_moves are less than or equal to 8 then get utility by using minmax search tree
		if(len(available_moves)<=8):
			for i in available_blocks:
				board=copy.deepcopy(temp_board)
				block=copy.deepcopy(temp_block)
				index=self.getblockUtility(board,block,i,flag)
			return max(index,key=index.get)
		# else get utility directly by observing current block situation because of current move you make
		else:
			for i in available_moves:
				board=copy.deepcopy(temp_board)
				block=copy.deepcopy(temp_block)
				update_lists(board,block,i,flag)
				index[i]=self.getUtility(block,flag)
			# checks if all values in dictionary are same that is if all cells have equal utility values then call other utility function
			if(len(set(index.values()))==1):
				index={}
				for i in available_moves:
					board=copy.deepcopy(temp_board)
					block=copy.deepcopy(temp_block)
					update_lists(board,block,i,flag)
					block_no=(i[0]/3)*3+i[1]/3
					index[i]=self.alternateUtility(board,block_no,flag)
				return max(index,key=index.get)
			else:
				return max(index,key=index.get)

class Player2:
	
	def __init__(self):
		pass
	def move(self,temp_board,temp_block,old_move,flag):
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]
                
                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)

	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(temp_board,blocks_allowed,temp_block)
		return cells[random.randrange(len(cells))]

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)	
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		for i in range(9):
			for j in range(9):
                                no = (i/3)*3
                                no += (j/3)
				if gameb[i][j] == '-' and block_stat[no] == '-':
					cells.append((i,j))	
	return cells
		
# Note that even if someone has won a block, it is not abandoned. But then, there's no point winning it again!
# Returns True if move is valid
def check_valid_move(game_board,block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True


	for_corner = [0,2,3,5,6,8]

	#List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		## we will have 3 representative blocks, to choose from

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			## top left 3 blocks are allowed
			blocks_allowed = [0,1,3]
		elif old_move[0] % 3 == 0 and old_move[1] in [2,5,8]:
			## top right 3 blocks are allowed
			blocks_allowed = [1,2,5]
		elif old_move[0] in [2,5,8] and old_move[1] % 3 == 0:
			## bottom left 3 blocks are allowed
			blocks_allowed  = [3,6,7]
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
			### bottom right 3 blocks are allowed
			blocks_allowed = [5,7,8]

		else:
			print "SOMETHING REALLY WEIRD HAPPENED!"
			sys.exit(1)

	else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			## upper-center block
			blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			## middle-left block
			blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			## lower-center block
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			## middle-right block
			blocks_allowed = [5]

		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]

        #Check if the block is won, or completed. If so you cannot move there. 

        for i in reversed(blocks_allowed):
            if block_stat[i] != '-':
                blocks_allowed.remove(i)
        
        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = get_empty_out_of(game_board, blocks_allowed,block_stat)

	#Checks if you made a valid move. 
        if current_move in cells:
     	    return True
        else:
    	    return False

def update_lists(game_board, block_stat, move_ret, fl):
	#move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3
	id1 = block_no/3
	id2 = block_no%3
	mg = 0
	mflg = 0
	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		
                if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
                                break

	
	if mflg == 1:
		block_stat[block_no] = fl
	
        #check for draw on the block.

        id1 = block_no/3
	id2 = block_no%3
        cells = []
	for i in range(id1*3,id1*3+3):
	    for j in range(id2*3,id2*3+3):
		if game_board[i][j] == '-':
		    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        
        return

def terminal_state_reached(game_board, block_stat):
	
        #Check if game is won!
        bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		print block_stat
		return True, 'W'
	## Col win
	elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		print block_stat
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		print block_stat
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
					smfl = 1
					break
		if smfl == 1:
                        #Game is still on!
			return False, 'Continue'
		
		else:
                        #Changed scoring mechanism
                        # 1. If there is a tie, player with more boxes won, wins.
                        # 2. If no of boxes won is the same, player with more corner move, wins. 
                        point1 = 0
                        point2 = 0
                        for i in block_stat:
                            if i == 'x':
                                point1+=1
                            elif i=='o':
                                point2+=1
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
                                point1 = 0
                                point2 = 0
                                for i in range(len(game_board)):
                                    for j in range(len(game_board[i])):
                                        if i%3!=1 and j%3!=1:
                                            if game_board[i][j] == 'x':
                                                point1+=1
                                            elif game_board[i][j]=='o':
                                                point2+=1
			        if point1>point2:
				    return True, 'P1'
			        elif point2>point1:
				    return True, 'P2'
                                else:
				    return True, 'D'	





def decide_winner_and_get_message(player,status, message):
	if player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# Game board is a 9x9 list, block_stat is a 1D list of 9 elements
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1 
	pl2 = obj2

	### basically, player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1,-1) # For the first move

	WINNER = ''
	MESSAGE = ''

        #Make your move in 6 seconds!
	TIMEALLOWED = 6

	print_lists(game_board, block_stat)

	while(1):

		# Player1 will move
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
		
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player1 to complete in TIMEALLOWED secs. 
		try:
			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
			print "ret_move_pl1=",ret_move_pl1
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)
	
                #Checking if list hasn't been modified! Note: Do not make changes in the lists passed in move function!
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			#Player1 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the move made is valid
		if not check_valid_move(game_board, block_stat,ret_move_pl1, old_move):
			## player1 loses - he made the wrong move.
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl

                #So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
                update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		# Checking if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

                # Now player2 plays

		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]


		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		try:
                	ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = dpecide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
                if not check_valid_move(game_board, block_stat,ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
                
                update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
                if gamestatus == True:
			print_lists(game_board, block_stat)
                        WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
                        break
		old_move = ret_move_pl2
		print_lists(game_board, block_stat)
	
	print WINNER
	print MESSAGE

if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player45()
		obj2 = Player2()

	elif option == '2':
		obj1 = Player45()
		obj2 = Manual_player()
	elif option == '3':
		obj1 = Manual_player()
		obj2 = Manual_player()
        
        # Deciding player1 / player2 after a coin toss
        # However, in the tournament, each player will get a chance to go 1st. 
	fg=0
        num = random.uniform(0,1)
        if num > 0.5:
		fg=1
		simulate(obj2, obj1)
	else:
		fg=-1
		simulate(obj1, obj2)
	if(fg==1):
		print 'played with o so 2nd chance'
	elif(fg==-1):
		print 'played with x so 1st chance'
