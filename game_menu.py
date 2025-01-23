# -*- coding: utf-8 -*-
import pygame
import sys
import snake_game
import tetris_game
import minesweeper_game
import pygame.freetype

# 初始化 Pygame
pygame.init()
pygame.freetype.init()

# 设置窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('游戏选择')

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BACKGROUND = (240, 245, 250)  # 浅蓝灰色背景
BUTTON_COLOR = (255, 255, 255)  # 纯白按钮
BUTTON_HOVER = (230, 235, 240)  # 浅灰色悬停
BUTTON_BORDER = (180, 185, 190)  # 浅灰色边框
TEXT_COLOR = (50, 55, 60)  # 深灰色文字

# 创建字体对象
try:
    # Mac系统中文字体路径
    font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
    game_font = pygame.freetype.Font(font_path, 36)
    title_font = pygame.freetype.Font(font_path, 48)
    small_font = pygame.freetype.Font(font_path, 24)  # 添加小号字体
except Exception as e:
    print(f"加载字体失败: {e}")
    try:
        # 尝试其他中文字体
        font_path = "/System/Library/Fonts/STHeiti Light.ttc"
        game_font = pygame.freetype.Font(font_path, 36)
        title_font = pygame.freetype.Font(font_path, 48)
        small_font = pygame.freetype.Font(font_path, 24)  # 添加小号字体
    except Exception as e:
        print(f"加载备用字体失败: {e}")
        # 如果都失败了，使用系统默认字体
        game_font = pygame.freetype.SysFont(None, 36)
        title_font = pygame.freetype.SysFont(None, 48)
        small_font = pygame.freetype.SysFont(None, 24)  # 添加小号字体

class Button:
    def __init__(self, x, y, width, height, text, description=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.description = description
        self.color = BUTTON_COLOR
        self.is_hovered = False
        self.border_radius = 10
        
    def draw(self, surface):
        # 绘制按钮阴影
        shadow_rect = self.rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(surface, BUTTON_BORDER, shadow_rect, border_radius=self.border_radius)
        
        # 绘制按钮
        color = BUTTON_HOVER if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, BUTTON_BORDER, self.rect, 2, border_radius=self.border_radius)
        
        # 绘制文本（居中）
        text_rect = game_font.get_rect(self.text)
        text_pos = (
            self.rect.centerx - text_rect.width // 2,
            self.rect.centery - text_rect.height // 2
        )
        game_font.render_to(surface, text_pos, self.text, TEXT_COLOR)
        
        # 如果有描述文本且鼠标悬停时显示
        if self.description and self.is_hovered:
            desc_rect = small_font.get_rect(self.description)
            desc_pos = (
                self.rect.centerx - desc_rect.width // 2,
                self.rect.bottom + 10
            )
            # 绘制描述文本背景
            bg_rect = pygame.Rect(
                desc_pos[0] - 10,
                desc_pos[1] - 5,
                desc_rect.width + 20,
                desc_rect.height + 10
            )
            pygame.draw.rect(surface, WHITE, bg_rect, border_radius=5)
            pygame.draw.rect(surface, BUTTON_BORDER, bg_rect, 1, border_radius=5)
            small_font.render_to(surface, desc_pos, self.description, TEXT_COLOR)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

def main():
    # 创建按钮 - 调整按钮大小和位置
    button_width = 200  # 适中的按钮宽度
    button_height = 60  # 适中的按钮高度
    vertical_spacing = 80  # 按钮之间的垂直间距
    
    # 标题位置
    title_y = 80  # 固定标题在顶部
    subtitle_y = title_y + 80  # 副标题在标题下方
    
    # 计算按钮起始位置，确保整体布局居中
    content_height = 3 * button_height + 2 * vertical_spacing  # 按钮区域总高度
    start_y = (WINDOW_HEIGHT + subtitle_y - content_height) // 2  # 从中间向下布局
    
    # 所有按钮水平居中
    center_x = WINDOW_WIDTH // 2 - button_width // 2
    
    # 创建三个按钮，垂直排列，添加描述
    snake_btn = Button(
        center_x, start_y,
        button_width, button_height,
        "贪吃蛇",
        "通过方向键控制蛇移动，吃到食物可以增加长度"
    )
    
    tetris_btn = Button(
        center_x, start_y + button_height + vertical_spacing,
        button_width, button_height,
        "俄罗斯方块",
        "经典俄罗斯方块，使用方向键控制方块移动和旋转"
    )
    
    minesweeper_btn = Button(
        center_x, start_y + 2 * (button_height + vertical_spacing),
        button_width, button_height,
        "扫雷",
        "经典扫雷游戏，左键点击揭示方块，右键标记地雷"
    )
    
    # 主循环
    running = True
    while running:
        screen.fill(BACKGROUND)
        
        # 渲染标题
        title_text = "经典游戏合集"
        title_rect = title_font.get_rect(title_text)
        title_pos = (
            WINDOW_WIDTH//2 - title_rect.width // 2,
            title_y
        )
        title_font.render_to(screen, title_pos, title_text, TEXT_COLOR)
        
        # 渲染副标题
        subtitle_text = "请选择要玩的游戏"
        subtitle_rect = game_font.get_rect(subtitle_text)
        subtitle_pos = (
            WINDOW_WIDTH//2 - subtitle_rect.width // 2,
            subtitle_y
        )
        game_font.render_to(screen, subtitle_pos, subtitle_text, TEXT_COLOR)
        
        # 绘制按钮
        snake_btn.draw(screen)
        tetris_btn.draw(screen)
        minesweeper_btn.draw(screen)
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if snake_btn.handle_event(event):
                snake_game.main()
                # 游戏结束后返回菜单
                pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                pygame.display.set_caption('游戏选择')
                
            if tetris_btn.handle_event(event):
                tetris_game.main()
                # 游戏结束后返回菜单
                pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                pygame.display.set_caption('游戏选择')
                
            if minesweeper_btn.handle_event(event):
                minesweeper_game.main()
                # 游戏结束后返回菜单
                pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                pygame.display.set_caption('游戏选择')
        
        pygame.display.flip()

if __name__ == "__main__":
    main() 