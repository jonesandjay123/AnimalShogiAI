import pygame
import sys
from board import create_board, draw_grid, draw_squares, draw_labels, draw_buttons, draw_pieces
from const import WIDTH, HEIGHT


def main():
    # Initialize pygame
    pygame.init()

    # Set the dimensions of the window
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Load and scale the background image
    background = pygame.image.load('assets/background.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    board = create_board()  # Create the initial board setup

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
                    print("Duel button clicked")
                # The setup button was clicked
                elif setup_button.collidepoint(pygame.mouse.get_pos()):
                    print("Setup button clicked")

        # Draw background image
        window.blit(background, (0, 0))

        draw_squares(window)  # Draw the squares on the board
        draw_grid(window)
        draw_labels(window)
        draw_buttons(window)
        draw_pieces(window, board)  # Draw the pieces on the board
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
