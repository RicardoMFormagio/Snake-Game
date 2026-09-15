import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 600))

running = True

cellSize = 20
snakeX = 300
snakeY = 200

directionX = 1
directionY = 0
clock = pygame.time.Clock()

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP):
                if not(directionX == 0 and directionY == 1):
                    directionY = -1
                    directionX = 0
            if (event.key == pygame.K_DOWN):
                if not(directionX == 0 and directionY == -1):
                    directionY = 1
                    directionX = 0
            if (event.key == pygame.K_RIGHT):
                if not(directionX == -1 and directionY == 0):
                    directionY = 1
                    directionX = 0

                


    screen.fill("dark blue")
    pygame.draw.rect(screen, "green", (snakeX, snakeY, cellSize, cellSize))

    snakeX += directionX * cellSize
    snakeY += directionY * cellSize

    pygame.display.flip()
    clock.tick(6)

pygame.quit()   

