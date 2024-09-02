import csv

# Load Train Data
def load_train_data(filename):
    trains = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            train_id = row['Train ID']
            trains[train_id] = {
                'Train Name': row['Train Name'],
                'Source Station': row['Source Station'],
                'Destination Station': row['Destination Station'],
                'Total Seats': int(row['Total Seats']),
                'Available Seats': int(row['Available Seats']),
                'Total Fare': int(row['Total Fare'])
            }
    return trains

# Load Passenger Data
def load_passenger_data(filename):
    passengers = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            print("Column Names:", reader.fieldnames)
            for row in reader:
                passengers.append({
                    'Passenger Name': row.get('Passenger Name', ''),
                    'Train ID': row.get('Train ID', ''),
                    'Number of Tickets': int(row.get('Number of Tickets', 0))
                })
    except Exception as e:
        print(f"Error reading passenger data: {e}")
    return passengers

# Checking Seat Availability
def check_seat_availability(trains, train_id, num_tickets):
    if train_id in trains:
        train = trains[train_id]
        if train['Available Seats'] >= num_tickets:
            return True
    return False

# Updating Seat Availability
def update_seat_availability(trains, train_id, num_tickets):
    if train_id in trains:
        train = trains[train_id]
        train['Available Seats'] -= num_tickets

# Write Updated Train Data to CSV
def write_updated_train_data(filename, trains):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['Train ID', 'Train Name', 'Source Station', 'Destination Station', 'Total Seats', 'Available Seats', 'Total Fare']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for train_id, details in trains.items():
            row = {
                'Train ID': train_id,
                'Train Name': details['Train Name'],
                'Source Station': details['Source Station'],
                'Destination Station': details['Destination Station'],
                'Total Seats': details['Total Seats'],
                'Available Seats': details['Available Seats'],
                'Total Fare': details['Total Fare']
            }
            writer.writerow(row)

# Reports
def generate_reports(trains, passengers):
    # Report 1
    print()
    print("Train Details Report:")
    print("Train ID | Train Name | Source Station | Destination Station | Total Seats | Available Seats")
    for train_id, details in trains.items():
        print(f"{train_id} | {details['Train Name']} | {details['Source Station']} | {details['Destination Station']} | {details['Total Seats']} | {details['Available Seats']}")
    print()
    
    # Report 2
    revenue = {}
    for passenger in passengers:
        train_id = passenger['Train ID']
        num_tickets = passenger['Number of Tickets']
        if train_id in trains:
            fare = trains[train_id]['Total Fare']
            if train_id in revenue:
                revenue[train_id] += num_tickets * fare
            else:
                revenue[train_id] = num_tickets * fare
    
    print("\nRevenue Report:")
    print("Train ID | Total Revenue")
    for train_id, total_revenue in revenue.items():
        print(f"{train_id} | {total_revenue}")

# Main function
def main():
    trains_file = 'trains.csv'
    passengers_file = 'passengers.csv'
    
    trains = load_train_data(trains_file)
    passengers = load_passenger_data(passengers_file)
    
    for passenger in passengers:
        train_id = passenger['Train ID']
        num_tickets = passenger['Number of Tickets']
        if check_seat_availability(trains, train_id, num_tickets):
            update_seat_availability(trains, train_id, num_tickets)
            print(f"Booking confirmed for {passenger['Passenger Name']} on Train {train_id}.")
        else:
            print(f"Insufficient seats for {passenger['Passenger Name']} on Train {train_id}.")
    
    # Write the updated train data back to CSV
    write_updated_train_data(trains_file, trains)
    
    generate_reports(trains, passengers)

if __name__ == "__main__":
    main()
