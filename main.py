# Student ID: 010659388
import csv

from common.package import Package

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