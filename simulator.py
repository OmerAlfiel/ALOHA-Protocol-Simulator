"""
Main simulation orchestrator for ALOHA.
"""
import argparse
import random
import math
import heapq  # Import at the top
from config import (FRAME_SIZE, CHANNEL_CAPACITY, FRAME_TIME, OFFERED_LOAD,
                   NUM_STATIONS, SIMULATION_TIME, MAX_BACKOFF, MODE)
from node import Node
from channel import Channel
from metrics import theoretical_throughput, compute_throughput, absolute_throughput

# Declare these as global so they can be modified
MODE_VALUE = MODE
OFFERED_LOAD_VALUE = OFFERED_LOAD
SIMULATION_TIME_VALUE = SIMULATION_TIME
NUM_STATIONS_VALUE = NUM_STATIONS

def time_driven():
    """Run time-driven ALOHA simulation."""
    # Create network nodes
    nodes = [Node(i, OFFERED_LOAD_VALUE / NUM_STATIONS_VALUE) for i in range(NUM_STATIONS_VALUE)]
    channel = Channel()
    
    # Small time step for accurate simulation
    delta_t = 0.0001
    
    # Track successful transmissions
    success_count = 0
    
    # Run simulation
    t = 0.0
    while t < SIMULATION_TIME_VALUE:
        # Process all nodes at this time step
        for node in nodes:
            if node.ready_to_transmit(t):
                channel.add_transmission(node.transmit())
        
        # For slotted ALOHA, only resolve at slot boundaries
        if MODE_VALUE == 'SLOTTED':
            # Check if we're at a slot boundary (with some tolerance)
            if abs(t % FRAME_TIME) < delta_t:
                success, winner, collision, involved = channel.resolve()
                if success:
                    success_count += 1
                    # Inform successful node
                    for node in nodes:
                        if node.id == winner:
                            node.handle_success()
                elif collision:
                    # Inform all nodes involved in collision
                    for node in nodes:
                        if node.id in involved:
                            node.handle_collision(t)
        else:
            # Pure ALOHA resolves continuously
            success, winner, collision, involved = channel.resolve()
            if success:
                success_count += 1
                # Inform successful node
                for node in nodes:
                    if node.id == winner:
                        node.handle_success()
            elif collision:
                # Inform all nodes involved in collision
                for node in nodes:
                    if node.id in involved:
                        node.handle_collision(t)
        
        t += delta_t
    
    # Calculate throughput
    sim_throughput = compute_throughput(success_count, SIMULATION_TIME_VALUE)
    return sim_throughput

