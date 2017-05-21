'''
Timing test of some dice routines
'''

from dice_lib import *
import time

rand_die = rand_die_sequence
def rand_fastdie(n):
    return fastdie(rand_die(n))


# ugh timeit is such a pain with module boundaries
# just make our own time testing routine

def time_test(codeline,setup="",repeat=5,ntest=10,maxn=1000000,
              testlist=[10,20,30,40,50,60,70,80,90,100,200,300,400,500]):
    print "---- timing %s"%(codeline)
    setup.replace(";","\n    ")
    if ntest>1:
        testcode='''for testx in xrange(ntest):
            %s'''%codeline
        ntest_str="%d loops, "%ntest
    else:
        testcode=codeline
        ntest_str=""
    fstr = '''
def f(n,repeat,ntest):
    %s
    timelist=[]
    for repeatx in xrange(repeat):
        start = time.time()
        %s
        stop = time.time()
        timelist.append(stop-start)
    return timelist
'''%(setup,testcode)
    #print fstr
    exec(fstr)
    for n in testlist:
        if n>maxn:
            continue
        timelist = f(n,repeat,ntest)
        timelist.sort()
        print "n=%-05d  %sbest of %d runs: %f  median: %f"%(
                n,ntest_str,repeat,min(timelist),timelist[repeat/2])


time_test("rand_die_sequence(n)")
time_test("rand_die_sequence_walk(n)")
time_test("rand_die_multiset(n)",maxn=200)
time_test("rand_die_multiset_walk(n)")
time_test("fastdie(A)",setup="A=rand_die(n)")
time_test("compare(A,B)",setup="A=rand_die(n);B=rand_die(n)")
time_test("fastdice_compare(Af,Bf)",
          setup="Af=rand_fastdie(n);Bf=rand_fastdie(n)")

