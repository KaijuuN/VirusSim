# virus.py
import random

class Virus:
    def __init__(self, name, virulence, mortality_rate, mutation_rate, mutation_marker="v1"):
        self.name = name
        self.virulence = virulence  # Infektionsrate
        self.mortality_rate = mortality_rate  # Sterblichkeitsrate
        self.mutation_rate = mutation_rate  # Mutationsrate
        self.mutation_marker = mutation_marker  # Initialer Marker für das Virus
    
    def mutate(self):
        # Virus mutiert mit der Wahrscheinlichkeit der Mutationsrate
        if random.random() < self.mutation_rate:
            self.virulence += random.uniform(0.01, 0.05)
            self.mortality_rate += random.uniform(0.01, 0.05)
            # Mutation Marker wird inkrementiert, z.B. von "v1" zu "v2"
            version_number = int(self.mutation_marker[1:]) + 1
            self.mutation_marker = f"v{version_number}"
            print(f"{self.name} hat mutiert! Neue Virulenz: {self.virulence:.2f}, Neue Sterberate: {self.mortality_rate:.2f}, Neuer Marker: {self.mutation_marker}")

# Example virus instance
covid19 = Virus(name="COVID-19", virulence=0.3, mortality_rate=0.02, mutation_rate=0.1, mutation_marker="v1")
