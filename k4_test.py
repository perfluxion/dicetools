'''
Calculate intranstive and tie fraction for k=4
'''

from dice_lib import *
import random
import time
import sys

if len(sys.argv)<4:
    print "Usage: k4_test <rand_type> <n> <ntest>\n"
    print "randomly choses 4 <n> sided dice,"
    print "and counts the fraction of ties and intransitives"
    print "<rand_type> options: "
    print "    sequence, multiset, sequence_walk, multiset_walk"
    sys.exit(1)
rand_type = sys.argv[1]
n = int(sys.argv[2])
ntest = int(sys.argv[3])

if rand_type == "sequence":
    rand_die = rand_die_sequence
elif rand_type == "sequence_walk":
    rand_die = rand_die_sequence_walk
elif rand_type == "multiset":
    rand_die = rand_die_multiset
elif rand_type == "multiset_walk":
    rand_die = rand_die_multiset_walk
else:
    print "Unsupported rand_type requested: %s"%rand_type
    sys.exit(1)

def rand_fastdie(n):
    return fastdie(rand_die(n))


def k4_test(n,ntest):
    k=4

    # for k=4, there are 4 inequivalent tournaments and 4 score sequences
    # http://www.ams.org/samplings/feature-column/fcarc-scores 
    tie=0
    score_possibilities = [[0,1,2,3],[0,2,2,2],[1,1,1,3],[1,1,2,2]]
    count = [0]*4
    for t in xrange(ntest):
        # verifies the random dice are distinct,
        # this should only matter for small n
        fdice = []
        while len(fdice)!=k:
            A = rand_fastdie(n)
            if A not in fdice:
                fdice.append(A)

        tied, beats = beats_count(fdice)
        if tied:
            tie += 1
            continue

        beats.sort()
        index = score_possibilities.index(beats)
        count[index] += 1
    print "----------------------"
    print "n=%d, k=%d, ntest=%d"%(n,k,ntest)
    print "tie=%f intransitive=%f (of non-tie = %f)"%(
           tie*(1.0/ntest),
           count[3]*(1.0/ntest),
           count[3]*1.0/(ntest-tie))
    for i in xrange(len(score_possibilities)):
        print "%r  %f   (of non-tie %f)"%(
                score_possibilities[i],count[i]*(1.0/ntest),
                count[i]*1.0/(ntest-tie))

# -------------------------------------------------------------------------

k = 4
print "Running k=4 test: n=%d, ntest=%d"%(n,ntest)

start=time.time()
k4_test(n,ntest)
stop=time.time()
print "run time",(stop-start)

