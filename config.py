# config.py
"""
Simulation configuration for ALOHA protocols.
"""
import math

# Simulation parameters
NUM_NODES = 50               # Number of nodes in the network
FRAME_TIME = 1.0             # Time to transmit one frame (arbitrary units)
TOTAL_TIME = 100000.0           # Total simulation time or number of slots
OFFERED_LOAD = 0.5           # G: average number of transmission attempts per frame time
BACKOFF_MAX = 5              # Max backoff window in slot units

# Protocol mode: 'PURE' or 'SLOTTED'
MODE = 'SLOTTED'                # Switch to 'SLOTTED' for Slotted ALOHA

# Time-driven vs Event-driven
SIMULATION_TYPE = 'TIME_DRIVEN'  # or 'EVENT_DRIVEN'
