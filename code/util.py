import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

width = 4

def printc(str, color = bcolors.OKBLUE, bold = 'notbolded'):
	if bold == 'bold':
		print color + bcolors.BOLD + bcolors.UNDERLINE + "%-*s" % (width, str) + bcolors.ENDC,
	else:
		print color + "%-*s" % (width, str) + bcolors.ENDC,


def selectRandomKey(weightDict):
    """
    For a map from <Type> -> number, return a random key, with probabilities proportional 
    to the weights (the numbers).

    :param weightDict: The dictionary from keys to weights to pick a random key from
    """
    weights = []
    elems = []
    for elem in weightDict:
        weights.append(weightDict[elem])
        elems.append(elem)
    total = sum(weights)
    key = random.uniform(0, total)
    runningTotal = 0.0
    chosenIndex = None
    for i in range(len(weights)):
        weight = weights[i]
        runningTotal += weight
        if runningTotal > key:
            chosenIndex = i
            return elems[chosenIndex]
    raise Exception('Should not reach here')


