'''
Calculate how common multiple values are in random dice.
'''

from dice_lib import *
import random
import time
import sys

if len(sys.argv)<4:
    print "Usage: histogram <rand_type> <n> <ntest>\n"
    print "randomly choses an <n> sided die, then does <ntest> comparisons"
    print "to random dice to get a score and std_dist histogram"
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

def do_max_counts(n,ntest):
    # 
    max_mult = {}
    num_0 = {}
    num_1 = {}
    num_2 = {}
    num_3 = {}
    num_4 = {}
    num_above = {}

    for t in xrange(ntest):
        A = rand_die(n)

        # convert to counts
        c = [0]*n
        for x in A:
            c[x-1] += 1

        m = max(c)
        if m in max_mult:
            max_mult[m] += 1
        else:
            max_mult[m] = 1

        num0 = 0
        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        above = 0
        for x in c:
            if x==0:
                num0 += 1
            elif x==1:
                num1 += 1
            elif x==2:
                num2 += 1
            elif x==3:
                num3 += 1
            elif x==4:
                num4 += 1
            else:
                above += 1
        for x,dictx in [(num0,num_0),(num1,num_1),(num2,num_2),
                        (num3,num_3),(num4,num_4),(above,num_above)]:
            if x in dictx:
                dictx[x] += 1
            else:
                dictx[x] = 1

    max_mult = list(max_mult.iteritems())
    max_mult.sort()

    num_0 = list(num_0.iteritems())
    num_0.sort()
    num_1 = list(num_1.iteritems())
    num_1.sort()
    num_2 = list(num_2.iteritems())
    num_2.sort()
    num_3 = list(num_3.iteritems())
    num_3.sort()
    num_4 = list(num_4.iteritems())
    num_4.sort()
    num_above = list(num_above.iteritems())
    num_above.sort()
    return (max_mult,num_0,num_1,num_2,num_3,num_4,num_above)

def stats(L,n,ntest):
    mn = L[0][0]
    mx = L[-1][0]

    q = 0
    total = 0
    mode = 0
    for x, count in L:
        total += x*count
        q += count
        if q-count < ntest/2 and q>= ntest/2:
            mode = x
    mean = total*(1.0/ntest)

    print "  min:  %-8d fraction of dice faces:%f"%(mn,mn*(1.0/n))
    print "  mode: %-8d fraction of dice faces:%f"%(mode,mode*(1.0/n))
    print "  mean: %-8.4f fraction of dice faces:%f"%(mean,mean*(1.0/n))
    print "  max:  %-8d fraction of dice faces:%f"%(mx,mx*(1.0/n))
    return mn,mode,mean,mx

# -------------------------------------------------------------------------

print "Running multiset freq test: n=%d, ntest=%d"%(n,ntest)

start=time.time()
max_mult,num_0,num_1,num_2,num_3,num_4,num_above = do_max_counts(n,ntest)
stop=time.time()
print "run time",(stop-start)

print "----------------------"
print "max multiplicity of numbers on a die"
for mult,count in max_mult:
    print "  %d: %d  fraction: %f"%(mult,count,count*(1.0/ntest))

print "how common multiplicity of 0 is"
stats(num_0,n,ntest)
print "how common multiplicity of 1 is"
stats(num_1,n,ntest)
print "how common multiplicity of 2 is"
stats(num_2,n,ntest)
print "how common multiplicity of 3 is"
stats(num_3,n,ntest)
print "how common multiplicity of 4 is"
stats(num_4,n,ntest)
print "how common multiplicity above 4 is"
stats(num_above,n,ntest)


