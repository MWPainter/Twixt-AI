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