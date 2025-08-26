import csv
import copy
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Vehicle:
    vin: str
    make: str
    model: str
    year: int
    range_miles: int
    top_speed: int
    zero_sixty: float
    mileage: int
    
    @classmethod
    def from_csv_row(cls, row: List[str]) -> 'Vehicle':
        """Create a Vehicle instance from a CSV row with proper type conversion."""
        try:
            return cls(
                vin=row[0].strip(),
                make=row[1].strip(),
                model=row[2].strip(),
                year=int(row[3]),
                range_miles=int(row[4]),
                top_speed=int(row[5]),
                zero_sixty=float(row[6]),
                mileage=int(row[7])
            )
        except (ValueError, IndexError) as e:
            print(f"Error processing row {row}: {e}")
            return None

def load_vehicle_inventory(filename: str) -> List[Vehicle]:
    """Load vehicle inventory from CSV file with error handling."""
    inventory = []
    
    try:
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            # Skip header row
            header = next(csv_reader)
            print(f'Column names: {", ".join(header)}')
            
            for line_count, row in enumerate(csv_reader, start=2):
                if len(row) >= 8:  # Ensure we have enough columns
                    vehicle = Vehicle.from_csv_row(row)
                    if vehicle:
                        inventory.append(vehicle)
                        print(f'Loaded: {vehicle.make} {vehicle.model} ({vehicle.year})')
                else:
                    print(f'Skipping invalid row {line_count}: insufficient data')
                    
        print(f'Successfully loaded {len(inventory)} vehicles from {filename}')
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return inventory

def display_vehicle_details(vehicle: Vehicle):
    """Display formatted vehicle information."""
    print(f"VIN: {vehicle.vin}")
    print(f"Make: {vehicle.make}")
    print(f"Model: {vehicle.model}")
    print(f"Year: {vehicle.year}")
    print(f"Range: {vehicle.range_miles} miles")
    print(f"Top Speed: {vehicle.top_speed} mph")
    print(f"0-60: {vehicle.zero_sixty} seconds")
    print(f"Mileage: {vehicle.mileage:,} miles")
    print("-" * 40)

def main():
    # Load inventory
    inventory = load_vehicle_inventory('car_fleet.csv')
    
    if not inventory:
        print("No vehicles loaded. Please check your CSV file.")
        return
    
    # Display all vehicles
    print("\n=== VEHICLE INVENTORY ===")
    for vehicle in inventory:
        display_vehicle_details(vehicle)
    
    # Example: Find vehicles by make
    print("\n=== VEHICLES BY MAKE ===")
    makes = set(vehicle.make for vehicle in inventory)
    for make in sorted(makes):
        count = len([v for v in inventory if v.make == make])
        print(f"{make}: {count} vehicles")

if __name__ == "__main__":
    main()