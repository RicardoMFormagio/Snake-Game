import pygame
import random

pygame.init()

screenWidth = 1000
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

cellSize = 20
snake = [(300, 200), (280, 200), (260, 200)]
directionX = 1
directionY = 0

score = 0
clock = pygame.time.Clock()

def foodPositioner():
    columns = screenWidth // cellSize
    lines = screenHeight // cellSize
    foodX = random.randint(0, columns - 1) * cellSize
    foodY = random.randint(0, lines - 1) * cellSize
    return (foodX, foodY)

food = foodPositioner()
running = True
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

    newHead = (snake[0][0] + directionX * cellSize, snake[0][1] + directionY * cellSize)
    if newHead[0] >= screenWidth or newHead[0] < 0:
        running = False
    if newHead[1] >= screenHeight or newHead[1] < 0:
        running = False
    for s in snake:
        if newHead == s:
            running = False

    screen.fill("dark blue")
    pygame.draw.rect(screen, "red", (food[0], food[1],  cellSize, cellSize))
    font = pygame.font.SysFont(None, 36)  
    text = font.render(f"Score: {score}", True, "white") 
    screen.blit(text, (10, 10))        

    snake.insert(0, newHead)
    if snake[0] != food: 
        snake.pop()
    else:
        food = foodPositioner()
        score += 100
    
    for s in snake:
            pygame.draw.rect(screen, "green", (s[0], s[1],  cellSize, cellSize))

    pygame.display.flip()
    clock.tick(8)

pygame.quit()   

