from twixt import twixtBoard
import sys
import agent
from util import printc, bcolors

if len(sys.argv) != 4:
	print "Incorrect number of arguments. Please refer to the Readme file"
	exit()

n = int(sys.argv[3])
depth = 2
width = 4
agents = [None, None]

if sys.argv[1] == "MCTreeSearch":
	agents[0] = agent.MCTreeSearchAgent()
elif sys.argv[1] == "HumanAgent":
	agents[0] = agent.HumanAgent(0)
elif sys.argv[1] == "PureMC":
	agents[0] = agent.PureMCAgent()
elif sys.argv[1] == "Minimax":
	agents[0] = agent.MinimaxAgent()

if sys.argv[2] == "MCTreeSearch":
	agents[1] = agent.MCTreeSearchAgent()
elif sys.argv[2] == "HumanAgent":
	agents[1] = agent.HumanAgent(1)
elif sys.argv[2] == "PureMC":
	agents[1] = agent.PureMCAgent()
elif sys.argv[2] == "Minimax":
	agents[1] = agent.MinimaxAgent()

#agent = [agent.MCTreeSearchAgent(agent.twoPinAwayPolicy, agent.twoPinAwayPolicy, 1000), agent.HumanAgent(1)]

def drawBoard(n, labels, assignments, bridges):
	for i in range(n):
		for j in range(n):
			if (i == 0 or i == n-1) and (j == 0 or j == n-1):
				print "%-*s" % (width, ""),
			else:
				if (i,j) in labels:
					if labels[(i,j)] in assignments[0]:
						#printc("%-*s" % (width, assignments[0][labels[(i,j)]])),
						if (i,j) in bridges:
							printc('O', bcolors.OKBLUE, 'bold'),
						else:
							printc('O'),
					elif labels[(i,j)] in assignments[1]:
						#printc("%-*s" % (width, assignments[1][labels[(i,j)]]), bcolors.FAIL),
						if (i,j) in bridges:
							printc('O', bcolors.FAIL, 'bold'),
						else:
							printc('O', bcolors.FAIL),
				else:
					print "%-*s" % (width, "x"),
			if j == n-1:
				print "\n"

iter = 1
tb = twixtBoard(n)
while tb.winner() == -1:
    print "iteration: ", iter
    iter += 1


    action = agents[tb.agent].getAction(tb)
    #print "agent, action: ", tb.agent, action
    tb.updateBoard(action)
    #print "pins: ", tb.pins
    #print "bridges: ", tb.bridges
    drawBoard(n, tb.label, tb.assignment, tb.bridges)

print tb.winner()

