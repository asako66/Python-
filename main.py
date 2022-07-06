import pygame
from pygame.locals import *
import sys
import math

SCREEN = Rect((0,0,640,480))

class Ball(pygame.sprite.Sprite):
  """ボール"""
  SPEED = 5
  ANGLE_LEFT, ANGLE_RIGHT = 135, 45

  def __init__(self, paddle, blocks):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image = pygame.image.load("picture/ball.png").convert_alpha()
    self.image = pygame.transform.scale(self.image, (24,24))
    self.rect = self.image.get_rect()
    self.paddle = paddle
    self.rect.centerx = self.paddle.rect.centerx
    self.rect.bottom = self.paddle.rect.top
    self.dx = 0
    self.dy = 0
    self.blocks = blocks
    self.status = "INIT"

  def update(self):
    if self.status == "INIT":
      self.rect.centerx = self.paddle.rect.centerx
      self.rect.bottom = self.paddle.rect.top
    if pygame.mouse.get_pressed()[0] == 1:
      self.status = "RUNNING"
      self.dx = Ball.SPEED
      self.dy = -Ball.SPEED
    self.rect.centerx += self.dx
    self.rect.centery += self.dy
    # 壁との反射
    if self.rect.left < SCREEN.left:  # 左側
      self.rect.left = SCREEN.left
      self.dx = -self.dx  # 速度を反転
    if self.rect.right > SCREEN.right:  # 右側
      self.rect.right = SCREEN.right
      self.dx = -self.dx
    if self.rect.top < SCREEN.top:  # 上側
      self.rect.top = SCREEN.top
      self.dy = -self.dy
    # パドルとの反射
    if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
      self.dy = -self.dy
    # ボールを落とした場合
    if self.rect.top > SCREEN.bottom:
      self.status = "INIT"
      self.dx = 0
      self.dy = 0
      self.rect.centerx = self.paddle.rect.centerx
      self.rect.bottom = self.paddle.rect.top # ボールを初期状態に
    blocks_collided = pygame.sprite.spritecollide(self, self.blocks, True)
    if blocks_collided:
      for block in blocks_collided:
        # ボールが左から衝突
        if self.rect.left < block.rect.left < self.rect.right < block.rect.right:
          self.rect.right = block.rect.left
          self.dx = -self.dx
        # ボールが右から衝突
        if block.rect.left < self.rect.left < block.rect.right < self.rect.right:
          self.rect.left = block.rect.right
          self.dx = -self.dx
        # ボールが上から衝突
        if self.rect.top < block.rect.top < self.rect.bottom < block.rect.bottom:
          self.rect.bottom = block.rect.top
          self.dy = -self.dy
        # ボールが下から衝突
        if block.rect.top < self.rect.top < block.rect.bottom < self.rect.bottom:
          self.rect.top = block.rect.bottom
          self.dy = -self.dy

    # パドルとの反射
    if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
      # パドルの左端に当たったとき135度方向、右端で45度方向とし、
      # その間は線形補間で反射方向を計算
      x1 = self.paddle.rect.left - self.rect.width  # ボールが当たる左端
      y1 = self.angle_left  # 左端での反射方向（135度）
      x2 = self.paddle.rect.right  # ボールが当たる右端
      y2 = self.angle_right  # 右端での反射方向（45度）
      m = float(y2-y1) / (x2-x1)  # 直線の傾き
      x = self.rect.left  # ボールが当たった位置
      y = m * (x - x1) + y1
      angle = math.radians(y)
      self.dx = self.speed * math.cos(angle)  # float
      self.dy = -self.speed * math.sin(angle) # float

class Paddle(pygame.sprite.Sprite):
  """パドル"""

  def __init__(self):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image = pygame.image.load("picture/paddle.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.bottom = SCREEN.bottom

  def update(self):
    self.rect.centerx = pygame.mouse.get_pos()[0]
    self.rect.clamp_ip(SCREEN)

class Block(pygame.sprite.Sprite):
  """ブロック"""

  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image = pygame.image.load("picture/Block.png").convert_alpha()
    self.image = pygame.transform.scale(self.image, (56,56))
    self.rect = self.image.get_rect()
    self.rect.left = SCREEN.left + x * self.rect.width
    self.rect.top = SCREEN.top + y * self.rect.height

  def update(self):
    pass

def main():
  # 初期設定
  pygame.init()
  screen = pygame.display.set_mode(SCREEN.size)
  pygame.display.set_caption("Hello World")
  clock = pygame.time.Clock()

  # 登場する人もの背景の作成
  # Sprite登録
  group = pygame.sprite.RenderUpdates()
  blocks = pygame.sprite.Group()
  Paddle.containers = group
  Ball.containers = group
  Block.containers = group, blocks

  paddle = Paddle()
  for x in range(1, 11):  # 1列から10列まで
    for y in range(1, 3):  # 1行から5行まで
      Block(x, y)
  ball = Ball(paddle, blocks)

  while True:
    # 画面（screen）をクリア
    screen.fill((0,0,0))

    # ゲームに登場する人もの背景の位置Update
    group.update()

    # 画面（screen）上に登場する人もの背景を描画
    group.draw(screen)

    # 画面（screen）の実表示
    pygame.display.update()

    # イベント処理
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN and event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()

    # 描画スピードの調整（FPS）
    clock.tick(60)

if __name__ == "__main__":
  main()
