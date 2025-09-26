import datetime

from main import update_package_9_address

class UserInterface:
    def __init__(self, package_hash_table, trucks):
        self.package_hash_table = package_hash_table
        self.trucks = trucks

    def start(self):
        print("Western Governors University Parcel Service (WGUPS)")
        print(f"The mileage for the route is: {sum(truck.mileage for truck in self.trucks)}")

        text = input("To start please type the word 'time' (All else will cause the program to quit): ")
        if text != "time":
            print("Entry invalid. Closing program.")
            exit()

        user_time = input("Please enter a time to check status of package(s). Format: HH:MM:SS ")
        h, m, s = user_time.split(":")
        convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        # Update package 9 if past 10:20
        if convert_timedelta >= datetime.timedelta(hours=10, minutes=20):
            update_package_9_address(self.package_hash_table)

        self.display_package_options(convert_timedelta)

    def display_package_options(self, convert_timedelta):
        choice = input(
            "To view the status of an individual package type 'solo'. "
            "For all packages grouped by truck type 'trucks'. "
            "For all packages in one list type 'all': "
        )

        if choice == "solo":
            self.show_solo_package(convert_timedelta)
        elif choice == "trucks":
            self.show_packages_by_truck(convert_timedelta)
        elif choice == "all":
            self.show_all_packages(convert_timedelta)
        else:
            print("Entry invalid. Closing program.")
            exit()

    def show_solo_package(self, convert_timedelta):
        package_id = input("Enter the numeric package ID: ")
        try:
            package = self.package_hash_table.lookup(int(package_id))
            package.update_status(convert_timedelta)
            print(package)
        except Exception:
            print("Entry invalid. Closing program.")
            exit()

    def show_packages_by_truck(self, convert_timedelta):
        from main import get_truck_definitions  # Avoid circular import
        trucks = get_truck_definitions()
        for idx, truck in enumerate(trucks, start=1):
            print(f"\nTruck {idx}:")
            for pid in truck.packages:
                package = self.package_hash_table.lookup(pid)
                package.update_status(convert_timedelta)
                print(package)

    def show_all_packages(self, convert_timedelta):
        for package_id in range(1, 41):
            package = self.package_hash_table.lookup(package_id)
            package.update_status(convert_timedelta)
            print(package, "\n")
