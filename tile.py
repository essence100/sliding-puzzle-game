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


        self.font = pygame.font.SysFont(
            "arial",
            42,
            bold=True
        )


        self.shadow_font = pygame.font.SysFont(
            "arial",
            42,
            bold=True
        )


        self.tile_color = self.get_color()


    # ======================
    # COLORS
    # ======================

    def get_color(self):

        colors = [

            (56,189,248),
            (34,211,238),
            (99,102,241),
            (168,85,247),
            (236,72,153),
            (14,165,233),
            (16,185,129),
            (245,158,11)

        ]

        return colors[self.number % len(colors)]




    # ======================
    # MOVE
    # ======================

    def move_to(self,x,y):

        self.target_x = x
        self.target_y = y

        self.moving = True




    # ======================
    # UPDATE
    # ======================

    def update(self):

        if not self.moving:
            return


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





    # ======================
    # DRAW
    # ======================

    def draw(self,screen):


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



        mouse = pygame.mouse.get_pos()


        hover = rect.collidepoint(mouse)



        # ======================
        # 3D SHADOW
        # ======================

        shadow = pygame.Rect(

            rect.x + 8,
            rect.y + 10,
            rect.width,
            rect.height

        )


        pygame.draw.rect(

            screen,

            (2,6,23),

            shadow,

            border_radius=20

        )




        # ======================
        # TILE BODY
        # ======================


        color = self.tile_color


        if hover:

            color = tuple(
                min(c+35,255)
                for c in color
            )



        pygame.draw.rect(

            screen,

            color,

            rect,

            border_radius=20

        )





        # ======================
        # GLASS HIGHLIGHT
        # ======================


        highlight = pygame.Rect(

            rect.x + 8,
            rect.y + 8,
            rect.width-16,
            rect.height//3

        )


        pygame.draw.rect(

            screen,

            (
                255,
                255,
                255
            ),

            highlight,

            border_radius=15

        )





        # ======================
        # BORDER
        # ======================


        pygame.draw.rect(

            screen,

            (
                255,
                255,
                255
            ),

            rect,

            width=2,

            border_radius=20

        )





        # ======================
        # NUMBER SHADOW
        # ======================


        shadow_text = self.shadow_font.render(

            str(self.number),

            True,

            (15,23,42)

        )


        shadow_rect = shadow_text.get_rect(

            center=(

                rect.centerx+2,

                rect.centery+3

            )

        )


        screen.blit(

            shadow_text,

            shadow_rect

        )






        # ======================
        # NUMBER
        # ======================


        text = self.font.render(

            str(self.number),

            True,

            WHITE

        )


        text_rect = text.get_rect(

            center=rect.center

        )


        screen.blit(

            text,

            text_rect

        )