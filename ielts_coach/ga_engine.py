# ga_engine.py
"""
Genetic Algorithm Engine for IELTS Study Coach.
Provides personalized study schedule optimization based on learning curves and cognitive fatigue.
"""

import math
import random
import copy

# Cognitive difficulty coefficient per skill
SKILL_DIFFICULTY = {
    "L": 1.2,  # Listening
    "R": 1.3,  # Reading
    "W": 1.5,  # Writing (highest cognitive load)
    "S": 1.4   # Speaking
}

# Learning rate coefficient (k) per skill
SKILL_LEARNING_RATE = {
    "L": 0.006,
    "R": 0.005,
    "W": 0.003,
    "S": 0.004
}

# Duration options in hours (45m to 2h in 15m increments)
DURATION_OPTIONS = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0]

def round_ielts(score: float) -> float:
    """
    Round band score according to IELTS rules:
    - Decimal part < 0.25 -> round down to .0
    - 0.25 <= Decimal part < 0.75 -> round to .5
    - Decimal part >= 0.75 -> round up to .0
    """
    base = int(score)
    decimal = score - base
    if decimal < 0.25:
        return float(base)
    elif decimal < 0.75:
        return base + 0.5
    else:
        return float(base + 1)

def calculate_learning_gain(p0: float, t: float, k: float, p_inf: float = 9.0) -> float:
    """
    Calculate learning gain using the learning curve formula:
    Pn = P_inf - (P_inf - P0) * e^(-k * t)
    """
    if t <= 0 or k <= 0:
        return float(p0)
    
    # Calculate learning curve
    pn = p_inf - (p_inf - p0) * math.exp(-k * t)
    
    # Cap at 9.0 and floor at p0
    return min(max(pn, p0), 9.0)

def calculate_fatigue(schedule: list, alpha: float = 1.3, beta: float = 0.2) -> float:
    """
    Calculate raw fatigue for a 7-day schedule.
    f(P) = sum_{day} [ sum_{j=1}^m (C_j * t_j^alpha) - beta * sum_{j=2}^m 1[s_j != s_{j-1}] ]
    """
    total_fatigue = 0.0
    
    for day in schedule:
        if not day:
            continue
        
        m = len(day)
        raw_fatigue_day = 0.0
        subject_changes = 0
        
        for j, session in enumerate(day):
            skill, duration = session
            difficulty = SKILL_DIFFICULTY.get(skill, 1.0)
            raw_fatigue_day += difficulty * (duration ** alpha)
            
            # Count subject changes (reward for variety)
            if j > 0:
                prev_skill = day[j-1][0]
                if skill != prev_skill:
                    subject_changes += 1
        
        fatigue_day = raw_fatigue_day - beta * subject_changes
        total_fatigue += max(fatigue_day, 0.0)  # Fatigue cannot be negative per day
        
    return total_fatigue

