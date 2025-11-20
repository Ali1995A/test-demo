import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏配置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
CELL_NUMBER_X = WINDOW_WIDTH // CELL_SIZE
CELL_NUMBER_Y = WINDOW_HEIGHT // CELL_SIZE

# 颜色定义
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')
clock = pygame.time.Clock()

# 字体设置
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        # 蛇的初始位置（身体由多个方块组成）
        self.body = [pygame.Vector2(5, 10), pygame.Vector2(4, 10), pygame.Vector2(3, 10)]
        self.direction = pygame.Vector2(1, 0)  # 初始向右移动
        self.new_block = False
    
    def draw_snake(self):
        """绘制蛇"""
        for block in self.body:
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, block_rect)
    
    def move_snake(self):
        """移动蛇"""
        if not self.new_block:
            # 删除尾部方块
            body_copy = self.body[:-1]
            # 在头部添加新方块
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
        else:
            # 如果吃到食物，不删除尾部方块（蛇变长）
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
    
    def add_block(self):
        """增加蛇的长度"""
        self.new_block = True
    
    def check_collision(self):
        """检查碰撞"""
        # 检查是否撞墙
        if not 0 <= self.body[0].x < CELL_NUMBER_X or not 0 <= self.body[0].y < CELL_NUMBER_Y:
            return True
        
        # 检查是否撞到自己
        for block in self.body[1:]:
            if block == self.body[0]:
                return True
        
        return False

class Food:
    def __init__(self):
        self.randomize()
    
    def draw_food(self):
        """绘制食物"""
        food_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)
    
    def randomize(self):
        """随机生成食物位置"""
        self.x = random.randint(0, CELL_NUMBER_X - 1)
        self.y = random.randint(0, CELL_NUMBER_Y - 1)
        self.pos = pygame.Vector2(self.x, self.y)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
    
    def update(self):
        """更新游戏状态"""
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        """绘制游戏元素"""
        screen.fill(BLACK)
        self.food.draw_food()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_collision(self):
        """检查蛇是否吃到食物"""
        if self.food.pos == self.snake.body[0]:
            # 重新生成食物
            self.food.randomize()
            # 确保食物不会生成在蛇身上
            for block in self.snake.body[1:]:
                if block == self.food.pos:
                    self.food.randomize()
            
            # 增加蛇长度和分数
            self.snake.add_block()
            self.score += 10
    
    def check_fail(self):
        """检查游戏是否结束"""
        if self.snake.check_collision():
            self.game_over()
    
    def game_over(self):
        """游戏结束"""
        pygame.quit()
        sys.exit()
    
    def draw_score(self):
        """显示分数"""
        score_text = str(self.score)
        score_surface = font.render(score_text, True, WHITE)
        score_x = int(WINDOW_WIDTH - 60)
        score_y = int(WINDOW_HEIGHT - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

# 创建游戏实例
game = Game()

# 设置游戏更新事件
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # 每150毫秒更新一次

# 游戏主循环
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == SCREEN_UPDATE:
            game.update()
        
        if event.type == pygame.KEYDOWN:
            # 控制蛇的方向
            if event.key == pygame.K_UP:
                if game.snake.direction.y != 1:  # 防止反向移动
                    game.snake.direction = pygame.Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if game.snake.direction.y != -1:
                    game.snake.direction = pygame.Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if game.snake.direction.x != -1:
                    game.snake.direction = pygame.Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if game.snake.direction.x != 1:
                    game.snake.direction = pygame.Vector2(-1, 0)
    
    # 绘制游戏画面
    game.draw_elements()
    pygame.display.update()
    clock.tick(60)