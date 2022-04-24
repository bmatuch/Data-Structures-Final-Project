#!/usr/bin/env python3

import requests
import collections
import datetime as dt
from time import sleep, time
from math import radians, cos, sin, asin, sqrt
from queue import PriorityQueue


# DEFINE CONSTANTS
URL = 'https://bmatuch.github.io/data/testdata.json'
RESTAURANT = "Chick-Fil-A Orders"
CHICK_LAT = 41.69843
CHICK_LONG = -86.23531


# LOAD IN RESTAURANT DATA FROM A JSON FILE ON WEB
def load_restaurant_data():
	headers = {'User-Agent': __name__}
	response = requests.get(URL, headers=headers).json() # JSON ALREADY IN DICT FORMAT

	orders = response[RESTAURANT]
	
	return orders


# FUNCTION TO CALCULATE THE DISTANCE FROM RESTAURANT TO USER
def calculate_distance(user_lat, user_long):

	# RESTAURANT + USER COORDINATES CONVERTED TO RADIANS
	r_lat_rad = radians(CHICK_LAT)
	r_long_rad = radians(CHICK_LONG)
	u_lat_rad = radians(user_lat)
	u_long_rad = radians(user_long)

	# CALCULATES THE CHANGE IN LAT + LONG BTWN CUSTOMER + RESTAURANT
	d_lat  = u_lat_rad  - r_lat_rad
	d_long = u_long_rad - r_long_rad

	# HAVERSINE'S FORMULA TO CALCULATE DISTANCE
	a = sin(d_lat / 2)**2 + cos(r_lat_rad) * cos(u_lat_rad) * sin(d_long / 2)**2
	c = 2 * asin(sqrt(a))

	r = 3956 # RADIUS OF THE EARTH IN MILES 

	distance = r*c

	# RETURNS DISTANCE ROUNDED TO 5 DECIMAL PLACES
	return round(distance, 5)


# CALCULATE ESTIMATED USER TIME TO RESTAURANT IN MINUTES
def calculate_time(distance, mode):

	v = 0

	if mode == "walk":
		v = 20
	elif mode == "run":
		v = 10.625
	elif mode == "bike":
		v = 5
	elif mode == "scooter":
		v = 4

	time = v*distance

	print(f'Customer will arrive in {round(time)} minutes via {mode}')

	return round (time, 2)

# Calculate the eta of order. Returns seconds since Unix epoch.
def calculate_eta(order):
	distance = calculate_distance(float(order["Latitude"]), float(order["Longitude"]))
	minutes = calculate_time(distance, "walk") # Change to order["Mode"] later
	seconds = minutes * 60;
	curr_time = time()

	return curr_time + seconds


# FUNCTION TO NICELY PRINT ORDERS SO IT IS CLEAR HOW THE DATA IS SIMULATED
def print_orders(data):
	print()
	print("NEW ORDERS:")

	for order in data:
		# CALLING HUGH'S FUNCTIONS
		distance = calculate_distance (float(order["Latitude"]), float(order["Longitude"]))
		time = calculate_time (distance, "walk")  # EVENTUALLY SHOULD BE order["Mode"]
		print(f'Name: {order["Name"]}, Order: {order["Order"]}, Time Estimate: {time} minutes')

	print()

def print_queue(theQueue):
	for element in theQueue:
		print((epoch_to_hourMinute(element[0]), element[1]))

def printPQ(thePQ):
	print("\nPriority Queue:")
	print_queue(thePQ.queue)
	print("")

def epoch_to_hourMinute(epochTime):
	theTime = dt.datetime.fromtimestamp(epochTime)
	return str(theTime.hour).rjust(2, '0') + ":" + str(theTime.minute).rjust(2, '0')

def add_order_to_PQ(thePQ, order):
	thePQ.put((calculate_eta(order), {"Name": order["Name"], "Order": order["Order"]}))

# MAIN FUNCTION
def main():
	ordersPQ = PriorityQueue(); # Create PQ
	printPQ(ordersPQ)
	t = dt.datetime.now()

	counter = 0
	orders = 3

	loop = True

	while loop:
		delta = dt.datetime.now()-t
		if delta.seconds >= 5:

			data = load_restaurant_data()
			print_orders(data)
			for order in data:
				add_order_to_PQ(ordersPQ, order)
			printPQ(ordersPQ)

			t = dt.datetime.now()
			counter += 1
			if counter == orders:
				loop = False
		sleep(1)
		print("...")



# MAIN EXECUTION
if __name__ == '__main__':
    main()
