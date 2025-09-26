from datetime import timedelta, datetime
from typing import Optional

def parse_deadline(deadline_str: str) -> timedelta:
    """
    Converts a deadline string from the CSV into a timedelta object.
    """

    if deadline_str.upper() == "EOD":
        return timedelta(hours=17) # EOD is defined as 5pm
    else:
        dt = datetime.strptime(deadline_str, "%I:%M %p") # Parse into datetime
        return timedelta(hours=dt.hour, minutes=dt.minute)


class Package:
    """
    Represents a delivery package with all required delivery details.
    """

    def __init__(
            self,
            package_id: int,
            address: str,
            city: str,
            state: str,
            zipcode: str,
            deadline_time: str,
            weight: str,
            status: str,
            departure_time: Optional[timedelta],
            delivery_time: Optional[timedelta]
    ):
        """
        Initializes a package.
        """
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = parse_deadline(deadline_time)
        self.weight = weight
        self.status = status
        self.departure_time = departure_time
        self.delivery_time = delivery_time

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of a package.
        """

        output = [
            f"Package ID: {self.package_id}",
            f"Address: {self.address}, {self.city}, {self.zipcode}",
            f"Deadline: {self.deadline_time}, Weight: {self.weight}",
            f"Status: {self.status} (Departed: {self.departure_time})"
        ]
        if self.delivery_time:
            output.append(f"Delivery Time: {self.delivery_time}")
        return "\n".join(output)

    def update_status(self, convert_timedelta) -> None:
        """
        Update the package's status based on the current time.
        """
        if self.delivery_time <= convert_timedelta:
            self.status = "Delivered"
        elif self.delivery_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"