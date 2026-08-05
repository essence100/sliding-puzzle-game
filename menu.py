import pygame

from settings import (
    WIDTH,
    HEIGHT
)



class Menu:


    def __init__(self, game):


        self.game = game


        self.font = pygame.font.SysFont(
            "arial",
            40,
            bold=True
        )


        self.small_font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )



        self.buttons = {


            "EASY": pygame.Rect(
                WIDTH//2 - 100,
                180,
                200,
                55
            ),


            "MEDIUM": pygame.Rect(
                WIDTH//2 - 100,
                270,
                200,
                55
            ),


            "HARD": pygame.Rect(
                WIDTH//2 - 100,
                360,
                200,
                55
            )

        }



    def handle_event(self,event):


        if event.type == pygame.MOUSEBUTTONDOWN:


            for level,button in self.buttons.items():


                if button.collidepoint(event.pos):


                    self.game.start_level(level)







    def draw(self,screen):


        screen.fill(
            (2,6,23)
        )


        title = self.font.render(

            "SLIDING PUZZLE",

            True,

            (255,255,255)

        )


        screen.blit(

            title,

            title.get_rect(

                center=(

                    WIDTH//2,

                    80

                )

            )

        )





        for level,button in self.buttons.items():


            pygame.draw.rect(

                screen,

                (56,189,248),

                button,

                border_radius=12

            )


            text = self.small_font.render(

                level,

                True,

                (0,0,0)

            )


            screen.blit(

                text,

                text.get_rect(

                    center=button.center

                )

            )