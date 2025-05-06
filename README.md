# ALOHA Protocol Simulator

This project implements a simulation of both Pure and Slotted ALOHA protocols, providing insights into network performance under different conditions.

## Overview

ALOHA is a pioneering random access protocol that allows multiple users to share a communications channel. This simulator implements both Pure ALOHA and Slotted ALOHA variants, demonstrating their performance characteristics and throughput under various load conditions.

## Project Structure

```bash
aloha-simulation/
├── simulator.py     # Main simulation logic
├── node.py         # Node behavior implementation
├── channel.py      # Channel model and collision handling
├── config.py       # Simulation configuration
├── experiment.py   # Parameter sweep experiments
└── metrics.py      # Performance metrics calculation
```

## Components

### Simulator (simulator.py)

- Implements both time-driven and event-driven simulation approaches
- Handles packet transmission scheduling and collision resolution
- Supports both Pure and Slotted ALOHA modes

### Node (node.py)

- Models individual network nodes
- Implements Poisson arrival process
- Handles collision backoff with exponential backoff strategy
- Manages packet transmission timing

### Channel (channel.py)

- Models the shared communication medium
- Detects and handles collisions
- Tracks transmission statistics
- Manages successful transmission resolution

### Configuration (config.py)

Key parameters:

- NUM_NODES: Number of nodes in the network
- FRAME_TIME: Time to transmit one frame
- TOTAL_TIME: Total simulation duration
- OFFERED_LOAD: Average transmission attempts per frame
- MODE: 'PURE' or 'SLOTTED' ALOHA
- SIMULATION_TYPE: 'TIME_DRIVEN' or 'EVENT_DRIVEN'

## Usage

### Basic Simulation

```bash
python simulator.py --mode PURE --load 0.5 --time 100000 --type TIME_DRIVEN
```

Parameters:

- `--mode`: PURE or SLOTTED
- `--load`: Offered load G (0.0-2.0)
- `--time`: Total simulation time
- `--type`: TIME_DRIVEN or EVENT_DRIVEN

### Running Experiments

```bash
python experiment.py
```

This will:

1. Run simulations across different load values
2. Generate performance comparison plots
3. Save results to JSON files
4. Create a visualization in 'aloha_comparison.png'

## Theoretical Background

### Pure ALOHA

- Nodes transmit immediately when they have data
- Theoretical maximum throughput: 18.4% (1/2e)
- More vulnerable to collisions

### Slotted ALOHA

- Transmissions aligned to time slots
- Theoretical maximum throughput: 36.8% (1/e)
- Better performance due to reduced collision vulnerability

## Performance Metrics

- Throughput (S): Successfully transmitted packets per frame time
- Offered Load (G): Average transmission attempts per frame time
- Theoretical maximum throughput:
  - Pure ALOHA: S = G * e^(-2G)
  - Slotted ALOHA: S = G * e^(-G)

## Implementation Details

### Simulation Approaches

1. Time-Driven Simulation
   - Fixed time step advancement
   - Good for visualizing system state
   - More computationally intensive

2. Event-Driven Simulation
   - Jumps between events
   - More efficient for large simulations
   - Better performance for sparse events

### Collision Handling

- Exponential backoff strategy
- Configurable maximum backoff window
- Collision detection and resolution

## Output and Visualization

The experiment module generates:

- JSON files with simulation results
- Performance comparison plots
- Theoretical vs. simulated throughput curves
- Maximum throughput indicators

## Requirements

- Python 3.6+
- NumPy
- Matplotlib

## Running Tests

Basic simulation verification:

```bash
python simulator.py --mode PURE --load 0.5 --time 1000
python simulator.py --mode SLOTTED --load 0.5 --time 1000
```

Full experiment suite:

```bash
python experiment.py
```

## Extensions and Future Work

Possible enhancements:

1. Additional MAC protocols (CSMA, CSMA/CD)
2. Variable packet sizes
3. Hidden terminal scenarios
4. Network visualization
5. Real-time simulation monitoring
