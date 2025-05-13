"""
Configuration parameters for ALOHA simulation.
"""
import math

# System parameters
FRAME_SIZE = 200             # Frame size in bits
CHANNEL_CAPACITY = 200000    # Channel capacity in bits per second (200 kbps)
FRAME_TIME = FRAME_SIZE / CHANNEL_CAPACITY  # Time to transmit one frame (0.001 s)

# Simulation parameters
OFFERED_LOAD = 1.0           # G: average number of transmission attempts per frame time
NUM_STATIONS = 50            # Number of stations in the network
SIMULATION_TIME = 1000.0     # Total simulation time in seconds
MAX_BACKOFF = 15             # Maximum backoff counter value

# Protocol mode: 'PURE' or 'SLOTTED'
MODE = 'PURE'             # ALOHA protocol mode
