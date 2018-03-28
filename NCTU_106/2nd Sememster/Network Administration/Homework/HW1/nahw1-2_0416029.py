import sys
import re
import operator
import prettytable
from optparse import OptionParser 

getMonth = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def main():
	checkArgs()
	result = {}
	
	file = open(args[0], 'r')
	logs = file.readlines()
	for log in logs:
		if 'Invalid user'not in log:
			continue
		content = list(filter(None, re.split(' |:|\n|<.*>', log)))

		timestamp = content[1:5]
		timestamp.insert(0, str(getMonth.index(content[0])))
		timestamp.insert(0, '2018')

		if options.AFTER and isntAfter(timestamp, list(filter(None, re.split('-|:', options.AFTER)))):
			continue

		if options.BEFORE and isntBefore(timestamp, list(filter(None, re.split('-|:', options.BEFORE)))):
			continue

		try:
			result[content[9]] += 1
		except:
			result[content[9]] = 1

	sort_key = 1
	sort_reverse = True

	if options.U:
		sort_key = 0
		sort_reverse = False

	if options.R:
		sort_reverse = not sort_reverse

	result = sorted(result.items(), key=operator.itemgetter(sort_key), reverse = sort_reverse)
	#print(*result, sep = '\n')
	
	table = prettytable.PrettyTable()
	table.field_names = ['user', 'count']
	index = 0
	for row in result:
		if options.N and index >= options.N:
			break
		if options.T and row[1] < options.T:
			continue
		table.add_row(row)
		index += 1
		
	print(table)
	
		
def isntAfter(timestamp, AFTER):
	for time in timestamp:
		if int(time) < int(AFTER[timestamp.index(time)]):
			return True
		elif int(time) > int(AFTER[timestamp.index(time)]):
			return False
	return False


def isntBefore(timestamp, BEFORE):
	for time in timestamp:
		if int(time) > int(BEFORE[timestamp.index(time)]):
			return True
		elif int(time) < int(BEFORE[timestamp.index(time)]):
			return False
	return False

def checkArgs():
	global options
	global args
	usage = 'usage: %prog [-h] [-u] [-after AFTER] [-before BEFORE] [-n N] [-t T] [-r] filename'
	optParse = OptionParser(usage)
	optParse.add_option('-u', action='store_true', default=False, dest='U', help='Summary failed login log and sort log by user')
	optParse.add_option('--after',type='string', default=False, dest='AFTER', help='Filter log after date. format YYYY-MM-DD-HH:MM:SS')
	optParse.add_option('--before',type='string', default=False, dest='BEFORE', help='Filter log before date. format YYYY-MM-DD-HH:MM:SS')
	optParse.add_option('-n',type='int', dest='N', default=False, help='Show only the user of most N-th times')
	optParse.add_option('-t',type='int', dest='T', default=False, help='Show only the user of attacking equal or more than T times')
	optParse.add_option('-r', action='store_true', default=False, dest='R', help='Sort in reverse order')
	options, args = optParse.parse_args()
	#print(options)
	#print(args)


if __name__ == "__main__":
	main()
