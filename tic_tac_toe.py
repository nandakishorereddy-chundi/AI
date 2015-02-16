#!/usr/bin/python
import random
infinity=999999999
depth=0
board = [0,1,2,
	 3,4,5,
	 6,7,8]

board[0]="o"
board[1]=" "
board[2]="x"
board[3]=" "
board[4]="x"
board[5]=" "
board[6]="o"
board[7]=" "
board[8]=" "

def checkComplete(state):
	for i in xrange(9):
		if(state[i]==" "):
			return 20
	return 0

def printBoard():
    print board[0],'|',board[1],'|',board[2]
    print '---------'
    print board[3],'|',board[4],'|',board[5]
    print '---------'
    print board[6],'|',board[7],'|',board[8]

def check(state,char,a,b,c):
	if(state[a]==char and state[b]==char and state[c]==char):
		return True

def checkAll(state,char):
	if(check(state,char,0,1,2)):
		return True
	if(check(state,char,3,4,5)):
		return True
	if(check(state,char,6,7,8)):
		return True
	if(check(state,char,0,3,6)):
		return True
	if(check(state,char,1,4,7)):
		return True
	if(check(state,char,2,5,8)):
		return True
	if(check(state,char,0,4,8)):
		return True
	if(check(state,char,2,4,6)):
		return True


def get_available_moves(state):
	available_moves=[]
	for i in xrange(0,9):
		if(state[i] == " "):
			available_moves.append(i)
	return available_moves

def terminalNode(state):
	global depth
	if(checkAll(state,'x')):
		return depth-10
	elif(checkAll(state,'o')):
		return 10-depth
	else:
	 	if(checkComplete(state)==0):
 			return 0
		else:
		  	return 20


def opponentMove(state):
	index={}
	states=[]
	def max_value(state):
		global depth
		print "matrices in states in max_value",states
		checkGame=terminalNode(state)
		if(checkGame==10-depth or checkGame==depth-10 or checkGame==0):
			print "state in max_value func in terminal node: ",state
			print "matrices in states when terminal node is reached in max_value is: ",states
			print "terminal state reached in max_value func"
			return checkGame
		v=-infinity
		available_moves=get_available_moves(state)
		for i in available_moves:
			depth+=1
			states.append(list(state))
			print "state in max_value func: ",state
			state[i]="o"
			new_vertex=min_value(state)
			if(len(states)==1):
				index[i]=new_vertex
				print "index after popping matrix in max_value func is: ",index
			v=max(v,new_vertex)
			print "v in max_value func",v
			state=states.pop()
			depth-=1
			print "states is popped in max_value and resulting state is ",state
		return v

	def min_value(state):
		global depth
		print "matrices in states in min_value",states
		checkGame=terminalNode(state)
		if(checkGame==10-depth or checkGame==depth-10 or checkGame==0):
			print "state in min_value func in terminal node: ",state
			print "matrices in states when terminal node is reached in min_value is: ",states
			print "terminal state reached in min_value func"
			return checkGame
		v=infinity
		available_moves=get_available_moves(state)
		for i in available_moves:
			depth+=1
			states.append(list(state))
			print "state in min_value func: ",state
			state[i]="x"
			v=min(v,max_value(state))
			print "v in min_value func",v
			state=states.pop()
			depth-=1
			print "states is popped in min_value and resulting state is ",state
		return v
	
	print "max_value func called"
	max_value(state)
	print index
	return max(index,key=index.get)
	
def startGame():
	finalFlag=1
	while(finalFlag):
		printBoard()
		input=int(raw_input("select spot: "))
		if(board[input]!='x' and board[input]!='o'):
			board[input]='x'

			if(checkAll(board,'x')):
				print"----------------X Wins------------------------------"
				finalFlag=0
			printBoard()
			#opponent move
			global depth
			depth=0
			state=list(board)
			index=opponentMove(state)
			print "index= ",index
			board[index]="o"
			if(checkAll(board,'o')):
				print"----------------O Wins------------------------------"
				finalFlag=0
		else:
			print "spot taken"
		if(finalFlag==0):
			printBoard()

startGame()
