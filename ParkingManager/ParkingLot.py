"""
Parking Lot Class - GUI Integration and Business Logic Delegation
"""

import sys
import os
import tkinter as tk

# Add the parent directory to Python path to find Vehicle and ElectricVehicle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import from parent directory
from models import ElectricVehicle, Vehicle

from ParkingService import ParkingService

class ParkingLot:
    def __init__(self, tk_vars):
        # Parking lot capacity tracking
        self.capacity = 0
        self.evCapacity = 0
        self.level = 1  # Default to level 1
        self.slotid = 0
        self.slotEvId = 0
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        
        # Initialize arrays for slots
        self.slots = []
        self.evSlots = []
        
        # Store Tkinter variables
        self.tk_vars = tk_vars
        self.tfield = tk_vars['tfield']
        
        # Initialize ParkingService for business logic delegation
        self.parking_service = ParkingService()

    # =============================================================================
    # CORE PARKING LOT METHODS
    # =============================================================================
    
    def createParkingLot(self, capacity, evcapacity, level):
        """Initialize parking lot with specified capacities"""
        try:
            # Delegate to ParkingService
            success = self.parking_service.create_parking_lot(level, capacity, evcapacity)
            
            if success:
                # Update current level
                self.level = level
                self.capacity = capacity
                self.evCapacity = evcapacity
                # Initialize local arrays for fallback
                self.slots = [-1] * capacity
                self.evSlots = [-1] * evcapacity
                
                # Show success message in console
                output = f'✅ Created a parking lot with {capacity} regular slots and {evcapacity} EV slots on level: {level}\n'
                self.tfield.insert(tk.END, output)
                self.tfield.see(tk.END)  # Scroll to bottom
                
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
            
            # Show fallback success message
            output = f'✅ Created a parking lot with {capacity} regular slots and {evcapacity} EV slots on level: {level} (Fallback Mode)\n'
            self.tfield.insert(tk.END, output)
            self.tfield.see(tk.END)  # Scroll to bottom
            
            return self.level

    def park(self, regnum, make, model, color, ev, motor):
        """Park a vehicle - DELEGATES to ParkingService.park_vehicle()"""
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
                # Also update local arrays for fallback compatibility
                slot_id = result['slot_id']
                if ev == 1:  # EV vehicle
                    if motor == 1:  # Electric motorcycle
                        vehicle = ElectricVehicle.ElectricBike(regnum, make, model, color)
                        vehicle.motorcycle = True  # Mark as motorcycle
                    else:  # Electric car
                        vehicle = ElectricVehicle.ElectricCar(regnum, make, model, color)
                        vehicle.motorcycle = False
                    self.evSlots[slot_id-1] = vehicle
                    self.numOfOccupiedEvSlots += 1
                else:  # Regular vehicle
                    if motor == 1:  # Motorcycle
                        vehicle = Vehicle.Motorcycle(regnum, make, model, color)
                        vehicle.motorcycle = True  # Mark as motorcycle
                    else:  # Car
                        vehicle = Vehicle.Car(regnum, make, model, color)
                        vehicle.motorcycle = False
                    self.slots[slot_id-1] = vehicle
                    self.numOfOccupiedSlots += 1
                
                return slot_id
            else:
                print(f"ParkingService message: {result['message']}")
                return -1
                
        except Exception as e:
            print(f"Service error in park(), using fallback: {e}")
            return self._fallback_park(regnum, make, model, color, ev, motor)

    def leave(self, slotid, ev):
        """Remove vehicle from specified slot - DELEGATES to ParkingService"""
        try:
            # Delegate to ParkingService
            result = self.parking_service.remove_vehicle(self.level, slotid, ev == 1)
            
            if result['success']:
                # Also update local arrays for fallback compatibility
                if ev == 1:  # EV slot
                    self.evSlots[slotid-1] = -1
                    self.numOfOccupiedEvSlots -= 1
                else:  # Regular slot
                    self.slots[slotid-1] = -1
                    self.numOfOccupiedSlots -= 1
                return True
            else:
                print(f"Removal failed: {result['message']}")
                return False
                
        except Exception as e:
            print(f"Service removal error, using fallback: {e}")
            return self._fallback_leave(slotid, ev)

    # =============================================================================
    # GUI EVENT HANDLERS
    # =============================================================================
    
    def makeLot(self):
        """Create parking lot (UI handler)"""
        try:
            level = int(self.tk_vars['level_value'].get())
            regular_spaces = int(self.tk_vars['num_value'].get())
            ev_spaces = int(self.tk_vars['ev_value'].get())
            
            res = self.createParkingLot(regular_spaces, ev_spaces, level)
            
        except ValueError as e:
            self.tfield.insert(tk.END, "❌ Error: Please enter valid numbers for all fields\n")
            self.tfield.see(tk.END)

    def parkCar(self):  
        """Park vehicle (UI handler)"""
        try:
            res = self.park(
                self.tk_vars['reg_value'].get(), 
                self.tk_vars['make_value'].get(), 
                self.tk_vars['model_value'].get(), 
                self.tk_vars['color_value'].get(), 
                self.tk_vars['ev_car_value'].get(), 
                self.tk_vars['ev_motor_value'].get()
            )
            if res == -1:
                self.tfield.insert(tk.END, "❌ Sorry, parking lot is full\n")
            else:
                vehicle_type = "EV " if self.tk_vars['ev_car_value'].get() == 1 else ""
                if self.tk_vars['ev_motor_value'].get() == 1:
                    vehicle_type += "Motorcycle"
                else:
                    vehicle_type += "Car"
                output = f'✅ {vehicle_type} Parked Successfully. Allocated slot: {res}\n'
                self.tfield.insert(tk.END, output)
            self.tfield.see(tk.END)
        except Exception as e:
            self.tfield.insert(tk.END, f"❌ Error parking vehicle: {str(e)}\n")
            self.tfield.see(tk.END)

    def removeCar(self):
        """Remove vehicle (UI handler)"""
        try:
            slot_id = int(self.tk_vars['slot_value'].get())
            is_ev = self.tk_vars['ev_car2_value'].get() == 1
            
            status = self.leave(slot_id, is_ev)
            if status:
                output = f'✅ Vehicle removed from slot {slot_id}\n'
                self.tfield.insert(tk.END, output)
            else:
                output = f'❌ Unable to remove vehicle from slot {slot_id}. Slot may be empty or invalid.\n'
                self.tfield.insert(tk.END, output)
            self.tfield.see(tk.END)
        except ValueError:
            self.tfield.insert(tk.END, "❌ Error: Please enter a valid slot number\n")
            self.tfield.see(tk.END)

    def status(self):
        """Display current status of all parked vehicles"""
        try:
            self.tfield.delete(1.0, tk.END)
            
            # Display regular vehicles
            output = "🅿️  Regular Vehicles (Cars & Motorcycles)\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\t\tType\n"
            self.tfield.insert(tk.END, output)
            
            regular_vehicles_found = False
            for i in range(len(self.slots)):
                if self.slots[i] != -1:
                    vehicle = self.slots[i]
                    vehicle_type = "Motorcycle" if hasattr(vehicle, 'motorcycle') and vehicle.motorcycle else "Car"
                    output = f"{i+1}\t{self.level}\t{vehicle.regnum}\t\t{vehicle.color}\t\t{vehicle.make}\t\t{vehicle.model}\t\t{vehicle_type}\n"
                    self.tfield.insert(tk.END, output)
                    regular_vehicles_found = True
            
            if not regular_vehicles_found:
                self.tfield.insert(tk.END, "No regular vehicles parked\n")
                
            # Display electric vehicles
            output = "\n⚡ Electric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\t\tType\n"
            self.tfield.insert(tk.END, output)
            
            ev_vehicles_found = False
            for i in range(len(self.evSlots)):
                if self.evSlots[i] != -1:
                    vehicle = self.evSlots[i]
                    vehicle_type = "EV Motorcycle" if hasattr(vehicle, 'motorcycle') and vehicle.motorcycle else "EV Car"
                    output = f"{i+1}\t{self.level}\t{vehicle.regnum}\t\t{vehicle.color}\t\t{vehicle.make}\t\t{vehicle.model}\t\t{vehicle_type}\n"
                    self.tfield.insert(tk.END, output)
                    ev_vehicles_found = True
            
            if not ev_vehicles_found:
                self.tfield.insert(tk.END, "No electric vehicles parked\n")
                    
        except Exception as e:
            self.tfield.insert(tk.END, f"❌ Error displaying status: {str(e)}\n")
        finally:
            self.tfield.see(tk.END)

    def clearInputs(self):
        """Clear all input fields"""
        try:
            self.tk_vars['num_value'].set("")
            self.tk_vars['ev_value'].set("")
            self.tk_vars['level_value'].set("1")
            self.tk_vars['make_value'].set("")
            self.tk_vars['model_value'].set("")
            self.tk_vars['color_value'].set("")
            self.tk_vars['reg_value'].set("")
            self.tk_vars['slot_value'].set("")
            self.tk_vars['slot1_value'].set("")
            self.tk_vars['slot2_value'].set("")
            self.tk_vars['reg1_value'].set("")
            self.tk_vars['ev_car_value'].set(0)
            self.tk_vars['ev_car2_value'].set(0)
            self.tk_vars['ev_motor_value'].set(0)
            self.tk_vars['motor_remove_value'].set(0)
            
            self.tfield.insert(tk.END, "📝 Input fields cleared\n")
            self.tfield.see(tk.END)
            
        except Exception as e:
            self.tfield.insert(tk.END, f"❌ Error clearing inputs: {str(e)}\n")
            self.tfield.see(tk.END)

    def clearConsole(self):
        """Clear only the output console"""
        self.tfield.delete(1.0, tk.END)
        self.tfield.insert(tk.END, "🧹 Console cleared\n")
        self.tfield.see(tk.END)

    def chargeStatus(self):
        """Display charge levels for all electric vehicles"""
        self.tfield.delete(1.0, tk.END)
        output = "⚡ Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        self.tfield.insert(tk.END, output)
        
        for i in range(len(self.evSlots)):
            if self.evSlots[i] != -1:
                output = str(i+1) + "\t" + str(self.level) + "\t" + str(self.evSlots[i].regnum) + "\t\t" + str(self.evSlots[i].charge) + "\n"                    
                self.tfield.insert(tk.END, output)
        self.tfield.see(tk.END)

    # =============================================================================
    # SEARCH AND QUERY METHODS
    # =============================================================================

    def slotNumByReg(self):
        """Find slot number by registration number (UI handler)"""
        slot_val = self.tk_vars['slot1_value'].get()
        slotnum = self.getSlotNumFromRegNum(slot_val)
        slotnum2 = self.getSlotNumFromRegNumEv(slot_val)
        output = ""
        if slotnum >= 0:
            output = "✅ Identified slot: " + str(slotnum) + "\n"
        elif slotnum2 >= 0:
            output = "✅ Identified slot (EV): " + str(slotnum2) + "\n"
        else:
            output = "❌ Not found\n"
        self.tfield.insert(tk.END, output)
        self.tfield.see(tk.END)

    def slotNumByColor(self):
        """Find slot numbers by color (UI handler)"""
        slotnums = self.getSlotNumFromColor(self.tk_vars['slot2_value'].get())
        slotnums2 = self.getSlotNumFromColorEv(self.tk_vars['slot2_value'].get())
        output = "✅ Identified slots: " + ', '.join(slotnums) + "\n"
        self.tfield.insert(tk.END, output)
        output = "✅ Identified slots (EV): " + ', '.join(slotnums2) + "\n"
        self.tfield.insert(tk.END, output)
        self.tfield.see(tk.END)

    def regNumByColor(self):
        """Find registration numbers by color (UI handler)"""
        regnums = self.getRegNumFromColor(self.tk_vars['reg1_value'].get())
        regnums2 = self.getRegNumFromColorEv(self.tk_vars['reg1_value'].get())
        output = "✅ Registration Numbers: "+ ', '.join(regnums) + "\n"        
        self.tfield.insert(tk.END, output)
        output = "✅ Registration Numbers (EV): "+ ', '.join(regnums2) + "\n"        
        self.tfield.insert(tk.END, output)
        self.tfield.see(tk.END)

    # =============================================================================
    # SEARCH METHODS - Multiple similar methods for different vehicle types
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

    # EV-specific versions of search methods
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
    # FALLBACK METHODS (TO BE REMOVED EVENTUALLY)
    # =============================================================================
    
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
                        vehicle = ElectricVehicle.ElectricBike(regnum, make, model, color)
                        vehicle.motorcycle = True
                    else:  # Electric car
                        vehicle = ElectricVehicle.ElectricCar(regnum, make, model, color)
                        vehicle.motorcycle = False
                    self.evSlots[slotid] = vehicle
                    self.slotEvId = self.slotEvId + 1
                    self.numOfOccupiedEvSlots = self.numOfOccupiedEvSlots + 1
                    slotid = self.slotEvId
            else:  # Regular vehicle
                if self.numOfOccupiedSlots < self.capacity:
                    slotid = self.getEmptySlot()
                    if (motor == 1):  # Motorcycle
                        vehicle = Vehicle.Motorcycle(regnum, make, model, color)
                        vehicle.motorcycle = True
                    else:  # Car
                        vehicle = Vehicle.Car(regnum, make, model, color)
                        vehicle.motorcycle = False
                    self.slots[slotid] = vehicle
                    self.slotid = self.slotid + 1
                    self.numOfOccupiedSlots = self.numOfOccupiedSlots + 1
                    slotid = self.slotid    
            return slotid
        else:
            return -1  # Parking lot full

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

    def edit(self, slotid, regnum, make, model, color, ev):
        """Edit vehicle details in specified slot"""
        if (ev == 1):
            self.evSlots[slotid] = ElectricVehicle.ElectricCar(regnum, make, model, color)
            return True
        else:
            self.slots[slotid] = Vehicle.Car(regnum, make, model, color)
            return True
        return False