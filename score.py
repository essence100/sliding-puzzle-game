import json
import os


SAVE_FILE = "save.json"





class ScoreManager:


    def __init__(self):


        self.best_time = None

        self.best_moves = None

        self.best_score = 0


        self.load()







    def load(self):


        if os.path.exists(SAVE_FILE):


            try:

                with open(
                    SAVE_FILE,
                    "r"
                ) as file:


                    data = json.load(file)



                    self.best_time = data.get(
                        "best_time",
                        None
                    )


                    self.best_moves = data.get(
                        "best_moves",
                        None
                    )


                    self.best_score = data.get(
                        "best_score",
                        0
                    )



            except:

                self.reset()



        else:

            self.reset()







    def save(self):


        data = {


            "best_time": self.best_time,


            "best_moves": self.best_moves,


            "best_score": self.best_score


        }



        with open(
            SAVE_FILE,
            "w"
        ) as file:


            json.dump(

                data,

                file,

                indent=4

            )









    def calculate_score(
        self,
        time,
        moves
    ):


        score = (

            10000

            -

            (time * 10)

            -

            (moves * 5)

        )



        if score < 0:

            score = 0



        return score







    def update_best(
        self,
        time,
        moves
    ):


        score = self.calculate_score(

            time,

            moves

        )



        updated = False





        # Best score

        if score > self.best_score:


            self.best_score = score

            updated = True






        # Best time

        if (

            self.best_time is None

            or

            time < self.best_time

        ):


            self.best_time = time

            updated = True







        # Best moves

        if (

            self.best_moves is None

            or

            moves < self.best_moves

        ):


            self.best_moves = moves

            updated = True







        if updated:


            self.save()



        return score







    def reset(self):


        self.best_time = None

        self.best_moves = None

        self.best_score = 0