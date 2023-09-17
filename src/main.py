import pygame
import pygame_gui
import sys
from board import create_scrolling_container, draw_control_buttons, draw_current_player, draw_grid, draw_available_moves, draw_labels, draw_buttons, draw_pieces
from const import WIDTH, HEIGHT
from game import Game
from setup import SetupMode

########################################
UI_VERTICAL_SCROLL_BAR_MOVED = 32866
########################################

def main():
    pygame.init()


    ########################################
    # 初始化UIManager
    ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    # 定義一個 pygame 矩形來設置 UIScrollingContainer 的位置和大小
    rect = pygame.Rect((550, 100), (300, 400))  # 將寬度減少30像素以創建空間來放置滾動條

    # 呼叫函數來創建 UIScrollingContainer
    scrolling_container, vertical_scroll_bar, labels, original_label_positions, total_scrollable_height = create_scrolling_container(ui_manager, rect)
    clock = pygame.time.Clock()
    ########################################



    game = Game()  # 創建 Game 類的一個實例
    setup = SetupMode(game) 

    window = pygame.display.set_mode((WIDTH, HEIGHT))

    background = pygame.image.load('assets/background.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    def handle_turn_button_click(start_player):
        game.create_initial_board_config(
            start_player=start_player, 
            board=game.board_config, 
            storage1=game.storage_area_player1, 
            storage2=game.storage_area_player2
        )
        game.toggle_setup_mode(False)

    run = True
    while run:
        ########################################
        time_delta = clock.tick(60)/1000.0
        ########################################
        for event in pygame.event.get():

            cursor_position = pygame.mouse.get_pos() # 獲取游標位置



            ########################################
            # 處理滾動容器的滾動事件
            if event.type == UI_VERTICAL_SCROLL_BAR_MOVED:
                # Get the current scroll position from the vertical scroll bar of the scrolling container
                new_scroll_position = scrolling_container.vert_scroll_bar.start_percentage * scrolling_container.scrolling_height
                
                for i, label in enumerate(labels):
                    new_y = original_label_positions[i][1] - new_scroll_position
                    label.set_relative_position((original_label_positions[i][0], new_y))
            ########################################    


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
                # 擺盤完後讓玩家２先走
                elif upper_turn_button and upper_turn_button.collidepoint(cursor_position):
                    handle_turn_button_click(start_player = -1)
                # 擺盤完後讓玩家１先走
                elif lower_turn_button and lower_turn_button.collidepoint(cursor_position):
                    handle_turn_button_click(start_player = 1)
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
                        game.toggle_chick_to_hen(piece)  # 切換小雞和母雞

        # 繪製背景圖片
        window.blit(background, (0, 0))

        ########################################
        # 繪製滾動容器的黑色邊界
        pygame.draw.rect(window, (0, 0, 0), rect, 2)
        ########################################


        # 立刻繪製按鈕
        duel_button, setup_button, upper_turn_button, lower_turn_button = draw_buttons(window, game.show_return_to_normal_game_route_button)

        draw_grid(window)
        # draw_storage_area(window)  # 繪製儲存區的格線
        draw_labels(window)       
        draw_pieces(window, game.board_config, game.storage_area_player1,
                    game.storage_area_player2, game.selected_piece, game.mouse_pos)
        draw_available_moves(window, game.available_moves)

        if not game.setup_mode and game.board_config:
            draw_current_player(window, game.current_player)

        game.declare_victory(window)

        ########################################
        draw_control_buttons(window)   # 棋譜的四個播放控制按鈕
        ui_manager.update(time_delta)  # 更新棋譜的容器顯示框
        ui_manager.draw_ui(window)     # 繪製棋譜的容器顯示框
        ########################################

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