def calculate_fitness(schedule: list, initial_bands: dict, target_bands: dict, total_days: int = 30) -> float:
    """
    Calculate the fitness score of a schedule, penalizing constraint violations.
    F(P) = sum_{i=1}^4 P_{n,i} - ControlledPenalty
    """
    # 1. Count hours and blocks per skill
    hours_by_skill = {"L": 0.0, "R": 0.0, "W": 0.0, "S": 0.0}
    blocks_by_skill = {"L": 0, "R": 0, "W": 0, "S": 0}
    total_blocks = 0
    penalty = 0.0
    
    for day in schedule:
        # Check max blocks per day constraint
        if len(day) > 4:
            penalty += (len(day) - 4) * 100.0
            
        for session in day:
            skill, duration = session
            if skill in hours_by_skill:
                hours_by_skill[skill] += duration
                blocks_by_skill[skill] += 1
                total_blocks += 1
                
                # Check min block size constraint (45 mins = 0.75h)
                if duration < 0.75:
                    penalty += 50.0
            else:
                # Invalid skill
                penalty += 100.0

    # Check max blocks per cycle constraint (24 blocks)
    if total_blocks > 24:
        penalty += (total_blocks - 24) * 100.0

    # Check min blocks per skill per cycle constraint (4 blocks)
    for skill, count in blocks_by_skill.items():
        if count < 4:
            penalty += (4 - count) * 150.0

    # 2. Calculate post-study scores (Learning Curve)
    learning_gain_sum = 0.0
    for skill in ["L", "R", "W", "S"]:
        p0 = initial_bands.get(skill, 6.0)
        # Scale 7-day hours to total_days
        total_hours = hours_by_skill[skill] * (total_days / 7.0)
        k = SKILL_LEARNING_RATE.get(skill, 0.005)
        pn = calculate_learning_gain(p0, total_hours, k)
        learning_gain_sum += pn

    # 3. Calculate fatigue penalty
    raw_fatigue = calculate_fatigue(schedule)
    
    # Max theoretical fatigue: 24 blocks of Writing (difficulty 1.5) of 2.0h each
    # alpha = 1.3
    max_theoretical_fatigue = 24.0 * 1.5 * (2.0 ** 1.3)
    normalized_fatigue = min(raw_fatigue / max_theoretical_fatigue, 1.0)
    
    # Max penalty band equivalent is 1.0
    controlled_penalty = normalized_fatigue * 1.0

    # Fitness is the gain sum minus fatigue and constraint penalties
    fitness = learning_gain_sum - controlled_penalty - penalty
    return fitness

def generate_initial_population(pop_size: int = 300) -> list:
    """
    Generate an initial population of chromosomes.
    A chromosome is a list of 7 days, each containing a list of (skill, duration) tuples.
    """
    population = []
    skills = ["L", "R", "W", "S"]
    
    for _ in range(pop_size):
        chromosome = [[] for _ in range(7)]
        
        # Ensure we have at least 4 blocks per skill to start with a decent candidate
        # Total minimum blocks = 16. We distribute them randomly across the 7 days.
        required_blocks = []
        for skill in skills:
            required_blocks.extend([skill] * 4)
            
        random.shuffle(required_blocks)
        
        # Distribute required blocks
        for skill in required_blocks:
            # Find a day with less than 4 blocks
            available_days = [d for d in range(7) if len(chromosome[d]) < 4]
            if not available_days:
                break
            day_idx = random.choice(available_days)
            duration = random.choice(DURATION_OPTIONS)
            chromosome[day_idx].append((skill, duration))
            
        # Randomly add 0 to 8 additional blocks (total blocks up to 24)
        num_additional = random.randint(0, 8)
        for _ in range(num_additional):
            available_days = [d for d in range(7) if len(chromosome[d]) < 4]
            total_blocks = sum(len(day) for day in chromosome)
            if not available_days or total_blocks >= 24:
                break
            day_idx = random.choice(available_days)
            skill = random.choice(skills)
            duration = random.choice(DURATION_OPTIONS)
            chromosome[day_idx].append((skill, duration))
            
        population.append(chromosome)
        
    return population

def crossover(parent1: list, parent2: list) -> tuple:
    """
    Single-point crossover on the day-level.
    """
    crossover_point = random.randint(1, 6)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(chromosome: list, mutation_rate: float = 0.1) -> list:
    """
    Mutate a chromosome.
    """
    mutated = copy.deepcopy(chromosome)
    skills = ["L", "R", "W", "S"]
    
    for day_idx in range(7):
        if random.random() < mutation_rate:
            day = mutated[day_idx]
            
            # Define mutation action
            action = random.choice(["change_duration", "change_skill", "remove_block", "add_block"])
            
            if action == "change_duration" and day:
                idx = random.randint(0, len(day) - 1)
                skill, _ = day[idx]
                new_duration = random.choice(DURATION_OPTIONS)
                day[idx] = (skill, new_duration)
                
            elif action == "change_skill" and day:
                idx = random.randint(0, len(day) - 1)
                _, duration = day[idx]
                new_skill = random.choice(skills)
                day[idx] = (new_skill, duration)
                
            elif action == "remove_block" and day:
                idx = random.randint(0, len(day) - 1)
                day.pop(idx)
                
            elif action == "add_block" and len(day) < 4:
                # Count total blocks in chromosome
                total_blocks = sum(len(d) for d in mutated)
                if total_blocks < 24:
                    new_skill = random.choice(skills)
                    new_duration = random.choice(DURATION_OPTIONS)
                    day.append((new_skill, new_duration))
                    
    return mutated

