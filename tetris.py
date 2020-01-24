import pygame
import random

screen_w = 800
screen_h = 700
play_w = 300
play_h = 600
block_size = 30

# game display
top_left_x = (screen_w - play_w) // 2
top_left_y = screen_h - play_h

O = [[(0, 0), (0, -1), (1, 0), (1, -1)]]
I = [[(1, 0), (1, -1), (1, -2), (1, -3)], [(-1, -1), (0, -1), (1, -1), (2, -1)]]
S = [[(0, 0), (1, 0), (1, -1), (2, -1)], [(1, 0), (1, -1), (0, -1), (0, -2)]]
Z = [[(0, -1), (1, -1), (1, 0), (2, 0)], [(0, 0), (0, -1), (1, -1), (1, -2)]]
J = [[(-1,-1), (-1, 0), (0, 0), (1, 0)], [(0, 0), (0, -1), (0, -2), (1, -2)],
     [(-1, -1), (0, -1), (1, -1), (1, 0)], [(-1, 0), (0, 0), (0, -1), (0, -2)]]
L = [[(-1, 0), (0, 0), (1, 0), (1, -1)], [(0, -2), (0, -1), (0, 0), (1, 0)],
     [(-1, 0), (-1, -1), (0, -1), (1, -1)], [(0, -2), (1,-2), (1, -1), (1, 0)]]
T = [[(-1, 0), (0, 0), (0, -1), (1, 0)], [(0, 0), (0, -1), (1, -1), (0, -2)],
     [(-1, -1), (0, -1), (0, 0), (1, -1)], [(-1, -1), (0, 0), (0, -1), (0, -2)]]

shapes = [O, I, S, Z, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def get_piece():
    return Piece(4, 0, random.choice(shapes))


def write_bold(text, size, color, surface, shift):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_w / 2 - label.get_width() / 2,
                         top_left_y + play_h / 2 - label.get_height() / 2 + shift))


