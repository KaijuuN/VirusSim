
# Bildschirmgröße
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Zellgröße für das Grid
CELL_SIZE = 20

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# Simulationsparameter
POPULATION_SIZE = 1000  # Anzahl der Individuen
INFECTION_RADIUS = 10  # Radius für Infektionsübertragungen
INFECTION_CHANCE = 0.5  # Wahrscheinlichkeit einer Infektion
RESISTANCE_CHANCE = 0.2  # Wahrscheinlichkeit, dass ein Individuum resistent ist
RECOVERY_TIME = 14  # Anzahl der Tage bis zur Genesung oder zum Tod
MORTALITY_RATE = 0.01  # Sterberate bei kranken Individuen

# Geschwindigkeit der Individuen
MIN_SPEED = 2
MAX_SPEED = 5

# Inkubationszeit
MIN_INCUBATION_PERIOD = 4
MAX_INCUBATION_PERIOD = 7

# Farben abhängig vom Gesundheitsstatus
STATUS_COLORS = {
    "SUSCEPTIBLE": (0, 0, 255),  # BLUE
    "INFECTED": (255, 165, 0),   # ORANGE
    "SICK": (255, 0, 0),         # RED
    "RECOVERED": (0, 255, 0),    # GREEN
    "DEAD": (169, 169, 169)      # GRAY
}