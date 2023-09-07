import pygame
import sys

# 初始化pygame
pygame.init()

# 設置窗口的寬度和高度
WIDTH, HEIGHT = 300, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))

# 設置顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 設置棋盤參數
ROWS, COLS = 4, 3
SQUARE_SIZE = WIDTH // COLS


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * SQUARE_SIZE, row *
                               SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            if (row + col) % 2 == 0:
                pygame.draw.rect(window, WHITE, rect)
            else:
                pygame.draw.rect(window, BLACK, rect)
            pygame.draw.line(window, BLACK, (col * SQUARE_SIZE,
                             0), (col * SQUARE_SIZE, HEIGHT))
        pygame.draw.line(window, BLACK, (0, row * SQUARE_SIZE),
                         (WIDTH, row * SQUARE_SIZE))


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_grid()
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
