# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!







def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    # Your code here
    text = text.lower()
    length = len(text)
    if length == 0:
        return (0, 0)
    i = 0

    while i >= 0 and i+1 < length and text[i] == text[i+1]:
        i += 1
    if i == length - 1:
        return (0, length)


    matrix = [[i == j and (i, j) or
                i < j and (0, 0) or
               (j+1 == i and text[i] == text[j]) and (j, i) or
               (j+2 == i and text[i] == text[j]) and (j, i) or
               (0, 0)
               for i in range(length)] for j in range(length)]



#    for i in matrix:
#        print i
    #print
    for d in range(2, length):
        for i in range(length-d):
            # evaluate on: text[i:i+diff]
            (x1, y1) = matrix[i][i+d-1]
            (x2, y2) = matrix[i+1][i+d]

            if text[i] == text[i+d] and (i+1, i+d-1) == (x1, y1) ==  (x2, y2) and (y1 - x1 > 0):
                matrix[i][i+d] = (i, i+d)
            else:
                if (y1-x1) > (y2-x2):
                    matrix[i][i+d] = (x1, y1)
                elif (y1-x1) < (y2-x2):
                    matrix[i][i+d] = (x2, y2)

#    print matrix
#        print diff
#        for i in matrix:
#            print i
    start, end = matrix[0][length-1]
    #print text, text[start:end+1]
    #for i in matrix:
    #    print i
    return (start, end+1)


def circle(text):

    length = len(text)
    text = text.lower()

    longest_d = (0, length> 0 and 1 or 0)
    for i in range(len(text)):
        d = 1
        dd = 0
        while i - d >= 0 and i + d < length and text[i-d] == text[i+d]:
            dd = d
            d += 1

        if dd > 0 and longest_d[1] - longest_d[0] < dd*2+1:
            longest_d =(i-dd, i+dd+1)

    for i in range(len(text)-1):
        j = i+1
        if text[i] == text[j]:
            if longest_d[1] - longest_d[0] < 2:
                longest_d =(i, j+1)
            d = 1
            dd = 0
            while i - d >= 0 and i + d < length and text[i-d] == text[i+d]:
                dd = d
                d += 1
            if dd > 0 and longest_d[1] - longest_d[0] < dd*2+2:
                longest_d =(i-dd, i+dd+1)

    #print longest_d, last_matched, i-last_matched, i+last_matched+1, text[(i-last_matched):(i+last_matched+1)]
    print longest_d, text[longest_d[0]:longest_d[1]]
    return longest_d


#longest_subpalindrome_slice('Race carr')

def test():
    L = longest_subpalindrome_slice
    #L = longest
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)

    return 'tests pass'
#    L('xxxxx')

#print test()



"""
 var a = [10,3,5,7,11,2,1,19,4,5,2,9,14,20,3];
var b = [], c = [];
var inc = [];
function max(a) {
    var len = a.length;
    // construct b
    var low, high, mid, i;
    for(i = 0; i < len; i++) {
        low = 0, high = i;
        while(low < high) {
            mid = low + Math.floor((high-low)/2);
            if(inc[mid] < a[i]) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        // till now, i have already find out how many items are smaller than a[i], which is stored at low
        b[i] = low + 1;
        inc[low] = a[i];
        console.log(a[i], 'b['+i+']', b[i], inc);
    }

    console.log('-----------');
    inc = [];
    // construct a
    for(i = len -1; i >=0; i--) {
        low = 0; high = i;
        while(low < high) {
            mid = low + Math.floor((high-low)/2);
            if(inc[mid] < a[i]) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        c[i] = low+1;
        inc[low] = a[i];
        console.log(a[i], 'b['+i+']', c[i], inc);
    }

    var max = 0;
    for(i = 0; i < len; i++) {
        if(b[i]+c[i] > max) {
            max = b[i] + c[i];
        }
    }
    console.log(len+1-max, 'numbers should be erased');

}
//max(a);"""


a = [10,3,5,7,11,2,1,19,4,5,2,9,14,20,3]
def findLongest(list):
    b = []
    for i in range(len(list)):
        j = i
        while j < len(list) and list[j] <= list[i]:
            j += 1
        if j < len(list) and list[j] > list[i]:
            b.append(j)
        else:
            b.append(i)

    print list


    c = []
    for i in range(len(b)):
        c.append(0)
    used_cached = False
    for i in range(len(list)):
        inc = []
        inc.append(list[i])
        next_index = b[i]
        while next_index != b[next_index]:
            if not c[next_index]:
                c[next_index] = 1
                inc.append(list[next_index])
                next_index = b[next_index]
            else:
                #use the cached
                used_cached = True
                break

        if used_cached:
            i = next_index
            while i < len(c):
                if c[i]:
                    inc.append(list[i])
                i += 1
        elif not i == next_index:
            c[next_index] = 1
            inc.append(list[next_index])

        print inc
    print c

findLongest(a)

#
#
#"Select sha256, md5, \
#            '%s' as verdict from sample where sha256 in (%s) and status not in (0,11,21,31,33) \
#            and timestampdiff(minute,create_date,now()) >%s order by malware desc" % (-101, sha256, 180)
#
#
#
#"Select sha256, md5,%s \
#            as verdict from %s where sha256 in (%s) order by malware desc"
#
#SELECT sha256, md5, '-101' as verdict
#FROM sample WHERE status NOT IN (0,11,21,31,33)
#AND timestampdiff(minute,create_date,now()) >180 ORDER BY malware DESC






