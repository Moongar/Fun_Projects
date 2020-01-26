import pygame
import random

screen_w = 800
screen_h = 800
play_w = 300
play_h = 600
block_size = 30

# game display
top_left_x = (screen_w - play_w) // 2
top_left_y = (screen_h - play_h) // 2

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
X = [[(0,0)]] # explosive

shapes = [O, I, S, Z, J, L, T, X]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128), (255, 0, 0)]


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


def draw_window(win, home_button, high_score=10, score=0, level=1):
    win.fill((0, 0, 0))
    # show title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 0))
    win.blit(label, (screen_w // 2 - label.get_width() // 2, (screen_h - play_h) // 4 - label.get_height() // 2))
    # show level
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('Level: ' + str(level), 1, (255, 255, 255))
    win.blit(label, (screen_w - (screen_w - play_w) / 4 - label.get_width() / 2, screen_h // 2 - 200))
    # show next piece text
    label = font.render('Next Piece', 1, (255, 255, 255))
    win.blit(label, (screen_w - (screen_w - play_w) / 4 - label.get_width() / 2, top_left_y + play_h / 2 - 100))
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
    # draw home button
    home_button.draw(win, (20, 100, 20))


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


def build_grid(locked):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for k, v in locked.items():
        grid[k[1]][k[0]] = v
    return grid


def rebuild_locked(grid):
    locked = {}
    for y in range(0, len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != (0, 0, 0):
                locked[(x, y)] = grid[y][x]
    return locked


def clear_rows(locked):
    grid = build_grid(locked)
    rows = 0
    for y in range(0, len(grid)):
        if all(grid[y][x] != (0, 0, 0) for x in range(len(grid[y]))):
            rows += 1
            for yy in range(1, y)[::-1]:
                grid[yy+1] = grid[yy]
    locked = rebuild_locked(grid)
    return locked, rows


def explosion(locked, pos):
    grid = build_grid(locked)
    for k in pos.keys():
        grid[k[1]][k[0]] = (0, 0, 0)
        if k[1] < play_h / block_size - 1:
            grid[k[1] + 1][k[0]] = (0, 0, 0)
            if k[0] == 0:
                grid[k[1]][k[0] + 1] = (0, 0, 0)
                grid[k[1] + 1][k[0] + 1] = (0, 0, 0)
            elif k[0] == play_w / block_size - 1:
                grid[k[1]][k[0] - 1] = (0, 0, 0)
                grid[k[1] + 1][k[0] - 1] = (0, 0, 0)
            else:
                grid[k[1]][k[0] + 1] = (0, 0, 0)
                grid[k[1] + 1][k[0] + 1] = (0, 0, 0)
                grid[k[1]][k[0] - 1] = (0, 0, 0)
                grid[k[1] + 1][k[0] - 1] = (0, 0, 0)
        else:
            if k[0] == 0:
                grid[k[1]][k[0] + 1] = (0, 0, 0)
            elif k[0] == play_w / block_size - 1:
                grid[k[1]][k[0] - 1] = (0, 0, 0)
            else:
                grid[k[1]][k[0] + 1] = (0, 0, 0)
                grid[k[1]][k[0] - 1] = (0, 0, 0)
    locked = rebuild_locked(grid)
    return locked


class Button:
    def __init__(self, dark_color, active_color, x, y, width, height, text):
        self.color = {'dark': dark_color, 'active': active_color}
        self.active = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - self.width // 2 - 2, self.y - self.height // 2 - 2,
                                            self.width + 4, self.height + 4), 0)
        if self.active:
            color = self.color['active']
        else:
            color = self.color['dark']
        pygame.draw.rect(win, color, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), 0)

        font = pygame.font.SysFont('comicsans', 50)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(text, (self.x + (self.width / 2 - self.width // 2 - text.get_width() / 2),
                        self.y + (self.height / 2 - self.height // 2 - text.get_height() / 2)))

    def hover(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x - self.width // 2 < pos[0] < self.x + self.width // 2:
            if self.y - self.height // 2 < pos[1] < self.y + self.height // 2:
                return True

        return False


def main(win):
    current_piece = get_piece()
    next_piece = get_piece()
    home_button = Button((0, 150, 0), (0, 255, 0),
                         screen_w // 2, screen_h - (screen_h - play_h) // 4, 200, 60, "Main Menu")
    explosion_sound = pygame.mixer.Sound("figures/hit.wav")
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
                if current_piece.y == 1 and current_piece.shape != X:
                    write_bold('YOU LOST!', 80, (255, 255, 255), win, 0)
                    pygame.display.update()
                    pygame.time.delay(1500)
                    update_high_score(score)
                    run = False
                else:
                    change_piece = True
                    current_piece.y -= 1

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not check_move(locked_blocks, render_shape(current_piece)):
                        current_piece.rotation -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.hover(mouse_pos):
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if home_button.hover(mouse_pos):
                    home_button.active = True
                else:
                    home_button.active = False

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
            if current_piece.shape == X:
                explosion_sound.play()
                locked_blocks = explosion(locked_blocks, current_pos)
            else:
                for k, v in current_pos.items():
                    locked_blocks[k] = v
                locked_blocks, cleared_rows = clear_rows(locked_blocks)
                score += cleared_rows * 10
            current_piece = next_piece
            next_piece = get_piece()
            change_piece = False

        # drawings
        draw_window(win, home_button, high_score=get_high_score(), score=score, level=level)
        draw_blocks(win, locked_blocks)
        draw_blocks(win, render_shape(next_piece), (270, 300))
        draw_blocks(win, render_shape(current_piece))
        # draw gir lines
        draw_grid_lines(win)
        pygame.display.update()


def main_menu(win):
    pygame.mixer.init(22100, -16, 2, 64)
    pygame.init()
    pygame.font.init()
    music = pygame.mixer.music.load("figures/music.mp3")
    pygame.mixer.music.play(-1)
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

# TODO: fix the rotation bug
# TODO: add sound volume control to the main menu
