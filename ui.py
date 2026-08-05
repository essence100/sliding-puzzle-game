import pygame


class WinScreen:


    def __init__(self, game):

        self.game = game


        self.font = pygame.font.SysFont(
            "arial",
            42,
            bold=True
        )


        self.title_font = pygame.font.SysFont(
            "arial",
            34,
            bold=True
        )


        self.small_font = pygame.font.SysFont(
            "arial",
            24,
            bold=True
        )


        self.restart_button = pygame.Rect(
            0,
            0,
            180,
            45
        )


        self.next_button = pygame.Rect(
            0,
            0,
            180,
            45
        )


        self.menu_button = pygame.Rect(
            0,
            0,
            180,
            45
        )





    # ==========================
    # BUTTON POSITIONS
    # ==========================

    def update_positions(self):


        center = self.game.screen.get_width() // 2


        self.restart_button.center = (
            center,
            500
        )


        self.next_button.center = (
            center,
            555
        )


        self.menu_button.center = (
            center,
            610
        )






    # ==========================
    # SCORE RATING
    # ==========================

    def get_rating(self):


        score = self.game.final_score


        if score >= 9000:

            return 5, "LEGENDARY"


        elif score >= 7000:

            return 4, "EXCELLENT"


        elif score >= 5000:

            return 3, "GREAT"


        elif score >= 3000:

            return 2, "GOOD"


        else:

            return 1, "KEEP TRYING"






    # ==========================
    # BUTTON DRAW
    # ==========================

    def draw_button(
        self,
        screen,
        button,
        text
    ):


        mouse = pygame.mouse.get_pos()



        if button.collidepoint(mouse):

            color = (
                125,
                211,
                252
            )

        else:

            color = (
                56,
                189,
                248
            )



        pygame.draw.rect(

            screen,

            color,

            button,

            border_radius=15

        )



        label = self.small_font.render(

            text,

            True,

            (0,0,0)

        )



        screen.blit(

            label,

            label.get_rect(

                center=button.center

            )

        )








    # ==========================
    # STAR DISPLAY
    # ==========================

    def draw_rating(
        self,
        screen
    ):


        stars, title = self.get_rating()


        star_text = ""


        for i in range(5):


            if i < stars:

                star_text += "★"


            else:

                star_text += "☆"





        stars_surface = self.title_font.render(

            star_text,

            True,

            (255,215,0)

        )


        screen.blit(

            stars_surface,

            stars_surface.get_rect(

                center=(

                    screen.get_width()//2,

                    360

                )

            )

        )




        title_surface = self.small_font.render(

            title,

            True,

            (56,189,248)

        )


        screen.blit(

            title_surface,

            title_surface.get_rect(

                center=(

                    screen.get_width()//2,

                    405

                )

            )

        )







    # ==========================
    # MAIN WIN SCREEN
    # ==========================

    def draw(
        self,
        screen
    ):


        self.update_positions()



        # DARK OVERLAY

        overlay = pygame.Surface(

            screen.get_size(),

            pygame.SRCALPHA

        )


        overlay.fill(

            (0,0,0,180)

        )


        screen.blit(

            overlay,

            (0,0)

        )






        # CARD

        card = pygame.Rect(

            80,

            60,

            560,

            560

        )


        pygame.draw.rect(

            screen,

            (15,23,42),

            card,

            border_radius=25

        )






        title = self.font.render(

            "🏆 PUZZLE COMPLETE",

            True,

            (255,215,0)

        )


        screen.blit(

            title,

            title.get_rect(

                center=(

                    card.centerx,

                    130

                )

            )

        )






        statistics = [


            f"SCORE : {self.game.final_score}",


            f"MOVES : {self.game.moves}",


            f"TIME  : {self.game.elapsed_seconds}s",


            f"LEVEL : {self.game.level_manager.current_level}"


        ]



        y = 190


        for item in statistics:


            text = self.small_font.render(

                item,

                True,

                (255,255,255)

            )


            screen.blit(

                text,

                text.get_rect(

                    center=(

                        card.centerx,

                        y

                    )

                )

            )


            y += 40






        self.draw_rating(screen)




        self.draw_button(

            screen,

            self.restart_button,

            "RESTART"

        )



        if self.game.level_manager.current_level != "HARD":


            self.draw_button(

                screen,

                self.next_button,

                "NEXT LEVEL"

            )



        self.draw_button(

            screen,

            self.menu_button,

            "MENU"

        )