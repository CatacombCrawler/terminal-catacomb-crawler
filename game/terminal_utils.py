"""
terminal utilities - shared helpers for terminal input modes
"""

import contextlib

try:
    import termios  # not available on windows
    import tty
except Exception:  # pragma: no cover
    termios = None
    tty = None

@contextlib.contextmanager
def normal_input_mode(terminal):
    """temporarily enable cooked input with echo for blocking input().
    shows the cursor during input and restores cbreak mode afterward.
    on platforms without termios, this is effectively a no-op besides cursor visibility.
    """
    # show cursor while the user types
    try:
        print(terminal.show_cursor, end="", flush=True)
    except Exception:
        pass

    if termios is not None and hasattr(terminal, "_keyboard_fd") and terminal._keyboard_fd is not None:
        fd = terminal._keyboard_fd
        try:
            saved_attrs = termios.tcgetattr(fd)
            saved_line_buffered = getattr(terminal, "_line_buffered", True)

            attrs = termios.tcgetattr(fd)
            attrs[3] |= (termios.ICANON | termios.ECHO)
            termios.tcsetattr(fd, termios.TCSANOW, attrs)

            if hasattr(terminal, "_line_buffered"):
                terminal._line_buffered = True

            yield
        finally:
            try:
                if tty is not None:
                    tty.setcbreak(fd, termios.TCSANOW)
            except Exception:
                try:
                    termios.tcsetattr(fd, termios.TCSAFLUSH, saved_attrs)
                except Exception:
                    pass
            if hasattr(terminal, "_line_buffered"):
                terminal._line_buffered = saved_line_buffered
    else:
        yield

    # hide cursor again
    try:
        print(terminal.hide_cursor, end="", flush=True)
    except Exception:
        pass
