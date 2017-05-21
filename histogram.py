'''
Calculate histogram of scores for a die, and std_dist histogram
'''

from dice_lib import *
import random
import time
import sys

if len(sys.argv)<4:
    print "Usage: histogram <rand_type> <n> <ntest>\n"
    print "randomly choses an <n> sided die, then does <ntest> comparisons"
    print "to random dice to get a score and std_dist histogram"
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


def do_score_histogram(A,n,ntest):
    # calculate score and std_dist histogram
    score = {}
    dist = {}

    A.sort()
    Adist = std_distance(A)
    Af = fastdie(A)
    for t in xrange(ntest):
        B = rand_die(n)
        B.sort()
        d = std_distance(B)
        if d in dist:
            dist[d] += 1
        else:
            dist[d] = 1

        Bf = fastdie(B)
        result = fastdice_compare(Af,Bf)
        if result in score:
            score[result] += 1
        else:
            score[result] = 1
        #if abs(result) > seen_abs_score:
        #    seen_abs_score = abs(result)
        #    print "%d: %r"%(result,B)

    score_histogram = list(score.iteritems())
    score_histogram.sort()
    dist_histogram = list(dist.iteritems())
    dist_histogram.sort()
    return (score_histogram,dist_histogram)

def closest_to_avg_die(n):
    if (n%2)==1:
        A = [(n+1)/2 for i in xrange(n)]
    else:
        A = [(n/2 if i<n/2 else 1 + n/2) for i in xrange(n)]
    assert( sum(A) == n*(n+1)/2 )
    return A

# -------------------------------------------------------------------------




print "Running histogram test: n=%d, ntest=%d"%(n,ntest)

#get a die for testing

if 0:
    # try to demand a certain std_dist
    # really slow unless request falls in main distribution hump
    while 1:
        A = rand_die(n)
        Adist = std_distance(A)
        if Adist == 100:
            break

if 0:
    # furthest from standard die
    A = closest_to_avg_die(n)

if 0:
    A = [i+1 for i in xrange(n)] # standard die
    #A = closest_to_avg_die(n) # furtherst from standard die
    request_dist = 100

    # random walk
    while 1:
        index0 = random.randrange(n)
        index1 = random.randrange(n)
        if A[index0]==1 or A[index1]==n:
            continue
        A[index0]-=1
        A[index1]+=1
        A.sort()
        if std_distance(A) == request_dist:
            break

if 0:
    # for comparing distributions, use the same A

    # n=100, chosen to be 100 std_distance from standard die
    A = [1, 3, 4, 5, 6, 7, 8, 8, 10, 11, 11, 12, 13, 15, 15, 16, 16, 18, 18, 21, 22, 23, 24, 26, 27, 27, 27, 30, 31, 31, 32, 33, 33, 34, 35, 35, 36, 38, 39, 39, 41, 41, 42, 43, 44, 46, 46, 48, 48, 50, 50, 51, 51, 51, 51, 53, 57, 57, 58, 58, 61, 61, 63, 63, 63, 64, 66, 66, 68, 68, 72, 75, 75, 75, 75, 78, 79, 79, 80, 82, 82, 83, 84, 85, 85, 86, 88, 88, 89, 89, 90, 90, 90, 92, 96, 97, 98, 99, 100, 100]


if 1:
    A = rand_die(n)

A.sort()
print "A:",A
Adist = std_distance(A)
print "dist:",Adist

start=time.time()
score_histogram,dist_histogram = do_score_histogram(A,n,ntest)
stop=time.time()
print "run time",(stop-start)

print "----------------------"
print "score histogram"
print "n=%d ntest=%d dist=%d"%(n,ntest,Adist)
print "min entry:",score_histogram[0]
print "max entry:",score_histogram[-1]
f=open("score_dist%d_n%d_%d.%s.csv"%(Adist,n,ntest,rand_type),"wb")
for val, count in score_histogram:
    f.write("%d,%d\n"%(val,count))
f.close()

print "----------------------"
print "std_dist histogram"
print "n=%d ntest=%d"%(n,ntest)
print "min entry:",dist_histogram[0]
print "max entry:",dist_histogram[-1]
f=open("stddist_n%d_%d.%s.csv"%(n,ntest,rand_type),"wb")
for val, count in dist_histogram:
    f.write("%d,%d\n"%(val,count))
f.close()

