from colorama import Fore, Style


# Update package 9's address at 10:20am
def update_package_9_address(package_hash_table):
    package_9 = package_hash_table.lookup(9)
    package_9.address = "410 S State St"
    package_9.zipcode = "84111"

# Calculates distance between two addresses
def distance_between(x_value, y_value, csv_distance):
    distance = csv_distance[x_value][y_value]
    if distance == '':
        distance = csv_distance[y_value][x_value]
    return float(distance)

# Gets address number from string of address
def extract_address(address, csv_address):
    for row in csv_address:
        if address in row[2]:
            return int(row[0])

# Checks if packages were delivered before their deadline
def check_all_deadlines(package_hash_table):
    all_met = True
    for package_id in range(1, 41):
        package = package_hash_table.lookup(package_id)
        if package.delivery_time > package.deadline_time:
            all_met = False
            print(Fore.RED + Style.BRIGHT + f"❌ Package {package.package_id} missed its deadline! "
                  f"Delivered at {package.delivery_time}, Deadline: {package.deadline_time}")
    if all_met:
        print(Fore.GREEN + Style.BRIGHT + "✅ All package deadlines have been met.")

def truncate(text, max_length):
    """Truncate a string and add ellipsis if too long."""
    return text if len(text) <= max_length else text[:max_length-3] + "..."