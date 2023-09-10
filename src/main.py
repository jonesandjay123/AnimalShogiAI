import pygame
import sys
from board import draw_grid, draw_storage_area, draw_labels, draw_buttons, draw_pieces
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
        duel_button, setup_button = draw_buttons(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEMOTION:  # The mouse was moved
                game.mouse_pos = event.pos  # Update the mouse position on mouse move
                if game.selected_piece and game.setup_mode:
                    # Update the position of the selected piece to follow the mouse
                    game.selected_piece.update_position(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:  # A mouse button was pressed
                # The duel button was clicked
                if duel_button.collidepoint(pygame.mouse.get_pos()):
                    print("對局按鈕被點擊")
                    game.create_initial_board_config()  # 初始化為對局模式的配置
                    game.setup_mode = False  # Set the mode to normal game mode
                # The setup button was clicked
                elif setup_button.collidepoint(pygame.mouse.get_pos()):
                    print("擺盤按鈕被點擊")
                    game.initialize_setup_mode()  # 清空棋盤，進入擺盤模式
                    game.setup_mode = True   # Set the mode to setup mode
                else:
                    # Try to select a piece if we are in setup mode
                    if game.setup_mode:
                        game.select_piece(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:  # A mouse button was released
                if game.selected_piece and game.setup_mode:
                    # Place the selected piece at the current mouse position
                    game.place_piece(pygame.mouse.get_pos())
                    # Reset the selected piece
                    game.selected_piece = None
                    game.selected_piece_origin = None
            elif event.type == pygame.KEYDOWN:  # A key was pressed
                if event.key == pygame.K_t:  # The "T" key was pressed
                    piece = game.get_piece_at_pos(pygame.mouse.get_pos())  # Get the piece under the mouse
                    if piece and piece.piece_type in ["C", "H"]:  # Check if it's a chick or a hen
                        game.toggle_chick_to_hen(piece)  # Toggle the piece

        # 繪製背景圖片
        window.blit(background, (0, 0))

        draw_grid(window)
        draw_storage_area(window)  # Draw the storage areas
        draw_labels(window)
        draw_buttons(window)
        draw_pieces(window, game.board_config, game.storage_area_player1,
                    game.storage_area_player2, game.selected_piece, game.mouse_pos)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
