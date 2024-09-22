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
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)


# Schriftarten
font = pg.font.SysFont(None, 24)

class HealthStatus(Enum):
    SUSCEPTIBLE = 1
    INFECTED = 2
    SICK = 3
    RECOVERED = 4
    DEAD = 5

class StatusColors(Enum):
    SUSCEPTIBLE: str = "blue"
    INFECTED: str = "red"
    SICK: str = "red"
    RECOVERED: str = "green"
    DEAD: str = "black"
    

class Individuum:
    def __init__(self, health: float = 100.0, resistance_chance: float = 0.2) -> None:
        self.health = health
        self.resistance_chance = resistance_chance  # Wahrscheinlichkeit resistent zu sein
        self.x = random.uniform(50, screen_width - 50)
        self.y = random.uniform(50, screen_height - 50)
        self.dx = random.uniform(-1, 1)  # Bewegung in x-Richtung
        self.dy = random.uniform(-1, 1)  # Bewegung in y-Richtung
        self.speed = random.uniform(1, 3)  # Geschwindigkeit
        self.health_status = HealthStatus.SUSCEPTIBLE
        self.days_infected = 0
        self.color = BLUE
        self.infection_timer = 0
        self.direction_change_timer = 0  # Timer für Richtungsänderung
        self.incubation_period = random.randint(4, 7)  # Inkubationszeit zwischen 2 und 5 Tagen
        

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
        if random.random() < self.resistance_chance:
            # Die Person ist resistent und wird nicht infiziert
            return
        if self.health_status == HealthStatus.SUSCEPTIBLE:
            self.health_status = HealthStatus.INFECTED
            
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
            if self.health_status == HealthStatus.INFECTED:
                self.color = ORANGE
            # Übergang von INFECTED zu SICK nach der Inkubationszeit
            if self.health_status == HealthStatus.INFECTED and self.days_infected >= self.incubation_period:
                self.health_status = HealthStatus.SICK
                

            # Wenn krank, Gesundheit verringern
            if self.health_status == HealthStatus.SICK:
                self.color = RED  # Rot signalisiert, dass die Person krank ist
                self.health -= random.uniform(0.5, 2.0)  # Verringert die Gesundheit
                if self.health <= 0:
                    self.health_status = HealthStatus.DEAD
                    self.color = GRAY

            # Genesungs- oder Todesprozess
            self.recover_or_die()


