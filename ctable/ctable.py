import curses
from .color import Color
from .utils import get_longest_list_in_dict, list_of_dicts_to_dict_of_lists


class Table:
    def __init__(self, stdscr, list_of_dicts, column_order):
        self.stdscr = stdscr
        self.hl = 0
        self.list_of_dicts = list_of_dicts
        self.column_order = column_order
        self.columns = list_of_dicts_to_dict_of_lists(
            self.list_of_dicts, self.column_order
        )
        self.longest_column_length = get_longest_list_in_dict(self.columns)
        self.stdscr.refresh()
        curses.curs_set(0)

    def make_columns(self):
        color = Color()
        xstart = 0
        for title, items in self.columns.items():
            title_length = len(title)
            longest_item = len(max(items, key=len))
            width = max(title_length, longest_item) + 1
            title_win = curses.newwin(1, width, 0, xstart)
            title_win.bkgd(" ", color.white_blue)
            title_win.addstr(0, 0, title)
            title_win.refresh()
            items_win = curses.newpad(self.longest_column_length, width)

            itemnum = 0
            pminrow = 0

            if self.hl >= curses.LINES - 2:
                pminrow = self.hl - curses.LINES + 2

            for item in items:
                if itemnum == self.hl:
                    items_win.addstr(itemnum, 0, item)
                    items_win.chgat(itemnum, 0, color.white_magenta_bold)
                else:
                    items_win.addstr(itemnum, 0, item)
                items_win.noutrefresh(
                    pminrow, 0, 1, xstart, curses.LINES - 1, xstart + width
                )
                itemnum += 1

            curses.doupdate()
            xstart += width

    def init(self):
        while True:
            self.make_columns()
            key = self.stdscr.getch()
            if key == ord("q"):
                break
            elif key == ord("j"):
                if self.hl <= self.longest_column_length - 2:
                    self.hl += 1
            elif key == ord("k"):
                if self.hl > 0:
                    self.hl -= 1
            elif key == ord("\n"):
                first_key = next(iter(self.columns))
                first_value = self.columns[first_key][self.hl]
                return next(
                    (item for item in self.list_of_dicts
                     if item[first_key] == first_value),
                    None
                )
