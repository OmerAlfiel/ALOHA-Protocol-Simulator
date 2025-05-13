"""
Node implementation for ALOHA simulation.
"""
import random
import math
from config import FRAME_TIME, MODE, MAX_BACKOFF

class Node:
    """Represents a network station implementing ALOHA protocol."""
    def __init__(self, node_id, offered_load):
        self.id = node_id
        self.offered_load = offered_load / FRAME_TIME  # Convert to rate per second
        self.backoff_counter = 0
        self.has_packet = False
        self.next_arrival = self._generate_arrival_time(0)
        self.next_transmission = self.next_arrival
    
    def _generate_arrival_time(self, current_time):
        """Generate next packet arrival based on Poisson process."""
        interarrival = random.expovariate(self.offered_load)
        return current_time + interarrival
    
    def ready_to_transmit(self, current_time):
        """Check if node is ready to transmit at current time."""
        # Generate new packet if needed
        if not self.has_packet and current_time >= self.next_arrival:
            self.has_packet = True
            # Schedule next packet arrival
            self.next_arrival = self._generate_arrival_time(current_time)
            
            # Schedule transmission
            if MODE == 'SLOTTED':
                # Align to next slot boundary
                next_slot = math.ceil(current_time / FRAME_TIME) * FRAME_TIME
                self.next_transmission = next_slot
            else:
                # Immediate transmission for pure ALOHA
                self.next_transmission = current_time
        
        # Check if it's time to transmit
        return self.has_packet and current_time >= self.next_transmission
    
    def transmit(self):
        """Transmit a packet."""
        # Packet is now "in the air"
        self.has_packet = False
        return self.id
    
    def handle_collision(self, current_time):
        """Handle collision using binary exponential backoff."""
        # Increment backoff counter with upper limit
        self.backoff_counter = min(self.backoff_counter + 1, MAX_BACKOFF)
        
        # Random backoff slots
        backoff_slots = random.randint(0, 2**self.backoff_counter - 1)
        backoff_time = backoff_slots * FRAME_TIME
        
        # Schedule retransmission
        if MODE == 'SLOTTED':
            # Align to slot boundary after backoff
            next_slot = math.ceil((current_time + backoff_time) / FRAME_TIME) * FRAME_TIME
            self.next_transmission = next_slot
        else:
            # Direct backoff for pure ALOHA
            self.next_transmission = current_time + backoff_time
        
        # Still have the packet
        self.has_packet = True
    
    def handle_success(self):
        """Reset backoff after successful transmission."""
        self.backoff_counter = 0
