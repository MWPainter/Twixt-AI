import twixt

tb = twixt.twixtBoard(7)
actions = [(0,3), (1,1), (1,5), (3,3), (2,3), (2,2), (4,3), (4,2), (3,1)]
for action in actions:
	tb.updateBoard(action)
	print tb.label
	print tb.assignment
print tb.getScore()