class Simulation:
    def __init__(self,population_size=100, cell_size=50):
        self.population_size = population_size
        self.population = [Individuum() for _ in range(self.population_size)]
        self.reset_button_rect = pg.Rect(screen_width - 120,10,100,40)
        self.infect_button_rect = pg.Rect(screen_width - 120,60,100,40)
        self.toggle_grid_button_rect = pg.Rect(screen_width - 120, 110, 100, 40)
        self.pause_button_rect = pg.Rect(screen_width - 120, 160, 100, 40)  # Pause/Start Button
        self.show_grid = False  # Grid-Ansicht standardmäßig ausgeschaltet
        self.simulation_days = 0
        self.day_timer = 0
        self.infection_radius = 10  # Radius, in dem eine Infektion stattfinden kann
        self.infection_chance = 0.5  # Wahrscheinlichkeit einer Infektion
        self.cell_size = cell_size  # Größe jeder Zelle im Raster
        self.grid_width = screen_width // self.cell_size
        self.grid_height = screen_height // self.cell_size
        self.simulation_paused = True  # Startet in pausiertem Zustand
        self.selected_individuum = None  # Das angeklickte Individuum

    def reset_population(self):
        self.population = [Individuum() for _ in range(self.population_size)]
        self.simulation_days = 0

    def infect_random_person(self):
        susceptible_person = [p for p in self.population if p.health_status == HealthStatus.SUSCEPTIBLE]
        if susceptible_person:
            random.choice(susceptible_person).infect()

    def toggle_pause(self):
        self.simulation_paused = not self.simulation_paused  # Wechsel zwischen Start/Pause


    def update_population(self, time_step):
        if self.simulation_paused:
            return  # Wenn die Simulation pausiert ist, überspringen wir die Aktualisierung
        grid = [[[] for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # Platziere jede Person in der entsprechenden Rasterzelle basierend auf ihrer Position
        for person in self.population:
            grid_x = int(person.x // self.cell_size)
            grid_y = int(person.y // self.cell_size)
            # Begrenze grid_x und grid_y, um Indexfehler zu vermeiden
            grid_x = min(max(grid_x, 0), self.grid_width - 1)
            grid_y = min(max(grid_y, 0), self.grid_height - 1)
            grid[grid_y][grid_x].append(person)

        # Aktualisiere jede Person und überprüfe Infektionen nur in benachbarten Zellen
        for person in self.population:
            person.move(time_step)
            if person.health_status == HealthStatus.INFECTED or person.health_status == HealthStatus.SICK:
                person.update_status(time_step)
                person.recover_or_die()
                self.spread_infection(person, grid)

        self.day_timer += time_step
        if self.day_timer >= 1000:
            self.simulation_days += 1
            self.day_timer = 0

    def spread_infection(self, infected_person, grid):
        if infected_person.health_status != HealthStatus.SICK:
            return  # Nur Kranke Personen können die Infektion verbreiten
    
        # Finde die Rasterzelle der infizierten Person
        grid_x = int(infected_person.x // self.cell_size)
        grid_y = int(infected_person.y // self.cell_size)

        # Begrenze grid_x und grid_y, um Indexfehler zu vermeiden
        grid_x = min(max(grid_x, 0), self.grid_width - 1)
        grid_y = min(max(grid_y, 0), self.grid_height - 1)

        # Überprüfe nur Personen in der gleichen Zelle und den benachbarten Zellen
        for dx in range(-1, 2):  # Überprüfe die Zelle selbst und die angrenzenden
            for dy in range(-1, 2):
                nx, ny = grid_x + dx, grid_y + dy
                if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                    for other_person in grid[ny][nx]:
                        if other_person.health_status == HealthStatus.SUSCEPTIBLE:
                            distance = math.sqrt((infected_person.x - other_person.x)**2 + (infected_person.y - other_person.y)**2)
                            if distance < self.infection_radius:
                                if random.random() < self.infection_chance:
                                    other_person.infect()

    
    def draw_population(self):
        for person in self.population:
            pg.draw.circle(screen, person.color,(int(person.x), int(person.y)),5)
        # Hebe das ausgewählte Individuum hervor
        if self.selected_individuum:
            pg.draw.circle(screen, WHITE, (int(self.selected_individuum.x), int(self.selected_individuum.y)), 8, 2)
    
    def draw_grid(self):
        for x in range(0, screen_width, self.cell_size):
            pg.draw.line(screen, GRAY, (x, 0), (x, screen_height))
        for y in range(0, screen_height, self.cell_size):
            pg.draw.line(screen, GRAY, (0, y), (screen_width, y))

    def count_status(self):
        susceptible = sum(1 for p in self.population if p.health_status == HealthStatus.SUSCEPTIBLE)
        infected = sum(1 for p in self.population if p.health_status == HealthStatus.INFECTED)
        sick = sum(1 for p in self.population if p.health_status == HealthStatus.SICK)
        recovered = sum(1 for p in self.population if p.health_status == HealthStatus.RECOVERED)
        dead = sum(1 for p in self.population if p.health_status == HealthStatus.DEAD)

        return susceptible, infected, sick, recovered, dead

    def draw_lables(self, susceptible, sick, infected, recovered, dead):
        screen.blit(font.render(f"Susceptible: {susceptible}", True, WHITE), (10,10))
        screen.blit(font.render(f"Infected: {infected}", True, WHITE), (10,50))
        screen.blit(font.render(f"Sick: {sick}", True, WHITE), (10,30))
        screen.blit(font.render(f"Recovered: {recovered}", True, WHITE), (10,70))
        screen.blit(font.render(f"Dead: {dead}", True, WHITE), (10,90))
        screen.blit(font.render(f"Days: {self.simulation_days}", True, WHITE), (10, 110))  # Tage-Label

        if self.selected_individuum:
            # Zeige die Informationen des ausgewählten Individuums an
            screen.blit(font.render(f"Selected Individuum - Health: {self.selected_individuum.health:.2f}", True, WHITE), (10, 130))
            screen.blit(font.render(f"Status: {self.selected_individuum.health_status.name}", True, WHITE), (10, 150))
            screen.blit(font.render(f"Days Infected: {self.selected_individuum.days_infected}", True, WHITE), (10, 170))
            screen.blit(font.render(f"Resistance Chance: {self.selected_individuum.resistance_chance}", True, WHITE), (10, 190))
    
    def draw_buttons(self):
        # Reset-Button
        pg.draw.rect(screen, GRAY, self.reset_button_rect)
        screen.blit(font.render("Reset", True, BLACK), (screen_width - 100, 20))

        # Infect-Button
        pg.draw.rect(screen, GRAY, self.infect_button_rect)
        screen.blit(font.render("Infect", True, BLACK), (screen_width - 100, 70))

        pg.draw.rect(screen, GRAY, self.toggle_grid_button_rect)
        screen.blit(font.render("I/O Grid", True, BLACK), (screen_width - 100, 120))

        # Pause/Start Button
        pg.draw.rect(screen, GRAY, self.pause_button_rect)
        screen.blit(font.render("Start" if self.simulation_paused else "Pause", True, BLACK), (screen_width - 100, 170))
    
    def handle_click(self,mouse_pos):
        if self.reset_button_rect.collidepoint(mouse_pos):
            self.reset_population()
        elif self.infect_button_rect.collidepoint(mouse_pos):
            self.infect_random_person()
        elif self.toggle_grid_button_rect.collidepoint(mouse_pos):
            self.show_grid = not self.show_grid  # Grid ein-/ausschalten
        elif self.pause_button_rect.collidepoint(mouse_pos):
            self.toggle_pause()  # Pause/Start der Simulation
        else:
            # Prüfe, ob ein Individuum angeklickt wurde
            for person in self.population:
                if math.sqrt((mouse_pos[0] - person.x)**2 + (mouse_pos[1] - person.y)**2) <= 5:
                    self.selected_individuum = person  # Setze das ausgewählte Individuum
                    break


def main():
    simulation = Simulation(population_size=100, cell_size=20)
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
       

        susceptible,sick,infected,recovered,dead = simulation.count_status()
        simulation.draw_lables(susceptible,sick,infected,recovered,dead)
        simulation.draw_buttons()

        if simulation.show_grid:
            simulation.draw_grid()

        pg.display.flip()
        
    
    pg.quit()

if __name__ == "__main__":
    main()
