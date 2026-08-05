import pygame

from level import LevelManager

import random

from tile import Tile

from settings import (
    DEFAULT_SIZE,
    BOARD_SIZE,
    TILE_GAP,
    WIDTH,
    HEIGHT
)



class Board:


    def __init__(self, level_manager=None):


        if level_manager:

            self.size = level_manager.get_size()

        else:

            self.size = DEFAULT_SIZE



        self.grid = []

        self.tiles = []

        self.completed = False


        self.create_board()





    # =================================
    # CREATE BOARD
    # =================================

    def create_board(self):


        number = 1


        for row in range(self.size):


            current_row = []


            for col in range(self.size):


                if number < self.size * self.size:


                    current_row.append(number)

                    number += 1


                else:


                    current_row.append(0)



            self.grid.append(current_row)



        self.create_tiles()







    # =================================
    # CREATE TILES
    # =================================

    def create_tiles(self):


        self.tiles = []



        tile_size = (

            BOARD_SIZE -

            (self.size - 1) * TILE_GAP

        ) // self.size




        start_x = (

            WIDTH - BOARD_SIZE

        ) // 2




        start_y = (

            HEIGHT - BOARD_SIZE

        ) // 2





        for row in range(self.size):


            for col in range(self.size):


                number = self.grid[row][col]



                if number != 0:



                    x = start_x + col * (

                        tile_size + TILE_GAP

                    )



                    y = start_y + row * (

                        tile_size + TILE_GAP

                    )



                    tile = Tile(

                        number,

                        x,

                        y,

                        tile_size,

                        row,

                        col

                    )



                    self.tiles.append(tile)








    # =================================
    # DRAW
    # =================================

    def draw(self, screen):



        self.draw_background(screen)



        for tile in self.tiles:


            tile.draw(screen)








    # =================================
    # BOARD PANEL UI
    # =================================

    def draw_background(self, screen):


        x = (

            WIDTH - BOARD_SIZE

        ) // 2 - 20



        y = (

            HEIGHT - BOARD_SIZE

        ) // 2 - 20



        size = BOARD_SIZE + 40





        # shadow


        shadow = pygame.Rect(

            x + 8,

            y + 10,

            size,

            size

        )


        pygame.draw.rect(

            screen,

            (15,23,42),

            shadow,

            border_radius=30

        )






        # panel


        panel = pygame.Rect(

            x,

            y,

            size,

            size

        )


        pygame.draw.rect(

            screen,

            (30,41,59),

            panel,

            border_radius=30

        )






        # glow border


        pygame.draw.rect(

            screen,

            (56,189,248),

            panel,

            width=3,

            border_radius=30

        )







        # empty cells background


        tile_size = (

            BOARD_SIZE -

            (self.size - 1) * TILE_GAP

        ) // self.size





        start_x = (

            WIDTH - BOARD_SIZE

        ) // 2




        start_y = (

            HEIGHT - BOARD_SIZE

        ) // 2





        for row in range(self.size):


            for col in range(self.size):


                if self.grid[row][col] == 0:



                    empty = pygame.Rect(

                        start_x + col * (

                            tile_size + TILE_GAP

                        ),

                        start_y + row * (

                            tile_size + TILE_GAP

                        ),

                        tile_size,

                        tile_size

                    )



                    pygame.draw.rect(

                        screen,

                        (15,23,42),

                        empty,

                        border_radius=18

                    )









    # =================================
    # UPDATE
    # =================================

    def update(self):


        for tile in self.tiles:


            tile.update()







    # =================================
    # FIND EMPTY
    # =================================

    def find_empty(self):


        for row in range(self.size):

            for col in range(self.size):


                if self.grid[row][col] == 0:


                    return row,col







    # =================================
    # GET TILE
    # =================================

    def get_tile(self,row,col):


        for tile in self.tiles:


            if tile.row == row and tile.col == col:


                return tile



        return None







    # =================================
    # MOVE
    # =================================

    def move(self,direction):


        if self.completed:


            return False



        empty_row,empty_col = self.find_empty()



        target_row = empty_row

        target_col = empty_col




        if direction == "UP":

            target_row += 1


        elif direction == "DOWN":

            target_row -= 1


        elif direction == "LEFT":

            target_col += 1


        elif direction == "RIGHT":

            target_col -= 1


        else:

            return False






        if (

            target_row < 0

            or target_row >= self.size

            or target_col < 0

            or target_col >= self.size

        ):


            return False






        tile = self.get_tile(

            target_row,

            target_col

        )



        if tile:


            tile.row = empty_row

            tile.col = empty_col



            self.move_animation(

                tile,

                empty_row,

                empty_col

            )



            self.grid[empty_row][empty_col], self.grid[target_row][target_col] = (

                self.grid[target_row][target_col],

                self.grid[empty_row][empty_col]

            )



            self.create_tile_positions()


            self.completed = self.check_win()



            return True



        return False







    # =================================
    # ANIMATION
    # =================================

    def move_animation(self,tile,row,col):


        tile_size = (

            BOARD_SIZE -

            (self.size - 1) * TILE_GAP

        ) // self.size



        start_x = (

            WIDTH - BOARD_SIZE

        ) // 2



        start_y = (

            HEIGHT - BOARD_SIZE

        ) // 2



        x = start_x + col*(tile_size+TILE_GAP)

        y = start_y + row*(tile_size+TILE_GAP)



        tile.move_to(x,y)








    # =================================
    # UPDATE POSITIONS
    # =================================

    def create_tile_positions(self):


        for row in range(self.size):

            for col in range(self.size):


                number=self.grid[row][col]



                if number != 0:


                    tile=self.get_tile_by_number(number)


                    if tile:


                        tile.row=row

                        tile.col=col







    def get_tile_by_number(self,number):


        for tile in self.tiles:


            if tile.number == number:

                return tile



        return None







    # =================================
    # CLICK
    # =================================

    def click_tile(self,mouse_pos):


        if self.completed:

            return False



        for tile in self.tiles:


            if tile.rect.collidepoint(mouse_pos):


                return self.move_tile(tile)



        return False







    def move_tile(self,tile):


        empty_row,empty_col=self.find_empty()



        distance=(

            abs(empty_row-tile.row)

            +

            abs(empty_col-tile.col)

        )



        if distance == 1:


            return self.swap_tile(tile)



        return False







    def swap_tile(self,tile):


        empty_row,empty_col=self.find_empty()



        old_row=tile.row

        old_col=tile.col




        self.grid[empty_row][empty_col],self.grid[old_row][old_col]=(

            self.grid[old_row][old_col],

            self.grid[empty_row][empty_col]

        )



        tile.row=empty_row

        tile.col=empty_col



        self.move_animation(

            tile,

            empty_row,

            empty_col

        )



        self.create_tile_positions()



        self.completed=self.check_win()



        return True







    # =================================
    # SHUFFLE
    # =================================

    def shuffle(self,moves=200):


        self.completed=False



        directions=[

            "UP",

            "DOWN",

            "LEFT",

            "RIGHT"

        ]



        for _ in range(moves):


            self.move(

                random.choice(directions)

            )



        self.completed=False







    # =================================
    # WIN CHECK
    # =================================

    def check_win(self):


        expected=1



        for row in range(self.size):


            for col in range(self.size):


                if row == self.size-1 and col == self.size-1:


                    return self.grid[row][col]==0




                if self.grid[row][col] != expected:


                    return False



                expected+=1



        return True