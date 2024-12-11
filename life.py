import pygame
from collections import defaultdict
from copy import deepcopy

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
FPS = 30
ZOOM_SPEED = 0.1


BG_COLOR = (30, 30, 30)
CELL_COLOR = (200, 200, 200)
GRID_COLOR = (50, 50, 50)


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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

glider = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}

glider_gun = {
    (0, 5), (0, 6),
    (1, 5), (1, 6),
    (10, 5), (10, 6), (10, 7),
    (11, 4), (11, 8),
    (12, 3), (12, 9),
    (13, 3), (13, 9),
    (14, 6),
    (15, 4), (15, 8),
    (16, 5), (16, 6), (16, 7),
    (17, 6),
    (20, 3), (20, 4), (20, 5),
    (21, 3), (21, 4), (21, 5),
    (22, 2), (22, 6),
    (24, 1), (24, 2), (24, 6), (24, 7),
    (34, 3), (34, 4),
    (35, 3), (35, 4),
}

eater = {
    (0, 0), (0, 1), (1, 0),
    (2, 1), (2, 3),
    (3, 3), (3, 4),
}

glider_duplicator = {
    (-2, 0), (-2, 1), (-1, -1), (-1, 2), (0, -2), (0, 3), # First duplicator structure
    (2, -2), (2, 3), (3, -1), (3, 2), (4, 0), (4, 1) # Second duplicator structure
}

glider_reflector = {
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), # Base of the reflector
    (1, -1), (1, 6), (2, 0), (2, 5), # Edges
    (-2, 0), (-2, 1), (-3, 1), (-4, 2), (-4, 3), (-3, 4), (-2, 4), # Reflecting edge
}


glider_gun = {
    (0, 5), (0, 6),
    (1, 5), (1, 6),
    (10, 5), (10, 6), (10, 7),
    (11, 4), (11, 8),
    (12, 3), (12, 9),
    (13, 3), (13, 9),
    (14, 6),
    (15, 4), (15, 8),
    (16, 5), (16, 6), (16, 7),
    (17, 6),
    (20, 3), (20, 4), (20, 5),
    (21, 3), (21, 4), (21, 5),
    (22, 2), (22, 6),
    (24, 1), (24, 2), (24, 6), (24, 7),
    (34, 3), (34, 4),
    (35, 3), (35, 4),
}


active_cells = glider_gun
intitial_cells = deepcopy(active_cells)
undo_cells = active_cells.copy()

running = False
zoom = 1.0
offset_x, offset_y = 0, 0

def draw_grid(screen, zoom, offset_x, offset_y):
    cell_size = int(CELL_SIZE * zoom)
    if cell_size < 1:
        return

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
    cell_size = int(CELL_SIZE * zoom)
    if cell_size < 1:
        return

    for cell in active_cells:
        x, y = cell
        screen_x = x * cell_size + offset_x + WIDTH // 2
        screen_y = y * cell_size + offset_y + HEIGHT // 2

        pygame.draw.rect(screen, CELL_COLOR, (screen_x, screen_y, cell_size, cell_size))

def get_cell_at_position(pos, zoom, offset_x, offset_y):
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
                if event.button == 4:  
                    zoom *= 1 + ZOOM_SPEED
                elif event.button == 5:  
                    zoom /= 1 + ZOOM_SPEED
                elif event.button == 1: 
                    cell = get_cell_at_position(event.pos, zoom, offset_x, offset_y)
                    if cell in active_cells:
                        active_cells.remove(cell) 
                    else:
                        active_cells.add(cell)  

            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    running = not running
                if event.key == pygame.K_c: 
                    active_cells = set()
                    running = False
                if event.key == pygame.K_i:
                    active_cells = intitial_cells

            # Dragging for panning
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                start_drag = event.pos
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  
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
