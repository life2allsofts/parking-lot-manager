"""
Main Entry Point for Parking Lot Manager
"""

import tkinter as tk
from ParkingLot import ParkingLot
from config import initialize_tk_widgets, get_tk_variables

def main():
    # Initialize tkinter root window
    root = tk.Tk()
    root.geometry("750x900")
    root.resizable(0,0)
    root.title("Parking Lot Manager")
    
    # Initialize Tkinter widgets that need the root window FIRST
    initialize_tk_widgets(root)
    
    # Get the initialized Tkinter variables
    tk_vars = get_tk_variables()
    
    # Initialize parking lot instance with Tkinter variables
    parkinglot = ParkingLot(tk_vars)
    
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
    num_entry = tk.Entry(root, textvariable=tk_vars['num_value'], width=8, font='Arial 11')
    num_entry.grid(row=2, column=1, padx=4, pady=2)

    # EV spaces input
    lbl_ev = tk.Label(root, text='Number of EV Spaces', font='Arial 11')
    lbl_ev.grid(row=2, column=2, padx=5, sticky='w')
    ev_entry = tk.Entry(root, textvariable=tk_vars['ev_value'], width=8, font='Arial 11')
    ev_entry.grid(row=2, column=3, padx=4, pady=4)

    # Floor level input
    lbl_level = tk.Label(root, text='Floor Level', font='Arial 11')
    lbl_level.grid(row=3, column=0, padx=5, sticky='w')
    level_entry = tk.Entry(root, textvariable=tk_vars['level_value'], width=8, font='Arial 11')
    level_entry.grid(row=3, column=1, padx=4, pady=4)
    level_entry.insert(tk.INSERT, "")  # Default value

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
    make_entry = tk.Entry(root, textvariable=tk_vars['make_value'], width=12, font='Arial 11')
    make_entry.grid(row=6, column=1, padx=4, pady=4)

    lbl_model = tk.Label(root, text='Model', font='Arial 11')
    lbl_model.grid(row=6, column=2, padx=5, sticky='w')
    model_entry = tk.Entry(root, textvariable=tk_vars['model_value'], width=12, font='Arial 11')
    model_entry.grid(row=6, column=3, padx=4, pady=4)
    
    lbl_color = tk.Label(root, text='Color', font='Arial 11')
    lbl_color.grid(row=7, column=0, padx=5, sticky='w')
    color_entry = tk.Entry(root, textvariable=tk_vars['color_value'], width=12, font='Arial 11')
    color_entry.grid(row=7, column=1, padx=4, pady=4)

    lbl_reg = tk.Label(root, text='Registration #', font='Arial 11')
    lbl_reg.grid(row=7, column=2, padx=5, sticky='w')
    reg_entry = tk.Entry(root, textvariable=tk_vars['reg_value'], width=12, font='Arial 11')
    reg_entry.grid(row=7, column=3, padx=4, pady=4)

    # Vehicle type checkboxes for parking
    evToggle = tk.Checkbutton(root, text='Electric Vehicle', variable=tk_vars['ev_car_value'], onvalue=1, offvalue=0, font='Arial 10')
    evToggle.grid(column=0, row=8, padx=4, pady=4, sticky='w')

    motorToggle = tk.Checkbutton(root, text='Motorcycle', variable=tk_vars['ev_motor_value'], onvalue=1, offvalue=0, font='Arial 10')
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
    slot_entry = tk.Entry(root, textvariable=tk_vars['slot_value'], width=12, font='Arial 11')
    slot_entry.grid(row=11, column=1, padx=4, pady=4)

    # EV checkbox for removal
    evRemoveToggle = tk.Checkbutton(root, text='EV Vehicle', variable=tk_vars['ev_car2_value'], onvalue=1, offvalue=0, font='Arial 10')
    evRemoveToggle.grid(column=2, row=11, padx=4, pady=4, sticky='w')

    # Motorcycle checkbox for removal (Note: This is for display only, removal doesn't need motorcycle type)
    motorRemoveToggle = tk.Checkbutton(root, text='Motorcycle', variable=tk_vars['motor_remove_value'], onvalue=1, offvalue=0, font='Arial 10')
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
    slot1_entry = tk.Entry(root, textvariable=tk_vars['slot1_value'], width=12, font='Arial 10')
    slot1_entry.grid(row=14, column=1, padx=4, pady=4)

    slotColorBtn = tk.Button(root, command=parkinglot.slotNumByColor, text="Get Slots by Color", 
                            font="Arial 10", bg='lightyellow', fg='black', activebackground="yellow", padx=5, pady=3)
    slotColorBtn.grid(column=2, row=14, padx=4, pady=4)
    slot2_entry = tk.Entry(root, textvariable=tk_vars['slot2_value'], width=12, font='Arial 10')
    slot2_entry.grid(row=14, column=3, padx=4, pady=4)
    
    regColorBtn = tk.Button(root, command=parkinglot.regNumByColor, text="Get Registrations by Color", 
                           font="Arial 10", bg='lightyellow', fg='black', activebackground="yellow", padx=5, pady=3)
    regColorBtn.grid(column=0, row=15, padx=4, pady=4)
    reg1_entry = tk.Entry(root, textvariable=tk_vars['reg1_value'], width=12, font='Arial 10')
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

    # Get the text widget and place it at row 18
    tfield = tk_vars['tfield']
    tfield.grid(column=0, row=18, padx=10, pady=10, columnspan=4, sticky='nsew')
    
    # Configure grid weights for proper resizing
    root.grid_rowconfigure(18, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Add initial welcome message
    tfield.insert(tk.END, "🚗 Welcome to Parking Lot Manager!\n")
    tfield.insert(tk.END, "👉 Start by creating a parking lot with the 'Create Lot' button above.\n\n")
    tfield.see(tk.END)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    main()