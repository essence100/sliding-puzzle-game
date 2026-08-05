import pygame


class Player:


    def __init__(self, board, game):

        self.board = board

        self.game = game



    def handle_event(self, event):


        moved = False



        # =====================
        # KEYBOARD MOVEMENT
        # =====================

        if event.type == pygame.KEYDOWN:



            if event.key == pygame.K_UP:

                moved = self.board.move(
                    "UP"
                )



            elif event.key == pygame.K_DOWN:

                moved = self.board.move(
                    "DOWN"
                )



            elif event.key == pygame.K_LEFT:

                moved = self.board.move(
                    "LEFT"
                )



            elif event.key == pygame.K_RIGHT:

                moved = self.board.move(
                    "RIGHT"
                )



        # =====================
        # MOUSE MOVEMENT
        # =====================

        elif event.type == pygame.MOUSEBUTTONDOWN:


            if event.button == 1:


                moved = self.board.click_tile(
                    event.pos
                )




        # =====================
        # REGISTER MOVE
        # =====================

        if moved:


            self.game.register_move()


            return True



        return False