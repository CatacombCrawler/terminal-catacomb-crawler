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


def read_line_with_inkey(terminal, prompt: str = "") -> str:
    """read a line visibly using terminal.inkey() while in cbreak.
    supports backspace and enter. returns the entered string.
    """
    if prompt:
        print(prompt, end="", flush=True)
    buffer = ""
    while True:
        key = terminal.inkey()
        # handle enter
        if key.name == 'KEY_ENTER' or key == '\n' or key == '\r':
            print()  # newline after submit
            return buffer
        # handle backspace
        if key.name == 'KEY_BACKSPACE' or key == '\b' or key == '\x7f':
            if buffer:
                buffer = buffer[:-1]
                print('\b \b', end="", flush=True)
            continue
        # handle escape -> treat as cancel/empty submit
        if key.name == 'KEY_ESCAPE':
            print()
            return buffer
        # accept printable characters
        if str(key) and not key.is_sequence:
            ch = str(key)
            # basic guard against non-printable
            if ch.isprintable():
                buffer += ch
                print(ch, end="", flush=True)
