# ALOHA Protocol Simulator

This project implements a simulation of both Pure and Slotted ALOHA protocols, providing insights into network performance under different conditions.

## Overview

ALOHA is a pioneering random access protocol that allows multiple users to share a communications channel. This simulator implements both Pure ALOHA and Slotted ALOHA variants, demonstrating their performance characteristics and throughput under various load conditions.

## Project Structure

```bash
aloha-simulation/
├── simulator.py    # Main simulation logic and orchestration
├── node.py         # Node behavior implementation with packet handling
├── channel.py      # Channel model and collision detection
├── config.py       # Simulation configuration parameters
├── metrics.py      # Performance metrics calculation
```

## How the Code Works

### Core Components and Flow

1. **Configuration (config.py)**
   - Defines system parameters like frame size, channel capacity
   - Sets simulation parameters (offered load, number of stations)
   - Controls protocol mode (PURE or SLOTTED ALOHA)
   - These parameters determine the fundamental behavior of the simulation

2. **Station Implementation (node.py)**
   - Each network station (Node) manages:
     - Packet generation based on Poisson process
     - Transmission scheduling
     - Collision handling with binary exponential backoff
     - Successful transmission acknowledgment
   - Key methods:
     - `ready_to_transmit()`: Determines when a node is ready to send
     - `transmit()`: Initiates packet transmission
     - `handle_collision()`: Implements backoff strategy after collision
     - `handle_success()`: Resets backoff counter after successful transmission

3. **Communication Channel (channel.py)**
   - Models the shared transmission medium
   - Tracks ongoing transmissions
   - Detects collisions when multiple nodes transmit simultaneously
   - Records statistics on successful transmissions and collisions
   - The `resolve()` method determines transmission outcomes:
     - No transmissions: Channel remains idle
     - One transmission: Successful transfer
     - Multiple transmissions: Collision occurs

4. **Metrics Calculation (metrics.py)**
   - Computes theoretical throughput based on ALOHA protocol equations:
     - Pure ALOHA: G * e^(-2G)
     - Slotted ALOHA: G * e^(-G)
   - Calculates simulated throughput from actual successful transmissions
   - Converts normalized throughput to absolute frames per second

5. **Main Simulator (simulator.py)**
   - Offers two simulation approaches:
     - Time-driven: Steps through simulation in small time increments
     - Event-driven: More efficient approach jumping between significant events
   - Manages the node-channel interactions
   - Collects and reports performance statistics
   - Processes command-line arguments to control simulation parameters

### Simulation Execution Flow

1. **Initialization**:
   - Parse command-line arguments
   - Create network nodes based on configuration
   - Initialize the shared channel
   - Set up simulation parameters

2. **For Time-Driven Simulation**:
   - Advance in small time steps (delta_t)
   - At each step:
     - Check if nodes are ready to transmit
     - Process any transmissions
     - Resolve channel state (success or collision)
     - Update node states accordingly

3. **For Event-Driven Simulation**:
   - Use a priority queue to manage events chronologically
   - Process three types of events:
     - ARRIVAL: New packet generated at a node
     - TRANSMISSION: Node begins transmitting packet
     - END_TRANSMISSION: Transmission completes, channel resolves outcome
   - Jump directly from one event to the next for efficiency

4. **Resolution and Statistics**:
   - Track successful transmissions
   - Calculate simulated throughput
   - Compare with theoretical expectations
   - Report performance metrics

## ALOHA Protocol Variants

### Pure ALOHA

- Nodes transmit immediately when they have data
- Vulnerable to collisions across entire frame duration
- Theoretical maximum throughput: 18.4% (1/2e)
- Implementation: Nodes transmit as soon as packets arrive

### Slotted ALOHA

- Transmissions aligned to time slots (frame boundaries)
- Collisions only occur within same slot period
- Theoretical maximum throughput: 36.8% (1/e)
- Implementation: Nodes defer transmission to the next slot boundary

## Expected Output

When running `simulator.py`, you'll see:

```bash
Mode: [PURE or SLOTTED]
Offered Load (G): [value]
Theoretical Throughput: [calculated value]
Simulated Throughput: [measured value]
Absolute Throughput: [frames/second]
Theoretical Absolute Throughput: [frames/second]
```

Interpretation:

- **Mode**: The ALOHA variant being simulated
- **Offered Load (G)**: Average number of transmission attempts per frame time
- **Theoretical Throughput**: Expected performance based on mathematical model
- **Simulated Throughput**: Actual performance from simulation (should approach theoretical value)
- **Absolute Throughput**: Real-world frame rate achieved by the network
- **Theoretical Absolute Throughput**: Maximum possible frame rate at given load

## Performance Analysis

The key performance metric in ALOHA is **throughput** (S), which represents the fraction of successful transmissions per frame time:

- As offered load (G) increases from 0, throughput initially increases
- At optimal load:
  - Pure ALOHA: G=0.5, S=0.184 (18.4%)
  - Slotted ALOHA: G=1.0, S=0.368 (36.8%)
- Beyond optimal load, collisions increase and throughput decreases

The simulation validates these theoretical relationships and allows exploration of:

- Effect of varying network size (number of stations)
- Impact of different backoff strategies
- Performance under changing load conditions

## Command-Line Usage

```bash
python simulator.py --mode [PURE|SLOTTED] --load [value] --time [seconds] --stations [count] --type [TIME_DRIVEN|EVENT_DRIVEN]
```

Parameters:

- `--mode`: ALOHA protocol variant (PURE or SLOTTED)
- `--load`: Offered load (G), typically 0.1 to 2.0
- `--time`: Simulation duration in seconds
- `--stations`: Number of network stations
- `--type`: Simulation approach (TIME_DRIVEN or EVENT_DRIVEN)

Example:

```bash
python simulator.py --mode SLOTTED --load 1.0 --time 1000 --stations 50 --type EVENT_DRIVEN
```

## Understanding Key Variables

- **FRAME_TIME**: Time to transmit one complete packet (seconds)
- **CHANNEL_CAPACITY**: Network bandwidth in bits per second
- **FRAME_SIZE**: Packet size in bits
- **OFFERED_LOAD**: Average packet generation rate across the network
- **MAX_BACKOFF**: Maximum number of backoff attempts before reset

## Implementation Details

1. **Poisson Arrival Process**:
   - Packet arrivals follow exponential interarrival times
   - `random.expovariate()` generates realistic traffic patterns

2. **Binary Exponential Backoff**:
   - After collision, nodes wait random time before retrying
   - Backoff window doubles with each collision (up to MAX_BACKOFF)
   - Reduces collision probability during congestion

3. **Event Queue Management**:
   - Priority queue maintains chronological event ordering
   - Efficient simulation of large networks over extended periods
   - Events processed in strict time sequence

4. **Simulation Optimization**:
   - Event-driven approach more efficient than time-driven
   - Larger simulations use sampling techniques to estimate performance
   - Parameters can be adjusted for speed vs. accuracy tradeoffs
