"""
Parking Lot Manager - Main GUI Application
Phase 2 Refactoring: Beginning God Class separation
"""

import Vehicle
import ElectricVehicle
import sys
import tkinter as tk

# =============================================================================
# PARKING SERVICE CLASSES - Your existing classes with get_status implemented
# =============================================================================

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

# =============================================================================
# GUI SETUP - Tkinter Root Window
# =============================================================================
root = tk.Tk()
root.geometry("750x900")  # Slightly wider to accommodate better layout
root.resizable(0,0)
root.title("Parking Lot Manager")

# =============================================================================
# INPUT VARIABLES - Tkinter StringVars for form data binding
# =============================================================================
command_value = tk.StringVar()
num_value = tk.StringVar()           # Number of regular spaces
ev_value = tk.StringVar()            # Number of EV spaces
make_value = tk.StringVar()          # Vehicle make
model_value = tk.StringVar()         # Vehicle model
color_value = tk.StringVar()         # Vehicle color
reg_value = tk.StringVar()           # Registration number
level_value = tk.StringVar()         # Floor level
ev_car_value = tk.IntVar()           # Electric vehicle checkbox
ev_car2_value = tk.IntVar()          # Remove EV checkbox
slot1_value = tk.StringVar()         # Slot lookup by registration
slot2_value = tk.StringVar()         # Slot lookup by color
reg1_value = tk.StringVar()          # Registration lookup by color
slot_value = tk.StringVar()          # Slot number for removal
ev_motor_value = tk.IntVar()         # Motorcycle checkbox
motor_remove_value = tk.IntVar()     # Motorcycle checkbox for removal

# =============================================================================
# GUI COMPONENTS - Output text field
# =============================================================================
tfield = tk.Text(root, width=80, height=15)
    
