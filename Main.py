from Buttons import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        screen.fill((255, 255, 255))

        button(10, 10, "Standard Simulation", 200, 60, (79, 148, 205), (99, 184, 255), 1)
        button(250, 10, "Social Distancing 20%", 220, 60, (79, 148, 205), (99, 184, 255), 1)
        button(10, 100, "Social Distancing 60%", 220, 60, (79, 148, 205), (99, 184, 255), 1)
        button(10, 200, "Exit", 100, 60, (205, 0, 0), (255, 0, 0), 1)
        button(250, 100, "Lockdown", 120, 60, (205, 0, 0), (255, 0, 0), 1)
        pygame.display.update()
    pygame.quit()


main()
