import pygame
import random
import scores
import sys

# 初始化 Pygame
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
BACKGROUND = (255, 255, 255)  # 白色背景
BLACK = (0, 0, 0)  # 纯黑色
GRAY = (128, 128, 128)  # 灰色
LIGHT_GRAY = (200, 200, 200)  # 浅灰色
WHITE = (255, 255, 255)  # 白色
ORANGE = (255, 159, 28)  # 橙色
ORANGE_HOVER = (230, 144, 25)  # 深橙色用于悬停
RED = (255, 0, 0)  # 红色用于地雷
BLUE = (0, 0, 255)  # 蓝色用于数字
GREEN = (0, 128, 0)  # 绿色用于数字

# 按钮颜色
BACK_BTN_COLOR = (240, 240, 240)  # 返回按钮使用浅灰白色
BACK_BTN_HOVER = (220, 220, 220)  # 返回按钮悬停色更柔和
BACK_BTN_TEXT = (80, 80, 80)  # 返回按钮文字用深灰色
START_BTN_COLOR = ORANGE  # 开始按钮使用橙色
START_BTN_HOVER = ORANGE_HOVER  # 开始按钮悬停色
BUTTON_TEXT = WHITE  # 开始按钮文字保持白色
BUTTON_BORDER = (200, 200, 200)  # 按钮边框和阴影颜色

# 游戏设置
CELL_SIZE = 30
GRID_SIZE = 16  # 16x16 网格
MINES_COUNT = 40  # 40个地雷

