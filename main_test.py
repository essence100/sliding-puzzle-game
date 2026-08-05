import pygame

from board import Board
from player import Player

from settings import (
    WIDTH,
    HEIGHT,
    TITLE,
    FPS,
    BACKGROUND
)


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    board = Board()
    player = Player(board)

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            player.handle_event(event)


        screen.fill(BACKGROUND)

        board.draw(screen)

        pygame.display.update()

        clock.tick(FPS)


    pygame.quit()


if __name__ == "__main__":
    main()