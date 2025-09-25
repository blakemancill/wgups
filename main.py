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

package_hash_table = ChainingHashTable()


def display_packages_by_truck(convert_timedelta):
    trucks = [
        ("Truck 1", [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]),
        ("Truck 2", [3, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]),
        ("Truck 3", [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33])
    ]

    for truck_name, package_ids in trucks:
        print(f"\n{truck_name}:")
        for package_id in package_ids:
            package = package_hash_table.lookup(package_id)
            package.update_status(convert_timedelta)
            print(str(package) + "\n")

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
                package_zip_code, package_deadline_time, package_weight, package_status, None, None
            )

            package_hash_table.insert(package_id, package)

# Checks if packages were delivered before their deadline
def check_all_deadlines():
    all_met = True
    for package_id in range(1, 41):
        package = package_hash_table.lookup(package_id)
        if package.delivery_time > package.deadline_time:
            all_met = False
            print(f"Package {package.package_id} missed its deadline! "
                  f"Delivered at {package.delivery_time}, Deadline: {package.deadline_time}")
    if all_met:
        print("All package deadlines have been met.")

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

# Update package 9's address at 10:20am
def update_package_9_address():
    package_9 = package_hash_table.lookup(9)
    package_9.address = "410 S State St"
    package_9.zipcode = "84111"

# Create truck objects
truck1 = Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))

truck2 = Truck(16, 18, None, [3, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=8))

truck3 = Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))

# Load packages into hash table
load_package_data("data/packages.csv", package_hash_table)

def nearest_neighbor(truck):
    not_delivered = []
    truck.time = truck.depart_time
    for package_id in truck.packages:
        package = package_hash_table.lookup(package_id)
        not_delivered.append(package)

    truck.packages.clear()

    while len(not_delivered) > 0:
        next_package = None
        next_address_dist = float('inf')

        # Prioritize by earliest deadline, then by shortest distance
        # Sort not_delivered by deadline (earliest first), then by distance from current truck location
        current_address_index = extract_address(truck.address)
        not_delivered.sort(key=lambda p: (
            p.deadline_time,  # Primary: earliest deadline first
            distance_between(current_address_index, extract_address(p.address))  # Secondary: shortest distance
        ))

        # Now pick the first eligible package (closest among earliest deadlines)
        for package in not_delivered:
            dist = distance_between(current_address_index, extract_address(package.address))
            next_package = package
            next_address_dist = dist
            break

        # Update truck and package
        truck.packages.append(next_package.package_id)
        not_delivered.remove(next_package)
        truck.mileage += next_address_dist
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_address_dist / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

nearest_neighbor(truck1)
nearest_neighbor(truck2)

# Only two drivers. First back gets next truck
truck3.depart_time = min(truck1.time, truck2.time)

if truck3.depart_time < datetime.timedelta(hours=10, minutes=20):
    truck3.depart_time = datetime.timedelta(hours=10, minutes=20)

nearest_neighbor(truck3)

check_all_deadlines()

if __name__ == "__main__":
    # User Interface
    # Upon running the program, the below message will appear.
    print("Western Governors University Parcel Service (WGUPS)")
    print("The mileage for the route is:")
    print(truck1.mileage + truck2.mileage + truck3.mileage)  # Print total mileage for all trucks
    # The user will be asked to start the process by entering the word "time"
    text = input("To start please type the word 'time' (All else will cause the program to quit).")
    # If the user doesn't type "leave" the program will ask for a specific time in regard to checking packages
    if text == "time":
        try:
            # The user will be asked to enter a specific time
            user_time = input("Please enter a time to check status of package(s). Use the following format, HH:MM:SS")
            (h, m, s) = user_time.split(":")
            convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            # Updates package 9 delivery address
            if convert_timedelta >= datetime.timedelta(hours=10, minutes=20):
                update_package_9_address()

            # The user will be asked if they want to see the status of all packages or only one, as well as trucks
            second_input = input("To view the status of an individual package please type 'solo'. "
                                 "For all packages grouped by truck type 'trucks'. "
                                 "For all packages in one list type 'all'.")

            # If the user enters "solo" the program will ask for one package ID
            if second_input == "solo":
                try:
                    # The user will be asked to input a package ID. Invalid entry will cause the program to quit
                    solo_input = input("Enter the numeric package ID")
                    package = package_hash_table.lookup(int(solo_input))
                    package.update_status(convert_timedelta)
                    print(str(package))
                except ValueError:
                    print("Entry invalid. Closing program.")
                    exit()

            elif second_input == "trucks":
                try:
                    display_packages_by_truck(convert_timedelta)
                except Exception as e:
                    print(f"Error displaying trucks: {e}")
                    exit()

            # If the user types "all" the program will display all package information at once
            elif second_input == "all":
                try:
                    for packageID in range(1, 41):
                        package = package_hash_table.lookup(packageID)
                        package.update_status(convert_timedelta)
                        print(str(package) + "\n")
                except ValueError:
                    print("Entry invalid. Closing program.")
                    exit()
            else:
                exit()
        except ValueError:
            print("Entry invalid. Closing program.")
            exit()
    elif input != "time":
        print("Entry invalid. Closing program.")
        exit()