# Student ID: 010659388
import csv
import datetime

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