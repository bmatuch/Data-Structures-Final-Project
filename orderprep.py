#!/usr/bin/env python3

import requests
import collections
import datetime as dt
from time import sleep
from math import radians, cos, sin, asin, sqrt


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


# CALCULATE ESTIMATED USER TIME TO RESTAURANT
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


# FUNCTION TO NICELY PRINT ORDERS SO IT IS CLEAR HOW THE DATA IS SIMULATED
def print_orders(data):
	print()
	print("NEW ORDERS:")

	for order in data:
		# CALLING HUGH'S FUNCTIONS
		distance = calculate_distance (float(order["Latitude"]), float(order["Longitude"]))
		eta = calculate_time (distance, "walk")  # EVENTUALLY SHOULD BE order["Mode"]
		print(f'Name: {order["Name"]}, Order: {order["Order"]}, Time Estimate: {eta} minutes')

	print()


# PRIORITY QUEUE FUNCTION


# MAIN FUNCTION
def main():
	t = dt.datetime.now()

	counter = 0
	orders = 3

	loop = True

	while loop:
		delta = dt.datetime.now()-t
		if delta.seconds >= 5:
			data = load_restaurant_data()
			print_orders(data)
			t = dt.datetime.now()
			counter += 1
			if counter == orders:
				loop = False
		sleep(1)
		print("...")



# MAIN EXECUTION
if __name__ == '__main__':
    main()
