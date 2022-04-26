#!/usr/bin/env python3

import requests
import datetime as dt
import random

from time import sleep, time
from math import radians, cos, sin, asin, sqrt
from queue import PriorityQueue


# DEFINE CONSTANTS
RESTAURANT = "Chick-Fil-A Orders"
CHICK_LAT = 41.69843
CHICK_LONG = -86.23531

# DATA TO PULL FROM
ORDERS = ["8 Nuggets", "12 Nuggets", "Frosted Lemonade", "Spicy Sandwich", "Market Salad", "Chicken Sandwich", "Grilled Chicken", "Spicy Deluxe", "Vanilla Shake"]

# THESSE LOCATIONS INCLUDE DUNCAN HALL, MCGLINN HALL, WALSH HALL, DUNNE HALL, HESBURGH LIBRARY, LAFORTUNE STUDENT CENTER, + DUNCAN STUDENT CENTER
LOCATIONS = [(41.69799, -86.24334),(41.69802, -86.24237),(41.70100, -86.23998),(41.70450, -86.23296),(41.70237, -86.23416),(41.69827, -86.23525),(41.70191, -86.23765)]
MODES = ["Walk", "Run", "Bike", "Scooter"]

# RANDOMLY GENERATE CUSTOMER DATA
def load_restaurant_data(num_customers, TOTAL_ORDERS):

	new_customers = []
	
	for i in range(num_customers):
				
		customer = {"Name": "", "Order": "", "Latitude": 0.0, "Longitude": 0.0, "Mode": ""}
		customer["Name"] = f'Customer {TOTAL_ORDERS}'
		
		customer["Order"] = ORDERS[random.randint(0, len(ORDERS)-1)]
		
		customer_loc = LOCATIONS[random.randint(0, len(LOCATIONS)-1)]
		
		customer["Latitude"] = customer_loc[0]
		customer["Longitude"] = customer_loc[1]
		
		customer["Mode"] = MODES[random.randint(0, len(MODES)-1)] 
		
		new_customers.append(customer)

		TOTAL_ORDERS += 1

	return new_customers


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

	if mode == "Walk":
		v = 20
	elif mode == "Run":
		v = 10.625
	elif mode == "Bike":
		v = 5
	elif mode == "Scooter":
		v = 4

	time = v*distance
	return round (time)



# FUNCTION TO NICELY PRINT ORDERS SO IT IS CLEAR HOW THE DATA IS SIMULATED
def print_orders(order):

	# CALLING FUNCTIONS TO CALC ETA
	distance = calculate_distance (float(order["Latitude"]), float(order["Longitude"]))
	time = calculate_time (distance, order["Mode"]) 

	# PRINTING EACH CUSTOMER'S ORDER + INFO
	print(f'{order["Name"]}\t\tETA: {time} minutes\t\tOrder: {order["Order"]}\t\tMode of Transportation: {order["Mode"]}')

	return time


# PRINT THE PRIORITY QUEUE
def print_list(nonPQ, processing_time):
	print('\033[1m' + "\nORDER QUEUE:" + '\033[0m')
	new_list = []

	for x in nonPQ:
		print(f'{x[1][0]}\t\tETA: {x[0]} minutes\t\tOrder: {x[1][1]}\t\tMode of Transportation: {x[1][2]}')
		x[0] -= processing_time;
		new_list.append(x)

	print("")

	return new_list


# ADDS ORDER TO THE LIST
def add_order_to_list(nonPQ, order, time):
	nonPQ.append([time, [order["Name"], order["Order"], order["Mode"]]])


# MAIN FUNCTION
def main():
	
	# CREATE LIST TO DEMONSTRATE REGULAR ORDER PROCESSING
	nonPQ = []
	t = dt.datetime.now()
	completed_orders = []
 
	counter = 0
	orders = 5
	workers = 5
	overload = False

	TOTAL_ORDERS = 1

	# INITIAL ASSUMPTION IS 5 WORKERS ARE WORKING; 10 ORDERS PROCESSED EVERY 3 MINUTES
	processing_time = 3
	processing_orders = 8

	loop = True
	while loop:
		delta = dt.datetime.now()-t
		if delta.seconds >= 3:

			
			print(f'\nThere are currently {workers} employees working.')
			print(f'For this simulation, {processing_orders} orders are completed every {processing_time} minutes.\n')

			if (counter != 0):

				if (processing_orders > len(nonPQ)):
					old_processing_orders = processing_orders
					processing_orders = len(nonPQ)
					overload = True

				for x in range(processing_orders):
					completed_orders.append(nonPQ.pop(0))

				if (overload == True):
					processing_orders = old_processing_orders
					overload = False

				print('\033[1m' + "\nNEWLY COMPLETED ORDERS:" + '\033[0m')
				for x in completed_orders:
					print(f'{x[1][0]}\t\tETA: {x[0]} minutes\t\tOrder: {x[1][1]}\t\tMode of Transportation: {x[1][2]}')

				# COMPLETED_ORDERS IS RESET SO THAT THE NEWLY COMPLETED ORDERS CAN BE SHOWN FOR CLARITY
				completed_orders = []

			new_customers = random.randint(5, 15)  # RANDOMLY GENERATES NEW NUMBER OF ORDERS
			data = load_restaurant_data(new_customers, TOTAL_ORDERS)
			TOTAL_ORDERS += new_customers

			print('\033[1m' + "\nNEW ORDERS:" + '\033[0m')
			for order in data:
				time = print_orders(order)
				add_order_to_list(nonPQ, order, time)

			nonPQ  = print_list(nonPQ, processing_time)	


			t = dt.datetime.now()
			counter += 1

		sleep(1)
		print("...")



# MAIN EXECUTION
if __name__ == '__main__':
    main()
