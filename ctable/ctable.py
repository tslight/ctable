import curses
from .color import Color
from .utils import (
    get_longest_list_in_dict,
    list_of_dicts_to_dict_of_lists,
    is_dict_subset_in_list_of_dicts,
    length_of_strings_or_ints,
)


class Table:
    def __init__(self, stdscr, list_of_dicts, column_order, footer=""):
        self.stdscr = stdscr
        self.maxy, self.maxx = self.stdscr.getmaxyx()
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
        hl_row_data = {}
        for title, items in self.columns.items():
            title_length = len(title)
            longest_item = len(str(max(items, key=length_of_strings_or_ints)))
            width = max(title_length, longest_item) + 1
            title_win = curses.newwin(1, width, 0, xstart)
            title_win.bkgd(" ", color.white_blue)
            title_win.addstr(0, 0, title)
            title_win.refresh()
            items_win = curses.newpad(self.longest_column_length, width)

            itemnum = 0
            pminrow = 0

            if self.hl >= curses.LINES - 3:
                pminrow = self.hl - curses.LINES + 3

            for item in items:

                if itemnum == self.hl:
                    items_win.addstr(itemnum, 0, str(item))
                    items_win.chgat(itemnum, 0, color.white_magenta_bold)
                    hl_row_data[title] = item
                else:
                    items_win.addstr(itemnum, 0, str(item))

                items_win.noutrefresh(
                    pminrow, 0, 1, xstart, self.maxy - 2, self.maxx - 1
                )
                itemnum += 1

            xstart += width

        footer = curses.newwin(1, xstart, self.maxy - 1, 0)
        footer.bkgd(" ", color.white_blue)
        footer.addstr(0, 0, f"[{self.hl}/{self.longest_column_length}] (Press ? or F1 for help)")
        footer.noutrefresh()
        curses.doupdate()

        return hl_row_data

    def init(self):
        while True:
            hl_row_data = self.make_columns()
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
                return is_dict_subset_in_list_of_dicts(self.list_of_dicts, hl_row_data)
