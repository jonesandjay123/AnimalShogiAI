from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, ROWS


def get_storage_cell_details():
    storage_cell_size = SQUARE_SIZE * 0.7
    margin = 8  # Adjust the margin as needed
    return storage_cell_size, margin


def get_storage_cell_coords(index, player, storage_cell_size, margin):
    storage_area_start_x = GRID_OFFSET_X - storage_cell_size * 2
    if player == 1:
        y = GRID_OFFSET_Y + ROWS * SQUARE_SIZE + margin
    else:  # player 2
        y = GRID_OFFSET_Y - storage_cell_size - margin
    x = storage_area_start_x + (index+2) * (storage_cell_size + margin)
    return x, y
