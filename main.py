import pygame

def main():
    pygame.init()
    
    win = pygame.display.set_mode((1200, 700))

    pygame.display.set_caption("RSXIV")
    run = True

    # object
    width = 20

    # current cord
    x = 250
    y = 250
    vel = 5

    while run:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > width:
            x -= vel
        if keys[pygame.K_RIGHT] and x < 500 - width:
            x += vel
        if keys[pygame.K_UP] and y > width:
            y -= vel
        if keys[pygame.K_DOWN] and y < 500 - width:
            y += vel

        win.fill((0, 0, 0))
        pygame.draw.circle(win, (255, 0, 0), [x, y], width, 0)

        pygame.display.update()

    pygame.quit()

main()
