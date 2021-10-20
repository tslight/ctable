import curses


class Color:
    def __init__(self):
        """
        Initialise curses color pairs. Iterate over primary 8 bit colors adding
        colors in the form foreground_background 3 times once with all 8 colors
        in the foreground and the default terminal background as the background
        once with white as the foreground and each color as background and once
        with black as the foreground and each color as the background.
        """
        curses.use_default_colors()  # https://stackoverflow.com/a/44015131
        for i in range(1, 8):
            curses.init_pair(i, i, -1)
            curses.init_pair(i + 7, curses.COLOR_WHITE, i)
            curses.init_pair(i + 14, curses.COLOR_BLACK, i)

        self.red_black = curses.color_pair(1)
        self.green_black = curses.color_pair(2)
        self.yellow_black = curses.color_pair(3)
        self.blue_black = curses.color_pair(4)
        self.magenta_black = curses.color_pair(5)
        self.cyan_black = curses.color_pair(6)
        self.white_black = curses.color_pair(7)
        self.white_red = curses.color_pair(8)
        self.white_green = curses.color_pair(9)
        self.white_yellow = curses.color_pair(10)
        self.white_blue = curses.color_pair(11)
        self.white_magenta = curses.color_pair(12)
        self.white_cyan = curses.color_pair(13)
        self.white_white = curses.color_pair(14)
        self.black_red = curses.color_pair(15)
        self.black_green = curses.color_pair(16)
        self.black_yellow = curses.color_pair(17)
        self.black_blue = curses.color_pair(18)
        self.black_magenta = curses.color_pair(19)
        self.black_cyan = curses.color_pair(20)
        self.black_white = curses.color_pair(21)

        self.red_black_bold = curses.color_pair(1) | curses.A_BOLD
        self.green_black_bold = curses.color_pair(2) | curses.A_BOLD
        self.yellow_black_bold = curses.color_pair(3) | curses.A_BOLD
        self.blue_black_bold = curses.color_pair(4) | curses.A_BOLD
        self.magenta_black_bold = curses.color_pair(5) | curses.A_BOLD
        self.cyan_black_bold = curses.color_pair(6) | curses.A_BOLD
        self.white_black_bold = curses.color_pair(7) | curses.A_BOLD
        self.white_red_bold = curses.color_pair(8) | curses.A_BOLD
        self.white_green_bold = curses.color_pair(9) | curses.A_BOLD
        self.white_yellow_bold = curses.color_pair(10) | curses.A_BOLD
        self.white_blue_bold = curses.color_pair(11) | curses.A_BOLD
        self.white_magenta_bold = curses.color_pair(12) | curses.A_BOLD
        self.white_cyan_bold = curses.color_pair(13) | curses.A_BOLD
        self.white_white_bold = curses.color_pair(14) | curses.A_BOLD
        self.black_red_bold = curses.color_pair(15) | curses.A_BOLD
        self.black_green_bold = curses.color_pair(16) | curses.A_BOLD
        self.black_yellow_bold = curses.color_pair(17) | curses.A_BOLD
        self.black_blue_bold = curses.color_pair(18) | curses.A_BOLD
        self.black_magenta_bold = curses.color_pair(19) | curses.A_BOLD
        self.black_cyan_bold = curses.color_pair(20) | curses.A_BOLD
        self.black_white_bold = curses.color_pair(21) | curses.A_BOLD
