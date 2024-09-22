import math
import random
from individuum import Individuum, HealthStatus
import pygame as pg
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, 
    POPULATION_SIZE, INFECTION_RADIUS, INFECTION_CHANCE,
    WHITE, GRAY, BLACK
)


class Simulation:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH  # Stelle sicher, dass diese gesetzt werden
        self.screen_height = SCREEN_HEIGHT  # Stelle sicher, dass diese gesetzt werden
        self.population = [Individuum(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT) for _ in range(POPULATION_SIZE)]
        self.reset_button_rect = pg.Rect(SCREEN_WIDTH - 120, 10, 100, 40)
        self.infect_button_rect = pg.Rect(SCREEN_WIDTH - 120, 60, 100, 40)
        self.toggle_grid_button_rect = pg.Rect(SCREEN_WIDTH - 120, 110, 100, 40)
        self.pause_button_rect = pg.Rect(SCREEN_WIDTH - 120, 160, 100, 40)
        self.show_grid = False
        self.simulation_days = 0
        self.day_timer = 0
        self.infection_radius = INFECTION_RADIUS
        self.infection_chance = INFECTION_CHANCE
        self.cell_size = CELL_SIZE
        self.grid_width = SCREEN_WIDTH // self.cell_size
        self.grid_height = SCREEN_HEIGHT // self.cell_size
        self.simulation_paused = True
        self.selected_individuum = None

    def reset_population(self):
        self.population = [Individuum(screen_width=self.screen_width, screen_height=self.screen_height) for _ in range(self.population_size)]
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
            person.move(time_step, self.screen_width, self.screen_height)
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

    def draw_population(self, screen):
        for person in self.population:
            pg.draw.circle(screen, person.color, (int(person.x), int(person.y)), 5)
        # Hebe das ausgewählte Individuum hervor
        if self.selected_individuum:
            pg.draw.circle(screen, WHITE, (int(self.selected_individuum.x), int(self.selected_individuum.y)), 8, 2)

    def draw_grid(self, screen):
        for x in range(0, self.screen_width, self.cell_size):
            pg.draw.line(screen, WHITE, (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, self.cell_size):
            pg.draw.line(screen, WHITE, (0, y), (self.screen_width, y))

    def count_status(self):
        susceptible = sum(1 for p in self.population if p.health_status == HealthStatus.SUSCEPTIBLE)
        infected = sum(1 for p in self.population if p.health_status == HealthStatus.INFECTED)
        sick = sum(1 for p in self.population if p.health_status == HealthStatus.SICK)
        recovered = sum(1 for p in self.population if p.health_status == HealthStatus.RECOVERED)
        dead = sum(1 for p in self.population if p.health_status == HealthStatus.DEAD)

        return susceptible, infected, sick, recovered, dead

    def draw_lables(self, screen, font, susceptible, sick, infected, recovered, dead):
        screen.blit(font.render(f"Susceptible: {susceptible}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Infected: {infected}", True, WHITE), (10, 50))
        screen.blit(font.render(f"Sick: {sick}", True, WHITE), (10, 30))
        screen.blit(font.render(f"Recovered: {recovered}", True, WHITE), (10, 70))
        screen.blit(font.render(f"Dead: {dead}", True, WHITE), (10, 90))
        screen.blit(font.render(f"Days: {self.simulation_days}", True, WHITE), (10, 110))  # Tage-Label

        if self.selected_individuum:
            # Zeige die Informationen des ausgewählten Individuums an
            screen.blit(font.render(f"Selected Individuum - Health: {self.selected_individuum.health:.2f}", True, WHITE), (10, 130))
            screen.blit(font.render(f"Status: {self.selected_individuum.health_status.name}", True, WHITE), (10, 150))
            screen.blit(font.render(f"Days Infected: {self.selected_individuum.days_infected}", True, WHITE), (10, 170))
            screen.blit(font.render(f"Resistance Chance: {self.selected_individuum.resistance_chance}", True, WHITE), (10, 190))

    def draw_buttons(self, screen, font):
        # Reset-Button
        pg.draw.rect(screen, GRAY, self.reset_button_rect)
        screen.blit(font.render("Reset", True, BLACK), (self.screen_width - 100, 20))

        # Infect-Button
        pg.draw.rect(screen, GRAY, self.infect_button_rect)
        screen.blit(font.render("Infect", True, BLACK), (self.screen_width - 100, 70))

        pg.draw.rect(screen, GRAY, self.toggle_grid_button_rect)
        screen.blit(font.render("I/O Grid", True, BLACK), (self.screen_width - 100, 120))

        # Pause/Start Button
        pg.draw.rect(screen, GRAY, self.pause_button_rect)
        screen.blit(font.render("Start" if self.simulation_paused else "Pause", True, BLACK), (self.screen_width - 100, 170))

    def handle_click(self, mouse_pos):
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
