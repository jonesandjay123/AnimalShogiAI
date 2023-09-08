import pygame
import sys

# 初始化pygame
pygame.init()

# 設置窗口的寬度和高度
WIDTH, HEIGHT = 900, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

# 設置顏色
DARK_WOOD = (101, 67, 33)
LIGHT_WOOD = (205, 133, 63)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 設置棋盤參數
ROWS, COLS = 4, 3
SQUARE_SIZE = 100

# 計算新的起點來將棋盤置中
GRID_OFFSET_X = 150
GRID_OFFSET_Y = (HEIGHT - (ROWS * SQUARE_SIZE)) // 2


def draw_grid():
    # 繪製棋盤的網格線
    for row in range(ROWS + 1):
        pygame.draw.line(window, BLACK,
                         (GRID_OFFSET_X, GRID_OFFSET_Y + row * SQUARE_SIZE),
                         (GRID_OFFSET_X + COLS * SQUARE_SIZE, GRID_OFFSET_Y + row * SQUARE_SIZE), 1)
    for col in range(COLS + 1):
        pygame.draw.line(window, BLACK,
                         (GRID_OFFSET_X + col * SQUARE_SIZE, GRID_OFFSET_Y),
                         (GRID_OFFSET_X + col * SQUARE_SIZE, GRID_OFFSET_Y + ROWS * SQUARE_SIZE), 1)

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
        window.blit(label_surface,
                    (GRID_OFFSET_X + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 10, GRID_OFFSET_Y - 30))
    # 繪製行標籤
    labels_row = ['1', '2', '3', '4']
    for i, label in enumerate(labels_row):
        label_surface = font.render(label, True, BLACK)
        window.blit(label_surface,
                    (GRID_OFFSET_X - 30, GRID_OFFSET_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 10))


def draw_buttons():
    font = pygame.font.Font('assets/NotoSansTC-Bold.ttf', 24)
    button_width, button_height = 60, 40

    # 繪製“對局”按鈕
    duel_button = pygame.Rect(
        GRID_OFFSET_X - button_width - 60, HEIGHT // 2 - 60, button_width, button_height)
    pygame.draw.rect(window, LIGHT_WOOD, duel_button)
    duel_label = font.render('對局', True, BLACK)
    window.blit(duel_label, (duel_button.x + 8, duel_button.y + 4))

    # 繪製“擺盤”按鈕
    setup_button = pygame.Rect(
        GRID_OFFSET_X - button_width - 60, HEIGHT // 2 + 20, button_width, button_height)
    pygame.draw.rect(window, LIGHT_WOOD, setup_button)
    setup_label = font.render('擺盤', True, BLACK)
    window.blit(setup_label, (setup_button.x + 8, setup_button.y + 4))
    return duel_button, setup_button


def main():
    # 載入和調整背景圖片的大小
    background = pygame.image.load('assets/background.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    run = True
    while run:
        duel_button, setup_button = draw_buttons()  # Get the button rectangles
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # A mouse button was pressed
                # The duel button was clicked
                if duel_button.collidepoint(pygame.mouse.get_pos()):
                    print("對局按鈕被點擊")
                # The setup button was clicked
                elif setup_button.collidepoint(pygame.mouse.get_pos()):
                    print("擺盤按鈕被點擊")

        # 繪製背景圖片
        window.blit(background, (0, 0))

        draw_grid()
        draw_labels()
        draw_buttons()
        draw_grid()
        draw_labels()
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
