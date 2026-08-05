class LevelManager:


    def __init__(self):


        self.levels = {


            "EASY": {


                "size": 3,

                "time": 300

            },



            "MEDIUM": {


                "size": 4,

                "time": 480

            },



            "HARD": {


                "size": 5,

                "time": 600

            }


        }




        self.current_level = "EASY"







    # =================================
    # GET BOARD SIZE
    # =================================


    def get_size(self):


        return self.levels[

            self.current_level

        ]["size"]







    # =================================
    # GET TIME LIMIT
    # =================================


    def get_time_limit(self):


        return self.levels[

            self.current_level

        ]["time"]







    # =================================
    # SET LEVEL
    # =================================


    def set_level(self, level):


        if level in self.levels:


            self.current_level = level







    # =================================
    # NEXT LEVEL
    # =================================


    def next_level(self):


        names = list(

            self.levels.keys()

        )



        index = names.index(

            self.current_level

        )





        if index < len(names) - 1:


            self.current_level = names[

                index + 1

            ]






        return self.current_level