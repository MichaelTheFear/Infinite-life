import pygame
from collections import defaultdict

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
FPS = 30
ZOOM_SPEED = 0.1

# Colors
BG_COLOR = (30, 30, 30)
CELL_COLOR = (200, 200, 200)
GRID_COLOR = (50, 50, 50)

# Game of Life Functions
def get_neighbors(cell):
    x, y = cell
    return [
        (x-1, y-1), (x-1, y), (x-1, y+1),
        (x, y-1),           (x, y+1),
        (x+1, y-1), (x+1, y), (x+1, y+1)
    ]

def step(active_cells):
    neighbor_counts = defaultdict(int)
    for cell in active_cells:
        for neighbor in get_neighbors(cell):
            neighbor_counts[neighbor] += 1

    new_active_cells = set()
    for cell, count in neighbor_counts.items():
        if count == 3 or (count == 2 and cell in active_cells):
            new_active_cells.add(cell)

    return new_active_cells

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Initial Setup
active_cells = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
running = False
zoom = 1.0
offset_x, offset_y = 0, 0

def draw_grid(screen, zoom, offset_x, offset_y):
    """Draw the background grid."""
    cell_size = int(CELL_SIZE * zoom)
    if cell_size < 1:
        return

    # Find the grid lines to draw
    start_x = int(-offset_x // cell_size - WIDTH // (2 * cell_size))
    end_x = int((WIDTH - offset_x) // cell_size - WIDTH // (2 * cell_size))
    start_y = int(-offset_y // cell_size - HEIGHT // (2 * cell_size))
    end_y = int((HEIGHT - offset_y) // cell_size - HEIGHT // (2 * cell_size))

    for x in range(start_x, end_x + 1):
        screen_x = x * cell_size + offset_x + WIDTH // 2
        pygame.draw.line(screen, GRID_COLOR, (screen_x, 0), (screen_x, HEIGHT))

    for y in range(start_y, end_y + 1):
        screen_y = y * cell_size + offset_y + HEIGHT // 2
        pygame.draw.line(screen, GRID_COLOR, (0, screen_y), (WIDTH, screen_y))

def draw_cells(screen, active_cells, zoom, offset_x, offset_y):
    """Draw the active cells."""
    cell_size = int(CELL_SIZE * zoom)
    if cell_size < 1:
        return

    for cell in active_cells:
        x, y = cell
        screen_x = x * cell_size + offset_x + WIDTH // 2
        screen_y = y * cell_size + offset_y + HEIGHT // 2

        pygame.draw.rect(screen, CELL_COLOR, (screen_x, screen_y, cell_size, cell_size))

def get_cell_at_position(pos, zoom, offset_x, offset_y):
    """Calculate the cell coordinates from a screen position."""
    cell_size = int(CELL_SIZE * zoom)
    screen_x, screen_y = pos
    grid_x = (screen_x - WIDTH // 2 - offset_x) // cell_size
    grid_y = (screen_y - HEIGHT // 2 - offset_y) // cell_size
    return int(grid_x), int(grid_y)

def main():
    global active_cells, running, zoom, offset_x, offset_y

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Mouse controls for zoom
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    zoom *= 1 + ZOOM_SPEED
                elif event.button == 5:  # Scroll down
                    zoom /= 1 + ZOOM_SPEED
                elif event.button == 1:  # Left click
                    cell = get_cell_at_position(event.pos, zoom, offset_x, offset_y)
                    if cell in active_cells:
                        active_cells.remove(cell)  # Deactivate cell
                    else:
                        active_cells.add(cell)  # Activate cell

            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start/pause simulation
                    running = not running
                if event.key == pygame.K_r:  # Reset simulation
                    active_cells = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
                    running = False
                if event.key == pygame.K_c:  # Clear grid
                    active_cells = set()
                    running = False

            # Dragging for panning
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                start_drag = event.pos
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # While holding left click
                    dx, dy = event.rel
                    offset_x += dx
                    offset_y += dy

        # Update simulation
        if running:
            active_cells = step(active_cells)

        # Draw grid and cells
        screen.fill(BG_COLOR)
        draw_grid(screen, zoom, offset_x, offset_y)
        draw_cells(screen, active_cells, zoom, offset_x, offset_y)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
