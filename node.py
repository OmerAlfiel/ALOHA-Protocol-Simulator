# node.py
"""
Node behavior for ALOHA simulation.
"""
import random
from config import FRAME_TIME

class Node:
    def __init__(self, node_id, arrival_rate):
        self.id = node_id
        self.arrival_rate = arrival_rate  # λ for Poisson arrivals
        self.next_arrival = self._generate_interarrival()
        self.backoff_time = 0
        self.has_packet = False
        self.collision_count = 0  # Initialize collision counter

    def _generate_interarrival(self):
        # Poisson process: interarrival time ~ Exp(λ)
        return random.expovariate(self.arrival_rate)

    def schedule_next(self, current_time):
        # After a packet is sent, schedule next arrival
        self.next_arrival = current_time + self._generate_interarrival()
        self.collision_count = 0  # Reset collision counter after successful transmission

    def ready_to_transmit(self, current_time):
        return current_time >= self.next_arrival and not self.has_packet

    def transmit(self, current_time):
        # Called when node attempts to transmit
        self.has_packet = True
        return self.id

    def handle_collision(self, current_time):
        # Simple backoff: wait random number of slots
        self.collision_count += 1  # Increment collision counter
        backoff_slots = random.randint(1, min(2**self.collision_count, 10))  # Exponential backoff with max
        self.next_arrival = current_time + backoff_slots * FRAME_TIME
        self.has_packet = False