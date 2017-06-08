'''
Run tests on distributions with various notions of inverse
'''

from dice_lib import *
import random
import time
import sys
from math import sqrt

if len(sys.argv)<4:
    print "Usage: inverse_test <rand_type> <n> <ntest>"
    print "... not a real utility, just a testing playground"
    print rand_type_options_string
    sys.exit(1)
rand_type = sys.argv[1]
n = int(sys.argv[2])
ntest = int(sys.argv[3])

rand_die = select_rand_type(rand_type)
if rand_die is None:
    print "Unsupported rand_type requested: %s"%rand_type
    sys.exit(1)

def rand_fastdie(n):
    return fastdie(rand_die(n))


dice=[]
inverse=[]
while len(dice)<ntest:
    A = rand_die(n)
    A.sort()
    if A not in dice:
        dienum = len(dice)
        dice.append(A)
        B = inverse_die(A)
        if A == B:
            inverse.append(dienum)
        else:
            dice.append(B)
            inverse.append(dienum+1)
            inverse.append(dienum)

fdice=[fastdie(x) for x in dice]
ndice=len(fdice)

#sanity check
for i in xrange(ndice):
    A = dice[i]
    B = dice[inverse[i]]
    if A != inverse_die(B):
        print "ERR: inverse sanity check fail"
        print A
        print B
        sys.exit(1)


scores=[]
beats=[]
for i in xrange(ndice):
    row=[]
    rowb=[]
    for j in xrange(ndice):
        val=fastdice_compare(fdice[i],fdice[j])
        row.append(val)
        if val<0:
            rowb.append(-1)
        elif val>0:
            rowb.append(1)
        else:
            rowb.append(0)
    scores.append(row)
    beats.append(rowb)

# Print the score matrix
fmt="%5d"
print " "*6,
for i in xrange(ndice):
    print fmt%i,
print ""
print ""
for i in xrange(ndice):
    print (fmt%i + " "),
    for j in xrange(ndice):
        print fmt%(scores[i][j]),
    print ""
print ""


print "Checking inverse score distribution hypothesis"
for i in xrange(ndice):
    a = [-x for x in scores[i]]
    b = list(scores[inverse[i]])
    a.sort()
    b.sort()
    if a != b:
        print "Found FAILURE! %d,%d" %(i,inverse[i])

print "Pass\n"



def norm(V):
    s=0.0
    for x in V:
        s += x*x
    return sqrt(s)

print "i: norm(diff),norm(sym),norm(anti), sum(scores[i]),sum(beats[i])"
for i in xrange(ndice):
    diff, sym, anti = sequence_to_difftriplet(dice[i])
    print "%d: %f, %f, %f  .. %d, %d"%(i,norm(diff),norm(sym),norm(anti),
                                   sum(scores[i]),sum(beats[i]))
    if 0:
        print dice[i]
        print diff
        print sym
        print anti


