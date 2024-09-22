import pygame as pg
from simulation import Simulation
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Virus SIM")

# Schriftarten
font = pg.font.SysFont(None, 24)

def main():
    simulation = Simulation()
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
        simulation.draw_population(screen)

        simulation.draw_virus_info(screen, font)

        susceptible, sick, infected, recovered, dead = simulation.count_status()
        simulation.draw_lables(screen, font, susceptible, sick, infected, recovered, dead)
        simulation.draw_buttons(screen, font)

        if simulation.show_grid:
            simulation.draw_grid(screen)

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
