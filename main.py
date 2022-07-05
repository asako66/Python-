import pygame
from pygame.locals import *
import sys

def main():
  # 初期設定
  pygame.init()
  screen = pygame.display.set_mode((600,400))
  SCREEN = screen.get_rect()
  pygame.display.set_caption("Hello World")
  clock = pygame.time.Clock()

  # 登場する人もの背景の作成

  while True:
    # 画面（screen）をクリア
    screen.fill((0,0,0))

    # ゲームに登場する人もの背景の位置Update

    # 画面（screen）上に登場する人もの背景を描画

    # 画面（screen）の実表示
    pygame.display.update()

    # イベント処理
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

    # 描画スピードの調整（FPS）
    clock.tick(60)

if __name__ == "__main__":
  main()
