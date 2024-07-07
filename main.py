import curses

def main(stdscr: curses.window):
    curses.curs_set(0)
    curses.mousemask(curses.REPORT_MOUSE_POSITION | curses.ALL_MOUSE_EVENTS)
    print("\033[?1002h")
    count = 0
    while True:
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, buttonstate = curses.getmouse()
            stdscr.addstr(0, 0, "buttonstate: {}            ".format(buttonstate))
            stdscr.addstr(1, 0, "x: {} y: {}            ".format(x, y))
            if buttonstate == 268435456:
                count += 1
            stdscr.addstr(3, 0, "count: {}     ".format(count))
            char = stdscr.inch(y,x)
            stdscr.addstr(5, 0, "character: {}     ".format(char))

curses.wrapper(main)
