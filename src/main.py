import pygame
import sys
from board import draw_grid, draw_squares, draw_labels, draw_buttons, draw_pieces
from const import WIDTH, HEIGHT
from game import Game


def main():
    # Initialize pygame
    pygame.init()

    game = Game()  # 創建 Game 類的一個實例

    # Set the dimensions of the window
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Load and scale the background image
    background = pygame.image.load('assets/background.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    run = True
    while run:
        duel_button, setup_button = draw_buttons(
            window)  # Get the button rectangles
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # A mouse button was pressed
                # The duel button was clicked
                if duel_button.collidepoint(pygame.mouse.get_pos()):
                    print("對局按鈕被點擊")
                    game.create_initial_board_config()  # 初始化為對局模式的配置
                # The setup button was clicked
                elif setup_button.collidepoint(pygame.mouse.get_pos()):
                    print("擺盤按鈕被點擊")
                    game.initialize_setup_mode()  # 清空棋盤，進入擺盤模式

        # 繪製背景圖片
        window.blit(background, (0, 0))

        draw_grid(window)
        draw_labels(window)
        draw_buttons(window)
        draw_pieces(window, game.board_config)  # Draw the pieces on the board

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
