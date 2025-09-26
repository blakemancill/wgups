import datetime

from common.package_utils import update_package_9_address, check_all_deadlines
try:
    from colorama import Fore, Style
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    class Fore:
        RED = GREEN = BLUE = YELLOW = MAGENTA = CYAN = WHITE = BLACK = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""
    print("Note: colorama not available - running without colors")

class UserInterface:
    def __init__(self, package_hash_table, trucks):
        self.package_hash_table = package_hash_table
        self.trucks = trucks

    def start(self):
        print(Fore.BLUE + Style.BRIGHT + "🏫 Western Governors University Parcel Service (WGUPS) 🏫🚚")
        check_all_deadlines(self.package_hash_table)
        print(Fore.GREEN + Style.BRIGHT + f"✅ The mileage for the route is: {sum(truck.mileage for truck in self.trucks)}")

        text = input(Fore.BLUE + Style.BRIGHT + "To start please type the word 'time' (All else will cause the program to quit): ")
        if text != "time":
            print(Fore.RED + Style.BRIGHT + "❌ Entry invalid. Closing program.")
            exit()

        while True:  # main loop
            # Prompt for a valid time
            while True:
                user_time = input(
                    Fore.BLUE + Style.BRIGHT + "Please enter a time to check status of package(s). Format: HH:MM:SS ")
                try:
                    h, m, s = user_time.split(":")
                    convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    break
                except ValueError:
                    print(Fore.RED + Style.BRIGHT + "❌ Invalid time format. Please use HH:MM:SS. Try again.")

            # Update package 9 if past 10:20
            if convert_timedelta >= datetime.timedelta(hours=10, minutes=20):
                update_package_9_address(self.package_hash_table)

            # Display menu, repeat until valid choice
            while True:
                choice = input(Fore.BLUE + Style.BRIGHT +
                               "To view the status of an individual package type 'solo'. "
                               "For all packages grouped by truck type 'trucks'. "
                               "For all packages in one list type 'all'. "
                               "To enter a new time, type 'time'. To quit, type 'quit': "
                               )

                if choice == "solo":
                    self.show_solo_package(convert_timedelta)
                elif choice == "trucks":
                    self.show_packages_by_truck(convert_timedelta)
                elif choice == "all":
                    self.show_all_packages(convert_timedelta)
                elif choice == "time":
                    break  # break menu loop → back to time input
                elif choice == "quit":
                    print(Fore.GREEN + "👋 Goodbye!")
                    return
                else:
                    print(Fore.RED + Style.BRIGHT + "❌ Entry invalid. Please try again.")

    def display_package_options(self, convert_timedelta):
        choice = input(Fore.BLUE + Style.BRIGHT +
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
            print(Fore.RED + Style.BRIGHT + "❌ Entry invalid. Closing program.")

    def show_solo_package(self, convert_timedelta):
        package_id = input(Fore.BLUE + Style.BRIGHT + "Enter the numeric package ID: ")
        try:
            package = self.package_hash_table.lookup(int(package_id))
            package.update_status(convert_timedelta)
            print(Fore.MAGENTA + Style.BRIGHT + f"\n{package}\n")
        except Exception:
            print(Fore.RED + Style.BRIGHT + "❌ Entry invalid. Closing program.")

    def show_packages_by_truck(self, convert_timedelta):
        for idx, truck in enumerate(self.trucks, start=1):
            print(Fore.YELLOW + Style.BRIGHT + f"\n{truck.summary(idx)}")
            print(Fore.CYAN + f"{'ID':<5}{'Address':<25}{'Status':<15}{'Delivery':<10}")
            print("-" * 60)
            for package_id in truck.packages:
                package = self.package_hash_table.lookup(package_id)
                package.update_status(convert_timedelta)
                print(package.short_str(idx))

    def show_all_packages(self, convert_timedelta):
        print(Fore.YELLOW + Style.BRIGHT + "\n📦 All Packages 📦")
        print(Fore.CYAN + f"{'ID':<5}{'Truck':<7}{'Address':<25}{'Status':<15}{'Delivery':<10}")
        print("-" * 70)
        for package_id in range(1, 41):
            package = self.package_hash_table.lookup(package_id)
            package.update_status(convert_timedelta)
            truck_num = next((i + 1 for i, t in enumerate(self.trucks) if package_id in t.packages), "--")
            print(package.short_str(truck_num))