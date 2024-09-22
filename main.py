from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import random
import matplotlib
from matplotlib import pyplot as plt


susceptible: int = 0
infected: int = 0
recovered: int = 0

infectionrate: int = 0
incubationrate: int = 0
mortalityrate: int = 0
recoveryrate: int = 0
    
@dataclass
class Individuum:

    health: float = 100.0

    is_susceptible: bool = True
    is_infected: bool = False
    is_recovered: bool = False
    is_dead: bool = False

    was_infected: bool = False
    is_infectious: bool = False

    has_immunity: bool = False
    immunity_factor: float = 0.0

    incubation: int = 0
    days_infected: int = field(default=0, init=False)

    # Verwende default_factory für zufällige Startposition
    x: float = field(default_factory=lambda: random.uniform(0, 50))
    y: float = field(default_factory=lambda: random.uniform(0, 50))

    def move(self, social_distancing_factor: float = 1.0):
        # A function that updates the positions of the persons in each time unit.
        self.x += random.uniform(-1,1)* social_distancing_factor
        self.y += random.uniform(-1,1)* social_distancing_factor

    def infect(self):
        if self.is_susceptible:
            self.is_susceptible = False
            self.is_infected = True
            self.incubation = 0
            self.days_infected = 0

    def recover_or_die(self, recovery_time: int, mortality_rate: float):
        if self.days_infected >= recovery_time:
            if random.random() < mortality_rate:
                self.is_dead = True
            else:
                self.is_recovered = True
                self.is_infected = False
                self.was_infected = True



    def update_status(self):
        if self.is_infected:
            self.days_infected += 1
            self.incubation += 1

def check_for_infection():
    # A function that checks whether an infection has occurred between two people.
    pass

def generate_dna():
    # A function that generates and visualizes a random DNA strand.
    pass



def main():
    population = [Individuum() for _ in range(100)]

    for day in range(356):
        for person in population:
            person.move(social_distancing_factor=.5)
            if person.is_infected:
                person.update_status()
                person.recover_or_die()


if __name__ == '__main__':
    main()