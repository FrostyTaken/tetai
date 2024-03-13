class Colours:
    cyan = (0, 255, 255)
    blue = (0, 0, 255)
    orange = (255, 165 ,0)
    yellow = (255, 255, 0)
    green = (0, 128, 0)
    purple = (128, 0, 128)
    red = (255, 0, 0)
    grey = (27, 30, 39)
    white = (255, 255, 255)
    light_purple = (210, 0, 255)
        
    @classmethod
    def get_cell_colour(cls):
        return [cls.grey, cls.cyan, cls.blue, cls.orange, cls.yellow, cls.green, cls.purple, cls.red]