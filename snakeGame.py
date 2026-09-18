import pygame
import random

pygame.init()

screenWidth = 1000
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Tamanho de cada "quadrado" do jogo. Tudo (cobra, comida, movimento) se move em múltiplos
# desse valor, o que mantém a cobra sempre alinhada a uma grade invisível.
cellSize = 20
# A cobra é uma lista de posições (x, y). O primeiro item é a cabeça.
snake = [(300, 200), (280, 200), (260, 200)]
# directionX/Y indicam para onde a cabeça se move a cada passo (-1, 0 ou 1 em cada eixo).
directionX = 1
directionY = 0

score = 0
clock = pygame.time.Clock()
gameState = "playing" 

def foodPositioner():
    # Divide a tela em colunas/linhas do tamanho da célula para sortear uma posição
    # que sempre caia exatamente em cima da grade (evita comida "desalinhada").
    columns = screenWidth // cellSize
    lines = screenHeight // cellSize
    foodX = random.randint(0, columns - 1) * cellSize
    foodY = random.randint(0, lines - 1) * cellSize
    return (foodX, foodY)

def reset():
    # Precisa de "global" porque essas variáveis foram criadas fora da função:
    # sem isso, o Python criaria cópias locais e o reset não afetaria o jogo de verdade.
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
while running:  # Loop principal do jogo: cada iteração é um "quadro" (frame)

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Cada "if" checa se a tecla pressionada é oposta à direção atual.
            # Isso impede que a cobra vire 180° sobre si mesma e "morra" instantaneamente
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

    # Calcula onde a nova cabeça vai ficar, somando a direção atual à posição da cabeça atual.
    newHead = (snake[0][0] + directionX * cellSize, snake[0][1] + directionY * cellSize)

    # Condições de game over: a nova cabeça saiu da tela (eixo X ou Y)...
    if newHead[0] >= screenWidth or newHead[0] < 0:
        gameState = "gameOver"
    if newHead[1] >= screenHeight or newHead[1] < 0:
        gameState = "gameOver"
    # ...ou a nova cabeça bateu em alguma parte do próprio corpo da cobra.
    for s in snake:
        if newHead == s:
            gameState = "gameOver"

    screen.fill("dark blue")
    pygame.draw.rect(screen, "red", (food[0], food[1],  cellSize, cellSize))
    font = pygame.font.SysFont(None, 36)  
    text = font.render(f"Score: {score}", True, "white") 
    screen.blit(text, (10, 10))        

    # Adiciona a nova cabeça na frente da lista: é assim que a cobra "anda".
    snake.insert(0, newHead)
    if snake[0] != food:
        # Se não comeu, remove o último segmento (a cauda), simulando movimento
        # sem crescer: entra uma célula na frente, sai uma célula atrás.
        snake.pop()
    else:
        # Se comeu, não remove a cauda (a cobra cresce) e sorteia nova comida.
        food = foodPositioner()
        score += 100

    for s in snake:
            pygame.draw.rect(screen, "green", (s[0], s[1],  cellSize, cellSize))

    # Loop de pausa exibido quando o jogo termina: fica travado aqui esperando
    # o jogador decidir entre reiniciar (ENTER) ou sair (ESC).
    while gameState == "gameOver":
        gameOverEvents = pygame.event.get()
        font = pygame.font.SysFont(None, 36)
        text = font.render("GAMEOVER - press ENTER to play again or ESC to close", True, "white")
        screen.blit(text, (150, 300))
        pygame.display.flip()
        for event in gameOverEvents:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN):
                    reset()
                    gameState = "playing"
                    break
                if (event.key == pygame.K_ESCAPE):
                    running = False
                    gameState = ""
                    break
        clock.tick(8)

    pygame.display.flip()  # Mostra na tela tudo o que foi desenhado neste quadro
    clock.tick(8)  # Limita o jogo a 8 quadros por segundo, controlando a velocidade da cobra

pygame.quit()

