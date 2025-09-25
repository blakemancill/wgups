class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline_time, weight, status, departure_time, delivery_time):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = departure_time
        self.delivery_time = delivery_time

    def __str__(self):
        output = []
        output.append(f"Package ID: {self.package_id}")
        output.append(f"Address: {self.address}, {self.city}, {self.zipcode}")
        output.append(f"Deadline: {self.deadline_time}, Weight: {self.weight}")
        output.append(f"Status: {self.status} (Departed: {self.departure_time})")
        if self.delivery_time:
            output.append(f"Delivery Time: {self.delivery_time}")
        return "\n".join(output)

    def update_status(self, convert_timedelta):
        if self.delivery_time <= convert_timedelta:
            self.status = "Delivered"
        elif self.delivery_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"