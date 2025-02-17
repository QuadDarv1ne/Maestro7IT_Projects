import pygame
import sys
import random
import json
from math import sqrt

# Конфигурация
CONFIG = {
    "colors": {
        "background": (245, 245, 245),
        "tile_colors": [(255, 200, 200), (200, 255, 200), (200, 200, 255), (255, 255, 200)],
        "text": (40, 40, 40),
        "highlight": (100, 200, 100)
    },
    "sizes": [3, 4, 5],
    "tile_size": 80,
    "anim_speed": 0.2
}

class DiamondTile:
    def __init__(self, numbers, position):
        self.numbers = numbers
        self.rotation = 0
        self.pos = position
        self.target_pos = position
        self.is_moving = False

    def get_rotated_numbers(self):
        return self.numbers[self.rotation:] + self.numbers[:self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def draw(self, surface):
        # Анимированное перемещение
        if self.pos != self.target_pos:
            self.pos = (
                self.pos[0] + (self.target_pos[0]-self.pos[0])*CONFIG["anim_speed"],
                self.pos[1] + (self.target_pos[1]-self.pos[1])*CONFIG["anim_speed"]
            )

        # Рисуем ромб
        size = CONFIG["tile_size"]
        points = [
            (self.pos[0], self.pos[1] - size//2),
            (self.pos[0] + size//2, self.pos[1]),
            (self.pos[0], self.pos[1] + size//2),
            (self.pos[0] - size//2, self.pos[1])
        ]
        
        # Рисуем треугольники
        for i in range(4):
            triangle = [self.pos, points[i], points[(i+1)%4]]
            pygame.draw.polygon(surface, CONFIG["colors"]["tile_colors"][i], triangle)
            pygame.draw.polygon(surface, CONFIG["colors"]["text"], triangle, 2)

        # Рисуем числа
        font = pygame.font.Font(None, 28)
        offsets = [(0, -30), (30, 0), (0, 30), (-30, 0)]
        for i, num in enumerate(self.get_rotated_numbers()):
            text = font.render(str(num), True, CONFIG["colors"]["text"])
            text_rect = text.get_rect(center=(self.pos[0]+offsets[i][0], self.pos[1]+offsets[i][1]))
            surface.blit(text, text_rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.menu = MainMenu(self)
        self.game_active = False
        self.records = self.load_records()
        self.mode = "time"  # Режим по умолчанию
        self.size = 3       # Размер по умолчанию

    def load_records(self):
        try:
            with open("records.json", "r") as f:
                return json.load(f)
        except:
            return {"time": {}, "moves": {}}

    def save_records(self):
        with open("records.json", "w") as f:
            json.dump(self.records, f)

    def start_game(self, size, mode):
        self.size = size
        self.mode = mode  # Обновляем режим при старте игры
        self.board = GameBoard(size, mode, self)
        self.game_active = True

    def run(self):
        while True:
            if self.game_active:
                self.board.run()
            else:
                self.menu.run()
            self.clock.tick(60)

class GameBoard:
    def __init__(self, size, mode, game):
        self.size = size
        self.mode = mode
        self.game = game
        self.generate_puzzle()
        self.init_positions()
        self.selected = None
        self.moves = 0
        self.time = 0
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()  # Добавьте эту строку

    def generate_puzzle(self):
        self.tiles = []
        for _ in range(self.size**2):
            numbers = [random.randint(0,9) for _ in range(4)]
            self.tiles.append(DiamondTile(numbers, (0,0)))
        random.shuffle(self.tiles)
        self.reserve = self.tiles.copy()
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]

    def init_positions(self):
        self.grid_pos = []
        center_x, center_y = self.game.screen.get_rect().center
        spacing = CONFIG["tile_size"] * 1.2
        
        for row in range(self.size):
            for col in range(self.size):
                x = center_x + (col - row) * spacing//2
                y = center_y + (col + row) * spacing//3
                self.grid_pos.append((x, y))

    def check_connections(self):
        for i in range(len(self.grid_pos)):
            row, col = divmod(i, self.size)
            tile = self.grid[row][col]
            if not tile:
                continue
            
            # Проверка соседей
            neighbors = [
                (row-1, col),  # Верх
                (row, col+1),   # Право
                (row+1, col),   # Низ
                (row, col-1)    # Лево
            ]
            
            for idx, (nr, nc) in enumerate(neighbors):
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    neighbor = self.grid[nr][nc]
                    if neighbor and tile.get_rotated_numbers()[idx] != neighbor.get_rotated_numbers()[(idx+2)%4]:
                        return False
        return True

    def draw_interface(self):
        # Панель информации
        time_text = self.font.render(f"Время: {self.time//60:02}:{self.time%60:02}", 
                                   True, CONFIG["colors"]["text"])
        moves_text = self.font.render(f"Ходы: {self.moves}", 
                                    True, CONFIG["colors"]["text"])
        self.game.screen.blit(time_text, (20, 20))
        self.game.screen.blit(moves_text, (20, 60))

        # Кнопки
        self.draw_button("Меню", (1100, 20), self.return_to_menu)

    def draw_button(self, text, pos, action):
        btn = pygame.Rect(pos[0], pos[1], 80, 40)
        pygame.draw.rect(self.game.screen, (200, 200, 200), btn)
        text_surf = self.font.render(text, True, CONFIG["colors"]["text"])
        self.game.screen.blit(text_surf, (pos[0]+10, pos[1]+10))
        return btn

    def return_to_menu(self):
        self.game.game_active = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # ЛКМ - выбор плитки
                if event.button == 1:
                    self.handle_click(pos)
                
                # ПКМ - вращение
                elif event.button == 3:
                    self.handle_rotation(pos)
    
    def handle_click(self, pos):
        # Проверка резерва
        for tile in self.reserve:
            if pygame.Rect(tile.pos[0]-40, tile.pos[1]-40, 80, 80).collidepoint(pos):
                self.selected = tile
                self.reserve.remove(tile)
                return
                
        # Проверка доски
        for i in range(len(self.grid_pos)):
            if pygame.Rect(self.grid_pos[i][0]-40, self.grid_pos[i][1]-40, 80, 80).collidepoint(pos):
                if self.grid[i//self.size][i%self.size] == self.selected:
                    self.grid[i//self.size][i%self.size] = None
                    self.selected = None
                    self.moves += 1

    def handle_rotation(self, pos):
        # Вращение на доске
        for i in range(len(self.grid_pos)):
            if pygame.Rect(self.grid_pos[i][0]-40, self.grid_pos[i][1]-40, 80, 80).collidepoint(pos):
                if self.grid[i//self.size][i%self.size]:
                    self.grid[i//self.size][i%self.size].rotate()
                    self.moves += 1
                    return
                    
        # Вращение в резерве
        for tile in self.reserve:
            if pygame.Rect(tile.pos[0]-40, tile.pos[1]-40, 80, 80).collidepoint(pos):
                tile.rotate()
                self.moves += 1
                return

    def run(self):
        last_time = pygame.time.get_ticks()
        while True:
            self.game.screen.fill(CONFIG["colors"]["background"])
            
            # Обновление времени
            current_time = pygame.time.get_ticks()
            if current_time - last_time > 1000:
                self.time += 1
                last_time = current_time
            
            # Отрисовка элементов
            self.draw_grid()    # Теперь метод существует
            self.draw_reserve()
            self.draw_interface()
            
            # Обработка событий
            self.handle_events()
            
            # Проверка победы
            if self.check_connections() and all(cell for row in self.grid for cell in row):
                self.show_victory()
                return
            
            pygame.display.flip()
            self.clock.tick(60)

    def draw_grid(self):
        for i, pos in enumerate(self.grid_pos):
            row = i // self.size
            col = i % self.size
            tile = self.grid[row][col]
            
            if tile:
                tile.target_pos = pos
                tile.draw(self.game.screen)
            else:
                pygame.draw.circle(self.game.screen, (200, 200, 200), pos, 5)

    def draw_reserve(self):
        for i, tile in enumerate(self.reserve):
            x = 50 + (i % 4) * 100
            y = 700 + (i // 4) * 100
            tile.target_pos = (x, y)
            tile.draw(self.game.screen)

    def show_victory(self):
        # Сохранение рекордов
        size_key = str(self.size)
        if self.mode == "time" and (self.time < self.game.records["time"].get(size_key, 9999)):
            self.game.records["time"][size_key] = self.time
        elif self.mode == "moves" and (self.moves < self.game.records["moves"].get(size_key, 9999)):
            self.game.records["moves"][size_key] = self.moves
        self.game.save_records()

        # Оверлей победы
        overlay = pygame.Surface((1200, 800), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 180), (0, 0, 1200, 800))
        
        font = pygame.font.Font(None, 72)
        text = font.render("ПОБЕДА!", True, CONFIG["colors"]["highlight"])
        overlay.blit(text, (500, 300))
        
        stats = [
            f"Режим: {'Время' if self.mode == 'time' else 'Ходы'}",
            f"Результат: {self.time//60:02}:{self.time%60:02}" if self.mode == "time" else f"Ходов: {self.moves}",
            f"Рекорд: {self.game.records[self.mode][size_key]}"
        ]
        
        for i, line in enumerate(stats):
            text = self.font.render(line, True, (255, 255, 255))
            overlay.blit(text, (500, 400 + i*40))
            
        self.game.screen.blit(overlay, (0, 0))
        pygame.display.flip()
        
        while True:
            event = pygame.event.wait()
            if event.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                return

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.font = pygame.font.Font(None, 48)

    def create_buttons(self):
        self.buttons = []
        # Кнопки выбора размера
        for i, size in enumerate(CONFIG["sizes"]):
            btn = pygame.Rect(500, 200 + i*100, 200, 60)
            self.buttons.append(("size", size, btn))
        
        # Кнопки режима
        self.buttons.append(("mode", "time", pygame.Rect(500, 500, 200, 60)))
        self.buttons.append(("mode", "moves", pygame.Rect(500, 600, 200, 60)))

    def draw(self):
        self.game.screen.fill(CONFIG["colors"]["background"])
        
        # Заголовок
        title = self.font.render("ТЕТРАВЕКС", True, CONFIG["colors"]["text"])
        self.game.screen.blit(title, (520, 100))
        
        # Кнопки
        for btn_type, value, rect in self.buttons:
            color = (200, 200, 200) if not (btn_type == "mode" and value == self.game.mode) else (150, 200, 150)
            pygame.draw.rect(self.game.screen, color, rect)
            
            text = self.font.render(
                f"Размер {value}" if btn_type == "size" else 
                f"Режим: {'Время' if value == 'time' else 'Ходы'}", 
                True, CONFIG["colors"]["text"])
            self.game.screen.blit(text, (rect.x+10, rect.y+10))
            
        pygame.display.flip()

    def run(self):
        self.create_buttons()
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn_type, value, rect in self.buttons:
                        if rect.collidepoint(pos):
                            if btn_type == "size":
                                self.game.start_game(value, "time")
                                return
                            elif btn_type == "mode":
                                self.game.mode = value

if __name__ == "__main__":
    game = Game()
    game.run()