# 窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class Button:
    def __init__(self, x, y, width, height, text, icon=None, small=False, button_color=None, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = button_color if button_color else START_BTN_COLOR
        self.hover_color = hover_color if hover_color else START_BTN_HOVER
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
        
        # 修改文字颜色逻辑
        text_color = BACK_BTN_TEXT if self.color == BACK_BTN_COLOR else BUTTON_TEXT
        
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
            font.render_to(surface, icon_pos, self.icon, text_color)
            font.render_to(surface, text_pos, self.text, text_color)
        else:
            # 没有图标，只绘制文本
            text_rect = font.get_rect(self.text)
            text_pos = (
                self.rect.centerx - text_rect.width//2,
                self.rect.centery - text_rect.height//2
            )
            font.render_to(surface, text_pos, self.text, text_color)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

class Minesweeper:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.mines_count = MINES_COUNT
        self.cell_size = CELL_SIZE
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.flagged = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.game_over = False
        self.win = False
        self.first_click = True
        self.start_time = None
        self.elapsed_time = 0
        self.flags_left = self.mines_count
        self.score = 0
        
        # 计算游戏区域的位置
        self.game_left = (WINDOW_WIDTH - self.grid_size * self.cell_size) // 2
        self.game_top = (WINDOW_HEIGHT - self.grid_size * self.cell_size) // 2
        
    def place_mines(self, first_x, first_y):
        # 确保第一次点击的位置及其周围没有地雷
        safe_cells = [(first_x + dx, first_y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                     if 0 <= first_x + dx < self.grid_size and 0 <= first_y + dy < self.grid_size]
        
        # 创建所有可能的位置列表，除去安全区域
        all_positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)
                        if (x, y) not in safe_cells]
        
        # 随机选择地雷位置
        mine_positions = random.sample(all_positions, self.mines_count)
        
        # 放置地雷
        for x, y in mine_positions:
            self.grid[x][y] = -1
            
        # 计算每个格子周围的地雷数
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] != -1:
                    count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if 0 <= x + dx < self.grid_size and 0 <= y + dy < self.grid_size:
                                if self.grid[x + dx][y + dy] == -1:
                                    count += 1
                    self.grid[x][y] = count
    
    def reveal_cell(self, x, y):
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return
        
        if self.revealed[x][y] or self.flagged[x][y]:
            return
            
        if self.first_click:
            self.first_click = False
            self.start_time = pygame.time.get_ticks()
            self.place_mines(x, y)
        
        self.revealed[x][y] = True
        
        if self.grid[x][y] == -1:
            self.game_over = True
            return
        
        if self.grid[x][y] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                        self.reveal_cell(new_x, new_y)
        
        # 检查是否获胜
        unrevealed_count = sum(row.count(False) for row in self.revealed)
        if unrevealed_count == self.mines_count:
            self.win = True
            self.calculate_score()
    
    def toggle_flag(self, x, y):
        if not self.revealed[x][y]:
            self.flagged[x][y] = not self.flagged[x][y]
            self.flags_left += -1 if self.flagged[x][y] else 1
    
    def calculate_score(self):
        if self.win:
            # 基础分数：1000分
            base_score = 1000
            # 时间奖励：越快完成得分越高
            time_bonus = max(0, 2000 - self.elapsed_time // 1000)  # 每秒扣除1分，最多扣除2000分
            # 剩余旗子奖励：每个正确放置的旗子50分
            flag_bonus = sum(50 for x in range(self.grid_size) for y in range(self.grid_size)
                           if self.flagged[x][y] and self.grid[x][y] == -1)
            
            self.score = base_score + time_bonus + flag_bonus
            
            # 保存最高分
            scores.save_score("minesweeper", self.score)
    
    def draw(self, screen):
        # 绘制网格
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = pygame.Rect(
                    self.game_left + x * self.cell_size,
                    self.game_top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                # 绘制基础方块
                if self.revealed[x][y]:
                    pygame.draw.rect(screen, LIGHT_GRAY, rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                
                # 绘制边框
                pygame.draw.rect(screen, BLACK, rect, 1)
                
                if self.revealed[x][y]:
                    if self.grid[x][y] == -1:
                        # 绘制地雷
                        pygame.draw.circle(screen, RED,
                                         (self.game_left + x * self.cell_size + self.cell_size // 2,
                                          self.game_top + y * self.cell_size + self.cell_size // 2),
                                         self.cell_size // 3)
                    elif self.grid[x][y] > 0:
                        # 绘制数字
                        text = str(self.grid[x][y])
                        text_rect = small_font.get_rect(text)
                        text_pos = (
                            self.game_left + x * self.cell_size + (self.cell_size - text_rect.width) // 2,
                            self.game_top + y * self.cell_size + (self.cell_size - text_rect.height) // 2
                        )
                        small_font.render_to(screen, text_pos, text, BLUE)
                elif self.flagged[x][y]:
                    # 绘制旗子
                    pygame.draw.polygon(screen, RED, [
                        (self.game_left + x * self.cell_size + self.cell_size // 4,
                         self.game_top + y * self.cell_size + self.cell_size // 4),
                        (self.game_left + x * self.cell_size + self.cell_size * 3 // 4,
                         self.game_top + y * self.cell_size + self.cell_size // 2),
                        (self.game_left + x * self.cell_size + self.cell_size // 4,
                         self.game_top + y * self.cell_size + self.cell_size * 3 // 4)
                    ])

def main():
    # 初始化屏幕
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('扫雷')
    clock = pygame.time.Clock()
    
    # 创建按钮
    start_btn = Button(
        WINDOW_WIDTH//2 - 100,
        int(WINDOW_HEIGHT * 0.6),
        200,
        60,
        "开始游戏",
        button_color=START_BTN_COLOR,
        hover_color=START_BTN_HOVER
    )
    
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
    
    game = None
    game_started = False
    high_score = scores.load_scores()["minesweeper"]
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
            if back_btn.handle_event(event):
                return
                
            if not game_started:
                if start_btn.handle_event(event):
                    game_started = True
                    game = Minesweeper()
                continue
                
            if game_started and not game.game_over and not game.win:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    grid_x = (mouse_pos[0] - game.game_left) // game.cell_size
                    grid_y = (mouse_pos[1] - game.game_top) // game.cell_size
                    
                    if 0 <= grid_x < game.grid_size and 0 <= grid_y < game.grid_size:
                        if event.button == 1:  # 左键点击
                            game.reveal_cell(grid_x, grid_y)
                        elif event.button == 3:  # 右键点击
                            game.toggle_flag(grid_x, grid_y)
        
        # 更新游戏时间
        if game_started and game and not game.game_over and not game.win and not game.first_click:
            game.elapsed_time = current_time - game.start_time
        
        # 绘制
        screen.fill(BACKGROUND)
        
        if not game_started:
            # 绘制标题
            title_text = "扫雷"
            title_rect = game_font.get_rect(title_text)
            title_pos = (
                WINDOW_WIDTH//2 - title_rect.width // 2,
                WINDOW_HEIGHT//4
            )
            game_font.render_to(screen, title_pos, title_text, BLACK)
            
            # 绘制最高分
            high_score_text = f"历史最高分：{high_score}"
            high_score_rect = game_font.get_rect(high_score_text)
            high_score_pos = (
                WINDOW_WIDTH//2 - high_score_rect.width // 2,
                WINDOW_HEIGHT//4 + title_rect.height + 20
            )
            game_font.render_to(screen, high_score_pos, high_score_text, BLACK)
            
            # 绘制开始按钮
            start_btn.draw(screen)
        else:
            # 绘制游戏状态
            if game.game_over:
                status_text = "游戏结束"
            elif game.win:
                status_text = f"胜利！得分：{game.score}"
            else:
                status_text = f"剩余旗子：{game.flags_left} | 时间：{game.elapsed_time//1000}秒"
            
            status_rect = game_font.get_rect(status_text)
            status_pos = (
                WINDOW_WIDTH//2 - status_rect.width // 2,
                20
            )
            game_font.render_to(screen, status_pos, status_text, BLACK)
            
            # 绘制游戏网格
            game.draw(screen)
            
            # 如果游戏结束，显示重新开始按钮
            if game.game_over or game.win:
                restart_btn = Button(
                    WINDOW_WIDTH//2 - 100,
                    WINDOW_HEIGHT - 80,
                    200,
                    60,
                    "重新开始",
                    button_color=START_BTN_COLOR,
                    hover_color=START_BTN_HOVER
                )
                restart_btn.draw(screen)
                
                if restart_btn.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pygame.mouse.get_pos(), 'button': 1})):
                    game = Minesweeper()
        
        # 始终显示返回按钮
        back_btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 