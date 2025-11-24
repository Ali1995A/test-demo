import pygame
import random
import sys
import os
from pygame.locals import *
import math

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 游戏常量
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
FPS = 60

# 颜色定义 - 更丰富的配色方案
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
DARK_BLUE = (25, 25, 112)
LIGHT_BLUE = (173, 216, 230)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("飞机大战 - 增强版")
clock = pygame.time.Clock()

# 字体系统
def load_fonts():
    """加载不同大小的字体"""
    fonts = {}
    try:
        fonts['small'] = pygame.font.Font(None, 24)
        fonts['normal'] = pygame.font.Font(None, 36)
        fonts['large'] = pygame.font.Font(None, 48)
        fonts['title'] = pygame.font.Font(None, 60)
    except:
        fonts['small'] = pygame.font.SysFont(None, 24)
        fonts['normal'] = pygame.font.SysFont(None, 36)
        fonts['large'] = pygame.font.SysFont(None, 48)
        fonts['title'] = pygame.font.SysFont(None, 60)
    return fonts

fonts = load_fonts()

# 音效系统（改进版）
def create_improved_sounds():
    """创建改进的音效系统"""
    try:
        # 使用pygame的音效生成功能
        shoot_sound = pygame.mixer.Sound(buffer=bytes(2000))
        explosion_sound = pygame.mixer.Sound(buffer=bytes(4000))
        hit_sound = pygame.mixer.Sound(buffer=bytes(3000))
        game_over_sound = pygame.mixer.Sound(buffer=bytes(8000))
        return shoot_sound, explosion_sound, hit_sound, game_over_sound
    except:
        return None, None, None, None

shoot_sound, explosion_sound, hit_sound, game_over_sound = create_improved_sounds()

