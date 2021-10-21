import ast
import curses
import json
from argparse import ArgumentParser
from .ctable import Table


def get_args():
    parser = ArgumentParser(
        description="""
    Display a typical API json object (a list of dictionaries) in a curses table.
    """
    )
    parser.add_argument("data", help="json data.")
    parser.add_argument(
        "--columns",
        "-c",
        nargs="+",
        help="Specify which fields you want to translate into columns.",
    )

    return parser.parse_args()


def init_table(stdscr, data, columns=None):
    if columns:
        columns = columns
    else:
        columns = list(set().union(*(d.keys() for d in data)))

    return Table(stdscr, data, columns).init()

def show_table(data, columns):
    return curses.wrapper(init_table, data, columns)

def main():
    args = get_args()

    if type(args.data) == list:
        data = args.data
    else:
        # data = ast.literal_eval(args.data)
        data = json.loads(args.data)

    print(show_table(data, args.columns))


if __name__ == "__main__":
    main()
