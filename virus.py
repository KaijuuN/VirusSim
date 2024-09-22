import random


class Virus:
    def __init__(self, name, mutation_rate):
        self.name = name
        self.mutation_rate = mutation_rate
        self.virulence = random.uniform(0.1, 0.5)  # Infektionsrate
        self.mortality_rate = random.uniform(0.01, 0.1)  # Sterblichkeitsrate
    
    def mutate(self):
        # Logik für die Mutation des Virus
        if random.random() < self.mutation_rate:
            self.virulence += random.uniform(0.01, 0.05)
            self.mortality_rate += random.uniform(0.01, 0.05)