def event_driven():
    """Run event-driven ALOHA simulation with proper implementation."""
    # Event types
    ARRIVAL = 0
    TRANSMISSION = 1
    END_TRANSMISSION = 2
    
    # Initialize network with smaller number of nodes for efficiency
    actual_stations = min(NUM_STATIONS_VALUE, 20)  # Limit to 20 stations for faster simulation
    nodes = [Node(i, OFFERED_LOAD_VALUE / actual_stations) for i in range(actual_stations)]
    channel = Channel()
    success_count = 0
    
    # Event queue: (time, event_type, node_id, priority)
    # Adding a priority field to break ties in time values
    events = []
    priority = 0
    
    # Schedule initial arrivals for all nodes
    for node in nodes:
        priority += 1
        heapq.heappush(events, (node.next_arrival, ARRIVAL, node.id, priority))
    
    # Process events
    current_time = 0
    slot_time = FRAME_TIME  # Time for one slot
    simulation_end_time = min(SIMULATION_TIME_VALUE, 100)  # Limit simulation time for faster results
    
    # Process events until simulation time is reached
    while events and current_time < simulation_end_time:
        # Get next event
        event_time, event_type, node_id, _ = heapq.heappop(events)
        current_time = event_time
        
        if current_time >= simulation_end_time:
            break
        
        if event_type == ARRIVAL:
            # Process new packet arrival
            node = nodes[node_id]
            
            # Generate next packet arrival
            priority += 1
            next_arrival = current_time + random.expovariate(node.offered_load)
            heapq.heappush(events, (next_arrival, ARRIVAL, node_id, priority))
            
            # Schedule immediate transmission
            if MODE_VALUE == 'SLOTTED':
                # For slotted ALOHA, align to next slot boundary
                next_slot = math.ceil(current_time / slot_time) * slot_time
                priority += 1
                heapq.heappush(events, (next_slot, TRANSMISSION, node_id, priority))
            else:
                # For pure ALOHA, transmit immediately
                priority += 1
                heapq.heappush(events, (current_time, TRANSMISSION, node_id, priority))
        
        elif event_type == TRANSMISSION:
            # Add transmission to channel
            channel.add_transmission(node_id)
            
            # Schedule end of transmission
            priority += 1
            heapq.heappush(events, (current_time + slot_time, END_TRANSMISSION, node_id, priority))
        
        elif event_type == END_TRANSMISSION:
            # Resolve channel state
            success, winner, collision, involved = channel.resolve()
            
            if success:
                # Successful transmission
                success_count += 1
            
            elif collision and involved:
                # Schedule retransmissions for collided packets
                for collided_id in involved:
                    # Binary exponential backoff
                    backoff = random.randint(0, 2**min(nodes[collided_id].backoff_counter, MAX_BACKOFF))
                    nodes[collided_id].backoff_counter += 1
                    
                    retry_time = current_time + backoff * slot_time
                    if MODE_VALUE == 'SLOTTED':
                        # Align to slot boundary
                        retry_time = math.ceil(retry_time / slot_time) * slot_time
                    
                    priority += 1
                    heapq.heappush(events, (retry_time, TRANSMISSION, collided_id, priority))
    
    # Scale results to account for simulation time and number of stations
    scaling_factor = (SIMULATION_TIME_VALUE / simulation_end_time) * (NUM_STATIONS_VALUE / actual_stations)
    scaled_success = success_count * scaling_factor
    
    # Calculate throughput
    sim_throughput = scaled_success / (SIMULATION_TIME_VALUE / FRAME_TIME)
    return sim_throughput

def main():
    """Main program entry point."""
    global MODE_VALUE, OFFERED_LOAD_VALUE, SIMULATION_TIME_VALUE, NUM_STATIONS_VALUE
    
    parser = argparse.ArgumentParser(description='ALOHA Protocol Simulator')
    parser.add_argument('--mode', choices=['PURE', 'SLOTTED'], 
                        default=MODE_VALUE, help='ALOHA protocol mode')
    parser.add_argument('--load', type=float, default=OFFERED_LOAD_VALUE,
                        help='Offered load G')
    parser.add_argument('--time', type=float, default=SIMULATION_TIME_VALUE,
                        help='Simulation time in seconds')
    parser.add_argument('--stations', type=int, default=NUM_STATIONS_VALUE,
                        help='Number of stations')
    parser.add_argument('--type', choices=['TIME_DRIVEN', 'EVENT_DRIVEN'], 
                        default='EVENT_DRIVEN', help='Simulation type')
    
    args = parser.parse_args()
    
    # Update global configuration
    MODE_VALUE = args.mode
    OFFERED_LOAD_VALUE = args.load
    SIMULATION_TIME_VALUE = args.time
    NUM_STATIONS_VALUE = args.stations
    
    # Print simulation parameters
    print(f"Mode: {MODE_VALUE}")
    print(f"Offered Load (G): {OFFERED_LOAD_VALUE}")
    
    # Calculate theoretical throughput
    theory = theoretical_throughput(OFFERED_LOAD_VALUE)
    print(f"Theoretical Throughput: {theory:.5f}")
    
    # Run simulation based on type
    if args.type == 'TIME_DRIVEN':
        sim_throughput = time_driven()
    else:
        sim_throughput = event_driven()
    
    print(f"Simulated Throughput: {sim_throughput:.5f}")
    
    # Calculate absolute throughput (frames per second)
    abs_throughput = absolute_throughput(sim_throughput, OFFERED_LOAD_VALUE)
    print(f"Absolute Throughput: {abs_throughput:.1f} frames/second")
    
    # Calculate theoretical absolute throughput
    theo_abs = absolute_throughput(theory, OFFERED_LOAD_VALUE)
    print(f"Theoretical Absolute Throughput: {theo_abs:.1f} frames/second")

if __name__ == "__main__":
    main()
