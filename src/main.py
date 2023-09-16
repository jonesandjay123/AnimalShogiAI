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

    available_moves = []
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEMOTION:  # 當滑鼠移動時
                game.mouse_pos = event.pos  # 更新滑鼠位置
                if game.selected_piece:
                    game.selected_piece.update_position(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 當滑鼠按下時
                # 對局按鈕被點擊
                if duel_button.collidepoint(pygame.mouse.get_pos()):
                    print("對局按鈕被點擊")
                    game.create_initial_board_config()  # 初始化為對局模式的配置
                    game.setup_mode = False
                    game.show_return_to_normal_game_route_button = False
                # 擺盤按鈕被點擊
                elif setup_button.collidepoint(pygame.mouse.get_pos()):
                    print("擺盤按鈕被點擊")
                    setup.initialize_setup_mode() # 清空棋盤，進入擺盤模式
                    game.setup_mode = True
                    game.show_return_to_normal_game_route_button = False
                else:
                    # 如果在擺盤模式下，則點擊了一個棋子
                    if game.setup_mode:
                        available_moves = game.select_piece(pygame.mouse.get_pos())
                    else:
                        # 如果在正常對局模式下，則點擊了一個棋子
                        available_moves = game.select_piece(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:  # 當滑鼠放開時
                if game.selected_piece and game.setup_mode:
                    # 把棋子放在滑鼠位置
                    setup.place_piece(pygame.mouse.get_pos())
                    # 重置選擇的棋子
                    game.selected_piece = None
                    game.selected_piece_origin = None
            elif event.type == pygame.KEYDOWN:  # 當按下鍵盤按鈕時
                if event.key == pygame.K_t:  # "Ｔ" 鍵被按下
                    piece = game.get_piece_at_pos(pygame.mouse.get_pos())  # 取得滑鼠位置的棋子
                    if piece and piece.piece_type in ["C", "H"]:  # 檢驗棋子是否為小雞或母雞
                        setup.toggle_chick_to_hen(piece)  # 切換小雞和母雞

        # 繪製背景圖片
        window.blit(background, (0, 0))

        # 立刻繪製按鈕
        duel_button, setup_button, upper_turn_button, lower_turn_button = draw_buttons(window, game.show_return_to_normal_game_route_button)

        draw_grid(window)
        # draw_storage_area(window)  # 繪製儲存區的格線
        draw_labels(window)
        draw_available_moves(window, available_moves)
        draw_pieces(window, game.board_config, game.storage_area_player1,
                    game.storage_area_player2, game.selected_piece, game.mouse_pos)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
