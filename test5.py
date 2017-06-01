'''Sayan_ipitm_test_6 v1.0
Partions a list of transactions according to their sizes.
Generates an IFM with the items and TID(transaction ids) and the rate of occurence.
Checks for identical transactions and if found, then the earliest TID is incremented
and the later one is deleted from the IFM'''
import csv
import bisect
from operator import add
from collections import defaultdict
from itertools import chain, combinations
import time
s=time.time()
transaction=[] #list of all the transactions
print transaction
part=[] #'holds all the partitions according to size
item=[] #'All the items that are available'
items=set()
rules=[]
mat=[] #'The IFM that is generated'
freqSet=defaultdict(int) #A dictionary that holds the support count of frequent patterns
'Takes transacions from the csv and converts them into lists'
def read_t2():
	transaction.append([3,frozenset([2,3,5]),1])
	transaction.append([3,frozenset([2,3,1]),2])
	transaction.append([3,frozenset([2,3,1]),3])
	transaction.append([4,frozenset([1,2,3,5]),4])
	transaction.append([2,frozenset([2,3]),5])
	transaction.append([2,frozenset([2,1]),6])
	transaction.append([3,frozenset([1,2,3]),7])
	transaction.append([4,frozenset([4,2,3,5]),8])
	transaction.append([4,frozenset([1,2,3,4]),9])
	transaction.append([3,frozenset([2,3,5]),10])
	transaction.append([3,frozenset([6,7,8]),11])
	item.append(1)
	item.append(2)
	item.append(3)
	item.append(4)
	item.append(5)
	item.append(6)
	item.append(7)
	item.append(8)
	items.add(frozenset([1]))
	items.add(frozenset([2]))
	items.add(frozenset([3]))
	items.add(frozenset([4]))
	items.add(frozenset([5]))
	items.add(frozenset([6]))
	items.add(frozenset([7]))
	items.add(frozenset([8]))
	print transaction

def transactions():
    count=[]
    tid=1
    with open('T10I4D100K.csv', 'rb') as csvfile:
    	 spamreader = csv.reader(csvfile)
    	 for row in spamreader:
    		for i in row:
				i=int(i)
				items.add(frozenset([i]))
				if i not in item:
					item.append(i)
				count.append(i)
    		transaction.append([len(count),frozenset(count),tid])
    		count =[];tid=tid+1
    transaction.sort()
'Partitions the transactions according to size'
def partition():
	size=[]
	transaction.sort()
	i=0
	while i<len(transaction):
		l=transaction[i][0]
		size.append(l)
		for j in range(i,len(transaction)):
			if transaction[j][0]>transaction[i][0]:
				i=j-1
				break
			else:
				size.append([transaction[j][2],transaction[j][1]])
				if j == len(transaction)-1 :
					i=j
		part.append(size)
		size=[]
		i=i+1
'Generates the IFM'
def gen_matrix():

	extra=[]
	item.sort()
	item.insert(0,'TID')
	#print item
	mat.append(item)
	extra=[0]*len(item)
	for j in range(len(transaction)):
		extra[0]=+transaction[j][2]
		for k in transaction[j][1]:
			m=bin_sort(k)
			extra[m]+=1
		mat.append(extra)
		extra=[]
		extra=[0]*len(item)
	mat[1:] = sorted(mat[1:])
'Deletes the identical entries and increases the first TID'
def ipitm():
    c=0
    for i in range(0,len(part)):
		for j in range(1,len(part[i])-1):
			for x in range(j+1,len(part[i])):
				if part[i][j][1]==part[i][x][1]:
					y = part[i][j][0]
					#print y,part[i][x][0]
					mat[y][1:]=[z+1 if z!=0 else 0 for z in mat[y][1:]]
					mat[part[i][x][0]][1:]=[z-1 if z!=0 else 0 for z in mat[part[i][x][0]][1:]]

def ipistm():
	a=part
	for i in range(0,len(part)-1):
		for j in range(1,len(part[i])):
			for x in range(1,len(part[i+1])):
				if part[i][j][1].issubset(part[i+1][x][1]):
					#print part[i+1][x][1],part[i][j][1]
					#print mat[part[i+1][x][0]],mat[part[i][j][0]]
					mat[part[i+1][x][0]][1:]=map(add,mat[part[i+1][x][0]][1:],mat[part[i][j][0]][1:])
					mat[part[i][j][0]][1:]=[z-z if z!=0 else 0 for z in mat[part[i][j][0]][1:]]
					#print mat[part[i+1][x][0]],mat[part[i][j][0]]
					break
	new_mat = [i for i in mat if set(i[1:]) != set([0])]
	print len(new_mat)
	return new_mat

def min_support(itemlist,transaction2,m_supp):
	s = defaultdict(int)
	itemSet = set()
	t = transaction2[0]
	for i in itemlist:
		j = [a+1 for a,b in enumerate(t[1:]) if b in i]
		for k in transaction2[1:]:
			s[i] += min([k[x] for x in j])
	for i,v in s.items():
		support=float(v)/(len(transaction2)-1)
		if support >= m_supp:
			itemSet.add(i)
			freqSet[i] = support
	return itemSet


def subsets(items):
    """ Returns non empty subsets of items"""
    return chain(*[combinations(items, i + 1) for i, a in enumerate(items)])

def joinSet(itemSet, length):
        """Joins sets to return n-length itemset where n=length"""
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

def run_apriori(minSupport,minConfidence,itemSet,transactionList):
	l=len(transactionList)
	largeSet = dict() # Global dictionary which stores (key=n-itemSets,value=support) which satisfy minSupport
	oneCSet = min_support(itemSet,transactionList,minSupport)
	currentLSet = oneCSet
	k = 2
	i=1
	while(currentLSet != set([])):
		largeSet[k-1] = currentLSet
		currentLSet = joinSet(currentLSet, k)
		currentCSet = min_support(currentLSet,transactionList,minSupport)
		currentLSet = currentCSet
		k = k + 1
	for key, value in largeSet.items()[1:]:
		for item in value:
			_subsets = map(frozenset, [x for x in subsets(item)])
			for element in _subsets:
				remain = item.difference(element)
				if len(remain)> 0:
					confidence = freqSet[item]/freqSet[element]
					if confidence >= minConfidence:
						rules.append([i,element,remain,confidence])
						i+=1


'A binary search function usng the bisect module to find the index number of the item in the item list'
def bin_sort(n):
    i = bisect.bisect_left(item,n,1,len(item))
    if i!=len(item) and item[i]==n:
        return i
    else:
        return -2

def write_csv(data):
    with open('dataset1-using-IPITSM.csv','wb') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":

	minSupport =0.01
	minConfidence = 0.01
	#transactions()
	read_t2()
	partition()
	gen_matrix()
	ipitm()
	n=ipistm()
	run_apriori(minSupport, minConfidence,items,n)
	write_csv(rules)
	print (s-time.time())
