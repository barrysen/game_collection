import pygame
import random
import sys
import scores

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

# 定义颜色
BACKGROUND = (255, 255, 255)  # 白色背景
BLACK = (0, 0, 0)  # 纯黑色
GRAY = (128, 128, 128)  # 灰色
LIGHT_GRAY = (200, 200, 200)  # 浅灰色
WHITE = (255, 255, 255)  # 白色
ORANGE = (255, 159, 28)  # 橙色
ORANGE_HOVER = (230, 144, 25)  # 深橙色用于悬停

# 游戏元素颜色
SNAKE_COLORS = [
    (46, 204, 113),  # 绿色
    (52, 152, 219),  # 蓝色
    (155, 89, 182),  # 紫色
    (241, 196, 15),  # 黄色
    (231, 76, 60),   # 红色
    (230, 126, 34),  # 橙色
]

# 按钮颜色
BACK_BTN_COLOR = (240, 240, 240)  # 返回按钮使用浅灰白色
BACK_BTN_HOVER = (220, 220, 220)  # 返回按钮悬停色更柔和
BACK_BTN_TEXT = (80, 80, 80)  # 返回按钮文字用深灰色
START_BTN_COLOR = ORANGE  # 开始按钮使用橙色
START_BTN_HOVER = ORANGE_HOVER  # 开始按钮悬停色
BUTTON_TEXT = WHITE  # 开始按钮文字保持白色
BUTTON_BORDER = (200, 200, 200)  # 按钮边框和阴影颜色

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
GAME_SPEED = 15

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = RIGHT  # 设置初始方向向右
        self.color = random.choice(SNAKE_COLORS)  # 随机选择颜色
        self.score = 0
        self.is_moving = True  # 默认开始移动

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x*BLOCK_SIZE)) % WINDOW_WIDTH, (cur[1] + (y*BLOCK_SIZE)) % WINDOW_HEIGHT)
        if new in self.positions[3:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            # 每次吃到食物时改变颜色
            if len(self.positions) > self.length:
                self.color = random.choice(SNAKE_COLORS)
            return True

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = RIGHT  # 重置方向为向右
        self.score = 0
        self.is_moving = True  # 重置为开始移动

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = random.choice(SNAKE_COLORS)  # 随机选择颜色
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                        random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)
        self.color = random.choice(SNAKE_COLORS)  # 每次重新生成时改变颜色

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# 定义方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

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

def main():
    snake = Snake()
    food = Food()
    running = True
    game_started = False
    high_score = scores.load_scores()["snake"]  # 加载最高分
    
    # 创建开始按钮 - 使用橙色
    start_btn = Button(
        WINDOW_WIDTH//2 - 100,
        WINDOW_HEIGHT//2 - 30,
        200,
        60,
        "开始游戏",
        button_color=START_BTN_COLOR,
        hover_color=START_BTN_HOVER
    )
    
    # 创建返回按钮 - 使用灰色
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
            # 处理返回按钮事件
            if back_btn.handle_event(event):
                return  # 直接返回到游戏选择菜单
                
            if not game_started:
                if start_btn.handle_event(event):
                    game_started = True
                    snake.is_moving = True
                continue
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                    snake.is_moving = True
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                    snake.is_moving = True
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                    snake.is_moving = True
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                    snake.is_moving = True
                elif event.key == pygame.K_SPACE:
                    snake.is_moving = not snake.is_moving

        screen.fill(BACKGROUND)
        
        if not game_started:
            # 1. 游戏标题
            title_text = "贪吃蛇"
            title_rect = game_font.get_rect(title_text)
            title_pos = (
                WINDOW_WIDTH//2 - title_rect.width // 2,
                WINDOW_HEIGHT//4
            )
            game_font.render_to(screen, title_pos, title_text, BLACK)
            
            # 2. 最高分显示
            high_score_text = f"历史最高分：{high_score}"
            high_score_rect = game_font.get_rect(high_score_text)
            high_score_pos = (
                WINDOW_WIDTH//2 - high_score_rect.width // 2,
                WINDOW_HEIGHT//4 + title_rect.height + 20
            )
            game_font.render_to(screen, high_score_pos, high_score_text, BLACK)
            
            # 3. 开始按钮 - 位于中间偏下位置
            start_btn.rect.centerx = WINDOW_WIDTH//2
            start_btn.rect.centery = WINDOW_HEIGHT * 0.6  # 位于屏幕60%处
            start_btn.draw(screen)
        else:
            # 游戏逻辑
            if snake.is_moving:
                if not snake.update():
                    # 游戏结束时保存最高分
                    scores.save_score("snake", snake.score)
                    high_score = scores.load_scores()["snake"]  # 重新加载最高分
                    snake.reset()
                    food.randomize_position()
                    game_started = False

            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()

            # 绘制游戏元素
            snake.draw(screen)
            food.draw(screen)
            score_text = f'得分: {snake.score}'
            high_score_text = f'最高分: {high_score}'
            game_font.render_to(screen, (10, 70), score_text, WHITE)
            game_font.render_to(screen, (10, 120), high_score_text, WHITE)  # 显示最高分
        
        # 始终显示返回按钮
        back_btn.draw(screen)
        
        pygame.display.update()
        clock.tick(10)

if __name__ == '__main__':
    main() 