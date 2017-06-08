'''
Run tests on distributions with various notions of inverse
'''

from dice_lib import *
import random
import time
import sys

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
for i in xrange(ndice):
    row=[]
    for j in xrange(ndice):
       row.append(fastdice_compare(fdice[i],fdice[j]))
    scores.append(row)

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

print "Done"

