from datetime import timedelta
from typing import Optional, List


class Truck:
    """
    Represents a delivery truck with packages, speed, capacity, and routing information
    """

    def __init__(
            self,
            capacity: int = 16,
            speed: float = 18.0,
            packages: List[int] | None = None,
            mileage: float = 0.0,
            address: str = "4001 South 700 East",
            depart_time: Optional[timedelta] | None = None
    ):
        self.capacity = capacity
        self.speed = speed
        self.packages = packages if packages is not None else []
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time # Current simulation clock

    def __str__(self) -> str:
        return (
            f"Truck(capacity={self.capacity}, speed={self.speed} mph, "
            f"mileage={self.mileage:.2f} mi, "
            f"packages={len(self.packages)}, "
            f"depart_time={self.depart_time})"
        )

    def summary(self, truck_id: int) -> str:
        """ Returns a user-friendly one-line summary for UI output."""
        return (
            f"🚚 Truck {truck_id}: "
            f"{len(self.packages)} packages | "
            f"Mileage: {self.mileage:.2f} mi | "
            f"Departed: {self.depart_time}"
        )