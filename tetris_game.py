import pygame
import random
from typing import List, Tuple
import scores

pygame.init()
pygame.freetype.init()

# 创建字体对象
try:
    # Mac系统中文字体路径
    font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
    game_font = pygame.freetype.Font(font_path, 36)
    small_font = pygame.freetype.Font(font_path, 20)  # 更小的字号
except Exception as e:
    print(f"加载字体失败: {e}")
    try:
        # 尝试其他中文字体
        font_path = "/System/Library/Fonts/STHeiti Light.ttc"
        game_font = pygame.freetype.Font(font_path, 36)
        small_font = pygame.freetype.Font(font_path, 20)  # 更小的字号
    except Exception as e:
        print(f"加载备用字体失败: {e}")
        game_font = pygame.freetype.SysFont(None, 36)
        small_font = pygame.freetype.SysFont(None, 20)  # 更小的字号

# 颜色定义
COLORS = [
    (200, 200, 200),    # 背景色 - 浅灰色
    (46, 204, 113),     # 绿色
    (52, 152, 219),     # 蓝色
    (155, 89, 182),     # 紫色
    (241, 196, 15),     # 黄色
    (231, 76, 60),      # 红色
    (230, 126, 34),     # 橙色
    (149, 165, 166)     # 灰色
]

# 基本颜色常量
BACKGROUND = (255, 255, 255)  # 白色背景
BLACK = (0, 0, 0)  # 纯黑色
GRAY = (128, 128, 128)  # 灰色
LIGHT_GRAY = (200, 200, 200)  # 浅灰色
WHITE = (255, 255, 255)  # 白色
ORANGE = (255, 159, 28)  # 橙色
ORANGE_HOVER = (230, 144, 25)  # 深橙色用于悬停

# 界面元素颜色
TEXT_COLOR = BLACK  # 文字颜色改为黑色
GRID_COLOR = LIGHT_GRAY  # 网格线颜色改为浅灰色

# 按钮颜色
BACK_BTN_COLOR = (240, 240, 240)  # 返回按钮使用浅灰白色
BACK_BTN_HOVER = (220, 220, 220)  # 返回按钮悬停色更柔和
BACK_BTN_TEXT = (80, 80, 80)  # 返回按钮文字用深灰色
START_BTN_COLOR = ORANGE  # 开始按钮使用橙色
START_BTN_HOVER = ORANGE_HOVER  # 开始按钮悬停色
BUTTON_TEXT = WHITE  # 开始按钮文字保持白色
BUTTON_BORDER = (200, 200, 200)  # 按钮边框和阴影颜色

# 方块形状定义
SHAPES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # J
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
    [[1, 2, 5, 6]],  # O
    [[5, 6, 8, 9], [1, 5, 6, 10]],  # S
    [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],  # T
    [[4, 5, 9, 10], [2, 6, 5, 9]]  # Z
]

class Button:
    def __init__(self, x, y, width, height, text, icon=None, small=False, button_color=None, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = button_color or START_BTN_COLOR
        self.hover_color = hover_color or START_BTN_HOVER
        self.is_hovered = False
        self.border_radius = 10
        self.icon = icon
        self.small = small
        
    def draw(self, surface):
        # 绘制按钮阴影
        shadow_rect = self.rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(surface, BUTTON_BORDER, shadow_rect, border_radius=self.border_radius)
        
        # 绘制按钮
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, BUTTON_BORDER, self.rect, 2, border_radius=self.border_radius)
        
        # 选择字体
        font = small_font if self.small else game_font
        
        # 计算文本位置
        if self.icon:
            # 如果有图标，先绘制图标
            icon_rect = font.get_rect(self.icon)
            text_rect = font.get_rect(self.text)
            total_width = icon_rect.width + text_rect.width + 5  # 5是图标和文字的间距
            
            icon_pos = (
                self.rect.centerx - total_width//2,
                self.rect.centery - icon_rect.height//2
            )
            text_pos = (
                self.rect.centerx - total_width//2 + icon_rect.width + 5,
                self.rect.centery - text_rect.height//2
            )
            
            # 绘制图标和文本
            font.render_to(surface, icon_pos, self.icon, BUTTON_TEXT)  # 使用白色文字
            font.render_to(surface, text_pos, self.text, BUTTON_TEXT)  # 使用白色文字
        else:
            # 没有图标，只绘制文本
            text_rect = font.get_rect(self.text)
            text_pos = (
                self.rect.centerx - text_rect.width//2,
                self.rect.centery - text_rect.height//2
            )
            font.render_to(surface, text_pos, self.text, BUTTON_TEXT)  # 使用白色文字
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

class Tetris:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0
        self.state = "start"  # 游戏开始就是运行状态
        self.figure = None
        self.figure_pos = [0, 0]
        self.next_figure = None
        self.level = 1
        
        self.new_figure()  # 创建第一个方块
    
    def new_figure(self) -> None:
        if not self.next_figure:
            self.next_figure = Figure(3, 0)
        self.figure = self.next_figure
        self.next_figure = Figure(3, 0)
    
    def intersects(self) -> bool:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if (i + self.figure.y > self.height - 1 or
                        j + self.figure.x > self.width - 1 or
                        j + self.figure.x < 0 or
                        self.field[i + self.figure.y][j + self.figure.x] > 0):
                        return True
        return False
    
    def freeze(self) -> None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
    
    def break_lines(self) -> None:
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i2 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i2][j] = self.field[i2-1][j]
        self.score += lines ** 2
        self.level = self.score // 10 + 1
    
    def go_space(self) -> None:
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()
    
    def go_down(self) -> None:
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()
    
    def go_side(self, dx: int) -> None:
        self.figure.x += dx
        if self.intersects():
            self.figure.x -= dx
    
    def rotate(self) -> None:
        rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = rotation