def draw_grid_lines(win):
    for i in range(1, play_h // block_size):
        pygame.draw.line(win,
                         (128, 128, 128),
                         [top_left_x, top_left_y + i*block_size],
                         [top_left_x+play_w, top_left_y+i*block_size])
        for j in range(1, play_w // block_size):
            pygame.draw.line(win,
                             (128, 128, 128),
                             [top_left_x + j*block_size, top_left_y],
                             [top_left_x + j*block_size, top_left_y + play_h])


def draw_blocks(win, blocks, offset=(0, 0)):
    for k, color in blocks.items():
        if k[1] + offset[1] >= 0:
            pygame.draw.rect(win,
                             color,
                             (top_left_x + k[0] * block_size + offset[0],
                              top_left_y + k[1] * block_size + offset[1], block_size, block_size),
                             0
                             )


def get_high_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return int(score)


def update_high_score(new_score):
    high_score = get_high_score()

    with open('scores.txt', 'w') as f:
        if int(high_score) < new_score:
            f.write(str(new_score))
        else:
            f.write(str(high_score))


def draw_window(win, high_score=10, score=0, level=1):
    win.fill((0, 0, 0))
    # show title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 0))
    win.blit(label, (top_left_x + play_w / 2 - label.get_width() / 2, 30))
    # show level
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('Level: ' + str(level), 1, (255, 255, 255))
    win.blit(label,
             (top_left_x + play_w + (screen_w - play_w) / 4 - label.get_width() / 2,
              top_left_y + play_h / 2 - 200))
    # show next piece
    label = font.render('Next Piece', 1, (255, 255, 255))
    win.blit(label,
             (top_left_x + play_w + (screen_w - play_w) / 4 - label.get_width() / 2, top_left_y + play_h / 2 - 100))
    # show high score
    label = font.render('Best Score', 1, (0, 155, 255))
    win.blit(label, (top_left_x / 2 - label.get_width() / 2, top_left_y + play_h / 2 - 200))
    label = font.render(str(high_score), 1, (0, 155, 255))
    win.blit(label, (top_left_x / 2 - label.get_width() / 2, top_left_y + play_h / 2 - 170))
    # current score
    label = font.render('Your Score', 1, (0, 255, 0))
    win.blit(label, (top_left_x / 2 - label.get_width() / 2, top_left_y + play_h / 2 - 100))
    label = font.render(str(score), 1, (0, 255, 0))
    win.blit(label, (top_left_x / 2 - label.get_width() / 2, top_left_y + play_h / 2 - 70))
    # draw red margin
    pygame.draw.rect(win, (255, 0, 50), (top_left_x, top_left_y, play_w, play_h), 6)


def render_shape(piece):
    grid_pos = {}
    for pos in piece.shape[piece.rotation % len(piece.shape)]:
        grid_pos[(pos[0] + piece.x, pos[1] + piece.y)] = piece.color

    return grid_pos


def check_move(locked, piece):
    for k in piece.keys():
        if (k in locked.keys()) or (k[0] < 0 or k[0] > 9) or (k[1] > 19):
            return False
    return True


def clear_rows(locked):
    rows = 0
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for k, v in locked.items():
        grid[k[1]][k[0]] = v
    for y in range(0, len(grid)):
        if all(grid[y][x] != (0, 0, 0) for x in range(len(grid[y]))):
            rows += 1
            for yy in range(1, y)[::-1]:
                grid[yy+1] = grid[yy]
    locked = {}
    for y in range(0, len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != (0, 0, 0):
                locked[(x, y)] = grid[y][x]
    return locked, rows


def main(win):
    current_piece = get_piece()
    next_piece = get_piece()
    clock = pygame.time.Clock()
    locked_blocks = {}
    score = 0
    fall_timer = 0
    fall_time = 0.32
    level = 1
    level_timer = 0
    key_lag = 0
    change_piece = False
    run = True
    while run:
        fall_timer += clock.get_rawtime()
        level_timer += clock.get_rawtime()
        clock.tick()

        if level_timer > 30000:
            level_timer = 0
            level += 1

        if fall_timer / 1000 > fall_time - level / 50:
            fall_timer = 0
            current_piece.y += 1
            if not check_move(locked_blocks, render_shape(current_piece)):
                if current_piece.y == 1:
                    write_bold('YOU LOST!', 80, (255, 255, 255), win, 0)
                    pygame.display.update()
                    pygame.time.delay(1500)
                    update_high_score(score)
                    run = False
                else:
                    change_piece = True
                    current_piece.y -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not check_move(locked_blocks, render_shape(current_piece)):
                        current_piece.rotation -= 1

        if key_lag > 0:
            key_lag += 1
        if key_lag == 30:
            key_lag = 0
        keys = pygame.key.get_pressed()
        if key_lag == 0:
            if keys[pygame.K_LEFT]:
                key_lag = 1
                current_piece.x -= 1
                if not check_move(locked_blocks, render_shape(current_piece)):
                    current_piece.x += 1
            if keys[pygame.K_RIGHT]:
                key_lag = 1
                current_piece.x += 1
                if not check_move(locked_blocks, render_shape(current_piece)):
                    current_piece.x -= 1
            if keys[pygame.K_DOWN]:
                key_lag = 1
                current_piece.y += 1
                if not check_move(locked_blocks, render_shape(current_piece)):
                    current_piece.y -= 1

        if change_piece:
            current_pos = render_shape(current_piece)
            for k, v in current_pos.items():
                locked_blocks[k] = v
            locked_blocks, cleared_rows = clear_rows(locked_blocks)
            score += cleared_rows * 10
            current_piece = next_piece
            next_piece = get_piece()
            change_piece = False

        # drawings
        draw_window(win, high_score=get_high_score(), score=score, level=level)
        draw_blocks(win, locked_blocks)
        draw_blocks(win, render_shape(next_piece), (270, 350))
        draw_blocks(win, render_shape(current_piece))
        # draw gir lines
        draw_grid_lines(win)
        pygame.display.update()


def main_menu(win):
    pygame.init()
    pygame.font.init()
    # main(win)
    run = True
    while run:
        win.fill((0, 0, 0))
        write_bold('Welcome To TETRIS!', 80, (0, 255, 0), win, -100)
        write_bold('Press Any Key to Play', 50, (255, 255, 255), win, +150)

        draw_blocks(win, render_shape(Piece(0, 0, shapes[2])), (0, 100))
        draw_blocks(win, render_shape(Piece(0, 0, shapes[3])), (200, 100))
        draw_blocks(win, render_shape(Piece(0, 0, shapes[5])), (-70, 300))
        draw_blocks(win, render_shape(Piece(0, 0, shapes[6])), (130, 300))
        draw_blocks(win, render_shape(Piece(0, 0, shapes[4])), (330, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Tetris')

main_menu(win)  # start game
