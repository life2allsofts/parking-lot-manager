class VehicleFactory:
    """Factory for creating vehicle objects used by ParkingService."""
    
    def create_vehicle(self, vehicle_type, regnum, make, model, color, is_electric=False):
        """
        Create a vehicle object based on type
        TODO: Integrate with actual Vehicle and ElectricVehicle classes later
        """
        # For now, return a dict - we'll integrate with actual classes in Phase 4
        return {
            "type": vehicle_type,
            "regnum": regnum,
            "make": make,
            "model": model,
            "color": color,
            "is_electric": is_electric,
            "charge": 0 if is_electric else None
        }

class ParkingService:
    def __init__(self):
        self.levels = {}  # {level: {'regular_spaces': int, 'ev_spaces': int, 'regular_slots': list, 'ev_slots': list}}
        self.vehicle_factory = VehicleFactory()
    
    def create_parking_lot(self, level, regular_spaces, ev_spaces):
        """Create a parking lot at the specified level with given capacities."""
        self.levels[level] = {
            'regular_spaces': regular_spaces,
            'ev_spaces': ev_spaces,
            'regular_slots': [None] * regular_spaces,  # None = empty
            'ev_slots': [None] * ev_spaces
        }
        return True

    def park_vehicle(self, level, vehicle_data):
        """
        Park a vehicle in the appropriate slot - EXTRACTED FROM ParkingManager.park()
        Returns dict with {'success': bool, 'slot_id': int, 'message': str}
        """
        try:
            # Check if level exists
            if level not in self.levels:
                return {'success': False, 'message': f'Parking lot level {level} does not exist'}
            
            lot_data = self.levels[level]
            regular_slots = lot_data['regular_slots']
            ev_slots = lot_data['ev_slots']
            
            # Extract vehicle data
            regnum = vehicle_data['regnum']
            make = vehicle_data['make']
            model = vehicle_data['model']
            color = vehicle_data['color']
            is_electric = vehicle_data.get('ev', 0) == 1
            is_motorcycle = vehicle_data.get('motor', 0) == 1
            
            # Determine vehicle type and target slots
            if is_electric:
                vehicle_type = "electric_motorcycle" if is_motorcycle else "electric_car"
                slots = ev_slots
                capacity = lot_data['ev_spaces']
            else:
                vehicle_type = "motorcycle" if is_motorcycle else "car" 
                slots = regular_slots
                capacity = lot_data['regular_spaces']
            
            # Find empty slot
            slot_id = -1
            for i in range(len(slots)):
                if slots[i] is None:
                    slot_id = i
                    break
            
            if slot_id == -1:
                return {'success': False, 'message': 'Sorry, parking lot is full'}
            
            # Create and park vehicle using factory
            vehicle = self.vehicle_factory.create_vehicle(vehicle_type, regnum, make, model, color, is_electric)
            slots[slot_id] = vehicle
            
            # Return 1-based slot number for user display (maintaining compatibility)
            return {'success': True, 'slot_id': slot_id + 1, 'message': f'Allocated slot number: {slot_id + 1}'}
            
        except Exception as e:
            return {'success': False, 'message': f'Error parking vehicle: {str(e)}'}

    def remove_vehicle(self, level, slot_id, is_ev_slot=False):
        """
        Remove vehicle from specified slot - EXTRACTED FROM ParkingManager.leave()
        Returns dict with {'success': bool, 'message': str}
        """
        try:
            if level not in self.levels:
                return {'success': False, 'message': f'Parking lot level {level} does not exist'}
            
            lot_data = self.levels[level]
            
            # Convert to 0-based index
            slot_index = slot_id - 1
            
            if is_ev_slot:
                slots = lot_data['ev_slots']
                slot_type = "EV"
            else:
                slots = lot_data['regular_slots']
                slot_type = "regular"
            
            # Check if slot exists and is occupied
            if slot_index < 0 or slot_index >= len(slots):
                return {'success': False, 'message': f'Invalid {slot_type} slot number: {slot_id}'}
            
            if slots[slot_index] is None:
                return {'success': False, 'message': f'{slot_type} slot {slot_id} is already empty'}
            
            # Remove the vehicle
            slots[slot_index] = None
            
            return {'success': True, 'message': f'Vehicle removed from {slot_type} slot {slot_id}'}
            
        except Exception as e:
            return {'success': False, 'message': f'Error removing vehicle: {str(e)}'}

    def get_status(self, level):
        """Get current status of parking lot at specified level - NOW IMPLEMENTED"""
        try:
            if level not in self.levels:
                return {'success': False, 'message': f'Parking lot level {level} does not exist'}
            
            lot_data = self.levels[level]
            regular_vehicles = []
            ev_vehicles = []
            
            # Process regular slots - only include occupied slots
            for i, vehicle in enumerate(lot_data['regular_slots']):
                if vehicle is not None:
                    vehicle_data = vehicle.copy()
                    vehicle_data['slot_id'] = i + 1  # 1-based slot numbering
                    regular_vehicles.append(vehicle_data)
            
            # Process EV slots - only include occupied slots
            for i, vehicle in enumerate(lot_data['ev_slots']):
                if vehicle is not None:
                    vehicle_data = vehicle.copy()
                    vehicle_data['slot_id'] = i + 1  # 1-based slot numbering
                    ev_vehicles.append(vehicle_data)
            
            return {
                'success': True,
                'regular_vehicles': regular_vehicles,
                'ev_vehicles': ev_vehicles,
                'message': f'Status retrieved for level {level}'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting status: {str(e)}'}

    def get_charge_status(self, level):
        """Get charge status for all electric vehicles - NOW IMPLEMENTED"""
        try:
            if level not in self.levels:
                return {'success': False, 'message': f'Parking lot level {level} does not exist'}
            
            lot_data = self.levels[level]
            charge_status = []
            
            # Process EV slots for charge status
            for i, vehicle in enumerate(lot_data['ev_slots']):
                if vehicle is not None and vehicle.get('is_electric', False):
                    charge_info = {
                        'slot_id': i + 1,
                        'regnum': vehicle['regnum'],
                        'charge': vehicle.get('charge', 0)
                    }
                    charge_status.append(charge_info)
            
            return {
                'success': True,
                'charge_status': charge_status,
                'message': f'Charge status retrieved for level {level}'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting charge status: {str(e)}'}