class Figure:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(SHAPES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)  # 确保不使用背景色
        self.rotation = 0
    
    def image(self) -> List[int]:
        return SHAPES[self.type][self.rotation]
    
    def rotate(self) -> None:
        self.rotation = (self.rotation + 1) % len(SHAPES[self.type])

def main():
    pygame.init()
    
    # 显示设置
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("俄罗斯方块")
    
    # 游戏常量
    CELL_SIZE = 30
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    
    # 计算游戏区域位置
    game_left = (size[0] - GRID_WIDTH * CELL_SIZE) // 2
    game_top = (size[1] - GRID_HEIGHT * CELL_SIZE) // 2
    
    # 创建游戏实例
    game = Tetris(GRID_HEIGHT, GRID_WIDTH)
    
    # 游戏循环
    clock = pygame.time.Clock()
    fps = 60
    counter = 0
    pressing_down = False
    
    game_started = False
    start_btn = Button(
        size[0]//2 - 100,
        int(size[1] * 0.6),
        200,
        60,
        "开始游戏",
        button_color=START_BTN_COLOR,
        hover_color=START_BTN_HOVER
    )
    
    # 创建返回按钮
    back_btn = Button(
        10,
        10,
        100,
        36,
        "返回",
        icon="←",
        small=True,
        button_color=BACK_BTN_COLOR,
        hover_color=BACK_BTN_HOVER
    )
    
    high_score = scores.load_scores()["tetris"]  # 加载最高分
    
    while True:
        if game_started and game.figure is None:
            game.new_figure()
        
        counter += 1
        
        if counter > fps // (2 * game.level):
            counter = 0
            if game.state == "start" and game_started:
                game.go_down()
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
            # 处理返回按钮事件
            if back_btn.handle_event(event):
                return  # 直接返回到游戏选择菜单
                
            if not game_started:
                if start_btn.handle_event(event):
                    game_started = True
                    game = Tetris(GRID_HEIGHT, GRID_WIDTH)
                continue
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 鼠标左键
                    game.rotate()
        
        if pressing_down:
            game.go_down()
        
        # 绘制背景
        screen.fill(BACKGROUND)
        
        if not game_started:
            # 1. 游戏标题
            title_text = "俄罗斯方块"
            title_rect = game_font.get_rect(title_text)
            title_pos = (
                size[0]//2 - title_rect.width // 2,
                size[1]//4
            )
            game_font.render_to(screen, title_pos, title_text, BLACK)
            
            # 2. 最高分显示
            high_score_text = f"历史最高分：{high_score}"
            high_score_rect = game_font.get_rect(high_score_text)
            high_score_pos = (
                size[0]//2 - high_score_rect.width // 2,
                size[1]//4 + title_rect.height + 20
            )
            game_font.render_to(screen, high_score_pos, high_score_text, BLACK)
            
            # 3. 开始按钮已在创建时定位在中间偏下位置
            start_btn.draw(screen)
        else:
            # 绘制游戏区域背景
            pygame.draw.rect(screen, WHITE,
                           [game_left - 1, game_top - 1,
                            GRID_WIDTH * CELL_SIZE + 2,
                            GRID_HEIGHT * CELL_SIZE + 2])
            
            # 绘制网格线
            for i in range(GRID_HEIGHT + 1):
                pygame.draw.line(screen, GRID_COLOR,
                               [game_left, game_top + i * CELL_SIZE],
                               [game_left + GRID_WIDTH * CELL_SIZE, game_top + i * CELL_SIZE])
            for j in range(GRID_WIDTH + 1):
                pygame.draw.line(screen, GRID_COLOR,
                               [game_left + j * CELL_SIZE, game_top],
                               [game_left + j * CELL_SIZE, game_top + GRID_HEIGHT * CELL_SIZE])
            
            # 绘制已落下的方块
            for i in range(game.height):
                for j in range(game.width):
                    if game.field[i][j] > 0:
                        pygame.draw.rect(screen, COLORS[game.field[i][j]],
                                       [game_left + j * CELL_SIZE,
                                        game_top + i * CELL_SIZE,
                                        CELL_SIZE - 1, CELL_SIZE - 1])
            
            # 绘制当前方块
            if game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in game.figure.image():
                            pygame.draw.rect(screen, COLORS[game.figure.color],
                                           [game_left + (j + game.figure.x) * CELL_SIZE,
                                            game_top + (i + game.figure.y) * CELL_SIZE,
                                            CELL_SIZE - 1, CELL_SIZE - 1])
            
            # 绘制分数和等级
            game_font.render_to(screen, [50, 100], f"分数: {game.score}", TEXT_COLOR)
            game_font.render_to(screen, [50, 150], f"等级: {game.level}", TEXT_COLOR)
            game_font.render_to(screen, [50, 200], f"最高分: {high_score}", TEXT_COLOR)
            
            # 游戏结束显示
            if game.state == "gameover":
                scores.save_score("tetris", game.score)  # 保存最高分
                high_score = scores.load_scores()["tetris"]  # 重新加载最高分
                game_started = False
        
        # 始终显示返回按钮
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main() 