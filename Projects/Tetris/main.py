import pygame as pg
import random
import sys

# Константы
FPS = 120
WINDOW_W, WINDOW_H = 600, 800
BLOCK_SIZE = 20
CUP_H, CUP_W = 20, 10
SIDE_FREQ, DOWN_FREQ = 0.15, 0.1
SIDE_MARGIN = (WINDOW_W - CUP_W * BLOCK_SIZE) // 2
TOP_MARGIN = WINDOW_H - (CUP_H * BLOCK_SIZE) - 5

# Цвета
COLORS = [(0, 0, 255), (0, 225, 0), (225, 0, 0), (225, 225, 0)]
LIGHTCOLORS = [(30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30)]
WHITE, GRAY, BLUE = (255, 255, 255), (185, 185, 185), (102, 0, 255)
BRD_COLOR, BG_COLOR, TXT_COLOR, TITLE_COLOR, INFO_COLOR = WHITE, BLUE, WHITE, COLORS[3], COLORS[0]

# Фигуры
FIGURES = {
    'S': [['ooooo', 'ooooo', 'ooxxo', 'oxxoo', 'ooooo'], ['ooooo', 'ooxoo', 'ooxxo', 'oooxo', 'ooooo']],
    'Z': [['ooooo', 'ooooo', 'oxxoo', 'ooxxo', 'ooooo'], ['ooooo', 'ooxoo', 'oxxoo', 'oxooo', 'ooooo']],
    'J': [['ooooo', 'oxooo', 'oxxxo', 'ooooo', 'ooooo'], ['ooooo', 'ooxxo', 'ooxoo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'oooxo', 'ooooo'], ['ooooo', 'ooxoo', 'ooxoo', 'oxxoo', 'ooooo']],
    'L': [['ooooo', 'oooxo', 'oxxxo', 'ooooo', 'ooooo'], ['ooooo', 'ooxoo', 'ooxoo', 'ooxxo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'oxooo', 'ooooo'], ['ooooo', 'oxxoo', 'ooxoo', 'ooxoo', 'ooooo']],
    'I': [['ooxoo', 'ooxoo', 'ooxoo', 'ooxoo', 'ooooo'], ['ooooo', 'ooooo', 'xxxxo', 'ooooo', 'ooooo']],
    'O': [['ooooo', 'ooooo', 'oxxoo', 'oxxoo', 'ooooo']],
    'T': [['ooooo', 'ooxoo', 'oxxxo', 'ooooo', 'ooooo'], ['ooooo', 'ooxoo', 'ooxxo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'ooxoo', 'ooooo'], ['ooooo', 'ooxoo', 'oxxoo', 'ooxoo', 'ooooo']]
}

class TetrisGame:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.fps_clock = pg.time.Clock()
        self.display_surf = pg.display.set_mode((WINDOW_W, WINDOW_H))
        self.basic_font = pg.font.SysFont('arial', 20)
        self.big_font = pg.font.SysFont('verdana', 45)
        pg.display.set_caption('Тетрис Lite')

        self.load_sounds()
        self.cup = self.empty_cup()
        self.points = 0
        self.level, self.fall_speed = self.calc_speed(self.points)
        self.falling_fig = self.get_new_fig()
        self.next_fig = self.get_new_fig()
        self.game_over = False
        self.state = 'MAIN_MENU'
        self.paused = False

    def load_sounds(self):
        pg.mixer.music.load("Tetris 1989 - Alexey Pazhitnov.mp3")
        self.game_over_sound = pg.mixer.Sound("Player Mode - Game Over.mp3")
        self.title_sound = pg.mixer.Sound("Title.mp3")

    def empty_cup(self):
        return [['o'] * CUP_H for _ in range(CUP_W)]

    def get_new_fig(self):
        shape = random.choice(list(FIGURES.keys()))
        return {
            'shape': shape,
            'rotation': random.randint(0, len(FIGURES[shape]) - 1),
            'x': int(CUP_W / 2) - int(5 / 2),
            'y': -2,
            'color': random.randint(0, len(COLORS) - 1)
        }

    def calc_speed(self, points):
        level = int(points / 10) + 1
        fall_speed = 0.27 - (level * 0.02)
        return level, fall_speed

    def check_pos(self, cup, fig, adj_x=0, adj_y=0):
        for x in range(5):
            for y in range(5):
                above_cup = y + fig['y'] + adj_y < 0
                if above_cup or FIGURES[fig['shape']][fig['rotation']][y][x] == 'o':
                    continue
                if not self.in_cup(x + fig['x'] + adj_x, y + fig['y'] + adj_y):
                    return False
                if cup[x + fig['x'] + adj_x][y + fig['y'] + adj_y] != 'o':
                    return False
        return True

    def in_cup(self, x, y):
        return 0 <= x < CUP_W and y < CUP_H

    def add_to_cup(self, cup, fig):
        for x in range(5):
            for y in range(5):
                if FIGURES[fig['shape']][fig['rotation']][y][x] != 'o':
                    cup[x + fig['x']][y + fig['y']] = fig['color']

    def is_completed(self, cup, y):
        return all(cup[x][y] != 'o' for x in range(CUP_W))

    def clear_completed(self, cup):
        removed_lines = 0
        y = CUP_H - 1
        while y >= 0:
            if self.is_completed(cup, y):
                for push_down_y in range(y, 0, -1):
                    for x in range(CUP_W):
                        cup[x][push_down_y] = cup[x][push_down_y - 1]
                for x in range(CUP_W):
                    cup[x][0] = 'o'
                removed_lines += 1
            else:
                y -= 1
        return removed_lines

    def convert_coords(self, block_x, block_y):
        return (SIDE_MARGIN + (block_x * BLOCK_SIZE)), (TOP_MARGIN + (block_y * BLOCK_SIZE))

    def draw_block(self, block_x, block_y, color, pixel_x=None, pixel_y=None):
        if color == 'o':
            return
        if pixel_x is None and pixel_y is None:
            pixel_x, pixel_y = self.convert_coords(block_x, block_y)

        pg.draw.rect(self.display_surf, COLORS[color], (pixel_x + 1, pixel_y + 1, BLOCK_SIZE - 1, BLOCK_SIZE - 1), 0, 3)
        pg.draw.rect(self.display_surf, LIGHTCOLORS[color], (pixel_x + 1, pixel_y + 1, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 0, 3)
        pg.draw.circle(self.display_surf, COLORS[color], (pixel_x + BLOCK_SIZE / 2, pixel_y + BLOCK_SIZE / 2), 5)

    def game_cup(self, cup):
        pg.draw.rect(self.display_surf, BRD_COLOR, (SIDE_MARGIN - 4, TOP_MARGIN - 4, (CUP_W * BLOCK_SIZE) + 8, (CUP_H * BLOCK_SIZE) + 8), 5)
        pg.draw.rect(self.display_surf, BG_COLOR, (SIDE_MARGIN, TOP_MARGIN, BLOCK_SIZE * CUP_W, BLOCK_SIZE * CUP_H))
        for x in range(CUP_W):
            for y in range(CUP_H):
                self.draw_block(x, y, cup[x][y])

    def draw_title(self):
        title_surf = self.big_font.render('Тетрис Lite', True, TITLE_COLOR)
        title_rect = title_surf.get_rect()
        title_rect.topleft = (WINDOW_W - 425, 30)
        self.display_surf.blit(title_surf, title_rect)

    def draw_info(self, points, level):
        points_surf = self.basic_font.render(f'Баллы: {points}', True, TXT_COLOR)
        points_rect = points_surf.get_rect()
        points_rect.topleft = (WINDOW_W - 550, 180)
        self.display_surf.blit(points_surf, points_rect)

        level_surf = self.basic_font.render(f'Уровень: {level}', True, TXT_COLOR)
        level_rect = level_surf.get_rect()
        level_rect.topleft = (WINDOW_W - 550, 250)
        self.display_surf.blit(level_surf, level_rect)

        pause_surf = self.basic_font.render('Пауза: пробел', True, INFO_COLOR)
        pause_rect = pause_surf.get_rect()
        pause_rect.topleft = (WINDOW_W - 550, 420)
        self.display_surf.blit(pause_surf, pause_rect)

        esc_surf = self.basic_font.render('Выход: Esc', True, INFO_COLOR)
        esc_rect = esc_surf.get_rect()
        esc_rect.topleft = (WINDOW_W - 550, 450)
        self.display_surf.blit(esc_surf, esc_rect)

    def draw_fig(self, fig, pixel_x=None, pixel_y=None):
        fig_to_draw = FIGURES[fig['shape']][fig['rotation']]
        if pixel_x is None and pixel_y is None:
            pixel_x, pixel_y = self.convert_coords(fig['x'], fig['y'])

        for x in range(5):
            for y in range(5):
                if fig_to_draw[y][x] != 'o':
                    self.draw_block(None, None, fig['color'], pixel_x + (x * BLOCK_SIZE), pixel_y + (y * BLOCK_SIZE))

    def draw_next_fig(self, fig):
        next_surf = self.basic_font.render('Следующая:', True, TXT_COLOR)
        next_rect = next_surf.get_rect()
        next_rect.topleft = (WINDOW_W - 150, 180)
        self.display_surf.blit(next_surf, next_rect)
        self.draw_fig(fig, pixel_x=WINDOW_W - 150, pixel_y=230)

    def txt_objects(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def show_text(self, text):
        title_surf, title_rect = self.txt_objects(text, self.big_font, TITLE_COLOR)
        title_rect.center = (WINDOW_W // 2, WINDOW_H // 2)
        self.display_surf.blit(title_surf, title_rect)

        press_key_surf, press_key_rect = self.txt_objects('Нажмите любую клавишу для продолжения', self.basic_font, TITLE_COLOR)
        press_key_rect.center = (WINDOW_W // 2, WINDOW_H // 2 + 100)
        self.display_surf.blit(press_key_surf, press_key_rect)

        pg.display.update()

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    waiting = False
            self.fps_clock.tick()

    def pause_screen(self):
        pause = pg.Surface((WINDOW_W, WINDOW_H), pg.SRCALPHA)
        pause.fill((0, 0, 255, 127))
        self.display_surf.blit(pause, (0, 0))

        if pg.mixer.music.get_busy():
            pg.mixer.music.pause()
        else:
            pg.mixer.music.unpause()

        self.show_text('Пауза')
        self.wait_for_key()

        if pg.mixer.music.get_busy():
            pg.mixer.music.unpause()

    def quit_game(self):
        for event in pg.event.get(pg.QUIT):
            self.stop_game()
        for event in pg.event.get(pg.KEYUP):
            if event.key == pg.K_ESCAPE:
                self.stop_game()
            pg.event.post(event)

    def stop_game(self):
        pg.quit()
        sys.exit()

    def run(self):
        while True:
            if self.state == 'MAIN_MENU':
                self.main_menu()
            elif self.state == 'GAME':
                self.run_tetris()
            elif self.state == 'GAME_OVER':
                self.game_over()

    def main_menu(self):
        self.title_sound.play()
        self.show_text('Тетрис Lite')
        self.wait_for_key()
        self.title_sound.stop()
        self.state = 'GAME'
        pg.mixer.music.play(-1)

    def game_over(self):
        self.game_over_sound.play()
        self.pause_screen()
        self.show_text('Игра закончена')
        self.wait_for_key()
        self.game_over_sound.stop()
        self.state = 'MAIN_MENU'

    def run_tetris(self):
        self.cup = self.empty_cup()
        last_move_down = pg.time.get_ticks()
        last_side_move = pg.time.get_ticks()
        last_fall = pg.time.get_ticks()
        going_down = False
        going_left = False
        going_right = False
        self.points = 0
        self.level, self.fall_speed = self.calc_speed(self.points)
        self.falling_fig = self.get_new_fig()
        self.next_fig = self.get_new_fig()
        self.game_over = False

        pg.mixer.music.play(-1)

        while not self.game_over:
            if self.falling_fig is None:
                self.falling_fig = self.next_fig
                self.next_fig = self.get_new_fig()
                last_fall = pg.time.get_ticks()

                if not self.check_pos(self.cup, self.falling_fig):
                    self.game_over = True

            self.quit_game()
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        self.paused = not self.paused
                        if self.paused:
                            self.pause_screen()
                        last_fall = pg.time.get_ticks()
                        last_move_down = pg.time.get_ticks()
                        last_side_move = pg.time.get_ticks()
                    elif event.key == pg.K_LEFT:
                        going_left = False
                    elif event.key == pg.K_RIGHT:
                        going_right = False
                    elif event.key == pg.K_DOWN:
                        going_down = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and self.check_pos(self.cup, self.falling_fig, adj_x=-1):
                        self.falling_fig['x'] -= 1
                        going_left = True
                        going_right = False
                        last_side_move = pg.time.get_ticks()

                    elif event.key == pg.K_RIGHT and self.check_pos(self.cup, self.falling_fig, adj_x=1):
                        self.falling_fig['x'] += 1
                        going_right = True
                        going_left = False
                        last_side_move = pg.time.get_ticks()

                    elif event.key == pg.K_UP:
                        self.falling_fig['rotation'] = (self.falling_fig['rotation'] + 1) % len(FIGURES[self.falling_fig['shape']])
                        if not self.check_pos(self.cup, self.falling_fig):
                            self.falling_fig['rotation'] = (self.falling_fig['rotation'] - 1) % len(FIGURES[self.falling_fig['shape']])

                    elif event.key == pg.K_DOWN:
                        going_down = True
                        if self.check_pos(self.cup, self.falling_fig, adj_y=1):
                            self.falling_fig['y'] += 1
                        last_move_down = pg.time.get_ticks()

                    elif event.key == pg.K_RETURN:
                        going_down = False
                        going_left = False
                        going_right = False
                        for i in range(1, CUP_H):
                            if not self.check_pos(self.cup, self.falling_fig, adj_y=i):
                                break
                        self.falling_fig['y'] += i - 1

            if not self.paused:
                if (going_left or going_right) and pg.time.get_ticks() - last_side_move > SIDE_FREQ * 1000:
                    if going_left and self.check_pos(self.cup, self.falling_fig, adj_x=-1):
                        self.falling_fig['x'] -= 1
                    elif going_right and self.check_pos(self.cup, self.falling_fig, adj_x=1):
                        self.falling_fig['x'] += 1
                    last_side_move = pg.time.get_ticks()

                if going_down and pg.time.get_ticks() - last_move_down > DOWN_FREQ * 1000 and self.check_pos(self.cup, self.falling_fig, adj_y=1):
                    self.falling_fig['y'] += 1
                    last_move_down = pg.time.get_ticks()

                if pg.time.get_ticks() - last_fall > self.fall_speed * 1000:
                    if not self.check_pos(self.cup, self.falling_fig, adj_y=1):
                        self.add_to_cup(self.cup, self.falling_fig)
                        self.points += self.clear_completed(self.cup)
                        self.level, self.fall_speed = self.calc_speed(self.points)
                        self.falling_fig = None
                    else:
                        self.falling_fig['y'] += 1
                        last_fall = pg.time.get_ticks()

            self.display_surf.fill(BG_COLOR)
            self.draw_title()
            self.game_cup(self.cup)
            self.draw_info(self.points, self.level)
            self.draw_next_fig(self.next_fig)
            if self.falling_fig is not None:
                self.draw_fig(self.falling_fig)
            pg.display.update()
            self.fps_clock.tick(FPS)

        pg.mixer.music.stop()
        self.state = 'GAME_OVER'

if __name__ == '__main__':
    game = TetrisGame()
    game.run()