# 增强的图片加载系统
def create_player_ship():
    """创建精美的玩家飞机"""
    surface = pygame.Surface((60, 80), pygame.SRCALPHA)
    
    # 主机身 - 渐变效果
    pygame.draw.polygon(surface, LIGHT_BLUE, [(30, 0), (10, 60), (50, 60)])
    pygame.draw.polygon(surface, BLUE, [(30, 10), (15, 50), (45, 50)])
    
    # 机翼
    pygame.draw.polygon(surface, DARK_BLUE, [(0, 30), (20, 40), (20, 50), (0, 60)])
    pygame.draw.polygon(surface, DARK_BLUE, [(60, 30), (40, 40), (40, 50), (60, 60)])
    
    # 机翼装饰
    pygame.draw.rect(surface, WHITE, (15, 35, 5, 15))
    pygame.draw.rect(surface, WHITE, (40, 35, 5, 15))
    
    # 驾驶舱
    pygame.draw.ellipse(surface, WHITE, (23, 15, 14, 20))
    pygame.draw.ellipse(surface, CYAN, (25, 17, 10, 16))
    
    # 尾翼
    pygame.draw.polygon(surface, DARK_BLUE, [(25, 50), (30, 70), (35, 50)])
    
    # 发动机火焰效果
    for i in range(3):
        alpha = 150 - i * 40
        color = (255, 100 + i * 50, 0, alpha)
        flame_surface = pygame.Surface((10, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(flame_surface, color[:3], (0, 0, 10, 20))
        surface.blit(flame_surface, (25, 60 + i * 5))
    
    return surface

def create_enemy_ship():
    """创建精美的敌机"""
    surface = pygame.Surface((50, 60), pygame.SRCALPHA)
    
    # 主机身
    pygame.draw.polygon(surface, RED, [(25, 0), (0, 50), (50, 50)])
    pygame.draw.polygon(surface, DARK_RED, [(25, 10), (5, 40), (45, 40)])
    
    # 机翼
    pygame.draw.polygon(surface, ORANGE, [(0, 20), (15, 30), (15, 40), (0, 50)])
    pygame.draw.polygon(surface, ORANGE, [(50, 20), (35, 30), (35, 40), (50, 50)])
    
    # 驾驶舱
    pygame.draw.ellipse(surface, WHITE, (18, 15, 14, 12))
    pygame.draw.ellipse(surface, YELLOW, (20, 17, 10, 8))
    
    # 武器
    pygame.draw.rect(surface, GRAY, (22, 45, 6, 15))
    pygame.draw.rect(surface, GRAY, (12, 50, 4, 10))
    pygame.draw.rect(surface, GRAY, (34, 50, 4, 10))
    
    return surface

def create_bullet():
    """创建精美的子弹"""
    surface = pygame.Surface((8, 20), pygame.SRCALPHA)
    
    # 子弹主体
    pygame.draw.rect(surface, YELLOW, (2, 0, 4, 15))
    pygame.draw.rect(surface, WHITE, (3, 2, 2, 11))
    
    # 子弹特效
    pygame.draw.circle(surface, ORANGE, (4, 17), 2)
    
    return surface

def create_explosion_frames():
    """创建爆炸动画帧"""
    frames = []
    for i in range(8):
        size = 60 - i * 6
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # 多层爆炸效果
        colors = [
            (255, 255, 255),  # 白色中心
            (255, 255, 0),    # 黄色
            (255, 165, 0),    # 橙色
            (255, 0, 0),      # 红色
            (139, 0, 0)       # 深红色
        ]
        
        center = size // 2
        for j, color in enumerate(colors):
            radius = center - j * 3 - i * 2
            if radius > 0:
                pygame.draw.circle(surface, color, (center, center), radius)
        
        frames.append(surface)
    
    return frames

def create_enhanced_background():
    """创建增强的背景"""
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # 渐变背景
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(15 + ratio * 30)
        g = int(15 + ratio * 30)
        b = int(60 + ratio * 90)
        color = (r, g, b)
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
    
    # 动态星星
    for _ in range(150):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.choice([1, 1, 1, 2, 2, 3])  # 大小权重
        brightness = random.randint(100, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(surface, color, (x, y), size)
    
    # 流星效果
    for _ in range(5):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(-100, SCREEN_HEIGHT)
        length = random.randint(20, 60)
        pygame.draw.line(surface, WHITE, (x, y), (x - length//3, y + length), 2)
    
    return surface

# 粒子系统
class Particle:
    def __init__(self, pos, vel, color, life):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.life = life
        self.max_life = life
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.life -= 1
        return self.life > 0
    
    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color[:3], alpha)
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (2, 2), 2)
            surface.blit(particle_surface, (self.pos[0] - 2, self.pos[1] - 2))

# 玩家飞机类 - 增强版
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = create_player_ship()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 6
        self.health = 100
        self.max_health = 100
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.invulnerable = False
        self.invulnerable_time = 0
        
    def update(self):
        # 键盘控制
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 50:  # 留出UI空间
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        
        # 无敌时间处理
        if self.invulnerable:
            if pygame.time.get_ticks() - self.invulnerable_time > 1000:
                self.invulnerable = False
        
        # 自动射击
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        if shoot_sound:
            shoot_sound.play()
    
    def take_damage(self, damage):
        if not self.invulnerable:
            self.health -= damage
            self.invulnerable = True
            self.invulnerable_time = pygame.time.get_ticks()
            return True
        return False
    
    def draw_health_bar(self, surface):
        # 生命条背景
        bar_width = 120
        bar_height = 15
        bar_x = 10
        bar_y = 10
        
        pygame.draw.rect(surface, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # 生命条
        health_ratio = self.health / self.max_health
        if health_ratio > 0.6:
            color = GREEN
        elif health_ratio > 0.3:
            color = YELLOW
        else:
            color = RED
        
        pygame.draw.rect(surface, color, (bar_x, bar_y, bar_width * health_ratio, bar_height))
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # 生命值文字
        health_text = fonts['small'].render(f"{self.health}/{self.max_health}", True, WHITE)
        text_rect = health_text.get_rect(center=(bar_x + bar_width//2, bar_y + bar_height//2))
        surface.blit(health_text, text_rect)

# 敌机类 - 增强版
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = create_enemy_ship()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -50)
        self.speedy = random.randrange(1, 3)
        self.speedx = random.randrange(-1, 2)
        self.health = 1
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # 边界检测
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()
        
        # 左右边界反弹
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speedx = -self.speedx

# 子弹类 - 增强版
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = create_bullet()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -12
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# 增强的爆炸效果类
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.frames = create_explosion_frames()
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        # 添加粒子效果
        self.particles = []
        for _ in range(10):
            pos = [center[0], center[1]]
            vel = [random.uniform(-3, 3), random.uniform(-3, 3)]
            color = random.choice([RED, ORANGE, YELLOW])
            life = random.randint(20, 40)
            self.particles.append(Particle(pos, vel, color, life))
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame]
        
        # 更新粒子
        self.particles = [p for p in self.particles if p.update()]
    
    def draw_particles(self, surface):
        for particle in self.particles:
            particle.draw(surface)

# 创建精灵组
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# 创建玩家
player = Player()
all_sprites.add(player)

# 生成敌机
for i in range(6):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# 游戏状态
score = 0
high_score = 0
game_over = False
paused = False
background = create_enhanced_background()

# UI相关函数
def draw_ui(surface):
    """绘制UI界面"""
    # 绘制生命条
    player.draw_health_bar(surface)
    
    # 绘制分数
    score_text = fonts['normal'].render(f"分数: {score}", True, WHITE)
    surface.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
    
    # 绘制最高分
    high_score_text = fonts['small'].render(f"最高分: {high_score}", True, WHITE)
    surface.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 10, 50))
    
    # 绘制敌机数量
    enemy_count = len(enemies)
    enemy_text = fonts['small'].render(f"敌机: {enemy_count}", True, WHITE)
    surface.blit(enemy_text, (10, 40))

def draw_game_over_screen(surface):
    """绘制游戏结束界面"""
    # 半透明背景
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # 游戏结束文字
    game_over_text = fonts['title'].render("游戏结束", True, RED)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
    surface.blit(game_over_text, text_rect)
    
    # 最终分数
    final_score_text = fonts['large'].render(f"最终分数: {score}", True, WHITE)
    text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    surface.blit(final_score_text, text_rect)
    
    # 重新开始提示
    restart_text = fonts['normal'].render("按 R 键重新开始", True, YELLOW)
    text_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
    surface.blit(restart_text, text_rect)
    
    # 退出提示
    exit_text = fonts['small'].render("按 ESC 键退出", True, WHITE)
    text_rect = exit_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
    surface.blit(exit_text, text_rect)

# 游戏主循环
running = True
while running:
    # 保持游戏运行速度
    clock.tick(FPS)
    
    # 处理事件
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_p:  # 暂停功能
                if not game_over:
                    paused = not paused
            elif event.key == K_SPACE:  # 空格键暂停功能
                if not game_over:
                    paused = not paused
            elif event.key == K_r and game_over:
                # 重新开始游戏
                game_over = False
                score = 0
                all_sprites = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                player = Player()
                all_sprites.add(player)
                for i in range(6):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)
        elif event.type == MOUSEBUTTONDOWN:
            # 鼠标点击暂停功能
            if not game_over and event.button == 1:  # 左键点击
                paused = not paused
    
    if not game_over and not paused:
        # 更新游戏逻辑
        all_sprites.update()
        
        # 检测子弹和敌机的碰撞
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            if explosion_sound:
                explosion_sound.play()
            
            # 更新最高分
            if score > high_score:
                high_score = score
        
        # 检测玩家和敌机的碰撞
        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            if player.take_damage(20):
                explosion = Explosion(hit.rect.center)
                all_sprites.add(explosion)
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
                if hit_sound:
                    hit_sound.play()
                if player.health <= 0:
                    game_over = True
                    if game_over_sound:
                        game_over_sound.play()
    
    # 渲染
    screen.blit(background, (0, 0))
    
    # 绘制所有精灵
    all_sprites.draw(screen)
    
    # 绘制爆炸粒子
    for sprite in all_sprites:
        if isinstance(sprite, Explosion):
            sprite.draw_particles(screen)
    
    # 绘制UI
    if not game_over:
        draw_ui(screen)
    
    # 绘制暂停提示
    if paused:
        pause_text = fonts['large'].render("游戏暂停 - 按 P 或空格键继续", True, YELLOW)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(pause_text, text_rect)
        
        # 鼠标操作提示
        mouse_text = fonts['small'].render("点击鼠标左键也可暂停/继续", True, WHITE)
        text_rect = mouse_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        screen.blit(mouse_text, text_rect)
    
    # 游戏结束显示
    if game_over:
        draw_game_over_screen(screen)
    
    # 刷新屏幕
    pygame.display.flip()

pygame.quit()
sys.exit()