# simulation.py
"""
Large-scale simulation of 1000 users for IELTS Study Planner.
Generates random user profiles, runs Genetic Algorithm, and compiles convergence stats.
Saves distribution plots to docs/simulation_results.png.
"""

import os
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from ielts_coach.ga_engine import run_ga

def generate_random_profile():
    """Generate a realistic random user profile."""
    skills = ["L", "R", "W", "S"]
    initial_bands = {}
    target_bands = {}
    
    # Random initial bands between 4.0 and 8.0, rounded to 0.5
    for s in skills:
        initial_bands[s] = round(random.uniform(4.0, 8.0) * 2) / 2.0
        
    # Target bands are initial + 0.5 to 1.5, capped at 9.0
    for s in skills:
        offset = round(random.choice([0.5, 1.0, 1.5]) * 2) / 2.0
        target_bands[s] = min(9.0, initial_bands[s] + offset)
        
    total_days = random.randint(14, 90)
    return initial_bands, target_bands, total_days

def run_simulation(num_users: int = 1000):
    print(f"🚀 Starting simulation of {num_users} users...")
    os.makedirs("docs", exist_ok=True)
    
    start_time = time.time()
    
    fitnesses = []
    initial_overalls = []
    target_overalls = []
    forecast_overalls = []
    success_count = 0  # Number of users who met or exceeded their overall target score
    
    for i in range(num_users):
        init_b, targ_b, days = generate_random_profile()
        
        # Calculate overalls
        init_overall = round(sum(init_b.values()) / 4.0 * 2) / 2.0
        targ_overall = round(sum(targ_b.values()) / 4.0 * 2) / 2.0
        
        initial_overalls.append(init_overall)
        target_overalls.append(targ_overall)
        
        # Run GA
        result = run_ga(init_b, targ_b, days)
        
        fit = result["fitness"]
        fitnesses.append(fit)
        
        forecast_overall = result["forecasted_scores"]["overall"]
        forecast_overalls.append(forecast_overall)
        
        if forecast_overall >= targ_overall:
            success_count += 1
            
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{num_users} users...")
            
    end_time = time.time()
    duration = end_time - start_time
    
    success_rate = (success_count / num_users) * 100
    avg_fitness = np.mean(fitnesses)
    avg_improvement = np.mean(np.array(forecast_overalls) - np.array(initial_overalls))
    
    print("\n--- Simulation Results ---")
    print(f"Total Users Simulated: {num_users}")
    print(f"Total Duration: {duration:.2f} seconds ({duration/num_users*1000:.2f} ms/user)")
    print(f"Overall Target Success Rate: {success_rate:.2f}%")
    print(f"Average Fitness Score: {avg_fitness:.4f}")
    print(f"Average Band Score Improvement: {avg_improvement:+.2f}")
    
    # Save statistics plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('#0f172a')
    
    # Plot 1: Fitness Distribution
    ax1.set_facecolor('#1e293b')
    ax1.hist(fitnesses, bins=30, color='#6366f1', edgecolor='#312e81', alpha=0.85)
    ax1.set_title("Fitness Score Distribution", color='white', fontsize=12, pad=10)
    ax1.set_xlabel("Fitness Value", color='white')
    ax1.set_ylabel("Count", color='white')
    ax1.tick_params(colors='white')
    ax1.grid(color='#334155', linestyle='--', alpha=0.5)
    
    # Plot 2: Improvement Distribution
    ax2.set_facecolor('#1e293b')
    improvements = np.array(forecast_overalls) - np.array(initial_overalls)
    ax2.hist(improvements, bins=15, color='#10b981', edgecolor='#064e3b', alpha=0.85)
    ax2.set_title("Overall Score Improvement Distribution", color='white', fontsize=12, pad=10)
    ax2.set_xlabel("Improvement (Bands)", color='white')
    ax2.set_ylabel("Count", color='white')
    ax2.tick_params(colors='white')
    ax2.grid(color='#334155', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plot_path = "docs/simulation_results.png"
    plt.savefig(plot_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"📊 Plot saved successfully to: {plot_path}")

if __name__ == "__main__":
    run_simulation(100)
