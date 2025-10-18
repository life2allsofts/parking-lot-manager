"""
Parking Lot Manager - Main GUI Application
Phase 2 Refactoring: Beginning God Class separation
"""

import Vehicle
import ElectricVehicle
import sys
import tkinter as tk
from ParkingService import ParkingService, VehicleFactory  # NEW: Import our service layer

# =============================================================================
# GUI SETUP - Tkinter Root Window
# =============================================================================
root = tk.Tk()
root.geometry("650x850")
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
level_remove_value = tk.StringVar()

# =============================================================================
# GUI COMPONENTS - Output text field
# =============================================================================
tfield = tk.Text(root, width=70, height=15)
    
# =============================================================================
# PARKING LOT CLASS - Business Logic (TO BE REFACTORED INTO ParkingService)
# =============================================================================
class ParkingLot:
    def __init__(self):
        # Parking lot capacity tracking
        self.capacity = 0
        self.evCapacity = 0
        self.level = 0
        self.slotid = 0
        self.slotEvId = 0
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        
        # NEW: Initialize ParkingService for business logic delegation
        self.parking_service = ParkingService()

    def createParkingLot(self, capacity, evcapacity, level):
        """Initialize parking lot with specified capacities"""
        self.slots = [-1] * capacity      # Regular slots array (-1 = empty)
        self.evSlots = [-1] * evcapacity  # EV slots array (-1 = empty)
        self.level = level
        self.capacity = capacity
        self.evCapacity = evcapacity
        return self.level

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
        Park a vehicle in the appropriate slot
        Returns slot number if successful, -1 if parking lot is full
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
        """Remove vehicle from specified slot"""
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
        """Display current status of all parked vehicles"""
        output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        tfield.insert(tk.INSERT, output)
        
        # Display regular vehicles
        for i in range(len(self.slots)):
            if self.slots[i] != -1:
                output = str(i+1) + "\t" + str(self.level) + "\t" + str(self.slots[i].regnum) + "\t\t" + str(self.slots[i].color) + "\t\t" + str(self.slots[i].make) + "\t\t" + str(self.slots[i].model) + "\n"                    
                tfield.insert(tk.INSERT, output)
            
        # Display electric vehicles
        output = "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        tfield.insert(tk.INSERT, output)
        for i in range(len(self.evSlots)):
            if self.evSlots[i] != -1:
                output = str(i+1) + "\t" + str(self.level) + "\t" + str(self.evSlots[i].regnum) + "\t\t" + str(self.evSlots[i].color) + "\t\t" + str(self.evSlots[i].make) + "\t\t" + str(self.evSlots[i].model) + "\n"                    
                tfield.insert(tk.INSERT, output)

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
        """Create parking lot (UI handler) - TO BE REFACTORED to use ParkingService"""
        try:
            # NEW: Input validation and error handling
            level = int(level_value.get())
            regular_spaces = int(num_value.get())
            ev_spaces = int(ev_value.get())
            
            # TODO: Replace with ParkingService delegation
            res = self.createParkingLot(regular_spaces, ev_spaces, level)
            
            output = f'Created a parking lot with {regular_spaces} regular slots and {ev_spaces} EV slots on level: {level}\n'
            tfield.insert(tk.INSERT, output)
            
        except ValueError as e:
            # NEW: User-friendly error message instead of crash
            tfield.insert(tk.INSERT, "Error: Please enter valid numbers for all fields\n")

    def parkCar(self):  
        """Park vehicle (UI handler)"""
        res = self.park(reg_value.get(), make_value.get(), model_value.get(), color_value.get(), ev_car_value.get(), ev_motor_value.get())
        if res == -1:
            tfield.insert(tk.INSERT, "Sorry, parking lot is full\n")
        else:
            output = 'Allocated slot number: '+ str(res) + "\n"
            tfield.insert(tk.INSERT, output)

    def removeCar(self):
        """Remove vehicle (UI handler)"""
        status = self.leave(int(slot_value.get()), int(ev_car2_value.get()))
        if status:
            output = 'Slot number ' + str(slot_value.get()) + ' is free\n'
            tfield.insert(tk.INSERT, output)
        else:
            tfield.insert(tk.INSERT, "Unable to remove a car from slot: " + slot_value.get() + "\n")

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
    label_head = tk.Label(root, text='Parking Lot Manager', font='Arial 14 bold')
    label_head.grid(row=0, column=0, padx=10, columnspan=4)

    # Lot Creation Section
    label_head = tk.Label(root, text='Lot Creation', font='Arial 12 bold')
    label_head.grid(row=1, column=0, padx=10, columnspan=4)

    # Regular spaces input
    lbl_num = tk.Label(root, text='Number of Regular Spaces', font='Arial 12')
    lbl_num.grid(row=2, column=0, padx=5)
    num_entry = tk.Entry(root, textvariable=num_value, width=6, font='Arial 12')
    num_entry.grid(row=2, column=1, padx=4, pady=2)

    # EV spaces input
    lbl_ev = tk.Label(root, text='Number of EV Spaces', font='Arial 12')
    lbl_ev.grid(row=2, column=2, padx=5)
    ev_entry = tk.Entry(root, textvariable=ev_value, width=6, font='Arial 12')
    ev_entry.grid(row=2, column=3, padx=4, pady=4)

    # Floor level input
    lbl_level = tk.Label(root, text='Floor Level', font='Arial 12')
    lbl_level.grid(row=3, column=0, padx=5)
    level_entry = tk.Entry(root, textvariable=level_value, width=6, font='Arial 12')
    level_entry.grid(row=3, column=1, padx=4, pady=4)
    level_entry.insert(tk.INSERT, "1")  # Default value

    # Create parking lot button
    parkMakeBtn = tk.Button(root, command=parkinglot.makeLot, text="Create Parking Lot", 
                           font="Arial 12", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5)
    parkMakeBtn.grid(row=4, column=0, padx=4, pady=4)

    # Car Management Section
    label_car = tk.Label(root, text='Car Management', font='Arial 12 bold')
    label_car.grid(row=5, column=0, padx=10, columnspan=4)

    # Vehicle details inputs
    lbl_make = tk.Label(root, text='Make', font='Arial 12')
    lbl_make.grid(row=6, column=0, padx=5)
    make_entry = tk.Entry(root, textvariable=make_value, width=12, font='Arial 12')
    make_entry.grid(row=6, column=1, padx=4, pady=4)

    lbl_model = tk.Label(root, text='Model', font='Arial 12')
    lbl_model.grid(row=6, column=2, padx=5)
    model_entry = tk.Entry(root, textvariable=model_value, width=12, font='Arial 12')
    model_entry.grid(row=6, column=3, padx=4, pady=4)
    
    lbl_color = tk.Label(root, text='Color', font='Arial 12')
    lbl_color.grid(row=7, column=0, padx=5)
    color_entry = tk.Entry(root, textvariable=color_value, width=12, font='Arial 12')
    color_entry.grid(row=7, column=1, padx=4, pady=4)

    lbl_reg = tk.Label(root, text='Registration #', font='Arial 12')
    lbl_reg.grid(row=7, column=2, padx=5)
    reg_entry = tk.Entry(root, textvariable=reg_value, width=12, font='Arial 12')
    reg_entry.grid(row=7, column=3, padx=4, pady=4)

    # Vehicle type checkboxes
    evToggle = tk.Checkbutton(root, text='Electric', variable=ev_car_value, onvalue=1, offvalue=0, font='Arial 12')
    evToggle.grid(column=0, row=8, padx=4, pady=4)

    motorToggle = tk.Checkbutton(root, text='Motorcycle', variable=ev_motor_value, onvalue=1, offvalue=0, font='Arial 12')
    motorToggle.grid(column=1, row=8, padx=4, pady=4)

    # Park car button
    parkBtn = tk.Button(root, command=parkinglot.parkCar, text="Park Car", 
                       font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5)
    parkBtn.grid(column=0, row=9, padx=4, pady=4)

    # Vehicle removal section
    lbl_slot = tk.Label(root, text='Slot #', font='Arial 12')
    lbl_slot.grid(row=10, column=0, padx=5)
    slot_entry = tk.Entry(root, textvariable=slot_value, width=12, font='Arial 12')
    slot_entry.grid(row=10, column=1, padx=4, pady=4)

    evRemoveToggle = tk.Checkbutton(root, text='Remove EV?', variable=ev_car2_value, onvalue=1, offvalue=0, font='Arial 12')
    evRemoveToggle.grid(column=2, row=10, padx=4, pady=4)

    removeBtn = tk.Button(root, command=parkinglot.removeCar, text="Remove Car", 
                         font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5)
    removeBtn.grid(column=0, row=11, padx=4, pady=4)

    # Spacer
    spacer1 = tk.Label(root, text="")
    spacer1.grid(row=12, column=0)

    # Search functionality
    slotRegBtn = tk.Button(root, command=parkinglot.slotNumByReg, text="Get Slot ID by Registration #", 
                          font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5)
    slotRegBtn.grid(column=0, row=13, padx=4, pady=4)
    slot1_entry = tk.Entry(root, textvariable=slot1_value, width=12, font='Arial 12')
    slot1_entry.grid(row=13, column=1, padx=4, pady=4)

    slotColorBtn = tk.Button(root, command=parkinglot.slotNumByColor, text="Get Slot ID by Color", 
                            font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5)
    slotColorBtn.grid(column=2, row=13, padx=4, pady=4)
    slot2_entry = tk.Entry(root, textvariable=slot2_value, width=12, font='Arial 12')
    slot2_entry.grid(row=13, column=3, padx=4, pady=4)
    
    regColorBtn = tk.Button(root, command=parkinglot.regNumByColor, text="Get Registration # by Color", 
                           font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5)
    regColorBtn.grid(column=0, row=14, padx=4, pady=4)
    reg1_entry = tk.Entry(root, textvariable=reg1_value, width=12, font='Arial 12')
    reg1_entry.grid(row=14, column=1, padx=4, pady=4)

    # Status buttons
    chargeStatusBtn = tk.Button(root, command=parkinglot.chargeStatus, text="EV Charge Status", 
                               font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5)
    chargeStatusBtn.grid(column=2, row=14, padx=4, pady=4)

    statusBtn = tk.Button(root, command=parkinglot.status, text="Current Lot Status", 
                         font="Arial 11", bg='PaleGreen1', fg='black', activebackground="PaleGreen3", padx=5, pady=5)
    statusBtn.grid(column=0, row=15, padx=4, pady=4)

    # Output text field
    tfield.grid(column=0, row=16, padx=10, pady=10, columnspan=4)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    main()