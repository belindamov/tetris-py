class Colours:
    pink_white = (245, 225, 252)
    muted_pink = (156, 67, 133)
    purple_pink = (110, 66, 98)
    baby_pink = (209, 128, 168)
    salmon = (255, 94, 135)
    purple = (215, 125, 219)
    purple2 = (158, 12, 207)
    grey_purple = (109, 91, 115)

    @classmethod
    def get_cell_colours(cls):
        return [cls.pink_white, cls.muted_pink, cls.purple_pink, cls.baby_pink, cls.salmon, cls.purple, cls.purple2,
                cls.grey_purple]