# =============================================================================
# PARKING LOT CLASS - Business Logic (TO BE REFACTORED INTO ParkingService)
# =============================================================================
class ParkingLot:
    def __init__(self):
        # Parking lot capacity tracking
        self.capacity = 0
        self.evCapacity = 0
        self.level = 1  # Default to level 1
        self.slotid = 0
        self.slotEvId = 0
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        
        # NEW: Initialize ParkingService for business logic delegation
        self.parking_service = ParkingService()

    def createParkingLot(self, capacity, evcapacity, level):
        """
        Initialize parking lot with specified capacities
        NOW DELEGATES to ParkingService.create_parking_lot()
        """
        try:
            # Delegate to ParkingService
            success = self.parking_service.create_parking_lot(level, capacity, evcapacity)
            
            if success:
                # Update current level
                self.level = level
                self.capacity = capacity
                self.evCapacity = evcapacity
                return self.level
            else:
                raise Exception("ParkingService failed to create parking lot")
                
        except Exception as e:
            # Fallback to original logic if service fails
            print(f"Service error in createParkingLot, using fallback: {e}")
            self.slots = [-1] * capacity
            self.evSlots = [-1] * evcapacity
            self.level = level
            self.capacity = capacity
            self.evCapacity = evcapacity
            return self.level

    def clearInputs(self):
        """Clear all input fields"""
        try:
            num_value.set("")
            ev_value.set("")
            level_value.set("1")  # Reset to default
            make_value.set("")
            model_value.set("")
            color_value.set("")
            reg_value.set("")
            slot_value.set("")
            slot1_value.set("")
            slot2_value.set("")
            reg1_value.set("")
            ev_car_value.set(0)
            ev_car2_value.set(0)
            ev_motor_value.set(0)
            motor_remove_value.set(0)
            
            tfield.insert(tk.INSERT, "📝 Input fields cleared\n")
            
        except Exception as e:
            tfield.insert(tk.INSERT, f"❌ Error clearing inputs: {str(e)}\n")

    def clearConsole(self):
        """Clear only the output console"""
        tfield.delete(1.0, tk.END)
        tfield.insert(tk.INSERT, "🧹 Console cleared\n")

    def getEmptySlot(self):
        """Find first available regular parking slot"""
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                return i
        return -1

    def getEmptyEvSlot(self):
        """Find first available EV parking slot"""
        for i in range(len(self.evSlots)):
            if self.evSlots[i] == -1:
                return i
        return -1

    def getEmptyLevel(self):
        """Check if level is completely empty"""
        if (self.numOfOccupiedEvSlots == 0 and self.numOfOccupiedSlots == 0):
            return self.level
        return -1

    def park(self, regnum, make, model, color, ev, motor):
        """
        Park a vehicle - DELEGATES to ParkingService.park_vehicle()
        Returns slot number if successful, -1 if parking lot is full
        """
        try:
            # Prepare vehicle data for service layer
            vehicle_data = {
                'regnum': regnum,
                'make': make, 
                'model': model,
                'color': color,
                'ev': ev,
                'motor': motor
            }
            
            # Delegate to ParkingService
            result = self.parking_service.park_vehicle(self.level, vehicle_data)
            
            if result['success']:
                return result['slot_id']  # Return the allocated slot number
            else:
                # You could log the error message here if needed
                print(f"ParkingService message: {result['message']}")
                return -1  # Parking lot full or error
                
        except Exception as e:
            # Fallback to original logic if service fails
            print(f"Service error in park(), using fallback: {e}")
            return self._fallback_park(regnum, make, model, color, ev, motor)

    def _fallback_park(self, regnum, make, model, color, ev, motor):
        """
        Fallback parking logic if ParkingService fails
        TODO: Remove this after ParkingService is fully tested and integrated
        """
        if (self.numOfOccupiedEvSlots < self.evCapacity or self.numOfOccupiedSlots < self.capacity):
            slotid = -1
            if (ev == 1):  # Electric vehicle
                if self.numOfOccupiedEvSlots < self.evCapacity:
                    slotid = self.getEmptyEvSlot()
                    if (motor == 1):  # Electric motorcycle
                        self.evSlots[slotid] = ElectricVehicle.ElectricBike(regnum, make, model, color)
                    else:  # Electric car
                        self.evSlots[slotid] = ElectricVehicle.ElectricCar(regnum, make, model, color)
                    self.slotEvId = self.slotEvId + 1
                    self.numOfOccupiedEvSlots = self.numOfOccupiedEvSlots + 1
                    slotid = self.slotEvId
            else:  # Regular vehicle
                if self.numOfOccupiedSlots < self.capacity:
                    slotid = self.getEmptySlot()
                    if (motor == 1):  # Motorcycle
                        self.slots[slotid] = Vehicle.Car(regnum, make, model, color)
                    else:  # Car
                        self.slots[slotid] = Vehicle.Motorcycle(regnum, make, model, color)
                    self.slotid = self.slotid + 1
                    self.numOfOccupiedSlots = self.numOfOccupiedSlots + 1
                    slotid = self.slotid    
            return slotid
        else:
            return -1  # Parking lot full

    def leave(self, slotid, ev):
        """Remove vehicle from specified slot - DELEGATES to ParkingService"""
        try:
            # Delegate to ParkingService
            result = self.parking_service.remove_vehicle(self.level, slotid, ev == 1)
            
            if result['success']:
                return True
            else:
                print(f"Removal failed: {result['message']}")  # Debug log
                return False
                
        except Exception as e:
            print(f"Service removal error, using fallback: {e}")
            return self._fallback_leave(slotid, ev)

    def _fallback_leave(self, slotid, ev):
        """Fallback removal logic if ParkingService fails"""
        if (ev == 1):  # EV slot
            if self.numOfOccupiedEvSlots > 0 and self.evSlots[slotid-1] != -1:
                self.evSlots[slotid-1] = -1
                self.numOfOccupiedEvSlots = self.numOfOccupiedEvSlots - 1
                return True
            else:
                return False
        else:  # Regular slot
            if self.numOfOccupiedSlots > 0 and self.slots[slotid-1] != -1:
                self.slots[slotid-1] = -1
                self.numOfOccupiedSlots = self.numOfOccupiedSlots - 1
                return True
            else:
                return False

    def edit(self, slotid, regnum, make, model, color, ev):
        """Edit vehicle details in specified slot"""
        if (ev == 1):
            self.evSlots[slotid] = ElectricVehicle.ElectricCar(regnum, make, model, color)
            return True
        else:
            self.slots[slotid] = Vehicle.Car(regnum, make, model, color)
            return True
        return False

    def status(self):
        """Display current status of all parked vehicles - UPDATED to use ParkingService"""
        try:
            # Clear the text field first to avoid clutter
            tfield.delete(1.0, tk.END)
            
            # Get status from ParkingService
            status_data = self.parking_service.get_status(self.level)
            
            if not status_data['success']:
                tfield.insert(tk.INSERT, "Error: " + status_data['message'] + "\n")
                return
                
            # Display regular vehicles
            output = "Regular Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
            tfield.insert(tk.INSERT, output)
            
            if status_data['regular_vehicles']:
                for vehicle in status_data['regular_vehicles']:
                    output = f"{vehicle['slot_id']}\t{self.level}\t{vehicle['regnum']}\t\t{vehicle['color']}\t\t{vehicle['make']}\t\t{vehicle['model']}\n"
                    tfield.insert(tk.INSERT, output)
            else:
                tfield.insert(tk.INSERT, "No regular vehicles parked\n")
                
            # Display electric vehicles
            output = "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
            tfield.insert(tk.INSERT, output)
            
            if status_data['ev_vehicles']:
                for vehicle in status_data['ev_vehicles']:
                    output = f"{vehicle['slot_id']}\t{self.level}\t{vehicle['regnum']}\t\t{vehicle['color']}\t\t{vehicle['make']}\t\t{vehicle['model']}\n"
                    tfield.insert(tk.INSERT, output)
            else:
                tfield.insert(tk.INSERT, "No electric vehicles parked\n")
                    
        except Exception as e:
            tfield.insert(tk.INSERT, f"Error displaying status: {str(e)}\n")

    def chargeStatus(self):
        """Display charge levels for all electric vehicles"""
        output = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        tfield.insert(tk.INSERT, output)
        
        for i in range(len(self.evSlots)):
            if self.evSlots[i] != -1:
                output = str(i+1) + "\t" + str(self.level) + "\t" + str(self.evSlots[i].regnum) + "\t\t" + str(self.evSlots[i].charge) + "\n"                    
                tfield.insert(tk.INSERT, output)

    # =============================================================================
    # SEARCH AND QUERY METHODS - Multiple similar methods for different vehicle types
    # TODO: Refactor to reduce code duplication
    # =============================================================================

    def getRegNumFromColor(self, color):
        """Get registration numbers of all vehicles with specified color"""
        regnums = []
        for i in self.slots:
            if i == -1:
                continue
            if i.color == color:
                regnums.append(i.regnum)
        return regnums

    def getSlotNumFromRegNum(self, regnum):
        """Find slot number by registration number"""
        for i in range(len(self.slots)):
            if (self.slots[i] != -1):
                if self.slots[i].regnum == regnum:
                    return i+1
        return -1

    def getSlotNumFromColor(self, color): 
        """Find slot numbers of all vehicles with specified color"""
        slotnums = []
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                continue
            if self.slots[i].color == color:
                slotnums.append(str(i+1))
        return slotnums

    def getSlotNumFromMake(self, make): 
        """Find slot numbers of all vehicles with specified make"""
        slotnums = []
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                continue
            if self.slots[i].make == make:
                slotnums.append(str(i+1))
        return slotnums

    def getSlotNumFromModel(self, model): 
        """Find slot numbers of all vehicles with specified model"""
        slotnums = []
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                continue
            if self.slots[i].model == model:
                slotnums.append(str(i+1))
        return slotnums

    # EV-specific versions of search methods (CODE DUPLICATION - TO BE REFACTORED)
    def getRegNumFromColorEv(self, color):
        regnums = []
        for i in self.evSlots:
            if i == -1:
                continue
            if i.color == color:
                regnums.append(i.regnum)
        return regnums

    def getSlotNumFromRegNumEv(self, regnum):
        for i in range(len(self.evSlots)):
            if (self.evSlots[i] != -1):
                if str(self.evSlots[i].regnum) == str(regnum):
                    return i+1
        return -1

    def getSlotNumFromColorEv(self, color): 
        slotnums = []
        for i in range(len(self.evSlots)):          
            if self.evSlots[i] == -1:
                continue
            if self.evSlots[i].color == color:
                slotnums.append(str(i+1))
        return slotnums

    def getSlotNumFromMakeEv(self, make): 
        slotnums = []
        for i in range(len(self.evSlots)):          
            if self.evSlots[i] == -1:
                continue
            if self.evSlots[i].make == make:
                slotnums.append(str(i+1))
        return slotnums

    def getSlotNumFromModelEv(self, model): 
        slotnums = []
        for i in range(len(self.evSlots)):          
            if self.evSlots[i] == -1:
                continue
            if self.evSlots[i].model == model:
                slotnums.append(str(i+1))
        return slotnums

    # =============================================================================
    # GUI EVENT HANDLERS - Bridge between UI and business logic
    # =============================================================================

    def slotNumByReg(self):
        """Find slot number by registration number (UI handler)"""
        slot_val = slot1_value.get()
        slotnum = self.getSlotNumFromRegNum(slot_val)
        slotnum2 = self.getSlotNumFromRegNumEv(slot_val)
        output = ""
        if slotnum >= 0:
            output = "Identified slot: " + str(slotnum) + "\n"
        elif slotnum2 >= 0:
            output = "Identified slot (EV): " + str(slotnum2) + "\n"
        else:
            output = "Not found\n"
        tfield.insert(tk.INSERT, output)

    def slotNumByColor(self):
        """Find slot numbers by color (UI handler)"""
        slotnums = self.getSlotNumFromColor(slot2_value.get())
        slotnums2 = self.getSlotNumFromColorEv(slot2_value.get())
        output = "Identified slots: " + ', '.join(slotnums) + "\n"
        tfield.insert(tk.INSERT, output)
        output = "Identified slots (EV): " + ', '.join(slotnums2) + "\n"
        tfield.insert(tk.INSERT, output)

    def regNumByColor(self):
        """Find registration numbers by color (UI handler)"""
        regnums = self.getRegNumFromColor(reg1_value.get())
        regnums2 = self.getRegNumFromColorEv(reg1_value.get())
        output = "Registration Numbers: "+ ', '.join(regnums) + "\n"        
        tfield.insert(tk.INSERT, output)
        output = "Registration Numbers (EV): "+ ', '.join(regnums2) + "\n"        
        tfield.insert(tk.INSERT, output)

    def makeLot(self):
        """Create parking lot (UI handler) - NOW DELEGATES to ParkingService"""
        try:
            # Input validation and error handling
            level = int(level_value.get())
            regular_spaces = int(num_value.get())
            ev_spaces = int(ev_value.get())
            
            # Delegate to ParkingService
            res = self.createParkingLot(regular_spaces, ev_spaces, level)
            
            output = f'Created a parking lot with {regular_spaces} regular slots and {ev_spaces} EV slots on level: {level}\n'
            tfield.insert(tk.INSERT, output)
            
        except ValueError as e:
            # User-friendly error message instead of crash
            tfield.insert(tk.INSERT, "Error: Please enter valid numbers for all fields\n")

    def parkCar(self):  
        """Park vehicle (UI handler) - IMPROVED with better messaging"""
        try:
            res = self.park(reg_value.get(), make_value.get(), model_value.get(), color_value.get(), ev_car_value.get(), ev_motor_value.get())
            if res == -1:
                tfield.insert(tk.INSERT, "❌ Sorry, parking lot is full\n")
            else:
                vehicle_type = "EV " if ev_car_value.get() == 1 else ""
                vehicle_type += "Motorcycle" if ev_motor_value.get() == 1 else "Car"
                output = f'✅ {vehicle_type} Parked Successfully. Allocated slot: {res}\n'
                tfield.insert(tk.INSERT, output)
        except Exception as e:
            tfield.insert(tk.INSERT, f"❌ Error parking vehicle: {str(e)}\n")

    def removeCar(self):
        """Remove vehicle (UI handler) - IMPROVED with better messaging"""
        try:
            slot_id = int(slot_value.get())
            is_ev = ev_car2_value.get() == 1
            
            status = self.leave(slot_id, is_ev)
            if status:
                output = f'✅ Vehicle removed from slot {slot_id}\n'
                tfield.insert(tk.INSERT, output)
            else:
                output = f'❌ Unable to remove vehicle from slot {slot_id}. Slot may be empty or invalid.\n'
                tfield.insert(tk.INSERT, output)
        except ValueError:
            tfield.insert(tk.INSERT, "❌ Error: Please enter a valid slot number\n")

