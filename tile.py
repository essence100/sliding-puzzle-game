import pygame

from settings import WHITE, BLACK


class Tile:


    def __init__(
        self,
        number,
        x,
        y,
        size,
        row,
        col
    ):


        self.number = number

        self.x = x
        self.y = y


        self.target_x = x
        self.target_y = y


        self.size = size


        self.row = row
        self.col = col


        self.speed = 15


        self.moving = False


        self.rect = pygame.Rect(
            x,
            y,
            size,
            size
        )


        # UI
        self.font = pygame.font.SysFont(
            "arial",
            42,
            bold=True
        )





    def move_to(self, x, y):

        self.target_x = x

        self.target_y = y

        self.moving = True






    def update(self):

        if not self.moving:

            return



        # X movement

        if self.x < self.target_x:

            self.x = min(
                self.x + self.speed,
                self.target_x
            )


        elif self.x > self.target_x:

            self.x = max(
                self.x - self.speed,
                self.target_x
            )




        # Y movement

        if self.y < self.target_y:

            self.y = min(
                self.y + self.speed,
                self.target_y
            )


        elif self.y > self.target_y:

            self.y = max(
                self.y - self.speed,
                self.target_y
            )




        if (
            self.x == self.target_x
            and
            self.y == self.target_y
        ):

            self.moving = False







    def draw(self, screen):


        self.rect.topleft = (
            self.x,
            self.y
        )



        rect = pygame.Rect(

            int(self.x),

            int(self.y),

            self.size,

            self.size

        )



        # Shadow

        shadow_rect = pygame.Rect(

            rect.x + 5,

            rect.y + 5,

            rect.width,

            rect.height

        )


        pygame.draw.rect(

            screen,

            (20,20,20),

            shadow_rect,

            border_radius=15

        )





        # Tile body

        pygame.draw.rect(

            screen,

            WHITE,

            rect,

            border_radius=15

        )





        # Border

        pygame.draw.rect(

            screen,

            (100,100,100),

            rect,

            width=2,

            border_radius=15

        )





        # Number

        text = self.font.render(

            str(self.number),

            True,

            BLACK

        )



        text_rect = text.get_rect(

            center=rect.center

        )



        screen.blit(

            text,

            text_rect

        )