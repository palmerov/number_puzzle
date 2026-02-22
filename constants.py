
class Constants:
    def __init__(
        self,
        weight_g: float,
        weight_h1: float,
        weight_h2: float,
        weight_h3: float,
        weight_h4: float,
        weight_h5: float,
        max_g: int,
        max_h1: int,
        max_h2: int,
        max_h3: int,
        max_h4: int,
        max_h5: int,
        save_statistics: bool = False,
    ):
        self.WEIGHT_G = weight_g
        self.WEIGHT_H1 = weight_h1
        self.WEIGHT_H2 = weight_h2
        self.WEIGHT_H3 = weight_h3
        self.WEIGHT_H4 = weight_h4
        self.WEIGHT_H5 = weight_h5

        self.MAX_G = max_g
        self.MAX_H1 = max_h1
        self.MAX_H2 = max_h2
        self.MAX_H3 = max_h3
        self.MAX_H4 = max_h4
        self.MAX_H5 = max_h5
        
        # statistics
        self.SAVE_STATISTICS = save_statistics
        self.LAST_MAX_G = 0.0
        self.LAST_MAX_H1 = 0.0
        self.LAST_MAX_H2 = 0.0
        self.LAST_MAX_H3 = 0.0
        self.LAST_MAX_H4 = 0.0
        self.LAST_MAX_H5 = 0.0
        
    def reset_statistics(self):
        self.LAST_MAX_G = 0.0
        self.LAST_MAX_H1 = 0.0
        self.LAST_MAX_H2 = 0.0
        self.LAST_MAX_H3 = 0.0
        self.LAST_MAX_H4 = 0.0
        self.LAST_MAX_H5 = 0.0
    
    def get_statistics(self) -> dict:
        return {
            "LAST_MAX_G": self.LAST_MAX_G,
            "LAST_MAX_H1": self.LAST_MAX_H1,
            "LAST_MAX_H2": self.LAST_MAX_H2,
            "LAST_MAX_H3": self.LAST_MAX_H3,
            "LAST_MAX_H4": self.LAST_MAX_H4,
            "LAST_MAX_H5": self.LAST_MAX_H5
        }
    
    def print_statistics(self):
        print(f"LAST_MAX_G: {self.LAST_MAX_G}, LAST_MAX_H1: {self.LAST_MAX_H1}, LAST_MAX_H2: {self.LAST_MAX_H2}, LAST_MAX_H3: {self.LAST_MAX_H3}, LAST_MAX_H4: {self.LAST_MAX_H4}, LAST_MAX_H5: {self.LAST_MAX_H5}")

# max_g is the maximum value of g
def max_g(dimension: int) -> float:
    if dimension == 3:
        return 60
    if dimension == 4:
        return 100
    if dimension == 5:
        return 170
    if dimension == 6:
        return 230
    if dimension == 7:
        return 270
    if dimension == 8:
        return 310
    if dimension == 9:
        return 350
    if dimension == 10:
        return 400


# max_h1 is the maximum value of h1
def max_h1(dimension: int) -> float:
    if dimension == 3:
        return 1.5
    if dimension == 4:
        return 2.5
    if dimension == 5:
        return 3
    if dimension == 6:
        return 4
    if dimension == 7:
        return 5
    if dimension == 8:
        return 6
    if dimension == 9:
        return 7
    if dimension == 10:
        return 8


# max_h2 is the maximum value of h2
def max_h2(dimension: int) -> float:
    if dimension == 3:
        return 9
    if dimension == 4:
        return 16
    if dimension == 5:
        return 25
    if dimension == 6:
        return 35   
    if dimension == 7:
        return 40
    if dimension == 8:
        return 45
    if dimension == 9:
        return 50
    if dimension == 10:
        return 55


# max_h3 is the maximum value of h3
def max_h3(dimension: int) -> float:
    if dimension == 3:
        return 2
    if dimension == 4:
        return 5
    if dimension == 5:
        return 7
    if dimension == 6:
        return 10
    if dimension == 7:
        return 11
    if dimension == 8:
        return 12
    if dimension == 9:
        return 14
    if dimension == 10:
        return 16


# max_h4 is the maximum value of h4
def max_h4(dimension: int) -> float:
    if dimension == 3:
        return 2
    if dimension == 4:
        return 4
    if dimension == 5:
        return 5
    if dimension == 6:
        return 6
    if dimension == 7:
        return 7
    if dimension == 8:
        return 8
    if dimension == 9:
        return 9
    if dimension == 10:
        return 10


# pon_h4 is the penalty value of h4
def max_h5(dimension: int) -> float:
    if dimension == 3:
        return 2
    if dimension == 4:
        return 3
    if dimension == 5:
        return 4
    if dimension == 6:
        return 5
    if dimension == 7:
        return 5
    if dimension == 8:
        return 6
    if dimension == 9:
        return 6
    if dimension == 10:
        return 7
