import pygame
from pygame.locals import *
import sys

SCREEN = Rect((0,0,640,480))

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

  paddle = Paddle()

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
