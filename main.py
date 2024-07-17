import curses
from enum import Enum

class Line(Enum):
    Empty = 0
    Light = 1
    #Heavy = 2


class Pixel:
    icons = {
        (0,0,0,0) : " ",
        (1,0,0,0) : "╵",
        (0,1,0,0) : "╴",
        (0,0,1,0) : "╶",
        (0,0,0,1) : "╷",
        (1,1,0,0) : "┘",
        (1,0,1,0) : "└",
        (1,0,0,1) : "│",
        (0,1,1,0) : "─",
        (0,1,0,1) : "┐",
        (0,0,1,1) : "┌",
        (1,1,1,0) : "┴",
        (1,1,0,1) : "┤",
        (1,0,1,1) : "├",
        (0,1,1,1) : "┬",
        (1,1,1,1) : "┼"
    }

    def __init__(self,
                 top = Line.Empty,
                 left = Line.Empty,
                 right = Line.Empty,
                 bottom = Line.Empty):   
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom

    def icon(self):
        icon = self.icons[(self.top.value, self.left.value, self.right.value, self.bottom.value)]
        return icon

    def draw(self, top = False, left = False, right = False, bottom = False):
        if top:
            self.top = Line.Light
        if left:
            self.left = Line.Light
        if right:
            self.right = Line.Light
        if bottom:
            self.bottom = Line.Light


def main(stdscr: curses.window):
    curses.curs_set(0)
    curses.mousemask(curses.REPORT_MOUSE_POSITION | curses.ALL_MOUSE_EVENTS)
    print("\033[?1002h")
    count = 0
    picture = {}
    draw = False
    previous = (0,0)
    while True:
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, buttonstate = curses.getmouse()
            stdscr.addstr(0, 0, "buttonstate: {}            ".format(buttonstate))
            stdscr.addstr(1, 0, "x: {} y: {}            ".format(x, y))
            if buttonstate == 268435456:
                if draw:
                    if previous not in picture:
                        picture[previous] = Pixel()
                    if (y,x) not in picture:
                        picture[(y,x)] = Pixel()
                    if previous[0] < y:
                        picture[previous].draw(bottom=True)
                        picture[(y,x)].draw(top=True)
                    elif previous[0] > y:
                        picture[previous].draw(top=True)
                        picture[(y,x)].draw(bottom=True)
                    if previous[1] < x:
                        picture[previous].draw(right=True)
                        picture[(y,x)].draw(left=True)
                    elif previous[1] > x:
                        picture[previous].draw(left=True)
                        picture[(y,x)].draw(right=True)
                    stdscr.addch(previous[0], previous[1], picture[previous].icon())
                    stdscr.addch(y,x, picture[(y,x)].icon())
                previous = (y,x)
                draw = True
                count += 1
            else:
                draw = False
            if buttonstate == 4096:
                if (y,x) in picture:
                    del picture[(y,x)]
                stdscr.addch(y,x," ")
            stdscr.addstr(3, 0, "count: {}     ".format(count))
            char = hex(stdscr.inch(y,x))
            stdscr.addstr(5, 0, "character: {}     ".format(char))
            stdscr.addstr(7, 0, "─━│┃┌┍┎┏┐┑┒┓")

curses.wrapper(main)
