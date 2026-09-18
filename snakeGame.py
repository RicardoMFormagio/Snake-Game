import pygame
import random

pygame.init()

screenWidth = 1000
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Tamanho de cada célula da grade; tudo se move em múltiplos desse valor.
cellSize = 20
# Lista de posições (x, y) da cobra; o primeiro item é a cabeça.
snake = [(300, 200), (280, 200), (260, 200)]
# Direção do movimento da cabeça a cada passo (-1, 0 ou 1 por eixo).
directionX = 1
directionY = 0

titleFont = font = pygame.font.SysFont(None, 64)
font = pygame.font.SysFont(None, 36)

score = 0
clock = pygame.time.Clock()
gameState = "menu" 

def foodPositioner():
    # Sorteia uma posição alinhada à grade de células.
    columns = screenWidth // cellSize
    lines = screenHeight // cellSize
    foodX = random.randint(0, columns - 1) * cellSize
    foodY = random.randint(0, lines - 1) * cellSize
    return (foodX, foodY)

def reset():
    # "global" é necessário para alterar as variáveis definidas fora da função.
    global score
    global snake
    global directionX
    global directionY
    global food
    global gameState
    score = 0
    snake = [(300, 200), (280, 200), (260, 200)]
    directionX = 1
    directionY = 0
    food = foodPositioner()
    gameState = "playing"

food = foodPositioner()
running = True
gameState = "menu"
while running:  # Loop principal: cada iteração é um quadro (frame)

    if gameState == "playing":

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Bloqueia a tecla oposta à direção atual, evitando virar 180°
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

        # Nova posição da cabeça, somando a direção à posição atual.
        newHead = (snake[0][0] + directionX * cellSize, snake[0][1] + directionY * cellSize)

        # Game over: cabeça saiu da tela...
        if newHead[0] >= screenWidth or newHead[0] < 0:
            gameState = "gameOver"
        if newHead[1] >= screenHeight or newHead[1] < 0:
            gameState = "gameOver"
        # ...ou colidiu com o próprio corpo.
        for s in snake:
            if newHead == s:
                gameState = "gameOver"

        screen.fill("dark blue")
        pygame.draw.rect(screen, "red", (food[0], food[1],  cellSize, cellSize))
        text = font.render(f"Score: {score}", True, "white") 
        screen.blit(text, (10, 10))        

        # Insere a nova cabeça: é assim que a cobra se move.
        snake.insert(0, newHead)
        if snake[0] != food:
            # Sem comer, remove a cauda (movimento sem crescer).
            snake.pop()
        else:
            # Ao comer, mantém a cauda (cobra cresce) e sorteia nova comida.
            food = foodPositioner()
            score += 100

        for s in snake:
                pygame.draw.rect(screen, "green", (s[0], s[1],  cellSize, cellSize))

    elif gameState == "menu":   
        menuEvents = pygame.event.get()
        screen.fill("black")
        
        titleText = titleFont.render("SNAKE GAME", True, "white")
        titleRect = titleText.get_rect(center=(screenWidth // 2, (screenHeight // 2)-100))
        screen.blit(titleText, titleRect)
 
        text1 = font.render("Press ENTER to play", True, "white")
        text2 = font.render("Press ESC to close", True, "white")

        rect1 = text1.get_rect(center=(screenWidth // 2, (screenHeight // 2)-50))
        rect2 = text2.get_rect(center=(screenWidth // 2, (screenHeight // 2)))
        screen.blit(text1, rect1)
        screen.blit(text2, rect2)

        pygame.display.flip()
        
        for event in menuEvents:
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN):
                    reset()
                    gameState = "playing"
                    break
                if (event.key == pygame.K_ESCAPE):
                    running = False
                    gameState = ""
                    break
        clock.tick(8)

    # Tela de game over: espera o jogador reiniciar (ENTER) ou sair (ESC).
    elif gameState == "gameOver":
        gameOverEvents = pygame.event.get()

        text1 = titleFont.render("GAMEOVER", True, "white")
        rect = text1.get_rect(center=(screenWidth // 2, (screenHeight // 2)-50))
        screen.blit(text1, rect)

        text4 = font.render(f"Final Score: {score}", True, "white")
        rect = text4.get_rect(center=(screenWidth // 2, (screenHeight // 2)))
        screen.blit(text4, rect)

        text2 = font.render("Press ENTER to go back to menu", True, "white")
        rect = text2.get_rect(center=(screenWidth // 2, (screenHeight // 2)+100))
        screen.blit(text2, rect)

        text3 = font.render("Press ESC to close", True, "white")
        rect = text3.get_rect(center=(screenWidth // 2, (screenHeight // 2)+150))
        screen.blit(text3, rect)

        pygame.display.flip()
        for event in gameOverEvents:
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN):
                    reset()
                    gameState = "menu"
                    break
                if (event.key == pygame.K_ESCAPE):
                    running = False
                    gameState = ""
                    break
        clock.tick(8)

    pygame.display.flip()  # Mostra na tela tudo o que foi desenhado neste quadro
    clock.tick(8)  # Limita o jogo a 8 quadros por segundo, controlando a velocidade da cobra

pygame.quit()

