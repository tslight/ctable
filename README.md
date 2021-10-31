# CURSES TABLES

``` text
usage: ctable [-h] [--columns COLUMNS [COLUMNS ...]] data

Display a typical API json object (a list of dictionaries) in a curses table.

positional arguments:
  data                  json data.

optional arguments:
  -h, --help            show this help message and exit
  --columns COLUMNS [COLUMNS ...], -c COLUMNS [COLUMNS ...]
                        Specify which fields you want to translate into columns.
```

## Keybindings

``` text
j, n, down  : Move down a row.
k, p, up    : Move up a row.
f, d, pgdn  : Move down a page.
b, u, pgup  : Move up a page.
g, <, home  : Go to first row.
G, >, end   : Go to last row.
v, i, enter : View row data.
q, x, escape: Exit.
```
