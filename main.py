from dataclasses import dataclass, field
from enum import Enum
import math
import numpy as np
import random
import pygame as pg


pg.init()

screen_width, screen_height = 1920,1080
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
        self.dx = random.uniform(-1, 1)  # Bewegung in x-Richtung
        self.dy = random.uniform(-1, 1)  # Bewegung in y-Richtung
        self.speed = random.uniform(1, 3)  # Geschwindigkeit
        self.health_status = HealthStatus.SUSCEPTIBLE
        self.days_infected = 0
        self.color = BLUE
        self.infection_timer = 0
        self.direction_change_timer = 0  # Timer für Richtungsänderung

    def move(self, time_step):
        # A function that updates the positions of the persons in each time unit.
        if self.health_status != HealthStatus.DEAD:
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed

        # Kollision mit dem Bildschirmrand -> Reflexion (Richtungsumkehr)
            if self.x <= 0 or self.x >= screen_width:
                self.dx *= -1  # Richtung in x-Richtung umkehren
            if self.y <= 0 or self.y >= screen_height:
                self.dy *= -1  # Richtung in y-Richtung umkehren
        # # Begrenzen auf den Bildschirmbereich
        #     self.x = max(0, min(screen_width, self.x))
        #     self.y = max(0, min(screen_height, self.y))
            self.direction_change_timer += time_step
            if self.direction_change_timer > 3000:  # Richtung alle 3 Sekunden leicht ändern
                self.change_direction()
                self.direction_change_timer = 0

    def change_direction(self):
        # Leichte Richtungsänderung um einen zufälligen Wert, damit die Bewegung natürlicher wirkt
        angle_change = random.uniform(-math.pi/6, math.pi/6)  # Richtungsänderung um bis zu 30°
        
        # Berechne die neue Richtung basierend auf dem Winkel
        new_dx = self.dx * math.cos(angle_change) - self.dy * math.sin(angle_change)
        new_dy = self.dx * math.sin(angle_change) + self.dy * math.cos(angle_change)
        
        # Normiere den Vektor, um die Geschwindigkeit konstant zu halten
        length = math.sqrt(new_dx**2 + new_dy**2)
        if length > 0:
            self.dx = new_dx / length
            self.dy = new_dy / length


    def infect(self):
        if self.health_status == HealthStatus.SUSCEPTIBLE:
            self.health_status = HealthStatus.INFECTED
            self.color = RED
            
            self.incubation = 0
            self.days_infected = 0
            self.infection_timer = 0

    def recover_or_die(self, recovery_time: int = 14, mortality_rate: float= 0.8):
        if self.days_infected >= recovery_time:
            if random.random() < mortality_rate:
                self.health_status = HealthStatus.DEAD
                self.color = GRAY
            else:
                self.health_status = HealthStatus.RECOVERED
                self.was_infected = True
                self.color = GREEN

    def update_status(self, time_step):
        self.infection_timer += time_step
        if self.infection_timer >= 1000:  # Nur alle 1 Sekunde updaten
            self.days_infected += 1
            self.infection_timer = 0
        match self.health_status:
            case HealthStatus.RECOVERED:
                print("Person is recovered.")
            case HealthStatus.DEAD:
                print("Person is dead and no longer moving.")


class Simulation:
    def __init__(self,population_size=100):
        self.population_size = population_size
        self.population = [Individuum() for _ in range(self.population_size)]
        self.reset_button_rect = pg.Rect(screen_width - 120,10,100,40)
        self.infect_button_rect = pg.Rect(screen_width - 120,60,100,40)
        self.simulation_days = 0
        self.day_timer = 0
        self.infection_radius = 10  # Radius, in dem eine Infektion stattfinden kann
        self.infection_chance = 0.5  # Wahrscheinlichkeit einer Infektion

    def reset_population(self):
        self.population = [Individuum() for _ in range(self.population_size)]
        self.simulation_days = 0

    def infect_random_person(self):
        susceptible_person = [p for p in self.population if p.health_status == HealthStatus.SUSCEPTIBLE]
        if susceptible_person:
            random.choice(susceptible_person).infect()

    def update_population(self, time_step):
        for person in self.population:
            person.move(time_step)
            if person.health_status == HealthStatus.INFECTED:
                person.update_status(time_step)
                person.recover_or_die()

                self.spread_infection(person)

        self.day_timer += time_step
        if self.day_timer >= 1000:
            self.simulation_days += 1
            self.day_timer = 0

    def spread_infection(self, infected_person):
        for other_person in self.population:
            if other_person.health_status == HealthStatus.SUSCEPTIBLE:
                distance = math.sqrt((infected_person.x - other_person.x)**2 + (infected_person.y - other_person.y)**2)
                if distance < self.infection_radius:
                    # Infektionswahrscheinlichkeit anwenden
                    if random.random() < self.infection_chance:
                        other_person.infect()
    
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
        screen.blit(font.render(f"Days: {self.simulation_days}", True, WHITE), (10, 90))  # Tage-Label
    
    def draw_buttons(self):
        # Reset-Button
        reset_button = pg.draw.rect(screen, GRAY, self.reset_button_rect)
        screen.blit(font.render("Reset", True, BLACK), (screen_width - 100, 20))

        # Infect-Button
        infect_button = pg.draw.rect(screen, GRAY, self.infect_button_rect)
        screen.blit(font.render("Infect", True, BLACK), (screen_width - 100, 70))

        return reset_button, infect_button
    
    def handle_click(self,mouse_pos):
        if self.reset_button_rect.collidepoint(mouse_pos):
            self.reset_population()
        if self.infect_button_rect.collidepoint(mouse_pos):
            self.infect_random_person()


def main():
    simulation = Simulation(population_size=1000)
    clock = pg.time.Clock()

    running = True

    while running:
        screen.fill(BLACK)
        time_step = clock.tick(30)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                simulation.handle_click(mouse_pos)


        simulation.update_population(time_step)
        simulation.draw_population()
       

        susceptible,infected,recovered,dead = simulation.count_status()
        simulation.draw_lables(susceptible,infected,recovered,dead)
        simulation.draw_buttons()

        pg.display.flip()
        
    
    pg.quit()

if __name__ == "__main__":
    main()
