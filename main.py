# Student ID: 010659388
import csv
import datetime

from common.ChainingHashTable import ChainingHashTable
from common.package import Package
from common.truck import Truck

# Read the csv files and place them into a list
with open("data/distances.csv") as csvfile:
    csv_distance = csv.reader(csvfile)
    csv_distance = list(csv_distance)

with open("data/addresses.csv") as csvfile1:
    csv_address = csv.reader(csvfile1)
    csv_address = list(csv_address)

with open("data/packages.csv") as csvfile2:
    csv_packages = csv.reader(csvfile2)
    csv_packages = list(csv_packages)

package_hash_table = ChainingHashTable()

# Creates package objects from the csv data, and loads package objects into hash table
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            package_id = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip_code = package[4]
            package_deadline_time = package[5]
            package_weight = package[6]
            package_status = "At Hub"

            package = Package(
                package_id, package_address, package_city, package_state,
                package_zip_code, package_deadline_time, package_weight, package_status
            )

            package_hash_table.insert(package_id, package)

# Calculates distance between two addresses
def distance_between(x_value, y_value):
    distance = csv_distance[x_value][y_value]
    if distance == '':
        distance = csv_distance[y_value][x_value]
    return float(distance)

# Gets address number from string of address
def extract_address(address):
    for row in csv_address:
        if address in row[2]:
            return int(row[0])

# Create truck objects
truck1 = Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))

truck2 = Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

truck3 = Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=9, minutes=5))

# Load packages into hash table
load_package_data("data/packages.csv", package_hash_table)

# Orders packages on a given truck using the nearest neighbor algorithm.
# Calculates the distance a truck drives once the package are sorted
def nearest_neighbor(truck):
    # Place all packages into array of not delivered
    not_delivered = []
    for package_id in truck.packages:
        package = package_hash_table.lookup(package_id)
        not_delivered.append(package)

    # Clear the package list of a given truck so the packages can be placed in optimal order
    truck.packages.clear()

    # Cycle through the list of not_delivered until none remain in the list
    # Adds the nearest package into the truck.packages list one by one
    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        for package in not_delivered:
            if distance_between(extract_address(truck.address), extract_address(package.address)) <= next_address:
                next_address = distance_between(extract_address(truck.address), extract_address(package.address))
                next_package = package
        # Adds next closest package to the truck package list
        truck.packages.append(next_package.ID)
        # Removes the same package from the not_delivered list
        not_delivered.remove(next_package)
        # Takes the mileage driven to this packaged into the truck.mileage attribute
        truck.mileage += next_address
        # Updates truck's current address attribute to the package it drove to
        truck.address = next_package.address
        # Updates the time it took for the truck to drive to the nearest package
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

nearest_neighbor(truck1)
nearest_neighbor(truck2)
truck3.depart_time = min(truck1.time, truck2.time)
nearest_neighbor(truck3)