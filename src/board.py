import pygame
import sys

# 初始化pygame
pygame.init()

# 設置窗口的寬度和高度
WIDTH, HEIGHT = 300, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))

# 設置顏色
DARK_WOOD = (101, 67, 33)
LIGHT_WOOD = (205, 133, 63)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 設置棋盤參數
ROWS, COLS = 4, 3
SQUARE_SIZE = WIDTH // COLS


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * SQUARE_SIZE, row *
                               SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            if (row + col) % 2 == 0:
                pygame.draw.rect(window, LIGHT_WOOD, rect)
            else:
                pygame.draw.rect(window, DARK_WOOD, rect)

    # 繪製虛線邊框
    pygame.draw.line(window, BLACK, (0, 0), (WIDTH, 0), 1)
    pygame.draw.line(window, BLACK, (0, 0), (0, HEIGHT), 1)
    pygame.draw.line(window, BLACK, (WIDTH, 0), (WIDTH, HEIGHT), 1)
    pygame.draw.line(window, BLACK, (0, HEIGHT), (WIDTH, HEIGHT), 1)


def draw_labels():
    font = pygame.font.SysFont(None, 24)

    # 繪製列標籤
    labels_col = ['A', 'B', 'C']
    for i, label in enumerate(labels_col):
        label_surface = font.render(label, True, BLACK)
        window.blit(label_surface, (i * SQUARE_SIZE +
                    SQUARE_SIZE // 2 - 10, 10))

    # 繪製行標籤
    labels_row = ['1', '2', '3', '4']
    for i, label in enumerate(labels_row):
        label_surface = font.render(label, True, BLACK)
        window.blit(label_surface,
                    (10, i * SQUARE_SIZE + SQUARE_SIZE // 2 - 10))


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_grid()
        draw_labels()
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
