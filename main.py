# Student ID: 010659388
import csv
import datetime
import os
from typing import List, Tuple

from common.chaining_hash_table import ChainingHashTable
from common.user_interface import UserInterface
from common.package import Package
from common.truck import Truck
from common.package_utils import extract_address, distance_between

def init_system(data_dir: str = "data") -> Tuple[ChainingHashTable, List[Truck]]:
    """Returns a tuple containing a hash table, and a list of trucks"""
    package_hash_table = ChainingHashTable()
    load_package_data(os.path.join(data_dir, "packages.csv"), package_hash_table)

    # Create truck objects
    trucks = get_truck_definitions()

    return package_hash_table, trucks

def main() -> None:
    # Read the csv files and place them into a list
    with open("data/distances.csv") as csvfile:
        csv_distance = csv.reader(csvfile)
        csv_distance = list(csv_distance)

    with open("data/addresses.csv") as csvfile1:
        csv_address = csv.reader(csvfile1)
        csv_address = list(csv_address)

    package_hash_table, trucks = init_system()
    deliver_all_trucks(trucks, package_hash_table, csv_address, csv_distance)

    # User Interface
    ui = UserInterface(package_hash_table, trucks)
    ui.start()

def deliver_all_trucks(
        trucks: List[Truck],
        package_hash_table: ChainingHashTable,
        csv_address: List[List[str]],
        csv_distance: List[List[str]]
) -> None:
    """Simulate deliveries for all trucks in the proper order."""
    # Deliver trucks 1 and 2 first
    nearest_neighbor(trucks[0], package_hash_table, csv_address, csv_distance)
    nearest_neighbor(trucks[1], package_hash_table, csv_address, csv_distance)

    # Truck 3 departs when first 2 are done, but not before 9:05
    trucks[2].depart_time = max(
        datetime.timedelta(hours=9, minutes=5),
        min(trucks[0].time, trucks[1].time)
    )
    nearest_neighbor(trucks[2], package_hash_table, csv_address, csv_distance)

def get_truck_definitions() -> List[Truck]:
    """
    Returns initialized truck objects with assigned package IDs and departure times
    """
    return [
        Truck(
            packages=[1, 13, 14, 15, 19, 16, 20, 27, 29, 30, 31, 34, 40],
            depart_time=datetime.timedelta(hours=8)
        ),
        Truck(
            packages=[2, 12, 17, 18, 21, 22, 23, 24, 26, 37, 35, 36, 38, 39],
            depart_time=datetime.timedelta(hours=8)
        ),
        Truck(
            packages=[3, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33, 9],
            depart_time=datetime.timedelta(hours=9, minutes=5)
        ),
    ]

# Creates package objects from the csv data, and loads package objects into hash table
def load_package_data(filename: str, package_hash_table: ChainingHashTable):
    """
    Creates package objects from the CSV data, and loads package objects into hash table
    """
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
                package_id,
                package_address,
                package_city,
                package_state,
                package_zip_code,
                package_deadline_time,
                package_weight,
                package_status,
                None,
                None
            )

            package_hash_table.insert(package_id, package)

def nearest_neighbor(
        truck: Truck,
        package_hash_table: ChainingHashTable,
        csv_address: List[List[str]],
        csv_distance: List[List[str]]
) -> None:
    not_delivered: List[Package] = [package_hash_table.lookup(pid) for pid in truck.packages]
    not_delivered = [p for p in not_delivered if p is not None]

    truck.packages.clear()
    truck.time = truck.depart_time

    package_9 = package_hash_table.lookup(9)
    if package_9:
        package_9.available_time = datetime.timedelta(hours=10, minutes=20)

    while not_delivered:
        current_address_index = extract_address(truck.address, csv_address)
        if current_address_index is None:
            raise ValueError(f"Truck address {truck.address} not found in CSV.")

        # Filter packages that are ready to deliver (truck waits if none)
        ready_packages = [p for p in not_delivered if
                          truck.time >= getattr(p, "available_time", datetime.timedelta(hours=8))]
        if not ready_packages:
            # Wait until the earliest package becomes available
            next_available_time = min(getattr(p, "available_time", datetime.timedelta(hours=8)) for p in not_delivered)
            truck.time = next_available_time
            continue
        else:
            # Sort by earliest deadline, then by shortest distance
            ready_packages.sort(
                key=lambda p: (
                    p.deadline_time,
                    distance_between(current_address_index, extract_address(p.address, csv_address), csv_distance)
                )
            )
            next_package = ready_packages[0]

        # Deliver the package
        next_address_dist = distance_between(current_address_index, extract_address(next_package.address, csv_address), csv_distance)
        truck.mileage += next_address_dist
        truck.time += datetime.timedelta(hours=next_address_dist / truck.speed)  # Truck speed 18 mph
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time
        truck.address = next_package.address
        truck.packages.append(next_package.package_id)
        not_delivered.remove(next_package)

if __name__ == "__main__":
    main()