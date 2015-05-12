from itertools import (takewhile,repeat)
import os
import time
from progressbar import Percentage, Bar, ProgressBar

def rawbigcount():
    f = open("random_sites.txt", 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    nLines = sum( buf.count(b'\n') for buf in bufgen if buf )
    f.close()
    return nLines


def main():
    nLines = sum(1 for _ in open('random_sites.txt'))
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=nLines).start()
    print nLines
    serverList = []
    numServers = []
    f = open("random_sites.txt", 'r')
    i = 0
    for line in f:
	line = line.rstrip()
	cmd = 'curl -I '+line+' > temp.txt'
	os.system(cmd)
	f2 = open("temp.txt", 'r')
	for line2 in f2:
	    if line2.startswith('Server'):
		line2 = line2.rstrip()
		print line2

		tempList = line2.split(': ')
		index = -1	
		try:
		    index = serverList.index(tempList[1])
		except ValueError:
		    index = -1	
		if index != -1:    	
		    numServers[index] = numServers[index]+1
		else:
		    serverList.append(tempList[1])
		    numServers.append(1)
        time.sleep(0.01)
        pbar.update(i+1)
	i += 1
    pbar.finish()
    for i in range(len(serverList)):
	print "Number of " + serverList[i] + " is " + str(numServers[i])
    #print serverList
    #print numServers 
    
main()
