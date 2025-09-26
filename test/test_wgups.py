import pytest
import datetime
import sys, os

from main import (
    extract_address, distance_between,
    load_package_data, nearest_neighbor,
    update_package_9_address, check_all_deadlines,
    init_system
)

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class TestWGUPSConstraints:
    """Test suite for WGUPS package delivery constraints"""

    @pytest.fixture
    def wgups_system(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base_dir, "data")

        # Load the CSVs
        import csv
        with open(os.path.join(data_dir, "distances.csv")) as f:
            csv_distance = list(csv.reader(f))
        with open(os.path.join(data_dir, "addresses.csv")) as f:
            csv_address = list(csv.reader(f))

        package_hash_table, truck1, truck2, truck3 = init_system(data_dir)

        nearest_neighbor(truck1, package_hash_table, csv_address, csv_distance)
        nearest_neighbor(truck2, package_hash_table, csv_address, csv_distance)
        truck3.depart_time = max(datetime.timedelta(hours=9, minutes=5),
                                 min(truck1.time, truck2.time))
        nearest_neighbor(truck3, package_hash_table, csv_address, csv_distance)

        return package_hash_table, truck1, truck2, truck3

    def test_packages_must_be_on_truck2(self, wgups_system):
        """Test that packages 2, 17, 35, 37 are on truck 2"""
        _, _, truck2, _ = wgups_system
        expected_packages = {2, 17, 35, 37}
        assert expected_packages.issubset(set(truck2.packages))