import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 600))

running = True

cellSize = 20
snake = [(300, 200), (280, 200), (260, 200)]

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
                    directionY = 0
                    directionX = 1
            if (event.key == pygame.K_LEFT):
                if not(directionX == 1 and directionY == 0):
                    directionY = 0
                    directionX = -1

    screen.fill("dark blue")

    for s in snake:
        pygame.draw.rect(screen, "green", (s[0], s[1],  cellSize, cellSize))
                
    newHead = (snake[0][0] + directionX * cellSize, snake[0][1] + directionY * cellSize)
    snake.insert(0, newHead)
    snake.pop()

    pygame.display.flip()
    clock.tick(6)

pygame.quit()   

