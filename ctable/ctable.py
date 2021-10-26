import curses
import curses.ascii
from .color import Color
from .utils import (
    get_longest_list_in_dict,
    list_of_dicts_to_dict_of_lists,
    dict_from_list_of_dicts,
    length_of_strings_or_ints,
)
from os import environ

environ.setdefault("ESCDELAY", "12")  # otherwise it takes an age!


class Table:
    def __init__(self, stdscr, list_of_dicts, column_order, footer=""):
        self.stdscr = stdscr
        self.maxy, self.maxx = self.stdscr.getmaxyx()
        self.currow = 0

        # pad data
        self.pminrow = 0
        self.pmincol = 0
        self.sminrow = 1
        self.smaxrow = self.maxy - 2
        self.smaxcol = self.maxx - 1

        self.list_of_dicts = list_of_dicts
        self.column_order = column_order
        self.columns = list_of_dicts_to_dict_of_lists(
            self.list_of_dicts, self.column_order
        )
        self.pmaxrow = get_longest_list_in_dict(self.columns)
        self.currow_data = {}
        self.color = Color()
        self.keys = {
            "j, n, DOWN  ": "Move down a row.",
            "k, p, UP    ": "Move up a row.",
            "f, d, PGDN  ": "Move down a page.",
            "b, u, PGUP  ": "Move up a page.",
            "g, <, HOME  ": "Go to first row.",
            "G, >, END   ": "Go to last row.",
            "v, i, ENTER ": "View row data.",
            "q, x, ESCAPE": "Exit.",
        }
        curses.curs_set(False)  # no cursor

    def resize(self):
        self.maxy, self.maxx = self.stdscr.getmaxyx()
        self.smaxrow = self.maxy - 2
        self.smaxcol = self.maxx - 1
        self.stdscr.erase()

    def get_column_widths(self):
        column_widths = []

        for title, items in self.columns.items():
            title_length = len(title)
            longest_item = len(str(max(items, key=length_of_strings_or_ints)))
            width = max(title_length, longest_item) + 1
            column_widths.append(width)

        total_width = sum(column_widths)

        while total_width > self.maxx:
            column_widths[column_widths.index(max(column_widths))] -= 1
            total_width -= 1

        return column_widths

    def make_footer(self):
        footer = curses.newwin(1, self.smincol, self.maxy - 1, 0)
        footer.bkgd(" ", self.color.white_blue)
        footerstr = (
            f"[{self.currow + 1}/{self.pmaxrow}]" + "(Press ? or F1 for help)"
        )
        footer.addstr(0, 0, footerstr)
        footer.noutrefresh()

    def is_pad_top(self):
        return self.currow <= 0

    def is_pad_bottom(self):
        return self.currow > self.pmaxrow

    def is_scr_top(self):
        return self.currow <= self.pminrow

    def is_scr_bottom(self):
        return self.currow > self.smaxrow - 2

    def up_pad(self):
        if self.pminrow > 0:
            self.pminrow -= 1

    def down_pad(self):
        if self.pminrow < self.pmaxrow - self.smaxrow:
            self.pminrow += 1

    def pgdn_pad(self):
        self.pminrow += self.smaxrow
        if self.pminrow >= self.pmaxrow - self.smaxrow:
            self.pminrow = self.pmaxrow - self.smaxrow

    def pgup_pad(self):
        self.pminrow -= self.maxy - 1
        if self.pminrow < 0:
            self.pminrow = 0

    def top_pad(self):
        self.pminrow = 0

    def bottom_pad(self):
        self.pminrow = self.pmaxrow - self.smaxrow

    def first_item(self):
        self.pminrow, self.currow = (0,) * 2

    def last_item(self):
        self.pminrow = self.pmaxrow - self.smaxrow
        self.currow = self.pmaxrow - 1

    def down_row(self):
        if self.currow >= self.pmaxrow - 1:
            self.first_item()
            return

        if self.is_pad_bottom():
            self.top_pad()

        if self.is_scr_bottom():
            self.pminrow = self.currow - self.smaxrow + 2

        self.currow += 1

    def up_row(self):
        if self.currow < 1:
            self.last_item()
            return

        if self.is_pad_top():
            self.bottom_pad()

        if self.is_scr_top():
            self.pminrow -= 1

        self.currow -= 1

    def pgdn_row(self):
        if self.pminrow >= self.pmaxrow - self.smaxrow:
            self.top_pad()
        else:
            self.pminrow += self.smaxrow

        self.currow += self.smaxrow

        if self.currow >= self.pmaxrow - 1:
            self.first_item()

    def pgup_row(self):
        if self.pminrow <= 0:
            self.bottom_pad()
        else:
            self.pminrow -= self.smaxrow

        self.currow -= self.smaxrow

        if self.currow < 0:
            self.last_item()

    def recenter(self):
        smiddle = int(self.smaxrow / 2)
        pmiddle = self.pminrow + smiddle
        if self.currow > self.pmaxrow - smiddle:
            self.bottom_pad()
        elif self.currow < smiddle:
            self.top_pad()
        elif self.currow > pmiddle:
            self.pminrow += self.currow - pmiddle
        elif self.currow < pmiddle:
            self.pminrow -= pmiddle - self.currow

    def make_columns(self, title, items, width):
        items_win = curses.newpad(self.pmaxrow, width)

        itemnum = 0

        for item in items:
            cellstr = str(item).encode("ascii", "ignore").decode()

            if len(cellstr) >= width:
                cellstr = f"{cellstr[:width - 2]}.."

            try:
                items_win.addstr(itemnum, 0, cellstr)
            except (curses.error):
                pass

            if itemnum == self.currow:
                items_win.chgat(itemnum, 0, self.color.white_magenta_bold)
                self.currow_data[title] = item

            items_win.noutrefresh(
                    self.pminrow,
                    self.pmincol,
                    self.sminrow,
                    self.smincol,
                    self.smaxrow,
                    self.smaxcol,
            )

            itemnum += 1

    def make_table(self):
        self.smincol = 0
        column_widths = self.get_column_widths()
        for index, (title, items) in enumerate(self.columns.items()):
            width = column_widths[index]
            titlestr = str(title).encode("ascii", "ignore").decode()

            if len(titlestr) >= width:
                titlestr = f"{title[:width - 2]}.."

            title_win = curses.newwin(1, width, 0, self.smincol)
            title_win.bkgd(" ", self.color.white_blue)
            title_win.addstr(0, 0, titlestr)
            title_win.noutrefresh()
            self.make_columns(title, items, width)
            self.smincol += width

        self.make_footer()
        curses.doupdate()

    def view_dict(self, d):
        win = curses.newwin(self.maxy, self.maxx, 0, 0)
        for index, (key, value) in enumerate(d.items()):
            win.addstr(index, 0, f"{key.capitalize()}: {value}")
            win.chgat(index, 0, len(key) + 1, self.color.yellow_black)
            win.noutrefresh()
            curses.doupdate()

    def init_dict_view(self, d):
        while True:
            self.stdscr.noutrefresh()
            self.view_dict(d)
            key = self.stdscr.getch()
            if key == ord("q") or key == curses.ascii.ESC:
                self.stdscr.erase()
                break
            elif key == curses.KEY_RESIZE:
                self.resize()

    def init(self):
        while True:
            self.stdscr.refresh()
            self.make_table()
            key = self.stdscr.getch()
            if key == ord("q") or key == curses.ascii.ESC:
                break
            elif key == curses.KEY_RESIZE:
                self.resize()
            elif key == ord("j") or key == ord("n") or key == curses.KEY_DOWN:
                self.down_row()
            elif key == ord("k") or key == ord("p") or key == curses.KEY_UP:
                self.up_row()
            elif key == ord("f") or key == ord("d") or key == curses.KEY_NPAGE:
                self.pgdn_row()
            elif key == ord("b") or key == ord("u") or key == curses.KEY_PPAGE:
                self.pgup_row()
            elif key == ord("g") or key == ord("<") or key == curses.KEY_HOME:
                self.first_item()
            elif key == ord("G") or key == ord(">") or key == curses.KEY_END:
                self.last_item()
            elif key == ord("z") or key == curses.ascii.ctrl(ord("l")):
                self.recenter()
            elif key == ord("\n"):
                og_dict = dict_from_list_of_dicts(self.list_of_dicts, self.currow_data)
                self.init_dict_view(og_dict)
            elif key == ord("?"):
                self.init_dict_view(self.keys)
