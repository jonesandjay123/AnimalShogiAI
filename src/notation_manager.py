import pygame

class NotationManager:
    def __init__(self):
        self.labels = []
        self.original_label_positions = []
        self.current_selected_index = -1
        self.total_scrollable_height = 0

    def handle_label_click(self, label, index):
        self.current_selected_index = index
        # 取消選中所有其他標籤
        for i, other_label in enumerate(self.labels):
            if i != index:
                other_label.colours['normal_bg'] = pygame.Color('black')  # 設定正常狀態的背景色
                other_label.colours['normal_text'] = pygame.Color('white')  # 設定正常狀態的文字顏色
                other_label.rebuild()
            
        label.colours['normal_bg'] = pygame.Color('blue')  # 設定被選中標籤的背景顏色
        label.colours['normal_text'] = pygame.Color('white')  # 設定被選中標籤的文字顏色
        label.rebuild()
        print(f"Label {index} selected")



    def get_current_selected_index(self):
        return self.current_selected_index

    def set_current_selected_index(self, index):
        self.current_selected_index = index

    def set_labels(self, label_list):
        self.labels = label_list

    def get_labels(self):
        return self.labels

    def clear_labels(self):
        for label in self.labels:
            label.kill()  # 使用 kill 方法來移除標籤
        self.labels = []  # 清空標籤列表
        self.original_label_positions = []  # 清空原始位置列表
        self.current_selected_index = -1  # 重置當前選中的索引
        self.total_scrollable_height = 0  # 重置可滾動的高度