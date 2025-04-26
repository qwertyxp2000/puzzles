from itertools import product, combinations
from collections import defaultdict

# Generate all possible 8-bit combos (pizza-sundaes)
all_combos = list(product([0, 1], repeat=8))

# Generate all 3^8 ways to assign each of the 8 toppings to one of 3 people (0, 1, 2)
all_assignments = list(product([0, 1, 2], repeat=8))

# For each assignment, generate the 3 preferred combos (one per person)
assignment_to_combos = defaultdict(set)
for assign in all_assignments:
    person_combos = {0: [0]*8, 1: [0]*8, 2: [0]*8}
    for i, p in enumerate(assign):
        person_combos[p][i] = 1
    assignment_to_combos[tuple(assign)] = {
        tuple(person_combos[0]),
        tuple(person_combos[1]),
        tuple(person_combos[2]),
    }

# Create a reverse map: for each combo, which assignments include it as a preferred combo
combo_to_assignments = defaultdict(set)
for assign, combos in assignment_to_combos.items():
    for combo in combos:
        combo_to_assignments[combo].add(assign)

# Choose all 4-combo subsets and compute how many assignments they eliminate
combo_sets = list(combinations(all_combos, 4))

# Let's test a subset of them for feasibility (due to combinatorial explosion)
sample_combo_sets = combo_sets[::10000]  # Sampled for performance
results = []

for combo_set in sample_combo_sets:
    eliminated = set()
    for combo in combo_set:
        eliminated.update(combo_to_assignments[combo])
    results.append((combo_set, len(eliminated)))

# Find best and worst cases among the sample
best = max(results, key=lambda x: x[1])
worst = min(results, key=lambda x: x[1])

print("Best 4 rejects (eliminate the most assignments):", best[0])
print("Number of assignments eliminated:", best[1])
print("\nWorst 4 rejects (eliminate the fewest assignments):", worst[0])
print("Number of assignments eliminated:", worst[1])
print(f"\nEvaluated {len(sample_combo_sets)} 4-reject sets.")
