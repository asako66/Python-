from shutil import move
import pygame
from pygame.locals import *
import sys

SCREEN = Rect((0,0,640,480))

class Ball(pygame.sprite.Sprite):
  """ボール"""
  SPEED = 5

  def __init__(self, paddle):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image = pygame.image.load("ball.png")
    self.rect = self.image.get_rect()
    self.paddle = paddle
    self.rect.centerx = self.paddle.rect.centerx
    self.rect.bottom = self.paddle.rect.top
    self.dx = 0
    self.dy = 0
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
      self.rect.bottom = self.paddle.rect.top
      # ボールを初期状態に

class Paddle(pygame.sprite.Sprite):
  """パドル"""

  def __init__(self):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image = pygame.image.load("paddle.png")
    self.rect = self.image.get_rect()
    self.rect.bottom = SCREEN.bottom

  def update(self):
    self.rect.centerx = pygame.mouse.get_pos()[0]
    self.rect.clamp_ip(SCREEN)


def main():
  # 初期設定
  pygame.init()
  screen = pygame.display.set_mode(SCREEN.size)
  pygame.display.set_caption("Hello World")
  clock = pygame.time.Clock()

  # 登場する人もの背景の作成
  # Sprite登録
  group = pygame.sprite.RenderUpdates()
  Paddle.containers = group
  Ball.containers = group

  paddle = Paddle()
  ball = Ball(paddle)

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
