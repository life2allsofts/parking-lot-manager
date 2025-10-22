"""
Main Entry Point for Parking Lot Manager
"""

import tkinter as tk
from ParkingLot import ParkingLot
from config import initialize_tk_widgets, get_tk_variables

def main():
    # =========================================================================
    # ROOT WINDOW INITIALIZATION
    # =========================================================================
    
    # Initialize tkinter root window
    root = tk.Tk()
    root.title("Parking Lot Manager")
    
    # Set a reasonable window size that fits most screens
    window_width = 750
    window_height = 800  # Reduced height to fit standard screens
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 4  # Position higher to avoid taskbar
    
    # Set window geometry and make it resizable
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.resizable(True, True)  # Enable both horizontal and vertical resizing
    
    # Set minimum window size to prevent it from becoming too small
    root.minsize(700, 600)

    # =========================================================================
    # GUI LAYOUT - Building the user interface
    # =========================================================================
    
    # Application title
    label_head = tk.Label(root, text='Parking Lot Manager', font='Arial 16 bold', bg='lightblue', fg='darkblue')
    label_head.grid(row=0, column=0, padx=10, pady=10, columnspan=4, sticky='ew')

    # =========================================================================
    # OUTPUT CONSOLE SECTION WITH SCROLLBAR (CREATED FIRST)
    # =========================================================================
    
    # Create the console frame and text widget FIRST before initializing tk widgets
    console_frame = tk.Frame(root, relief='sunken', bd=1)
    console_frame.grid(column=0, row=18, padx=10, pady=10, columnspan=4, sticky='nsew')

    # Create scrollbar for the text widget
    scrollbar = tk.Scrollbar(console_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create text widget with scrollbar functionality
    tfield = tk.Text(console_frame, 
                    height=12,  # Reduced height to fit better
                    width=80, 
                    yscrollcommand=scrollbar.set,
                    font='Arial 10', 
                    wrap=tk.WORD,
                    bg='white', 
                    fg='black',
                    padx=5,
                    pady=5)
    tfield.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure scrollbar to work with text widget
    scrollbar.config(command=tfield.yview)

    # Now initialize Tkinter widgets with the root window
    initialize_tk_widgets(root)
    
    # Get the initialized Tkinter variables
    tk_vars = get_tk_variables()
    
    # IMPORTANT: Replace the tfield in tk_vars with our new scrollable one
    tk_vars['tfield'] = tfield
    
    # Initialize parking lot instance with Tkinter variables
    parkinglot = ParkingLot(tk_vars)

    # =========================================================================
    # LOT CREATION SECTION
    # =========================================================================
    
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

    # =========================================================================
    # CAR MANAGEMENT SECTION - PARK VEHICLE
    # =========================================================================
    
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

    # =========================================================================
    # VEHICLE REMOVAL SECTION
    # =========================================================================
    
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

    # =========================================================================
    # SEARCH AND STATUS SECTION
    # =========================================================================
    
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

    # =========================================================================
    # OUTPUT CONSOLE LABELS AND BUTTONS
    # =========================================================================
    
    # Output text field with Clear Console button
    tfield_label = tk.Label(root, text='Output Console:', font='Arial 11 bold')
    tfield_label.grid(column=0, row=17, padx=10, pady=(10,0), sticky='w')

    # Clear Console button next to the output label
    clearConsoleBtn = tk.Button(root, command=parkinglot.clearConsole, text="🧹 Clear Console", 
                               font="Arial 9", bg='lightgray', fg='black', activebackground="gray", padx=5, pady=2)
    clearConsoleBtn.grid(column=1, row=17, padx=5, pady=(10,0), sticky='w')

    # =========================================================================
    # WINDOW CONFIGURATION AND FINAL SETUP
    # =========================================================================
    
    # Configure grid weights for proper resizing - give weight to the console row
    root.grid_rowconfigure(18, weight=1)  # Console row gets expansion priority
    for col in range(4):
        root.grid_columnconfigure(col, weight=1)  # All columns get some expansion
    
    # Add initial welcome message to the ACTUAL text widget we're using
    tfield.insert(tk.END, "🚗 Welcome to Parking Lot Manager!\n")
    tfield.insert(tk.END, "👉 Start by creating a parking lot with the 'Create Lot' button above.\n\n")
    tfield.see(tk.END)  # Auto-scroll to bottom to show latest messages
    
    # Ensure window is brought to front and focused
    root.lift()
    root.focus_force()
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    main()