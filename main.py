from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import random
import pygame as pg


pg.init()

screen_width, screen_height = 800,600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Virus SIM")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)


# Schriftarten
font = pg.font.SysFont(None, 24)

class HealthStatus(Enum):
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3
    DEAD = 4

class StatusColors(Enum):
    SUSCEPTIBLE: str = "blue"
    INFECTED: str = "red"
    RECOVERED: str = "green"
    DEAD: str = "black"
    

class Individuum:
    def __init__(self, health: float = 100.0) -> None:
        self.health = health
        self.x = random.uniform(50,screen_width-50)
        self.y = random.uniform(50,screen_height-50)
        self.health_status = HealthStatus.SUSCEPTIBLE
        self.days_infected = 0
        self.color = BLUE

    def move(self, social_distancing_factor: float = 1.0):
        # A function that updates the positions of the persons in each time unit.
        if self.health_status != HealthStatus.DEAD:
            self.x += random.uniform(-1,1)* social_distancing_factor
            self.y += random.uniform(-1,1)* social_distancing_factor
        # Begrenzen auf den Bildschirmbereich
            self.x = max(0, min(screen_width, self.x))
            self.y = max(0, min(screen_height, self.y))

    def infect(self):
        if self.health_status == HealthStatus.SUSCEPTIBLE:
            self.health_status = HealthStatus.INFECTED
            self.color = RED
            
            self.incubation = 0
            self.days_infected = 0

    def recover_or_die(self, recovery_time: int, mortality_rate: float):
        if self.days_infected >= recovery_time:
            if random.random() < mortality_rate:
                self.health_status = HealthStatus.DEAD
                self.color = GRAY
            else:
                self.health_status = HealthStatus.RECOVERED
                self.was_infected = True
                self.color = GREEN

    def update_status(self):
        match self.health_status:
            case HealthStatus.INFECTED:
                self.days_infected += 1
                self.incubation += 1
            case HealthStatus.RECOVERED:
                print(f"Person is recovered and immune with factor {self.immunity_factor}.")
            case HealthStatus.DEAD:
                print("Person is dead and no longer moving.")


population_size = 100
population = [Individuum() for _ in range(population_size)]

def update_population():
    for person in population:
        person.move(social_distancing_factor=.5)
        if person.health_status == HealthStatus.INFECTED:
            person.update_status()
            person.recover_or_die()

def draw_population():
    for person in population:
        pg.draw.circle(screen, person.color,(int(person.x), int(person.y)),5)

def count_status():
    susceptible = sum(1 for p in population if p.health_status == HealthStatus.SUSCEPTIBLE)
    infected = sum(1 for p in population if p.health_status == HealthStatus.INFECTED)
    recovered = sum(1 for p in population if p.health_status == HealthStatus.RECOVERED)
    dead = sum(1 for p in population if p.health_status == HealthStatus.DEAD)

    return susceptible, infected, recovered, dead

def draw_lables(susceptible, infected, recovered, dead):
    screen.blit(font.render(f"Susceptible: {susceptible}", True, WHITE), (10,10))
    screen.blit(font.render(f"Infected: {infected}", True, WHITE), (10,30))
    screen.blit(font.render(f"Recovered: {recovered}", True, WHITE), (10,50))
    screen.blit(font.render(f"Dead: {dead}", True, WHITE), (10,70))

running = True
clock = pg.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
    update_population()
    draw_population()
    susceptible,infected,recovered,dead = count_status()
    draw_lables(susceptible,infected,recovered,dead)
    pg.display.flip()
    clock.tick(30)

pg.quit()