import pygame


from level import LevelManager
from menu import Menu
from board import Board
from player import Player
from score import ScoreManager


from settings import (
    WIDTH,
    HEIGHT,
    TITLE,
    FPS,
    BACKGROUND,
    WHITE,
    BUTTON_COLOR,
    BUTTON_HOVER,
    BUTTON_TEXT,
    WIN_GOLD,
    STAR_COLOR
)



class Game:


    def __init__(self):


        # =========================
        # WINDOW
        # =========================


        self.screen = pygame.display.set_mode(
            (
                WIDTH,
                HEIGHT
            )
        )


        pygame.display.set_caption(
            TITLE
        )


        self.clock = pygame.time.Clock()


       # =========================
# SOUNDS
# =========================

        self.win_sound = None

        self.win_played = False

        


        # =========================
        # SYSTEMS
        # =========================


        self.level_manager = LevelManager()


        self.score_manager = ScoreManager()






        # =========================
        # FONTS
        # =========================


        self.font = pygame.font.SysFont(
            "arial",
            42,
            bold=True
        )


        self.big_font = pygame.font.SysFont(
            "arial",
            60,
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







        # =========================
        # MENU
        # =========================


        self.menu = Menu(self)







        # =========================
        # STATE
        # =========================


        self.state = "MENU"


        self.running = True







        # =========================
        # GAME VALUES
        # =========================


        self.moves = 0


        self.elapsed_seconds = 0


        self.final_score = 0


        self.score_saved = False



        # LEVEL TIME


        self.time_limit = 300


        self.time_over = False



        self.timer_started = False


        self.start_ticks = 0







        # =========================
        # BACKGROUND
        # =========================


        self.bg_offset = 0







        # =========================
        # STAR SYSTEM
        # =========================


        self.star_start = 0


        self.star_delay = 450







        # =========================
        # BUTTONS
        # =========================


        self.restart_button = None


        self.next_button = None


        self.menu_button = None










    # =================================
    # CREATE GAME
    # =================================


    def create_game(self):


        self.board = Board(

            level_manager=self.level_manager

        )



        self.board.shuffle()





        # reset values


        self.moves = 0


        self.elapsed_seconds = 0



        self.time_limit = (

            self.level_manager.get_time_limit()

        )



        self.time_over = False



        self.final_score = 0


        self.score_saved = False

        self.win_played = False

        self.timer_started = False


        self.start_ticks = 0





        self.player = Player(

            self.board,

            self

        )







        # =========================
        # BUTTON POSITIONS
        # =========================


        self.restart_button = pygame.Rect(

            WIDTH//2 - 110,

            HEIGHT//2 + 90,

            220,

            50

        )





        self.next_button = pygame.Rect(

            WIDTH//2 - 110,

            HEIGHT//2 + 150,

            220,

            50

        )





        self.menu_button = pygame.Rect(

            WIDTH//2 - 110,

            HEIGHT//2 + 210,

            220,

            50

        )






        self.star_start = pygame.time.get_ticks()










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





        if current == "HARD":


            self.state = "FINISHED"


            return






        self.level_manager.next_level()


        self.create_game()


        self.state = "PLAYING"









    # =================================
    # BACK MENU
    # =================================


    def back_to_menu(self):


        self.state = "MENU"










    # =================================
    # REGISTER MOVE
    # =================================


    def register_move(self):


        self.moves += 1





        if not self.timer_started:


            self.timer_started = True


            self.start_ticks = pygame.time.get_ticks()










    # =================================
    # SAVE SCORE
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






            # =====================
            # MENU
            # =====================


            elif self.state == "MENU":


                self.menu.handle_event(event)







            # =====================
            # PLAYING
            # =====================


            elif self.state == "PLAYING":


                self.player.handle_event(event)







            # =====================
            # COMPLETED
            # =====================


            elif self.state == "COMPLETED":



                if event.type == pygame.MOUSEBUTTONDOWN:



                    if self.restart_button.collidepoint(event.pos):


                        self.restart()




                    elif self.next_button.collidepoint(event.pos):


                        self.next_level()




                    elif self.menu_button.collidepoint(event.pos):


                        self.back_to_menu()








            # =====================
            # TIME OVER
            # =====================


            elif self.state == "TIME_OVER":



                if event.type == pygame.MOUSEBUTTONDOWN:



                    if self.restart_button.collidepoint(event.pos):


                        self.restart()




                    elif self.menu_button.collidepoint(event.pos):


                        self.back_to_menu()








            # =====================
            # FINISHED
            # =====================


            elif self.state == "FINISHED":



                if event.type == pygame.MOUSEBUTTONDOWN:



                    if self.menu_button.collidepoint(event.pos):


                        self.back_to_menu()










    # =================================
    # UPDATE
    # =================================


    def update(self):


        # background animation


        self.bg_offset += 0.5



        if self.bg_offset > HEIGHT:


            self.bg_offset = 0






        if self.state != "PLAYING":


            return








        self.board.update()








        # =========================
        # TIMER
        # =========================


        if self.timer_started:



            self.elapsed_seconds = (

                pygame.time.get_ticks()

                -

                self.start_ticks

            ) // 1000





            # TIME OVER CHECK


            if self.elapsed_seconds >= self.time_limit:



                self.elapsed_seconds = self.time_limit


                self.time_over = True


                self.state = "TIME_OVER"


                return







        # =========================
        # WIN CHECK
        # =========================


        if self.board.completed:


            if self.state != "COMPLETED":


                self.state = "COMPLETED"


                self.star_start = pygame.time.get_ticks()


                self.save_score()



                # =========================
# WIN SOUND
# =========================

        if self.win_sound:

            self.win_sound.play()


        self.win_played = True








    # =================================
    # DRAW BACKGROUND
    # =================================


    def draw_background(self):


        self.screen.fill(

            BACKGROUND

        )







        circles = [


            (120,120,90),


            (780,150,120),


            (200,600,140),


            (700,550,160)


        ]





        for x,y,r in circles:



            pygame.draw.circle(



                self.screen,


                (

                    30,

                    64,

                    175

                ),



                (

                    x,

                    (y + self.bg_offset) % HEIGHT

                ),



                r,

                width=3


            )








        overlay = pygame.Surface(


            (

                WIDTH,

                HEIGHT

            ),


            pygame.SRCALPHA


        )




        overlay.fill(


            (

                2,

                6,

                23,

                80

            )


        )




        self.screen.blit(


            overlay,


            (

                0,

                0

            )


        )












    # =================================
    # TITLE
    # =================================


    def draw_title(self):


        title = self.font.render(


            "SLIDING PUZZLE",


            True,


            WHITE


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


        panel = pygame.Rect(


            WIDTH//2 - 140,


            60,


            280,


            70


        )





        pygame.draw.rect(


            self.screen,


            (

                15,

                23,

                42

            ),


            panel,


            border_radius=18


        )




        pygame.draw.rect(


            self.screen,


            (

                56,

                189,

                248

            ),


            panel,


            width=2,


            border_radius=18


        )





        level_text = self.small_font.render(


            f"LEVEL: {self.level_manager.current_level}",


            True,


            (

                56,

                189,

                248

            )


        )





        size_text = self.small_font.render(


            f"{self.level_manager.get_size()} x {self.level_manager.get_size()}",


            True,


            WHITE


        )





        self.screen.blit(


            level_text,


            level_text.get_rect(


                center=(


                    WIDTH//2,


                    82


                )


            )


        )





        self.screen.blit(


            size_text,


            size_text.get_rect(


                center=(


                    WIDTH//2,


                    108


                )


            )


        )












    # =================================
    # TIME + MOVES DISPLAY
    # =================================


    def draw_info(self):


        remaining = (


            self.time_limit


            -

            self.elapsed_seconds


        )



        if remaining < 0:


            remaining = 0






        minutes = remaining // 60


        seconds = remaining % 60







        if remaining <= 30:


            time_color = (

                239,

                68,

                68

            )


        else:


            time_color = WHITE







        time_panel = pygame.Rect(


            25,


            120,


            220,


            60


        )





        moves_panel = pygame.Rect(


            WIDTH-245,


            120,


            220,


            60


        )






        for panel in [


            time_panel,


            moves_panel


        ]:




            pygame.draw.rect(


                self.screen,


                (

                    15,

                    23,

                    42

                ),


                panel,


                border_radius=18


            )





            pygame.draw.rect(


                self.screen,


                (

                    56,

                    189,

                    248

                ),


                panel,


                width=2,


                border_radius=18


            )








        time_text = self.timer_font.render(


            f"TIME {minutes:02}:{seconds:02}",


            True,


            time_color


        )






        moves_text = self.timer_font.render(


            f"MOVES {self.moves}",


            True,


            WHITE


        )







        self.screen.blit(


            time_text,


            time_text.get_rect(


                center=time_panel.center


            )


        )






        self.screen.blit(


            moves_text,


            moves_text.get_rect(


                center=moves_panel.center


            )


        )
            # =================================
    # BUTTON
    # =================================


    def draw_button(

        self,

        rect,

        text

    ):


        mouse = pygame.mouse.get_pos()


        color = BUTTON_COLOR




        if rect.collidepoint(mouse):


            color = BUTTON_HOVER







        # shadow


        shadow = rect.copy()


        shadow.y += 6





        pygame.draw.rect(

            self.screen,

            (

                0,

                0,

                0

            ),

            shadow,

            border_radius=18

        )







        # body


        pygame.draw.rect(

            self.screen,

            color,

            rect,

            border_radius=18

        )







        # border


        pygame.draw.rect(

            self.screen,

            WHITE,

            rect,

            width=2,

            border_radius=18

        )







        label = self.small_font.render(

            text,

            True,

            BUTTON_TEXT

        )





        self.screen.blit(

            label,

            label.get_rect(

                center=rect.center

            )

        )









    # =================================
    # CALCULATE STARS
    # =================================


    def calculate_stars(self):


        if self.final_score >= 8000:


            return 3




        elif self.final_score >= 5000:


            return 2




        return 1











    # =================================
    # DRAW STARS
    # =================================


    def draw_stars(self):


        total = self.calculate_stars()



        elapsed = (

            pygame.time.get_ticks()

            -

            self.star_start

        )




        visible = min(

            total,

            elapsed // self.star_delay + 1

        )





        positions = [


            WIDTH//2 - 70,


            WIDTH//2,


            WIDTH//2 + 70


        ]





        for i in range(visible):


            star_font = pygame.font.SysFont(

                "arial",

                70,

                bold=True

            )





            star = star_font.render(

                "★",

                True,

                STAR_COLOR

            )





            self.screen.blit(

                star,

                star.get_rect(

                    center=(

                        positions[i],

                        HEIGHT//2 - 120

                    )

                )

            )












    # =================================
    # WIN SCREEN
    # =================================


    def draw_win_screen(self):


        overlay = pygame.Surface(

            (

                WIDTH,

                HEIGHT

            ),

            pygame.SRCALPHA

        )




        overlay.fill(

            (

                0,

                0,

                0,

                170

            )

        )




        self.screen.blit(

            overlay,

            (

                0,

                0

            )

        )








        title = self.big_font.render(

            "🏆 LEVEL COMPLETE!",

            True,

            WIN_GOLD

        )





        score = self.small_font.render(

            f"SCORE : {self.final_score}",

            True,

            WHITE

        )






        moves = self.small_font.render(

            f"MOVES : {self.moves}",

            True,

            WHITE

        )







        self.screen.blit(

            title,

            title.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2 - 190

                )

            )

        )







        self.draw_stars()







        self.screen.blit(

            score,

            score.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2 - 30

                )

            )

        )






        self.screen.blit(

            moves,

            moves.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2 + 20

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

                "NEXT LEVEL"

            )



        else:



            self.draw_button(

                self.next_button,

                "FINISH"

            )







        self.draw_button(

            self.menu_button,

            "MENU"

        )












    # =================================
    # TIME OVER SCREEN
    # =================================


    def draw_time_over(self):


        overlay = pygame.Surface(

            (

                WIDTH,

                HEIGHT

            ),

            pygame.SRCALPHA

        )




        overlay.fill(

            (

                0,

                0,

                0,

                190

            )

        )




        self.screen.blit(

            overlay,

            (

                0,

                0

            )

        )







        title = self.big_font.render(

            "⏰ TIME OVER",

            True,

            (

                239,

                68,

                68

            )

        )







        text = self.small_font.render(

            "TIME FINISHED",

            True,

            WHITE

        )







        self.screen.blit(

            title,

            title.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2 - 80

                )

            )

        )







        self.screen.blit(

            text,

            text.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2 - 20

                )

            )

        )







        self.draw_button(

            self.restart_button,

            "RESTART"

        )





        self.draw_button(

            self.menu_button,

            "MENU"

        )












    # =================================
    # FINISH SCREEN
    # =================================


    def draw_finish_screen(self):


        self.draw_background()






        title = self.big_font.render(

            "🎉 CONGRATULATIONS!",

            True,

            WIN_GOLD

        )






        text = self.small_font.render(

            "YOU COMPLETED ALL LEVELS",

            True,

            WHITE

        )







        self.screen.blit(

            title,

            title.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2 - 80

                )

            )

        )






        self.screen.blit(

            text,

            text.get_rect(

                center=(

                    WIDTH//2,

                    HEIGHT//2

                )

            )

        )







        self.draw_button(

            self.menu_button,

            "BACK TO MENU"

        )












    # =================================
    # DRAW LOOP
    # =================================


    def draw(self):



        # MENU


        if self.state == "MENU":



            self.menu.draw(

                self.screen

            )



            pygame.display.flip()



            return








        # FINISHED


        if self.state == "FINISHED":



            self.draw_finish_screen()



            pygame.display.flip()



            return









        # TIME OVER


        if self.state == "TIME_OVER":



            self.draw_time_over()



            pygame.display.flip()



            return










        # GAME


        self.draw_background()



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
    # RUN LOOP
    # =================================


    def run(self):


        while self.running:



            self.handle_events()



            self.update()



            self.draw()



            self.clock.tick(FPS)