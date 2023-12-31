import pygame
import pygame_gui
from datetime import datetime
import os
import sys
import json
from board import add_new_label, create_scrolling_container, draw_control_buttons, draw_current_player, draw_grid, draw_available_moves, draw_labels, draw_buttons, draw_pieces
from utils import get_piece_at_pos
from notation_manager import NotationManager
from const import WIDTH, HEIGHT
from game import Game
from setup import SetupMode


def main():
    pygame.init()

    # 初始化UIManager
    ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    # 定義一個 pygame 矩形來設置 UIScrollingContainer 的位置和大小
    rect = pygame.Rect((550, 100), (250, 400))  # 將寬度減少30像素以創建空間來放置滾動條

    # 呼叫函數來創建 UIScrollingContainer
    scrolling_container, vertical_scroll_bar, text_entry_line = create_scrolling_container(ui_manager, rect)

    last_scroll_position = 0 # 用於跟踪滾動條的位置
    scroll_step = 0.01  # 這是每次滾動的距離，您可以根據需要調整它
    clock = pygame.time.Clock()

    notation_manager = NotationManager() # 創建 NotationManager 類的一個實例
    game = Game(ui_manager=ui_manager, scrolling_container=scrolling_container, notation_manager=notation_manager) # 創建 Game 類的一個實例

    setup = SetupMode(game) 

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    control_buttons = draw_control_buttons(window)

    background = pygame.image.load('assets/background.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    def save_game_state(game):
        # 如果遊戲處於擺盤模式並且沒有棋盤配置，則不保存任何東西
        if game.board_config == {} or game.setup_mode:
            return

        try:
            # 獲取當前的時間並創建一個基於時間的文件名
            current_time = datetime.now().strftime("%Y%m%d_%H%M")
            
            # For AI train
            filename_ai_train = f"output/ai_train_game_state_{current_time}.json"
            ai_train_str = json.dumps(game.board_hist, separators=(',', ':'), ensure_ascii=False)
            with open(filename_ai_train, 'w') as file:
                file.write(ai_train_str)
            
            # For easy read
            filename_easy_read = f"output/easy_read_game_state_{current_time}.txt"
            easy_read_str = json.dumps(game.board_hist, indent=4, ensure_ascii=False)
            easy_read_str = easy_read_str.replace("\\", "")
            with open(filename_easy_read, 'w') as file:
                file.write(easy_read_str)

            # For notation
            filename_notation = f"output/notation_{current_time}.txt"
            notations = [label.text for label in game.notation_manager.labels]
            notation_str = "\n".join(notations)
            with open(filename_notation, 'w') as file:
                file.write(notation_str)

            print(f"Game state saved to {filename_ai_train} and {filename_easy_read}")
        except Exception as e:
            print(f"Failed to save the game state: {e}")
    
    def load_game_state():
        input_dir = "input"
        try:
            # 獲取目錄下所有文件
            files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
            # 如果沒有文件，則打印一條消息
            if not files:
                print("No files found in the input directory.")
                return
            # 找到最新的文件
            latest_file = max(files, key=os.path.getctime)
            # 讀取和打印文件內容
            with open(latest_file, "r") as file:
                data = file.read()
                print(data)
        except Exception as e:
            # 如果在嘗試讀取文件時發生錯誤，則打印錯誤消息
            print(f"An error occurred while trying to load the game state: {e}")

    def handle_turn_button_click(start_player):
        game.create_initial_board_config(
            start_player=start_player, 
            board=game.board_config, 
            storage1=game.storage_area_player1, 
            storage2=game.storage_area_player2
        )
        game.toggle_setup_mode(False)

    
    def process_events(event, game, ui_manager, vertical_scroll_bar, scrolling_container, text_entry_line):
        ui_manager.process_events(event)  # 處理事件列隊中的事件

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if "label_" in event.ui_element.most_specific_combined_id:  # 檢查是否點擊了一個標籤
                label_index = int(event.ui_element.most_specific_combined_id.split('_')[-1])  # 獲取標籤索引
                game.notation_manager.handle_label_click(game.notation_manager.labels[label_index], label_index, game)  # 調用處理函數
            if vertical_scroll_bar and (event.ui_element == vertical_scroll_bar.bottom_button or event.ui_element == vertical_scroll_bar.top_button):
                # 使用新的 scroll_step 值來更新滾動條的位置
                if event.ui_element == vertical_scroll_bar.bottom_button:
                    vertical_scroll_bar.scroll_position = min(vertical_scroll_bar.scroll_position + scroll_step, 1)
                else:
                    vertical_scroll_bar.scroll_position = max(vertical_scroll_bar.scroll_position - scroll_step, 0)
                
                # 根據新的滾動位置更新標籤的位置
                if scrolling_container.vert_scroll_bar is not None:
                    current_scroll_position = scrolling_container.vert_scroll_bar.scroll_position
                else:
                    current_scroll_position = 0
                for i, label in enumerate(game.notation_manager.labels):
                    if event.ui_element == label:
                        game.notation_manager.handle_label_click(game.notation_manager.labels[i], i, game)
                    new_y = game.notation_manager.original_label_positions[i][1] - (current_scroll_position * game.notation_manager.total_scrollable_height)
                    label.set_relative_position((game.notation_manager.original_label_positions[i][0], new_y))

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == text_entry_line:
                # 手動匯入的局必須要清除標籤跟board_hist，以視為新的對局
                game.notation_manager.clear_labels()
                game.board_hist = {}
                add_new_label(ui_manager, scrolling_container, "Load from Notation", notation_manager)
                game.load_game_state(text_entry_line.get_text())


    run = True
    while run:
        time_delta = clock.tick(60)/1000.0

        for event in pygame.event.get():
            process_events(event, game, ui_manager, vertical_scroll_bar, scrolling_container, text_entry_line)

            cursor_position = pygame.mouse.get_pos() # 獲取游標位置
            
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEMOTION:  # 當滑鼠移動時
                game.mouse_pos = event.pos # 讓棋子得以跟著游標移動
                if game.selected_piece:
                    game.selected_piece.update_position(cursor_position)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 當滑鼠按下時
                # 擺盤完後讓玩家２先走(刻意把條件擺在對局按鈕前，以便把觸發事件的優先序蓋到上面)
                if upper_turn_button and upper_turn_button.collidepoint(cursor_position):
                    handle_turn_button_click(start_player = -1)
                # 擺盤完後讓玩家１先走(同上，要高過對局按鈕的點擊事件)
                elif lower_turn_button and lower_turn_button.collidepoint(cursor_position):
                    handle_turn_button_click(start_player = 1)
                # 對局按鈕被點擊
                elif duel_button.collidepoint(cursor_position):
                    game.create_initial_board_config()  # 初始化為對局模式的配置
                    game.toggle_setup_mode(False)
                # 擺盤按鈕被點擊
                elif setup_button.collidepoint(cursor_position):
                    setup.initialize_setup_mode() # 清空棋盤，進入擺盤模式
                    game.toggle_setup_mode(True)


                elif control_buttons["play_right"].collidepoint(cursor_position):
                    current_index = game.notation_manager.get_current_selected_index()
                    if current_index is None or current_index < 0:  # 新增此行來處理當前索引為 -1 的情況
                        current_index = -1
                    if current_index < len(game.notation_manager.labels) - 1:
                        game.notation_manager.set_current_selected_index(current_index + 1)
                        game.notation_manager.handle_label_click(game.notation_manager.labels[current_index + 1], current_index + 1, game)
                elif control_buttons["play_left"].collidepoint(cursor_position):
                    current_index = game.notation_manager.get_current_selected_index()
                    if current_index is None or current_index < 0:  # 新增此行來處理當前索引為 -1 的情況
                        current_index = 0
                    if current_index > 0:
                        game.notation_manager.set_current_selected_index(current_index - 1)
                        game.notation_manager.handle_label_click(game.notation_manager.labels[current_index - 1], current_index - 1, game)

                elif control_buttons["forward_right"].collidepoint(cursor_position):
                    if game.notation_manager.labels:
                        game.notation_manager.set_current_selected_index(len(game.notation_manager.labels) - 1)
                        game.notation_manager.handle_label_click(game.notation_manager.labels[-1], len(game.notation_manager.labels) - 1, game)
                elif control_buttons["forward_left"].collidepoint(cursor_position):
                    if game.notation_manager.labels:
                        game.notation_manager.set_current_selected_index(0)
                        game.notation_manager.handle_label_click(game.notation_manager.labels[0], 0, game)


                # 非按鈕區域被點擊
                else:
                    game.click_on_piece(cursor_position)

            elif event.type == pygame.MOUSEBUTTONUP:  # 當滑鼠放開時(擺盤模式下的長壓拖曳釋放)
                if game.selected_piece and game.setup_mode:
                    setup.place_piece(cursor_position)
                    
            elif event.type == pygame.KEYDOWN:  # 當按下鍵盤按鈕時
                if event.key == pygame.K_t:  # "Ｔ" 鍵被按下
                    piece = get_piece_at_pos(cursor_position, game.board_config, game.storage_area_player1, game.storage_area_player2)
                    if piece and piece.piece_type in ["C", "H"]:  # 檢驗棋子是否為小雞或母雞
                        game.toggle_chick_to_hen(piece)  # 切換小雞和母雞
                elif event.key == pygame.K_s:  # "S" 鍵被按下
                    save_game_state(game)
                elif event.key == pygame.K_l:  # "L" 鍵被按下
                    load_game_state()

        # 繪製背景圖片
        window.blit(background, (0, 0))

        # 繪製棋譜容器的黑色邊界
        pygame.draw.rect(window, (0, 0, 0), rect, 2)

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

        draw_control_buttons(window)   # 棋譜的四個播放控制按鈕

        # 持续监控滚动条的位置，并在滚动条的位置发生变化时更新标签的位置。
        if scrolling_container.vert_scroll_bar is not None:
            current_scroll_position = scrolling_container.vert_scroll_bar.scroll_position
        else:
            current_scroll_position = 0
        
        # 新增以下這行來限制 current_scroll_position 在 0 和 1 之間
        current_scroll_position = min(1, max(0, current_scroll_position))

        if current_scroll_position != last_scroll_position:
            for i, label in enumerate(game.notation_manager.labels):
                new_y = game.notation_manager.original_label_positions[i][1] - (current_scroll_position * game.notation_manager.total_scrollable_height)
                label.set_relative_position((game.notation_manager.original_label_positions[i][0], new_y))
                # print(f"New position of label {i}: {new_y}")  # 新添加的 log
            last_scroll_position = current_scroll_position
            # print(f"Current scroll position: {current_scroll_position}")  # 新添加的 log
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window)


        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
