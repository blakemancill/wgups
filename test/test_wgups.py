import pytest
import datetime
import sys, os
import csv

from main import (
    extract_address, distance_between,
    load_package_data, nearest_neighbor,
    update_package_9_address, check_all_deadlines,
    init_system
)

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class TestWGUPSConstraints:
    """Test suite for WGUPS package delivery constraints"""

    def load_system(self, data_dir=None):
        """Helper function to load CSVs and initialize system"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = data_dir or os.path.join(base_dir, "data")

        with open(os.path.join(data_dir, "distances.csv")) as f:
            csv_distance = list(csv.reader(f))
        with open(os.path.join(data_dir, "addresses.csv")) as f:
            csv_address = list(csv.reader(f))

        package_hash_table, truck1, truck2, truck3 = init_system(data_dir)
        return package_hash_table, truck1, truck2, truck3, csv_address, csv_distance

    @pytest.fixture
    def wgups_system(self):
        """Fixture to initialize and simulate deliveries for all trucks"""
        package_hash_table, truck1, truck2, truck3, csv_address, csv_distance = self.load_system()

        nearest_neighbor(truck1, package_hash_table, csv_address, csv_distance)
        nearest_neighbor(truck2, package_hash_table, csv_address, csv_distance)

        truck3.depart_time = max(datetime.timedelta(hours=9, minutes=5),
                                 min(truck1.time, truck2.time))
        nearest_neighbor(truck3, package_hash_table, csv_address, csv_distance)

        return package_hash_table, truck1, truck2, truck3, csv_address, csv_distance

    def test_packages_must_be_on_truck2(self, wgups_system):
        _, _, truck2, _, _, _ = wgups_system
        expected_packages = {2, 17, 35, 37}
        assert expected_packages.issubset(set(truck2.packages))

    def test_package_9_address_update_and_timing(self):
        package_hash_table, truck1, truck2, truck3, csv_address, csv_distance = self.load_system()

        # Deliver trucks 1 and 2 before 10:20am
        nearest_neighbor(truck1, package_hash_table, csv_address, csv_distance)
        nearest_neighbor(truck2, package_hash_table, csv_address, csv_distance)

        # Truck 3 departs before 10:20am
        truck3.depart_time = datetime.timedelta(hours=9, minutes=5)
        nearest_neighbor(truck3, package_hash_table, csv_address, csv_distance)

        package_9 = package_hash_table.lookup(9)
        # Before 10:20am, address should be original
        assert package_9.address != "410 S State St"

        # Update package 9 after 10:20am
        update_package_9_address(package_hash_table)
        assert package_9.address == "410 S State St"

    def test_late_arriving_packages_departure_time(self):
        """Test that truck with late packages (6, 25, 28, 32) leaves after 9:05"""
        _, _, _, truck3, _, _ = self.load_system()
        assert truck3.depart_time >= datetime.timedelta(hours=9, minutes=5), \
            "Truck 3 should depart at or after 9:05 AM"

    def test_packages_delivered_together(self):
        """Tests that packages 13, 15, 19 are delivered together on the same truck"""
        _, truck1, truck2, truck3, _, _ = self.load_system()
        package_set = {13, 15, 19}

        trucks = [truck1, truck2, truck3]
        trucks_with_all_packages = [
            truck for truck in trucks if package_set.issubset(set(truck.packages))
        ]

        # There should exist only one truck with all packages
        assert len(trucks_with_all_packages) == 1, "Packages 13, 15, 19 must all be on the same truck"

    def test_all_packages_delivered_before_deadline(self, wgups_system):
        """Tests that all packages meet their deadlines"""
        package_hash_table, _, _, _, _, _ = wgups_system

        for package_id in range(1, 41):
            package = package_hash_table.lookup(package_id)
            assert package.delivery_time is not None, f"Package {package.package_id} was not delivered!"
            assert package.delivery_time <= package.deadline_time, (
                f"Package {package.package_id} missed its deadline! "
                f"Delivered at {package.delivery_time}, Deadline: {package.deadline_time}"
            )