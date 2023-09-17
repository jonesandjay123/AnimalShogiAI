labels = []
current_selected_index = -1  # 初始值設為-1，表示沒有選中任何標籤

def handle_label_click(label, index):
    global current_selected_index
    current_selected_index = index
    # 取消選中所有其他標籤
    for i, other_label in enumerate(labels):
        if i != index:
            other_label.set_text(f'Test Label {i}')  # 重設背景顏色
            other_label.rebuild()
    
    label.set_text(f'Test Label {index} (selected)')  # 設置選中標籤的背景顏色
    label.rebuild()
    print(f"Label {index} selected")

def get_current_selected_index():
    return current_selected_index

def set_labels(label_list):
    global labels
    labels = label_list

def get_labels():
    return labels

def set_current_selected_index(index):
    global current_selected_index
    current_selected_index = index

def get_current_selected_index():
    global current_selected_index
    return current_selected_index
