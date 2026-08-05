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


        # SYSTEMS

        self.level_manager = LevelManager()

        self.score_manager = ScoreManager()


        # FONTS

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


        # MENU

        self.menu = Menu(self)


        # GAME STATE

        self.state = "MENU"

        self.running = True





    # =================================
    # CREATE GAME
    # =================================

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



        # WIN BUTTONS

        self.restart_button = pygame.Rect(

            WIDTH//2 - 100,
            HEIGHT//2 + 70,
            200,
            45

        )


        self.next_button = pygame.Rect(

            WIDTH//2 - 100,
            HEIGHT//2 + 125,
            200,
            45

        )


        self.menu_button = pygame.Rect(

            WIDTH//2 - 100,
            HEIGHT//2 + 180,
            200,
            45

        )







    # =================================
    # START LEVEL
    # =================================

    def start_level(self, level):


        self.level_manager.set_level(level)


        self.create_game()


        self.state = "PLAYING"







    # =================================
    # RESTART
    # =================================

    def restart(self):


        self.create_game()


        self.state = "PLAYING"







    # =================================
    # NEXT LEVEL
    # =================================

    def next_level(self):


        current = self.level_manager.current_level


        if current != "HARD":


            self.level_manager.next_level()


            self.create_game()


            self.state = "PLAYING"







    # =================================
    # BACK TO MENU
    # =================================

    def back_to_menu(self):


        self.state = "MENU"







    # =================================
    # MOVES
    # =================================

    def register_move(self):


        self.moves += 1



        if not self.timer_started:


            self.timer_started = True


            self.start_ticks = pygame.time.get_ticks()






    # =================================
    # SCORE
    # =================================

    def save_score(self):


        if self.score_saved:

            return



        self.final_score = self.score_manager.update_best(

            self.elapsed_seconds,

            self.moves

        )


        self.score_saved = True







    # =================================
    # EVENTS
    # =================================

    def handle_events(self):


        for event in pygame.event.get():


            if event.type == pygame.QUIT:


                self.running = False



            elif self.state == "MENU":


                self.menu.handle_event(event)



            elif self.state == "PLAYING":


                self.player.handle_event(event)




            elif self.state == "COMPLETED":



                if event.type == pygame.KEYDOWN:


                    if event.key == pygame.K_r:


                        self.restart()



                elif event.type == pygame.MOUSEBUTTONDOWN:



                    if self.restart_button.collidepoint(event.pos):


                        self.restart()



                    elif self.next_button.collidepoint(event.pos):


                        self.next_level()



                    elif self.menu_button.collidepoint(event.pos):


                        self.back_to_menu()
                            # =================================
    # UPDATE
    # =================================

    def update(self):


        if self.state == "MENU":

            return



        self.board.update()



        # TIMER

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





        # WIN CHECK

        if self.board.completed:


            if self.state != "COMPLETED":


                self.state = "COMPLETED"


                self.save_score()







    # =================================
    # TITLE
    # =================================

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






    # =================================
    # LEVEL DISPLAY
    # =================================

    def draw_level(self):


        level_text = self.small_font.render(

            f"LEVEL: {self.level_manager.current_level}",

            True,

            (56,189,248)

        )


        size_text = self.small_font.render(

            f"{self.level_manager.get_size()} x {self.level_manager.get_size()}",

            True,

            (255,255,255)

        )



        self.screen.blit(

            level_text,

            (

                WIDTH//2 - 70,

                65

            )

        )


        self.screen.blit(

            size_text,

            (

                WIDTH//2 - 35,

                95

            )

        )







    # =================================
    # TIMER + MOVES
    # =================================

    def draw_info(self):


        minutes = self.elapsed_seconds // 60


        seconds = self.elapsed_seconds % 60



        time_text = self.timer_font.render(

            f"TIME: {minutes:02}:{seconds:02}",

            True,

            (255,255,255)

        )



        moves_text = self.timer_font.render(

            f"MOVES: {self.moves}",

            True,

            (255,255,255)

        )




        self.screen.blit(

            time_text,

            (35,120)

        )



        self.screen.blit(

            moves_text,

            (

                WIDTH-170,

                120

            )

        )









    # =================================
    # BUTTON DRAW
    # =================================

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
            # =================================
    # WIN SCREEN
    # =================================

    def draw_win_screen(self):


        overlay = pygame.Surface(

            (WIDTH, HEIGHT),

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


        score_text = self.small_font.render(

            f"SCORE: {self.final_score}",

            True,

            (255,255,255)

        )


        level_text = self.small_font.render(

            f"LEVEL: {self.level_manager.current_level}",

            True,

            (56,189,248)

        )


        moves_text = self.small_font.render(

            f"MOVES: {self.moves}",

            True,

            (255,255,255)

        )



        self.screen.blit(

            title,

            title.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2-120

                )

            )

        )



        self.screen.blit(

            score_text,

            score_text.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2-70

                )

            )

        )



        self.screen.blit(

            level_text,

            level_text.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2-35

                )

            )

        )



        self.screen.blit(

            moves_text,

            moves_text.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2

                )

            )

        )




        # BUTTONS


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









    # =================================
    # DRAW
    # =================================

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


        self.draw_level()


        self.draw_info()



        self.board.draw(

            self.screen

        )



        if self.state == "COMPLETED":


            self.draw_win_screen()




        pygame.display.flip()







    # =================================
    # MAIN LOOP
    # =================================

    def run(self):


        while self.running:


            self.handle_events()


            self.update()


            self.draw()


            self.clock.tick(FPS)