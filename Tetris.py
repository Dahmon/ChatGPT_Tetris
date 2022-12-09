import sys
import pygame
import random

# define colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_GREY = (100, 100, 100)

# block colors
colors = [BLUE, CYAN, GREEN, ORANGE, PINK, RED, WHITE, YELLOW, LIGHT_GREY]

# define shapes
block_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# define game variables
block_size = 20
board_width = 20
board_height = 40

# initialize game speed
speed = 10

# initialize game
pygame.init()

# set up the game window
window = pygame.display.set_mode([board_width * block_size, board_height * block_size])
pygame.display.set_caption('Tetris')

# initialize game board
board = [[0 for x in range(board_width)] for y in range(board_height)]

# initialize block
current_block = None
next_block = None
current_block_x = 0
current_block_y = 0

# initialize game clock
clock = pygame.time.Clock()

# initialize game font
font = pygame.font.Font(None, 24)

# initialize game score
score = 0


def create_block():
    """Create a new block at the top of the board."""
    global current_block, current_block_x, current_block_y, next_block
    # choose a random block shape and color
    index = random.randint(0, len(block_shapes) - 1)

    # set current_block to next_block if next_block is defined, otherwise generate a new block
    if next_block:
        current_block = next_block
    else:
        current_block = block_shapes[index]

    # generate a new block for next_block
    next_block = block_shapes[random.randint(0, len(block_shapes) - 1)]

    current_block_x = int(board_width / 2) - int(len(current_block[0]) / 2)
    current_block_y = 0


def rotate_block():
    """Rotate the block clockwise."""
    global current_block
    rows = len(current_block)
    cols = len(current_block[0])
    new_block = [[0 for x in range(rows)] for y in range(cols)]
    for i in range(rows):
        for j in range(cols):
            new_block[j][rows - 1 - i] = current_block[i][j]
    current_block = new_block


def move_block(dx, dy):
    """Move the block by (dx, dy)."""
    global current_block_x, current_block_y
    current_block_x += dx
    current_block_y += dy


def draw_board():
    """Draw the game board, grid, and preview of the next block."""
    # draw game board and grid
    for y in range(board_height):
        for x in range(board_width):
            if board[y][x] == 0:
                pygame.draw.rect(
                    window,
                    BLACK,
                    (
                        x * block_size,
                        y * block_size,
                        block_size,
                        block_size
                    )
                )
            else:
                pygame.draw.rect(
                    window,
                    colors[board[y][x] - 1],
                    (
                        x * block_size,
                        y * block_size,
                        block_size,
                        block_size
                    )
                )

    for x in range(board_width):
        pygame.draw.line(window, LIGHT_GREY, (x * block_size, 0), (x * block_size, board_height * block_size))
    for y in range(board_height):
        pygame.draw.line(window, LIGHT_GREY, (0, y * block_size), (board_width * block_size, y * block_size))

    # draw score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), 1, WHITE)
    window.blit(text, (10, 10))

    # draw next block
    if next_block:
        for y in range(len(next_block)):
            for x in range(len(next_block[0])):
                if next_block[y][x]:
                    pygame.draw.rect(
                        window,
                        colors[next_block[y][x] - 1],
                        (
                            x * block_size + block_size,
                            y * block_size + 4 * block_size,
                            block_size,
                            block_size
                        )
                    )


def draw_block():
    """Draw the current block."""
    for y in range(len(current_block)):
        for x in range(len(current_block[0])):
            if current_block[y][x] == 0:
                continue
            pygame.draw.rect(window, colors[current_block[y][x] - 1], (current_block_x * block_size + x * block_size, current_block_y * block_size + y * block_size, block_size, block_size))


def check_collision():
    """Check if the current block collides with any blocks on the board or goes out of bounds."""
    for y in range(len(current_block)):
        for x in range(len(current_block[0])):
            if current_block[y][x] == 0:
                continue
            if current_block_y + y >= board_height or current_block_x + x < 0 or current_block_x + x >= board_width:
                return True
            if board[current_block_y + y][current_block_x + x] != 0:
                return True
    return False


def check_collisions(dx, dy):
    """Check for collisions with the game board and other blocks."""
    if dx == 0 and dy == 1: # only check for collisions when moving down
        for y in range(len(current_block)):
            for x in range(len(current_block[0])):
                if current_block[y][x]:
                    # check if block is outside of the game board
                    if (current_block_y + y) >= board_height or (current_block_x + x) < 0 or (current_block_x + x) >= board_width:
                        return True
                    # check if block is colliding with another block
                    if board[current_block_y + y][current_block_x + x]:
                        return True
    return False


def add_block_to_board():
    """Add the current block to the game board."""
    global board, current_block_x, current_block_y
    for y in range(len(current_block)):
        for x in range(len(current_block[0])):
            # check if current cell of block is not empty and is within the bounds of the board
            if current_block[y][x] != 0 and current_block_y + y >= 0 and current_block_y + y < board_height and current_block_x + x >= 0 and current_block_x + x < board_width:
                board[current_block_y + y][current_block_x + x] = current_block[y][x]

    # clear any complete rows
    clear_complete_rows()


def clear_complete_rows():
    global board, score, speed
    num_rows_cleared = 0
    for row in range(board_height):
        if 0 not in board[row]:
            num_rows_cleared += 1
            for y in range(row, 0, -1):
                board[y] = board[y - 1]
            board[0] = [0 for x in range(board_width)]
    if num_rows_cleared > 0:
        score += num_rows_cleared * 10
        speed += num_rows_cleared


def check_game_over():
    """Check if the game is over."""
    for x in range(board_width):
        if board[0][x] != 0:
            return True
    return False


def game_over():
    """End the game."""
    pygame.quit()
    sys.exit()


# create the first block
create_block()

# main game loop
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_block(-1, 0)
                if check_collision():
                    move_block(1, 0)
            if event.key == pygame.K_RIGHT:
                move_block(1, 0)
                if check_collision():
                    move_block(-1, 0)
            if event.key == pygame.K_UP:
                rotate_block()
                if check_collision():
                    rotate_block()
            if event.key == pygame.K_DOWN:
                # move block to bottom of board
                while not check_collision():
                    move_block(0, 1)
                move_block(0, -1)
                add_block_to_board()
                create_block()

    # move the block down
    move_block(0, 1)

    # check for collision
    if check_collision():
        move_block(0, -1)
        add_block_to_board()
        create_block()

    # check for game over
    if check_game_over():
        game_over()

    # draw the game
    window.fill(BLACK)
    draw_board()
    draw_block()
    pygame.display.update()

    # limit frame rate
    clock.tick(speed)
