class LevelManager:


    def __init__(self):


        self.levels = {

            "EASY": 3,

            "MEDIUM": 4,

            "HARD": 5

        }


        self.current_level = "EASY"





    def get_size(self):


        return self.levels[
            self.current_level
        ]






    def set_level(self, level):


        if level in self.levels:


            self.current_level = level





    def next_level(self):


        names = list(
            self.levels.keys()
        )


        index = names.index(
            self.current_level
        )


        if index < len(names)-1:


            self.current_level = names[index+1]



        return self.current_level