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
            42,
            bold=True
        )


        self.small_font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )


        self.buttons = {


            "EASY": pygame.Rect(
                WIDTH//2 - 120,
                190,
                240,
                60
            ),


            "MEDIUM": pygame.Rect(
                WIDTH//2 - 120,
                290,
                240,
                60
            ),


            "HARD": pygame.Rect(
                WIDTH//2 - 120,
                390,
                240,
                60
            )

        }



        self.hover_color = (
            125,
            211,
            252
        )


        self.normal_color = (
            56,
            189,
            248
        )



        self.text_color = (
            0,
            0,
            0
        )





    def handle_event(self,event):


        if event.type == pygame.MOUSEBUTTONDOWN:


            if event.button == 1:


                for level, button in self.buttons.items():


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

                    90

                )

            )

        )





        subtitle = self.small_font.render(

            "Choose Difficulty",

            True,

            (148,163,184)

        )


        screen.blit(

            subtitle,

            subtitle.get_rect(

                center=(

                    WIDTH//2,

                    140

                )

            )

        )






        mouse_pos = pygame.mouse.get_pos()





        for level, button in self.buttons.items():



            if button.collidepoint(mouse_pos):


                color = self.hover_color


            else:


                color = self.normal_color






            pygame.draw.rect(

                screen,

                color,

                button,

                border_radius=15

            )





            text = self.small_font.render(

                level,

                True,

                self.text_color

            )




            screen.blit(

                text,

                text.get_rect(

                    center=button.center

                )

            )