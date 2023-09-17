class NotationManager:
    def __init__(self):
        self.labels = []
        self.original_label_positions = []
        self.current_selected_index = -1
        self.total_scrollable_height = 0

    def handle_label_click(self, label, index):
        # 取消選中所有其他標籤
        for i, other_label in enumerate(self.labels):
            if i != index:
                other_label.set_text(f'Test Label {i}')  # 重設背景顏色
                other_label.rebuild()
        
        label.set_text(f'Test Label {index} (selected)')  # 設置選中標籤的背景顏色
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