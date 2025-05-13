"""
Performance metrics for ALOHA simulation.
"""
import math
from config import MODE, FRAME_TIME

def theoretical_throughput(G):
    """Calculate theoretical throughput based on protocol mode."""
    if MODE == 'PURE':
        return G * math.exp(-2 * G)
    else:  # SLOTTED mode
        return G * math.exp(-G)

def compute_throughput(success_count, total_time):
    """Compute simulated throughput from successful transmissions."""
    # Number of possible transmission slots in the simulation time
    slot_count = total_time / FRAME_TIME
    
    # Normalized throughput (S): successful transmissions per slot
    return success_count / slot_count

def absolute_throughput(normalized_throughput, offered_load):
    """Convert normalized throughput to absolute frames per second."""
    frame_rate = offered_load / FRAME_TIME  # Total frames per second
    return normalized_throughput * frame_rate