# =============================================================================
# MAIN APPLICATION SETUP - GUI Layout and Event Binding
# =============================================================================
def main():
    # Initialize parking lot instance
    parkinglot = ParkingLot()
    
    # =========================================================================
    # GUI LAYOUT - Building the user interface
    # =========================================================================
    
    # Application title
    label_head = tk.Label(root, text='Parking Lot Manager', font='Arial 16 bold', bg='lightblue', fg='darkblue')
    label_head.grid(row=0, column=0, padx=10, pady=10, columnspan=4, sticky='ew')

    # Lot Creation Section
    label_creation = tk.Label(root, text='🅿️ Lot Creation', font='Arial 12 bold', bg='lightyellow')
    label_creation.grid(row=1, column=0, padx=10, columnspan=4, sticky='ew')

    # Regular spaces input
    lbl_num = tk.Label(root, text='Number of Regular Spaces', font='Arial 11')
    lbl_num.grid(row=2, column=0, padx=5, sticky='w')
    num_entry = tk.Entry(root, textvariable=num_value, width=8, font='Arial 11')
    num_entry.grid(row=2, column=1, padx=4, pady=2)

    # EV spaces input
    lbl_ev = tk.Label(root, text='Number of EV Spaces', font='Arial 11')
    lbl_ev.grid(row=2, column=2, padx=5, sticky='w')
    ev_entry = tk.Entry(root, textvariable=ev_value, width=8, font='Arial 11')
    ev_entry.grid(row=2, column=3, padx=4, pady=4)

    # Floor level input
    lbl_level = tk.Label(root, text='Floor Level', font='Arial 11')
    lbl_level.grid(row=3, column=0, padx=5, sticky='w')
    level_entry = tk.Entry(root, textvariable=level_value, width=8, font='Arial 11')
    level_entry.grid(row=3, column=1, padx=4, pady=4)
    level_entry.insert(tk.INSERT, "1")  # Default value

    # Create parking lot button
    parkMakeBtn = tk.Button(root, command=parkinglot.makeLot, text="Create Parking Lot", 
                           font="Arial 11", bg='lightgreen', fg='black', activebackground="green", padx=10, pady=5)
    parkMakeBtn.grid(row=4, column=0, padx=4, pady=4)

    # Clear input fields button
    clearInputsBtn = tk.Button(root, command=parkinglot.clearInputs, text="Clear Inputs", 
                              font="Arial 11", bg='lightyellow', fg='black', activebackground="yellow", padx=10, pady=5)
    clearInputsBtn.grid(row=4, column=1, padx=4, pady=4)

    # Car Management Section
    label_car = tk.Label(root, text='🚗 Park Vehicle', font='Arial 12 bold', bg='lightgreen')
    label_car.grid(row=5, column=0, padx=10, pady=5, columnspan=4, sticky='ew')

    # Vehicle details inputs
    lbl_make = tk.Label(root, text='Make', font='Arial 11')
    lbl_make.grid(row=6, column=0, padx=5, sticky='w')
    make_entry = tk.Entry(root, textvariable=make_value, width=12, font='Arial 11')
    make_entry.grid(row=6, column=1, padx=4, pady=4)

    lbl_model = tk.Label(root, text='Model', font='Arial 11')
    lbl_model.grid(row=6, column=2, padx=5, sticky='w')
    model_entry = tk.Entry(root, textvariable=model_value, width=12, font='Arial 11')
    model_entry.grid(row=6, column=3, padx=4, pady=4)
    
    lbl_color = tk.Label(root, text='Color', font='Arial 11')
    lbl_color.grid(row=7, column=0, padx=5, sticky='w')
    color_entry = tk.Entry(root, textvariable=color_value, width=12, font='Arial 11')
    color_entry.grid(row=7, column=1, padx=4, pady=4)

    lbl_reg = tk.Label(root, text='Registration #', font='Arial 11')
    lbl_reg.grid(row=7, column=2, padx=5, sticky='w')
    reg_entry = tk.Entry(root, textvariable=reg_value, width=12, font='Arial 11')
    reg_entry.grid(row=7, column=3, padx=4, pady=4)

    # Vehicle type checkboxes for parking
    evToggle = tk.Checkbutton(root, text='Electric Vehicle', variable=ev_car_value, onvalue=1, offvalue=0, font='Arial 10')
    evToggle.grid(column=0, row=8, padx=4, pady=4, sticky='w')

    motorToggle = tk.Checkbutton(root, text='Motorcycle', variable=ev_motor_value, onvalue=1, offvalue=0, font='Arial 10')
    motorToggle.grid(column=1, row=8, padx=4, pady=4, sticky='w')

    # Park car button
    parkBtn = tk.Button(root, command=parkinglot.parkCar, text="🚗 Park Vehicle", 
                       font="Arial 11", bg='lightblue', fg='black', activebackground="blue", padx=10, pady=5)
    parkBtn.grid(column=0, row=9, padx=4, pady=4, columnspan=2)

    # Vehicle Removal Section - CLEARLY SEPARATED
    label_remove = tk.Label(root, text='🚪 Remove Vehicle', font='Arial 12 bold', bg='lightcoral')
    label_remove.grid(row=10, column=0, padx=10, pady=5, columnspan=4, sticky='ew')

    lbl_slot = tk.Label(root, text='Slot # to Remove', font='Arial 11')
    lbl_slot.grid(row=11, column=0, padx=5, sticky='w')
    slot_entry = tk.Entry(root, textvariable=slot_value, width=12, font='Arial 11')
    slot_entry.grid(row=11, column=1, padx=4, pady=4)

    # EV checkbox for removal
    evRemoveToggle = tk.Checkbutton(root, text='EV Vehicle', variable=ev_car2_value, onvalue=1, offvalue=0, font='Arial 10')
    evRemoveToggle.grid(column=2, row=11, padx=4, pady=4, sticky='w')

    # Motorcycle checkbox for removal (Note: This is for display only, removal doesn't need motorcycle type)
    motorRemoveToggle = tk.Checkbutton(root, text='Motorcycle', variable=motor_remove_value, onvalue=1, offvalue=0, font='Arial 10')
    motorRemoveToggle.grid(column=3, row=11, padx=4, pady=4, sticky='w')

    removeBtn = tk.Button(root, command=parkinglot.removeCar, text="🚪 Remove Vehicle", 
                         font="Arial 11", bg='lightcoral', fg='black', activebackground="red", padx=10, pady=5)
    removeBtn.grid(column=0, row=12, padx=4, pady=4, columnspan=2)

    # Search and Status Section
    label_search = tk.Label(root, text='🔍 Search & Status', font='Arial 12 bold', bg='lightcyan')
    label_search.grid(row=13, column=0, padx=10, pady=5, columnspan=4, sticky='ew')

    # Search functionality
    slotRegBtn = tk.Button(root, command=parkinglot.slotNumByReg, text="Get Slot by Registration", 
                          font="Arial 10", bg='lightyellow', fg='black', activebackground="yellow", padx=5, pady=3)
    slotRegBtn.grid(column=0, row=14, padx=4, pady=4)
    slot1_entry = tk.Entry(root, textvariable=slot1_value, width=12, font='Arial 10')
    slot1_entry.grid(row=14, column=1, padx=4, pady=4)

    slotColorBtn = tk.Button(root, command=parkinglot.slotNumByColor, text="Get Slots by Color", 
                            font="Arial 10", bg='lightyellow', fg='black', activebackground="yellow", padx=5, pady=3)
    slotColorBtn.grid(column=2, row=14, padx=4, pady=4)
    slot2_entry = tk.Entry(root, textvariable=slot2_value, width=12, font='Arial 10')
    slot2_entry.grid(row=14, column=3, padx=4, pady=4)
    
    regColorBtn = tk.Button(root, command=parkinglot.regNumByColor, text="Get Registrations by Color", 
                           font="Arial 10", bg='lightyellow', fg='black', activebackground="yellow", padx=5, pady=3)
    regColorBtn.grid(column=0, row=15, padx=4, pady=4)
    reg1_entry = tk.Entry(root, textvariable=reg1_value, width=12, font='Arial 10')
    reg1_entry.grid(row=15, column=1, padx=4, pady=4)

    # Status buttons
    chargeStatusBtn = tk.Button(root, command=parkinglot.chargeStatus, text="🔋 EV Charge Status", 
                               font="Arial 10", bg='lightgreen', fg='black', activebackground="green", padx=5, pady=3)
    chargeStatusBtn.grid(column=2, row=15, padx=4, pady=4)

    statusBtn = tk.Button(root, command=parkinglot.status, text="📊 Current Lot Status", 
                         font="Arial 10", bg='PaleGreen1', fg='black', activebackground="PaleGreen3", padx=5, pady=3)
    statusBtn.grid(column=0, row=16, padx=4, pady=4)

    # Output text field with Clear Console button
    tfield_label = tk.Label(root, text='Output Console:', font='Arial 11 bold')
    tfield_label.grid(column=0, row=17, padx=10, pady=(10,0), sticky='w')

    # Clear Console button next to the output label
    clearConsoleBtn = tk.Button(root, command=parkinglot.clearConsole, text="🧹 Clear Console", 
                               font="Arial 9", bg='lightgray', fg='black', activebackground="gray", padx=5, pady=2)
    clearConsoleBtn.grid(column=1, row=17, padx=5, pady=(10,0), sticky='w')

    tfield.grid(column=0, row=18, padx=10, pady=10, columnspan=4, sticky='nsew')
    
    # Configure grid weights for proper resizing
    root.grid_rowconfigure(18, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    main()