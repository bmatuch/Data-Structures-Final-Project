#!/usr/bin/env python3

from queue import PriorityQueue # Import PQ class from queue library

def numbers():
	# In this case numbers are inserted, which serve both as the priority number and data
	myPQ = PriorityQueue() # Constructor
	myPQ.put(3) # Use put() to insert
	myPQ.put(10)
	myPQ.put(-1)

	print("The PQ has " + str(myPQ.qsize()) + " elements.") # qsize() returns size of queue

	while not myPQ.empty(): # Boolean. True if PQ is empty (qsize() == 0)
		print(myPQ.get()) # Removes and returns element

def tuples():
	# A better aproach is to insert tuples of the form (priority number, data)
	# In this case the data are strings
	myPQ = PriorityQueue() # Constructor
	myPQ.put((3, "a")) # Use put() to insert
	myPQ.put((1, "This"))
	myPQ.put((4, "PQ"))
	myPQ.put((2, "is"))

	print("The PQ has " + str(myPQ.qsize()) + " elements.") # qsize() returns size of queue

	while not myPQ.empty():
		print(myPQ.get()) # get() removes and returns element

def main():
	print("Numbers:")
	numbers()
	print("---------------")

	print("Tuples:")
	tuples()
	print("---------------")

if __name__ == '__main__':
	main()
