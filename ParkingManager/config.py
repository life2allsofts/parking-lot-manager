"""
Configuration and global variables for Parking Manager
"""

import tkinter as tk

# Global variables - will be initialized after Tk() is created
command_value = None
num_value = None
ev_value = None
make_value = None
model_value = None
color_value = None
reg_value = None
level_value = None
ev_car_value = None
ev_car2_value = None
slot1_value = None
slot2_value = None
reg1_value = None
slot_value = None
ev_motor_value = None
motor_remove_value = None
tfield = None

def initialize_tk_widgets(root):
    """Initialize all Tkinter variables after root window is created"""
    global command_value, num_value, ev_value, make_value, model_value, color_value
    global reg_value, level_value, ev_car_value, ev_car2_value, slot1_value, slot2_value
    global reg1_value, slot_value, ev_motor_value, motor_remove_value, tfield
    
    # Initialize StringVars
    command_value = tk.StringVar()
    num_value = tk.StringVar()
    ev_value = tk.StringVar()
    make_value = tk.StringVar()
    model_value = tk.StringVar()
    color_value = tk.StringVar()
    reg_value = tk.StringVar()
    level_value = tk.StringVar(value="1")  # Set default value
    slot1_value = tk.StringVar()
    slot2_value = tk.StringVar()
    reg1_value = tk.StringVar()
    slot_value = tk.StringVar()
    
    # Initialize IntVars
    ev_car_value = tk.IntVar()
    ev_car2_value = tk.IntVar()
    ev_motor_value = tk.IntVar()
    motor_remove_value = tk.IntVar()
    
    # Initialize text field
    tfield = tk.Text(root, width=80, height=15, wrap=tk.WORD, font=("Consolas", 10))
    
    return tfield

def get_tk_variables():
    """Return a dictionary of all Tkinter variables"""
    return {
        'command_value': command_value,
        'num_value': num_value,
        'ev_value': ev_value,
        'make_value': make_value,
        'model_value': model_value,
        'color_value': color_value,
        'reg_value': reg_value,
        'level_value': level_value,
        'ev_car_value': ev_car_value,
        'ev_car2_value': ev_car2_value,
        'slot1_value': slot1_value,
        'slot2_value': slot2_value,
        'reg1_value': reg1_value,
        'slot_value': slot_value,
        'ev_motor_value': ev_motor_value,
        'motor_remove_value': motor_remove_value,
        'tfield': tfield
    }

def get_tfield():
    """Get the text field widget - use this in other modules"""
    return tfield