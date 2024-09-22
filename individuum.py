from enum import Enum
import math
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STATUS_COLORS, 
    MIN_INCUBATION_PERIOD, MAX_INCUBATION_PERIOD, 
    RESISTANCE_CHANCE, MIN_SPEED, MAX_SPEED, GRAY, GREEN, RED
)
from virus import Virus


class HealthStatus(Enum):
    SUSCEPTIBLE = 1
    INFECTED = 2
    SICK = 3
    RECOVERED = 4
    DEAD = 5

class Individuum:
    def __init__(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, health: float = 100.0) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.health = health
        self.resistance_chance = RESISTANCE_CHANCE
        self.x = random.uniform(50, screen_width - 50)
        self.y = random.uniform(50, screen_height - 50)
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self.speed = random.uniform(MIN_SPEED, MAX_SPEED)
        self.health_status = HealthStatus.SUSCEPTIBLE
        self.days_infected = 0
        self.color = STATUS_COLORS["SUSCEPTIBLE"]
        self.infection_timer = 0
        self.direction_change_timer = 0
        self.incubation_period = random.randint(MIN_INCUBATION_PERIOD, MAX_INCUBATION_PERIOD)
        self.virus = None  # No virus by default

    def update_color(self):
        # Die Farbe wird direkt auf self.color gesetzt, ohne Rückgabewert.
        self.color = STATUS_COLORS[self.health_status.name]
        

    def move(self, time_step, screen_width, screen_height):
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


    def infect(self, virus: Virus):
        if random.random() < self.resistance_chance:
            # Die Person ist resistent und wird nicht infiziert
            return
        if self.health_status == HealthStatus.SUSCEPTIBLE:
            self.health_status = HealthStatus.INFECTED
            self.virus = virus  # Associate the virus with the individual
            
            self.incubation = 0
            self.days_infected = 0
            self.infection_timer = 0

    def recover_or_die(self):
        if self.health_status == HealthStatus.SICK and self.days_infected >= 14:
            if random.random() < self.virus.mortality_rate:
                self.health_status = HealthStatus.DEAD
                self.color = GRAY
            else:
                self.health_status = HealthStatus.RECOVERED
                self.color = GREEN

    def update_status(self, time_step):
        self.infection_timer += time_step
        self.update_color()
        if self.infection_timer >= 1000:  # Nur alle 1 Sekunde updaten
            self.days_infected += 1
            if self.health_status == HealthStatus.INFECTED:
                self.infection_timer = 0
                if random.random() < self.virus.virulence:
                    self.health_status = HealthStatus.SICK
                
            # Übergang von INFECTED zu SICK nach der Inkubationszeit
            if self.health_status == HealthStatus.INFECTED and self.days_infected >= self.incubation_period:
                self.health_status = HealthStatus.SICK
            # Wenn krank, Gesundheit verringern
            if self.health_status == HealthStatus.SICK:
                self.color = RED  # Rot signalisiert, dass die Person krank ist
                self.health -= random.uniform(0.5, 2.0)  # Verringert die Gesundheit
                if self.health <= 0:
                    self.health_status = HealthStatus.DEAD
                   
            # Genesungs- oder Todesprozess
            self.recover_or_die()


