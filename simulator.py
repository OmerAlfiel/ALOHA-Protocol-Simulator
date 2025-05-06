# simulator.py
"""
Main simulation orchestrator for ALOHA.
"""
import heapq
import argparse
from config import NUM_NODES, TOTAL_TIME, FRAME_TIME, SIMULATION_TYPE, MODE, OFFERED_LOAD
from node import Node
from channel import Channel
from metrics import compute_throughput, theoretical_throughput

def time_driven():
    nodes = [Node(i, OFFERED_LOAD) for i in range(NUM_NODES)]
    channel = Channel()
    success = 0

    t = 0.0
    while t < TOTAL_TIME:
        # Schedule arrivals and transmissions
        for node in nodes:
            if node.ready_to_transmit(t):
                channel.add_transmission(node.transmit(t))
        
        # Resolve channel state at frame boundaries
        if MODE == 'SLOTTED' or t % FRAME_TIME == 0:
            s, winner, coll, involved_nodes = channel.resolve()
            if s:
                success += 1
                # Schedule next packet for successful node
                for node in nodes:
                    if node.id == winner:
                        node.schedule_next(t)
                        break
            elif coll:
                # Handle collision for all involved nodes
                for node in nodes:
                    if node.id in involved_nodes:
                        node.handle_collision(t)
        
        t += FRAME_TIME

    throughput = compute_throughput(success, TOTAL_TIME)
    theoretical = theoretical_throughput()
    
    print(f"Mode: {MODE}")
    print(f"Offered Load (G): {OFFERED_LOAD}")
    print(f"Theoretical Throughput: {theoretical:.5f}")
    print(f"Simulated Throughput: {throughput:.5f}")
    
    return throughput

def event_driven():
    event_queue = []  # Priority queue of events
    nodes = [Node(i, OFFERED_LOAD) for i in range(NUM_NODES)]
    channel = Channel()
    success = 0
    
    # Initialize event queue with first arrival for each node
    for node in nodes:
        heapq.heappush(event_queue, (node.next_arrival, node.id, "ARRIVE"))
    
    # Process events until simulation time
    current_time = 0
    active_transmissions = set()  # Set of currently active transmissions
    
    while event_queue and current_time < TOTAL_TIME:
        time, node_id, event_type = heapq.heappop(event_queue)
        current_time = time
        
        # Handle different event types
        if event_type == "ARRIVE":
            # Process arrival event
            node = nodes[node_id]
            
            # If in SLOTTED mode, align to next slot boundary
            if MODE == 'SLOTTED':
                slot_boundary = (current_time // FRAME_TIME + 1) * FRAME_TIME
                heapq.heappush(event_queue, (slot_boundary, node_id, "TRANSMIT"))
            else:
                # In PURE mode, transmit immediately
                heapq.heappush(event_queue, (current_time, node_id, "TRANSMIT"))
                
            # Schedule next arrival
            next_arrival = current_time + node._generate_interarrival()
            heapq.heappush(event_queue, (next_arrival, node_id, "ARRIVE"))
            
        elif event_type == "TRANSMIT":
            node = nodes[node_id]
            # Start transmission
            active_transmissions.add(node_id)
            # Schedule end of transmission
            heapq.heappush(event_queue, (current_time + FRAME_TIME, node_id, "END_TRANSMIT"))
            
        elif event_type == "END_TRANSMIT":
            # End of transmission
            active_transmissions.remove(node_id)
            
            # Check for collision
            if len(active_transmissions) == 0:  # No collision
                success += 1
                nodes[node_id].schedule_next(current_time)
            else:  # Collision occurred
                for tx_id in list(active_transmissions):
                    nodes[tx_id].handle_collision(current_time)
                    active_transmissions.remove(tx_id)
                    heapq.heappush(event_queue, (nodes[tx_id].next_arrival, tx_id, "TRANSMIT"))
    
    throughput = compute_throughput(success, TOTAL_TIME)
    theoretical = theoretical_throughput()
    
    print(f"Mode: {MODE}")
    print(f"Offered Load (G): {OFFERED_LOAD}")
    print(f"Theoretical Throughput: {theoretical:.5f}")
    print(f"Simulated Throughput: {throughput:.5f}")
    
    return throughput

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ALOHA Protocol Simulator')
    parser.add_argument('--mode', choices=['PURE', 'SLOTTED'], help='ALOHA protocol mode')
    parser.add_argument('--load', type=float, help='Offered load G')
    parser.add_argument('--time', type=float, help='Total simulation time')
    parser.add_argument('--type', choices=['TIME_DRIVEN', 'EVENT_DRIVEN'], help='Simulation type')
    
    args = parser.parse_args()
    
    # Update config if arguments provided
    if args.mode:
        MODE = args.mode
    if args.load:
        OFFERED_LOAD = args.load
    if args.time:
        TOTAL_TIME = args.time
    if args.type:
        SIMULATION_TYPE = args.type
    
    if SIMULATION_TYPE == 'TIME_DRIVEN':
        time_driven()
    else:
        event_driven()