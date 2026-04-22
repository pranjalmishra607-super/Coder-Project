from collections import deque
from datetime import datetime

class Train:
    def __init__(self, train_id, name, source, destination, seats):
        self.train_id = train_id
        self.name = name
        self.source = source
        self.destination = destination
        self.total_seats = seats
        self.available_seats = seats
        self.reservations = []

class Reservation:
    def __init__(self, reservation_id, train_id, passenger_name, seats_count):
        self.reservation_id = reservation_id
        self.train_id = train_id
        self.passenger_name = passenger_name
        self.seats_count = seats_count
        self.booking_date = datetime.now()

class RailwayReservationSystem:
    def __init__(self):
        self.trains = {}
        self.reservations = {}
        self.reservation_queue = deque()
        self.next_reservation_id = 1000

    def add_train(self, train_id, name, source, destination, seats):
        train = Train(train_id, name, source, destination, seats)
        self.trains[train_id] = train
        print(f"Train {name} added successfully")

    def book_ticket(self, train_id, passenger_name, seats_count):
        if train_id not in self.trains:
            print("Train not found")
            return False
        
        train = self.trains[train_id]
        if train.available_seats >= seats_count:
            train.available_seats -= seats_count
            res_id = self.next_reservation_id
            reservation = Reservation(res_id, train_id, passenger_name, seats_count)
            self.reservations[res_id] = reservation
            train.reservations.append(res_id)
            self.next_reservation_id += 1
            print(f"Booking confirmed! Reservation ID: {res_id}")
            return True
        else:
            print(f"Only {train.available_seats} seats available")
            self.reservation_queue.append((train_id, passenger_name, seats_count))
            print("Added to waitlist")
            return False

    def cancel_reservation(self, reservation_id):
        if reservation_id in self.reservations:
            res = self.reservations[reservation_id]
            train = self.trains[res.train_id]
            train.available_seats += res.seats_count
            train.reservations.remove(reservation_id)
            del self.reservations[reservation_id]
            print("Reservation cancelled successfully")
            return True
        return False

    def view_train_status(self, train_id):
        if train_id in self.trains:
            train = self.trains[train_id]
            print(f"\n{train.name} ({train.train_id})")
            print(f"Route: {train.source} -> {train.destination}")
            print(f"Available Seats: {train.available_seats}/{train.total_seats}")
        else:
            print("Train not found")

    def search_trains(self, source, destination):
        results = [t for t in self.trains.values() 
                   if t.source.lower() == source.lower() and 
                   t.destination.lower() == destination.lower()]
        if results:
            for train in results:
                self.view_train_status(train.train_id)
        else:
            print("No trains found for this route")

# Example Usage
if __name__ == "__main__":
    system = RailwayReservationSystem()
    
    system.add_train(1, "Express 101", "Delhi", "Mumbai", 100)
    system.add_train(2, "Rajdhani", "Delhi", "Bangalore", 80)
    
    system.search_trains("Delhi", "Mumbai")
    system.book_ticket(1, "John Doe", 5)
    system.book_ticket(1, "Jane Smith", 3)
    system.view_train_status(1)
    system.cancel_reservation(1000)