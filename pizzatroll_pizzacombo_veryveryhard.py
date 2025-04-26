import random

# Define toppings
pizza_toppings = ["Olives", "Pepperoni", "Peppers", "Mushrooms", "Cheese"]
sundae_toppings = ["Cherry-on-top", "Whipped Cream", "Chocolate Sauce"]

people = ["Arno", "Willa", "Shyler"]

# Assign random favorites (mutually exclusive toppings)
favorites = {}
used_pizza = set()
used_sundae = set()

for person in people:
    available_pizza = [t for t in pizza_toppings if t not in used_pizza]
    available_sundae = [t for t in sundae_toppings if t not in used_sundae]
    
    # Randomly pick 0 or more available toppings
    fav_pizza = set(random.sample(available_pizza, random.randint(0, len(available_pizza))))
    fav_sundae = set(random.sample(available_sundae, random.randint(0, len(available_sundae))))
    
    used_pizza.update(fav_pizza)
    used_sundae.update(fav_sundae)
    
    favorites[person] = (fav_pizza, fav_sundae)

# Generate 4 random reject combos
rejects = set()
while len(rejects) < 4:
    random_pizza = set(random.sample(pizza_toppings, random.randint(0, len(pizza_toppings))))
    random_sundae = set(random.sample(sundae_toppings, random.randint(0, len(sundae_toppings))))
    # Make sure this combo isn't someone's favored
    if all((random_pizza != favs[0] or random_sundae != favs[1]) for favs in favorites.values()):
        rejects.add((frozenset(random_pizza), frozenset(random_sundae)))

# Function to evaluate a guess
def evaluate_guess(pizza_guess, sundae_guess):
    result = {}
    for person, (fav_pizza, fav_sundae) in favorites.items():
        pizza_match = pizza_guess == fav_pizza
        sundae_match = sundae_guess == fav_sundae
        
        if pizza_match and sundae_match:
            result[person] = "Favored"
        elif (pizza_guess & fav_pizza and sundae_guess & fav_sundae):
            result[person] = "Lack"
        else:
            result[person] = "Reject"
    return result

# Pretty print functions
def print_toppings(label, toppings):
    return label + (": (none)" if not toppings else ": " + ", ".join(toppings))

# --- Simulation starts ---
print("=== Secret Favorites (for debug) ===")
for person, (p, s) in favorites.items():
    print(f"{person}:\n  Pizza {print_toppings('Toppings', p)}\n  Sundae {print_toppings('Toppings', s)}")

print("\n=== Pre-generated Rejects ===")
for idx, (p, s) in enumerate(rejects, 1):
    print(f"Reject {idx}:\n  Pizza {print_toppings('Toppings', p)}\n  Sundae {print_toppings('Toppings', s)}")

print("\n=== Ready for Guesses! ===\n")

# Interactive mode example
while True:
    raw_pizza = input("Enter pizza toppings separated by commas (or blank for none): ").strip()
    pizza_guess = set(tp.strip() for tp in raw_pizza.split(",") if tp.strip())
    
    raw_sundae = input("Enter sundae toppings separated by commas (or blank for none): ").strip()
    sundae_guess = set(tp.strip() for tp in raw_sundae.split(",") if tp.strip())

    results = evaluate_guess(pizza_guess, sundae_guess)
    print("\nResult of guess:")
    for person, outcome in results.items():
        print(f"{person}: {outcome}")
    print("\n----------------------\n")
