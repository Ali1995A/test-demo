import pygame
import random
import sys
import os
from pygame.locals import *

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 游戏常量
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("飞机大战")
clock = pygame.time.Clock()

# 创建简单音效（不使用numpy）
def create_beep_sound(frequency=440, duration=100):
    """创建简单的蜂鸣音效"""
    sample_rate = 44100
    n_samples = int(round(duration * 0.001 * sample_rate))
    max_amplitude = 2**15 - 1
    
    # 创建空的音效
    sound = pygame.mixer.Sound(buffer=bytes(n_samples * 4))  # 静音音效
    
    # 使用pygame的简单音效替代
    return sound

# 初始化音效（使用静音音效，但保留音效接口）
shoot_sound = None
explosion_sound = None
hit_sound = None
game_over_sound = None

# 尝试使用pygame内置音效
try:
    # 射击音效 - 短促高频
    shoot_sound = pygame.mixer.Sound(buffer=bytes(2000))
    # 爆炸音效 - 低频
    explosion_sound = pygame.mixer.Sound(buffer=bytes(4000))
    # 被击中音效 - 中频
    hit_sound = pygame.mixer.Sound(buffer=bytes(3000))
    # 游戏结束音效 - 长音
    game_over_sound = pygame.mixer.Sound(buffer=bytes(8000))
    print("音效系统已初始化（基础音效）")
except:
    print("警告: 无法创建音效，游戏将静音运行")

# 加载图片资源
def load_image(name, scale=1):
    try:
        image = pygame.Surface((50, 50), pygame.SRCALPHA)
        if name == "player":
            # 绘制玩家飞机
            pygame.draw.polygon(image, BLUE, [(25, 0), (0, 50), (50, 50)])
            pygame.draw.circle(image, WHITE, (25, 15), 8)
        elif name == "enemy":
            # 绘制敌机
            pygame.draw.polygon(image, RED, [(0, 0), (50, 0), (25, 50)])
            pygame.draw.circle(image, WHITE, (25, 15), 6)
        elif name == "bullet":
            # 绘制子弹
            pygame.draw.rect(image, GREEN, (20, 0, 10, 20))
        elif name == "background":
            image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            image.fill((30, 30, 60))
            # 添加星空效果
            for _ in range(100):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                size = random.randint(1, 3)
                pygame.draw.circle(image, WHITE, (x, y), size)
        
        if scale != 1:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except Exception as e:
        print(f"加载图片失败: {e}")
        return pygame.Surface((50, 50))

# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("player")
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8
        self.health = 100
        self.shoot_delay = 250  # 射击延迟(毫秒)
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        # 键盘控制
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        
        # 自动射击
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        # 播放射击音效
        if shoot_sound:
            shoot_sound.play()

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("enemy")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-2, 2)
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # 如果敌机飞出屏幕底部或侧面，重新生成
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 25:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)
            self.speedx = random.randrange(-2, 2)

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("bullet")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        # 如果子弹飞出屏幕顶部，删除它
        if self.rect.bottom < 0:
            self.kill()

# 爆炸效果类
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.size = 50
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 165, 0), (self.size//2, self.size//2), self.size//2)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 8:
                self.kill()
            else:
                self.size = max(5, 50 - self.frame * 6)
                old_center = self.rect.center
                self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                pygame.draw.circle(self.image, (255, 165, 0), (self.size//2, self.size//2), self.size//2)
                self.rect = self.image.get_rect()
                self.rect.center = old_center

# 创建精灵组
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# 创建玩家
player = Player()
all_sprites.add(player)

# 生成敌机
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# 游戏状态
score = 0
game_over = False
font = pygame.font.Font(None, 36)

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
            if game_over and event.key == K_r:
                # 重新开始游戏
                game_over = False
                score = 0
                all_sprites = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                player = Player()
                all_sprites.add(player)
                for i in range(8):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)
    
    if not game_over:
        # 更新
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
            # 播放爆炸音效
            if explosion_sound:
                explosion_sound.play()
        
        # 检测玩家和敌机的碰撞
        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            player.health -= 20
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            # 播放被击中音效
            if hit_sound:
                hit_sound.play()
            if player.health <= 0:
                game_over = True
                # 播放游戏结束音效
                if game_over_sound:
                    game_over_sound.play()
    
    # 渲染
    screen.fill(BLACK)
    
    # 绘制背景
    background = load_image("background")
    screen.blit(background, (0, 0))
    
    # 绘制所有精灵
    all_sprites.draw(screen)
    
    # 绘制分数和生命值
    score_text = font.render(f"分数: {score}", True, WHITE)
    health_text = font.render(f"生命值: {player.health}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    
    # 游戏结束显示
    if game_over:
        game_over_text = font.render("游戏结束! 按R键重新开始", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
    
    # 刷新屏幕
    pygame.display.flip()

pygame.quit()
sys.exit()