def run_ga(initial_bands: dict, target_bands: dict, total_days: int, pop_size: int = 300, generations: int = 100) -> dict:
    """
    Run the Genetic Algorithm to optimize the IELTS study schedule.
    """
    # 1. Initialize population
    population = generate_initial_population(pop_size)
    best_chromosome = None
    best_fitness = -float("inf")
    no_improvement_count = 0
    
    # 2. GA Loop
    for generation in range(generations):
        # Evaluate fitness for all individuals
        fitness_scores = [calculate_fitness(ind, initial_bands, target_bands, total_days) for ind in population]
        
        # Find best individual of this generation
        max_idx = fitness_scores.index(max(fitness_scores))
        gen_best_fitness = fitness_scores[max_idx]
        gen_best_chromosome = population[max_idx]
        
        # Check overall improvement
        if gen_best_fitness > best_fitness:
            best_fitness = gen_best_fitness
            best_chromosome = copy.deepcopy(gen_best_chromosome)
            no_improvement_count = 0
        else:
            no_improvement_count += 1
            
        # Early stopping condition: 10 generations without improvement
        if no_improvement_count >= 10:
            break
            
        # Selection & Reproduction
        new_population = []
        
        # Elitism: Keep the top 10% best individuals
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k], reverse=True)
        elitism_count = max(1, int(pop_size * 0.1))
        for idx in sorted_indices[:elitism_count]:
            new_population.append(copy.deepcopy(population[idx]))
            
        # Fill the rest of the population
        while len(new_population) < pop_size:
            # Tournament selection for parents
            def select_parent():
                tournament = random.sample(list(zip(population, fitness_scores)), 3)
                return max(tournament, key=lambda item: item[1])[0]
                
            parent1 = select_parent()
            parent2 = select_parent()
            
            # Crossover (rate: 0.8)
            if random.random() < 0.8:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
                
            # Mutation (rate: 0.1)
            child1 = mutate(child1, mutation_rate=0.1)
            child2 = mutate(child2, mutation_rate=0.1)
            
            new_population.extend([child1, child2])
            
        # Trim population to exact size
        population = new_population[:pop_size]

    # 3. Forecast scores for the best schedule
    hours_by_skill = {"L": 0.0, "R": 0.0, "W": 0.0, "S": 0.0}
    for day in best_chromosome:
        for skill, duration in day:
            if skill in hours_by_skill:
                hours_by_skill[skill] += duration
                
    forecasted_scores = {}
    for skill in ["L", "R", "W", "S"]:
        p0 = initial_bands.get(skill, 6.0)
        total_hours = hours_by_skill[skill] * (total_days / 7.0)
        k = SKILL_LEARNING_RATE.get(skill, 0.005)
        pn = calculate_learning_gain(p0, total_hours, k)
        forecasted_scores[skill] = round(pn, 2)
        
    # Calculate overall score
    avg_score = sum(forecasted_scores.values()) / 4.0
    forecasted_scores["overall"] = round_ielts(avg_score)
    
    return {
        "status": "success",
        "schedule": best_chromosome,
        "forecasted_scores": forecasted_scores,
        "fitness": round(best_fitness, 4)
    }
