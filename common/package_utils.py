from colorama import Fore, Style

from common.chaining_hash_table import ChainingHashTable


def update_package_9_address(package_hash_table) -> None:
    """
    Update package #9's address and ZIP code at 10:20am per project requirements
    """
    package_9 = package_hash_table.lookup(9)
    package_9.address = "410 S State St"
    package_9.zipcode = "84111"

def distance_between(x_value: int, y_value: int, csv_distance: list[list[str]]) -> float:
    """
    Gets the distance in miles between two addresses using the distance table.
    """
    distance = csv_distance[x_value][y_value]
    if distance == '':
        distance = csv_distance[y_value][x_value]
    return float(distance)

def extract_address(address: str, csv_address: list[list[str]]) -> int | None:
    """
    Extracts the address index (ID) from the addresses CSV.
    """
    for row in csv_address:
        if address in row[2]:
            return int(row[0])
    return None


def check_all_deadlines(package_hash_table: ChainingHashTable) -> None:
    """
    Verify whether all packages were delivered before their deadlines.

    Prints a green success message if all deadlines were met, or a red warning for each late package.
    """
    all_met = True
    for package_id in range(1, 41):
        package = package_hash_table.lookup(package_id)
        if package.delivery_time > package.deadline_time:
            all_met = False
            print(Fore.RED + Style.BRIGHT + f"❌ Package {package.package_id} missed its deadline! "
                  f"Delivered at {package.delivery_time}, Deadline: {package.deadline_time}")
    if all_met:
        print(Fore.GREEN + Style.BRIGHT + "✅ All package deadlines have been met.")

def truncate(text: str, max_length: int) -> str:
    """Truncate a string to a maximum length, adding ellipsis if needed"""
    return text if len(text) <= max_length else text[:max_length-3] + "..."