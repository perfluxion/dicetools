'''Library of functions for investigating intransitive dice
'''

import random
import itertools
from math import log


def rand_die_multiset(n):
    '''random proper die selected uniformly from multiset representation

    die properties:
      allowed values: integers 1 to n
      sum constrained to n*(n+1)/2
    random distribution:
      die selected uniform in multiset representation

    die returned in sorted sequence representation
    '''
    s = n*(n+1)/2

    while 1:
        # randomly select n-1 location in range(2n-1)
        # these locations breaks the range into n segments
        m = []
        while len(m)<n-1:
            x = random.randrange(2*n-1)
            if x not in m:
                m.append(x)
        m.sort()

        # count spots between locations
        c = [0]*n
        prev = m[0]
        c[0] = prev
        for i in xrange(1,n-1):
            c[i] = m[i] - prev - 1
            prev = m[i]
        c[n-1] = (2*n-2) - prev
       
        #assert(sum(c) == n)

        # convert to sorted sequence representation
        A = []
        for i in xrange(n):
            A += [i+1]*c[i]

        if sum(A) == s:
            return A

def rand_die_sequence(n):
    '''random proper die selected uniformly from unsorted sequence representation

    die properties:
      allowed values: integers 1 to n
      sum constrained to n*(n+1)/2
    random distribution:
      die selected uniform in unsorted sequence representation

    die returned in unsorted sequence representation
    '''
    s = n*(n+1)/2
    while 1:
        # generate n-1 values for the die,
        # then try to get the last value from the constraint
        # toss the result and try again if not possible
        A = [random.randrange(n)+1 for x in xrange(n-1)]
        diff = s - sum(A)
        if diff<=0 or diff>n:
            continue
        A.append(diff)
        return A

def rand_die_max2multiset(n):
    '''random proper die selected uniformly from multiset representation
    with restriction that entries are maximum of 2

    die properties:
      allowed values: integers 1 to n
      sum constrained to n*(n+1)/2
    random distribution:
      die selected uniform in multiset representation with max 2 constraint

    die returned in sorted sequence representation
    '''
    s = n*(n+1)/2
    while 1:
        c = [random.randint(0,2) for i in xrange(n-1)]
        diff = n-sum(c)
        if diff<0 or diff>2:
            continue
        c.append(diff)

        # convert to sorted sequence representation
        A = []
        for i in xrange(n):
            A += [i+1]*c[i]

        if sum(A) == s:
            return A


def rand_die_sequence_walk(n, burn = lambda x: 3*x*log(x)):
    '''random proper die generated with randomwalk, limit is uniform in
    unsorted sequence representation

    Could possibly be faster than rand_die_sequence for very large n.

    burn(n) sets how the number of random steps should scale with n.
    If this is large enough, the results should select uniformly in the
    unsorted sequence representation.
    '''
    nsteps = int(burn(n))

    # start at standard die
    die = [i+1 for i in xrange(n)]
    for i in xrange(nsteps):
        a = random.randint(1, n) # amount to add/subtract
        x = random.randrange(n)  # position to subtract from die value
        y = random.randrange(n)  # position to add to die value
        if die[x] <= a or die[y] > (n-a):
            continue
        else:
            die[x] -= a
            die[y] += a
    return die

def rand_die_multiset_walk(n, burn = lambda x: 3*x*log(x)):
    '''random proper die generated with randomwalk, limit is uniform in
    multiset representation

    Intended to be a faster version of rand_die_multiset.

    burn(n) sets how the number of random steps should scale with n.
    If this is large enough, the results should select uniformly in the
    multiset representation.
    '''
    nsteps = int(burn(n))

    # start in multiset representation of standard die
    die = [1]*n
    for i in xrange(nsteps):
        a = random.randrange(1,n/2) # amount to change die value
        x = random.randrange(a,n) # take a die from here and move it down
        y = random.randrange(n-a) # take a die from here and move it up
        if x==y:
            if die[x] < 2:
                continue
        elif die[x] < 1 or die[y] < 1:
            continue
        die[x] -= 1
        die[x-a] += 1
        die[y] -= 1
        die[y+a] += 1
    #assert(sum(die)==n)
    #assert(min(die)>=0)

    # convert to sorted sequence representation
    A = []
    for i in xrange(n):
        A += [i+1]*die[i]
    return A

