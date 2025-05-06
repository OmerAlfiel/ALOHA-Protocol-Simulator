# metrics.py
"""
Performance metrics for ALOHA protocols.
"""
import math
from config import OFFERED_LOAD, MODE, FRAME_TIME

def theoretical_throughput(G=None):
    """Calculate theoretical throughput for given offered load G"""
    if G is None:
        G = OFFERED_LOAD
        
    if MODE == 'PURE':
        return G * math.exp(-2 * G)
    else:
        return G * math.exp(-G)

def compute_throughput(success_count, total_time):
    slots = total_time / FRAME_TIME
    raw_throughput = success_count / slots  # Successful transmissions per slot
    return raw_throughput  # or return normalized_throughput

def compute_efficiency(throughput, G=None):
    # Ratio of achieved to maximum theoretical throughput
    max_throughput = 0.5 if MODE == 'SLOTTED' else 0.184  # e^-1/2 for slotted, e^-2/2e for pure
    return throughput / max_throughput

def compute_delay(successful_transmissions, delay_sum):
    # Average delay for successful transmissions
    if successful_transmissions == 0:
        return float('inf')
    return delay_sum / successful_transmissions