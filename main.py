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

    def recover_or_die(self, recovery_time: int = 14, mortality_rate: float= 0.01):
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


class Simulation:
    def __init__(self,population_size=100):
        self.population_size = population_size
        self.population = [Individuum() for _ in range(self.population_size)]
        self.reset_button_rect = pg.Rect(screen_width - 120,10,100,40)
        self.infect_button_rect = pg.Rect(screen_width - 120,60,100,40)

    def reset_population(self):
        self.population = [Individuum() for _ in range(self.population_size)]

    def infect_random_person(self):
        susceptible_person = [p for p in self.population if p.health_status == HealthStatus.SUSCEPTIBLE]
        if susceptible_person:
            random.choice(susceptible_person).infect()

    def update_population(self):
        for person in self.population:
            person.move(social_distancing_factor=.5)
            if person.health_status == HealthStatus.INFECTED:
                person.update_status()
                person.recover_or_die()
    
    def draw_population(self):
        for person in self.population:
            pg.draw.circle(screen, person.color,(int(person.x), int(person.y)),5)

    def count_status(self):
        susceptible = sum(1 for p in self.population if p.health_status == HealthStatus.SUSCEPTIBLE)
        infected = sum(1 for p in self.population if p.health_status == HealthStatus.INFECTED)
        recovered = sum(1 for p in self.population if p.health_status == HealthStatus.RECOVERED)
        dead = sum(1 for p in self.population if p.health_status == HealthStatus.DEAD)

        return susceptible, infected, recovered, dead

    def draw_lables(self, susceptible, infected, recovered, dead):
        screen.blit(font.render(f"Susceptible: {susceptible}", True, WHITE), (10,10))
        screen.blit(font.render(f"Infected: {infected}", True, WHITE), (10,30))
        screen.blit(font.render(f"Recovered: {recovered}", True, WHITE), (10,50))
        screen.blit(font.render(f"Dead: {dead}", True, WHITE), (10,70))
    
    def draw_buttons(self):
        # Reset-Button
        reset_button = pg.draw.rect(screen, GRAY, (screen_width - 120, 10, 100, 40))
        screen.blit(font.render("Reset", True, BLACK), (screen_width - 100, 20))

        # Infect-Button
        infect_button = pg.draw.rect(screen, GRAY, (screen_width - 120, 60, 100, 40))
        screen.blit(font.render("Infect", True, BLACK), (screen_width - 100, 70))

        return reset_button, infect_button
    
    def handle_click(self,mouse_pos):
        if self.reset_button_rect.collidepoint(mouse_pos):
            self.reset_population()
        if self.infect_button_rect.collidepoint(mouse_pos):
            self.infect_random_person()


def main():
    simulation = Simulation(population_size=100)
    clock = pg.time.Clock()

    running = True

    while running:
        screen.fill(BLACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                simulation.handle_click(mouse_pos)


        simulation.update_population()
        simulation.draw_population()
       

        susceptible,infected,recovered,dead = simulation.count_status()
        simulation.draw_lables(susceptible,infected,recovered,dead)
        simulation.draw_buttons()

        pg.display.flip()
        clock.tick(30)
    
    pg.quit()

if __name__ == "__main__":
    main()