def rand_die_max2multiset_walk(n, burn = lambda x: 3*x*log(x)):
    '''random proper die generated with randomwalk, limit is uniform in
    multiset representation with restriction that entries are a maximum of 2

    Intended to be a faster version of rand_die_max2multiset.

    burn(n) sets how the number of random steps should scale with n.
    If this is large enough, the results should select uniformly in the
    multiset representation with restriction that entries are a maximum of 2
    '''
    nsteps = int(burn(n))

    # start in multiset representation of standard die
    die = [1]*n
    for i in xrange(nsteps):
        a = random.randrange(1,n/2) # amount to change die value
        x = random.randrange(a,n) # take a die from here and move it down
        y = random.randrange(n-a) # take a die from here and move it up
        if x==y:
            if die[x] < 2:
                continue
        elif die[x] < 1 or die[y] < 1:
            continue
        if x-a == y+a:
            if die[x-a] > 0:
                continue
        elif die[x-a] > 1 or die[y+a] > 1:
            continue

        die[x] -= 1
        die[x-a] += 1
        die[y] -= 1
        die[y+a] += 1
    assert(sum(die)==n)
    assert(min(die)>=0)
    assert(max(die)<=2)

    # convert to sorted sequence representation
    A = []
    for i in xrange(n):
        A += [i+1]*die[i]
    return A


rand_type_options = {
    "sequence": rand_die_sequence,
    "sequence_walk": rand_die_sequence_walk,
    "multiset": rand_die_multiset,
    "multiset_walk": rand_die_multiset_walk,
    "max2multiset": rand_die_max2multiset,
    "max2multiset_walk": rand_die_max2multiset_walk,
    }

rand_type_options_string = (
"""<rand_type> options: 
    sequence, sequence_walk, multiset, multiset_walk, 
    max2multiset, max2multiset_walk
"""
)

def select_rand_type(rand_type):
    if rand_type in rand_type_options:
        return rand_type_options[rand_type]
    return None


def distance(A,B):
    '''L_1 distance between A,B

    This assumes sorted sequence representation.
    '''
    diff = 0
    for i in xrange(len(A)):
        diff += abs(A[i] - B[i])
    return diff

def std_distance(A):
    '''L_1 distance between A and standard die

    This assumes sorted sequence representation.
    '''
    diff = 0
    for i in xrange(len(A)):
        diff += abs(i+1 - A[i])
    return diff

def compare(A,B):
    '''calculate over all pairs how many times A wins - B wins

    This is slow, O(n^2).

    Assumes A and B are in sequence representation.
    The sequence do not need to be sorted.
    '''
    a_win=0
    for i in A:
        for j in B:
            if i==j:
                continue
            elif i>j:
                a_win += 1
            else:
                a_win -= 1
    return a_win

def fastdie(A):
    '''Convert from sequence representation to fastdie representation

    This assumes the die only has integer values 1 to n.
    '''
    # for a die, precalculate:
    # fastdie[i] = ( 
    #   count of die entries equal to i+1,
    #   (entries that would lose to i+1)-(entries that would win to i+1) )

    # first count amount of each entry
    n = len(A)
    f = [0]*n
    for x in A:
        f[x-1] += 1

    less = 0
    more = n
    for i in xrange(n):
        c = f[i]
        more -= c
        f[i] = (c,less-more)
        less += c
    return f

def fastdice_compare(Af,Bf):
    a_win = 0
    for i in xrange(len(Af)):
        a_win += Af[i][0]*Bf[i][1]
    return a_win

def beats_count(fdice):
    '''calculates tournament counts, aborting early if tie detected

    return (bool_ties, [ number of wins for each die ] ) 
    if there are ties, aborts early and the beats count is not returned
    '''
    k = len(fdice)
    beats=[0]*k
    for i in xrange(k-1):
        for j in xrange(i+1,k):
            result = fastdice_compare(fdice[i],fdice[j])
            if result==0:
                return (True,None)
            if result>0:
                beats[i] += 1
            else:
                beats[j] += 1
    return (False,beats)

def has_intransitive_sequence(fdice):
    '''try all permutations looking for an intransitive sequence

    This is slow but works for any k
    '''
    k = len(fdice)
    for p in itertools.permutations(range(k)):
        for i in xrange(k-1):
            if fastdice_compare(fdice[p[i]],fdice[p[i+1]])<0:
                break
        else:
            if fastdice_compare(fdice[p[0]],fdice[p[-1]])<0:
                return p
    return None

def sequence_to_multiset(A):
    n = len(A)
    B = [0]*n
    for x in A:
        B[x-1] += 1
    return B

def multiset_to_sequence(A):
    n = len(A)
    B = []
    for i in xrange(n):
        B += [i+1]*A[i]
    return B

def inverse_die(A):
    B = sequence_to_multiset(A)
    B.reverse()
    return multiset_to_sequence(B)


