#!/usr/bin/env python3

import os
import sys
from math import radians, cos, sin, asin, sqrt

def calculate_distance(user_lat, user_long):
	
	# chick-fil-a coordinates
	restaurant_lat = 41.69843
	restaurant_long = -86.23531

	print(f'Restaurant coordinates: \t{restaurant_lat} {restaurant_long}')

	# restaurant and user coordinates converted to radians
	r_lat_rad = radians(restaurant_lat)
	r_long_rad = radians(restaurant_long)
	u_lat_rad = radians(user_lat)
	u_long_rad = radians(user_long)

	# change in lat & long
	d_lat  = u_lat_rad  - r_lat_rad
	d_long = u_long_rad - r_long_rad
	
	# Haversine's formula
	a = sin(d_lat / 2)**2 + cos(r_lat_rad) * cos(u_lat_rad) * sin(d_long / 2)**2

	c = 2 * asin(sqrt(a))

	# radius of earth in miles
	r = 3956 
	
	distance = r*c

	print(f'Customer is {round(distance,3)} miles from the restaurant')

	return round(distance,3)

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


def main():
	
	# default latitude & longitude
	latitude = 41.69915
	longitude = -86.23875

	# default mode (walk)
	mode = "walk"
	
	arguments = sys.argv[1:]

	for argument in arguments:
		if "." in argument:
			if float(argument) > 0:
				latitude = float(argument)
			elif float(argument) < 0:
				longitude = float(argument)

		else:
			mode = argument.lower()
	
	print(f'Customer coordinates: \t\t{round(latitude,5)} {round(longitude,5)}')

	distance = calculate_distance(latitude, longitude)
	eta = calculate_time(distance, mode)

# Main Execution
if __name__ == '__main__':
	main()


