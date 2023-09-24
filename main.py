import time
import pygame
import numpy as np

# Define color constants for the game
COLOR_BG = (10, 10, 10)         # Background color
COLOR_GRID = (40, 40, 40)       # Grid lines color
COLOR_DIE_NEXT = (170, 170, 170) # Color of cells that will die in the next generation
COLOR_ALIVE_NEXT = (255, 255, 255) # Color of cells that will be alive in the next generation

# Function to update the game state and draw cells on the screen
def update(screen, cells, size, with_progress=False):
    # Create a new array to hold the updated cell states
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    # Iterate over each cell in the input array
    for row, col in np.ndindex(cells.shape):
        # Count the number of live neighbors for the current cell
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        # Set the default cell color based on its current state
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        # Apply the rules of Conway's Game of Life
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                # Cell dies in the next generation
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                # Cell remains alive
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                # Dead cell becomes alive in the next generation
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        # Draw the cell on the screen using the determined color
        pygame.draw.rect(screen, color, (col*size, row*size, size - 1, size - 1))

    # Return the updated cell array
    return updated_cells

# Main function for running the game
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    cells = np.zeros((60, 80))  # Initialize the cell grid
    screen.fill(COLOR_GRID)     # Fill the background with the grid color
    update(screen, cells, 10)  # Initial drawing of the cells

    pygame.display.flip()
    pygame.display.update()

    running = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Toggle simulation on/off
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                # Add live cells by clicking the mouse
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()
        screen.fill(COLOR_GRID)

        if running:
            # If the simulation is running, update cell states
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()
        time.sleep(0.001)

if __name__ == '__main__':
    main()  # Start the main function when the script is executed
