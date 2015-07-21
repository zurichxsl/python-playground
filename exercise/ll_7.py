"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

#1. The person who arrived on Wednesday bought the laptop.
#2. The programmer is not Wilkes.
#3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools, operator
def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    # represent a person (name, career, good)
    sets = set([(Wilkes, Hamming, Minsky, Knuth, Simon)
    for Wilkes, Hamming, Minsky, Knuth, Simon in itertools.permutations([1,2,3,4,5], 5)
    for programmer, writer, manager, designer in itertools.permutations([1,2,3,4,5], 4)
    for laptop, droid, tablet, iphone in itertools.permutations([1,2,3,4,5], 4)
    if laptop is 3 and\
       programmer is not Wilkes and\
       ((programmer is Wilkes and droid is Hamming) or (programmer is Hamming and droid is Wilkes)) and\
       writer is not Minsky and\
       Knuth is not manager and tablet is not manager and\
       Knuth == Simon + 1 and\
       designer is not 4 and\
       tablet is not 5 and\
       designer is not droid and\
       Knuth == manager + 1 and\
       ((laptop is 1 and Wilkes is writer) or (Wilkes is 1 and laptop is writer)) and\
       (iphone is 2 or tablet is 2)])
    possibles = []
    print sets
    for Wilkes, Hamming, Minsky, Knuth, Simon in sets:
        result = {}
        result['Wilkes'] = Wilkes
        result['Hamming'] = Hamming
        result['Minsky'] = Minsky
        result['Knuth'] = Knuth
        result['Simon'] = Simon
        sorted_x = sorted(result.items(), key=operator.itemgetter(1))
        r = []
        for name, v in sorted_x:
            r.append(name)
        print r
        possibles.append(r)
    return possibles





logic_puzzle()




