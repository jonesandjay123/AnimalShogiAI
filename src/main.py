import pygame
import sys
from board import draw_grid, draw_available_moves, draw_labels, draw_buttons, draw_pieces
from const import WIDTH, HEIGHT
from game import Game
from setup import SetupMode

def main():
    pygame.init()

    game = Game()  # 創建 Game 類的一個實例
    setup = SetupMode(game) 

    window = pygame.display.set_mode((WIDTH, HEIGHT))

    background = pygame.image.load('assets/background.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    run = True
    while run:
        for event in pygame.event.get():

            cursor_position = pygame.mouse.get_pos() # 獲取游標位置

            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEMOTION:  # 當滑鼠移動時
                game.mouse_pos = event.pos # 讓棋子得以跟著游標移動
                if game.selected_piece:
                    game.selected_piece.update_position(cursor_position)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 當滑鼠按下時
                # 對局按鈕被點擊
                if duel_button.collidepoint(cursor_position):
                    game.create_initial_board_config()  # 初始化為對局模式的配置
                    game.toggle_setup_mode(False)
                # 擺盤按鈕被點擊
                elif setup_button.collidepoint(cursor_position):
                    setup.initialize_setup_mode() # 清空棋盤，進入擺盤模式
                    game.toggle_setup_mode(True)
                # 非按鈕區域被點擊
                else:
                    game.click_on_piece(cursor_position)

            elif event.type == pygame.MOUSEBUTTONUP:  # 當滑鼠放開時(擺盤模式下的長壓拖曳釋放)
                if game.selected_piece and game.setup_mode:
                    setup.place_piece(cursor_position)
                    
            elif event.type == pygame.KEYDOWN:  # 當按下鍵盤按鈕時
                if event.key == pygame.K_t:  # "Ｔ" 鍵被按下
                    piece = game.get_piece_at_pos(cursor_position)
                    if piece and piece.piece_type in ["C", "H"]:  # 檢驗棋子是否為小雞或母雞
                        setup.toggle_chick_to_hen(piece)  # 切換小雞和母雞

        # 繪製背景圖片
        window.blit(background, (0, 0))

        # 立刻繪製按鈕
        duel_button, setup_button, upper_turn_button, lower_turn_button = draw_buttons(window, game.show_return_to_normal_game_route_button)

        draw_grid(window)
        # draw_storage_area(window)  # 繪製儲存區的格線
        draw_labels(window)       
        draw_pieces(window, game.board_config, game.storage_area_player1,
                    game.storage_area_player2, game.selected_piece, game.mouse_pos)
        draw_available_moves(window, game.available_moves)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
