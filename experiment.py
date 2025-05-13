# experiment.py
"""
Parameter sweep experiments for ALOHA simulation.
"""
import config
import subprocess
import math
import numpy as np
import matplotlib.pyplot as plt
import os
import json

def run_simulations(mode='PURE', simulation_type='TIME_DRIVEN', load_range=None):
    if load_range is None:
        load_range = [i * 0.1 for i in range(1, 21)]
        
    results = []
    config.MODE = mode
    config.SIMULATION_TYPE = simulation_type
    
    print(f"Running {mode} ALOHA simulations...")
    
    for G in load_range:
        print(f"  Simulating G = {G:.1f}")
        # Update offered load
        config.OFFERED_LOAD = G
        try:
            # Run simulation and capture output
            output = subprocess.check_output(
                ['python', 'simulator.py'], 
                stderr=subprocess.STDOUT
            ).decode()
            throughput = float(output.strip().split('\n')[-2].split(':')[-1])
            results.append((G, throughput))
            print(f"    Throughput: {throughput:.5f}")
        except subprocess.CalledProcessError as e:
            print(f"Error running simulation: {e.output.decode()}")
            results.append((G, 0))
    
    return results

def plot_results(results_pure, results_slotted=None):
    plt.figure(figsize=(10, 6))
    
    # Plot simulated results
    G_values_pure = [r[0] for r in results_pure]
    throughput_values_pure = [r[1] for r in results_pure]
    plt.plot(G_values_pure, throughput_values_pure, 'bo-', label='Pure ALOHA (Simulated)')
    
    if results_slotted:
        G_values_slotted = [r[0] for r in results_slotted]
        throughput_values_slotted = [r[1] for r in results_slotted]
        plt.plot(G_values_slotted, throughput_values_slotted, 'ro-', label='Slotted ALOHA (Simulated)')
    
    # Plot theoretical curves
    G_theory = np.linspace(0.01, 2, 100)
    S_pure = [G * math.exp(-2*G) for G in G_theory]
    S_slotted = [G * math.exp(-G) for G in G_theory]
    
    plt.plot(G_theory, S_pure, 'b--', label='Pure ALOHA (Theoretical)')
    plt.plot(G_theory, S_slotted, 'r--', label='Slotted ALOHA (Theoretical)')
    
    plt.xlabel('Offered Load (G)')
    plt.ylabel('Throughput (S)')
    plt.title('ALOHA Protocol Performance')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 2)
    plt.ylim(0, 0.5)
    
    # Add max throughput indicators
    plt.axhline(y=1/(2*math.e), color='b', linestyle=':', alpha=0.5)
    plt.axhline(y=1/math.e, color='r', linestyle=':', alpha=0.5)
    
    # Mark optimal points
    plt.plot(0.5, 0.5/math.e, 'ro', markersize=8)
    plt.plot(0.5, 0.5/math.e, 'o', color='white', markersize=4)
    plt.plot(0.5, 0.5/math.e, 'ro', markersize=2)
    
    plt.plot(0.5, 0.5/(2*math.e), 'bo', markersize=8)
    plt.plot(0.5, 0.5/(2*math.e), 'o', color='white', markersize=4)
    plt.plot(0.5, 0.5/(2*math.e), 'bo', markersize=2)
    
    plt.savefig('aloha_comparison.png')
    plt.show()

def save_results(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f)

def load_results(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def main():
    # Run simulations or load previous results
    if os.path.exists('pure_results.json') and os.path.exists('slotted_results.json'):
        print("Loading saved simulation results...")
        pure_results = load_results('pure_results.json')
        slotted_results = load_results('slotted_results.json')
    else:
        print("Running simulations...")
        # Define a common load range for both simulations
        load_range = [i * 0.1 for i in range(1, 21)]  # G from 0.1 to 2.0
        
        # Run Pure ALOHA simulations
        pure_results = run_simulations(mode='PURE', load_range=load_range)
        save_results(pure_results, 'pure_results.json')
        
        # Run Slotted ALOHA simulations
        slotted_results = run_simulations(mode='SLOTTED', load_range=load_range)
        save_results(slotted_results, 'slotted_results.json')
    
    # Plot results
    plot_results(pure_results, slotted_results)

if __name__ == "__main__":
    main()
