class VehicleFactory:
    """Minimal VehicleFactory to create vehicle records used by ParkingService."""
    def create_vehicle(self, vehicle_type, regnum, make, model, color, is_electric=False):
        # Return a simple dict representing a vehicle; replace with full Vehicle object if available.
        return {
            "type": vehicle_type,
            "regnum": regnum,
            "make": make,
            "model": model,
            "color": color,
            "is_electric": is_electric,
        }

class ParkingService:
    def __init__(self):
        self.levels = {}  # {level: ParkingLot}
        self.vehicle_factory = VehicleFactory()
    
    def create_parking_lot(self, level, regular_spaces, ev_spaces):
        # We'll implement this by extracting from ParkingManager
        pass
    
    def park_vehicle(self, level, vehicle_type, regnum, make, model, color, is_electric=False):
        # Extract parking logic here
        pass
    
    def remove_vehicle(self, level, slot_id, is_ev_slot=False):
        # Extract removal logic
        pass
    
    def get_status(self, level):
        # Extract status logic
        pass