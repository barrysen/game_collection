# -*- coding: utf-8 -*-
import pygame
import sys
import snake_game
import tetris_game
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
    def __init__(self, x, y, width, height, text, icon=None, small=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = icon  # 添加图标
        self.color = BUTTON_COLOR
        self.is_hovered = False
        self.border_radius = 10
        self.small = small  # 是否使用小号字体
        
    def draw(self, surface):
        # 绘制按钮阴影
        shadow_rect = self.rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(surface, BUTTON_BORDER, shadow_rect, border_radius=self.border_radius)
        
        # 绘制按钮
        color = BUTTON_HOVER if self.is_hovered else self.color
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
            font.render_to(surface, icon_pos, self.icon, TEXT_COLOR)
            font.render_to(surface, text_pos, self.text, TEXT_COLOR)
        else:
            # 没有图标，只绘制文本
            text_rect = font.get_rect(self.text)
            text_pos = (
                self.rect.centerx - text_rect.width//2,
                self.rect.centery - text_rect.height//2
            )
            font.render_to(surface, text_pos, self.text, TEXT_COLOR)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

def main():
    # 创建按钮 - 调整按钮大小和位置
    button_width = 240
    button_height = 80
    spacing = 60  # 按钮之间的间距
    
    total_width = 2 * button_width + spacing
    start_x = (WINDOW_WIDTH - total_width) // 2
    
    snake_btn = Button(start_x, WINDOW_HEIGHT//2, button_width, button_height, "贪吃蛇")
    tetris_btn = Button(start_x + button_width + spacing, WINDOW_HEIGHT//2, button_width, button_height, "俄罗斯方块")
    
    # 主循环
    running = True
    while running:
        screen.fill(BACKGROUND)
        
        # 渲染标题
        title_text = "经典游戏合集"
        title_rect = title_font.get_rect(title_text)
        title_pos = (
            WINDOW_WIDTH//2 - title_rect.width // 2,
            WINDOW_HEIGHT//3 - title_rect.height // 2
        )
        title_font.render_to(screen, title_pos, title_text, TEXT_COLOR)
        
        # 渲染副标题
        subtitle_text = "请选择要玩的游戏"
        subtitle_rect = game_font.get_rect(subtitle_text)
        subtitle_pos = (
            WINDOW_WIDTH//2 - subtitle_rect.width // 2,
            WINDOW_HEIGHT//3 + title_rect.height
        )
        game_font.render_to(screen, subtitle_pos, subtitle_text, TEXT_COLOR)
        
        # 绘制按钮
        snake_btn.draw(screen)
        tetris_btn.draw(screen)
        
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
        
        pygame.display.flip()

if __name__ == "__main__":
    main() 