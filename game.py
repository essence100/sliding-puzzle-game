from level import LevelManager
from menu import Menu

import pygame

from board import Board
from player import Player
from score import ScoreManager

from settings import (
    WIDTH,
    HEIGHT,
    TITLE,
    FPS,
    BACKGROUND
)


class Game:


    def __init__(self):

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            TITLE
        )


        self.clock = pygame.time.Clock()


        self.level_manager = LevelManager()

        self.score_manager = ScoreManager()


        self.font = pygame.font.SysFont(
            "arial",
            42,
            bold=True
        )


        self.small_font = pygame.font.SysFont(
            "arial",
            24,
            bold=True
        )


        self.timer_font = pygame.font.SysFont(
            "arial",
            26,
            bold=True
        )


        self.menu = Menu(self)


        self.state = "MENU"

        self.running = True



        # buttons

        self.restart_button = pygame.Rect(
            WIDTH//2 - 250,
            HEIGHT - 90,
            160,
            50
        )


        self.next_button = pygame.Rect(
            WIDTH//2 - 80,
            HEIGHT - 90,
            160,
            50
        )


        self.menu_button = pygame.Rect(
            WIDTH//2 + 90,
            HEIGHT - 90,
            160,
            50
        )






    def create_game(self):


        self.board = Board(
            level_manager=self.level_manager
        )


        self.board.shuffle()


        self.moves = 0


        self.timer_started = False


        self.start_ticks = 0


        self.elapsed_seconds = 0



        self.final_score = 0


        self.score_saved = False



        self.player = Player(

            self.board,

            self

        )






    def start_level(self, level):


        self.level_manager.set_level(level)


        self.create_game()


        self.state = "PLAYING"







    def restart(self):


        self.create_game()


        self.state = "PLAYING"








    def back_to_menu(self):


        self.state = "MENU"







    def next_level(self):


        current = self.level_manager.current_level


        if current != "HARD":


            self.level_manager.next_level()


            self.create_game()


            self.state = "PLAYING"









    def register_move(self):


        self.moves += 1



        if not self.timer_started:


            self.timer_started = True


            self.start_ticks = pygame.time.get_ticks()







    def save_score(self):


        if self.score_saved:

            return



        self.final_score = self.score_manager.update_best(

            self.elapsed_seconds,

            self.moves

        )


        self.score_saved = True







    def handle_events(self):


        for event in pygame.event.get():


            if event.type == pygame.QUIT:


                self.running = False



            elif self.state == "MENU":


                self.menu.handle_event(event)




            elif self.state == "PLAYING":


                self.player.handle_event(event)




            elif self.state == "COMPLETED":


                if event.type == pygame.MOUSEBUTTONDOWN:


                    if self.restart_button.collidepoint(event.pos):

                        self.restart()



                    elif self.menu_button.collidepoint(event.pos):

                        self.back_to_menu()



                    elif (
                        self.next_button.collidepoint(event.pos)
                        and
                        self.level_manager.current_level != "HARD"
                    ):


                        self.next_level()







    def update(self):


        if self.state == "MENU":

            return



        self.board.update()




        if (

            self.timer_started

            and

            self.state == "PLAYING"

        ):


            self.elapsed_seconds = (

                pygame.time.get_ticks()

                -

                self.start_ticks

            ) // 1000






        if self.board.completed:


            self.state = "COMPLETED"


            self.save_score()







    def draw_title(self):


        title = self.font.render(

            "SLIDING PUZZLE",

            True,

            (255,255,255)

        )


        self.screen.blit(

            title,

            title.get_rect(

                center=(

                    WIDTH//2,

                    35

                )

            )

        )








    def draw_info(self):


        minutes = self.elapsed_seconds // 60


        seconds = self.elapsed_seconds % 60



        time_text = self.timer_font.render(

            f"TIME: {minutes:02}:{seconds:02}",

            True,

            (255,255,255)

        )


        move_text = self.timer_font.render(

            f"MOVES: {self.moves}",

            True,

            (255,255,255)

        )


        self.screen.blit(

            time_text,

            (35,95)

        )


        self.screen.blit(

            move_text,

            (WIDTH-170,95)

        )








    def draw_button(
        self,
        rect,
        text
    ):


        pygame.draw.rect(

            self.screen,

            (56,189,248),

            rect,

            border_radius=12

        )


        label = self.small_font.render(

            text,

            True,

            (0,0,0)

        )


        self.screen.blit(

            label,

            label.get_rect(

                center=rect.center

            )

        )









    def draw_win_screen(self):


        overlay = pygame.Surface(

            (WIDTH,HEIGHT),

            pygame.SRCALPHA

        )


        overlay.fill(

            (0,0,0,180)

        )


        self.screen.blit(

            overlay,

            (0,0)

        )




        title = self.font.render(

            "🏆 YOU WIN!",

            True,

            (255,215,0)

        )



        score = self.small_font.render(

            f"SCORE: {self.final_score}",

            True,

            (255,255,255)

        )



        level = self.small_font.render(

            f"LEVEL: {self.level_manager.current_level}",

            True,

            (0,255,120)

        )



        self.screen.blit(

            title,

            title.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2-100

                )

            )

        )



        self.screen.blit(

            score,

            score.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2-50

                )

            )

        )



        self.screen.blit(

            level,

            level.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2

                )

            )

        )



        self.draw_button(

            self.restart_button,

            "RESTART"

        )


        if self.level_manager.current_level != "HARD":


            self.draw_button(

                self.next_button,

                "NEXT"

            )


        self.draw_button(

            self.menu_button,

            "MENU"

        )







    def draw(self):


        if self.state == "MENU":


            self.menu.draw(

                self.screen

            )


            pygame.display.flip()

            return





        self.screen.fill(

            BACKGROUND

        )



        self.draw_title()


        self.draw_info()



        self.board.draw(

            self.screen

        )




        if self.state == "COMPLETED":


            self.draw_win_screen()





        pygame.display.flip()







    def run(self):


        while self.running:


            self.handle_events()


            self.update()


            self.draw()


            self.clock.tick(FPS)