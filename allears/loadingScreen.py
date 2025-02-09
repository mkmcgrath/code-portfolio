import curses
from PIL import Image, ImageSequence
import time


def gif_to_ascii_frames(gif_path, width=80):
    """Convert GIF to ASCII frames."""
    frames = []
    gif = Image.open(gif_path)
    for frame in ImageSequence.Iterator(gif):
        # Resize frame
        frame = frame.convert("L").resize(
            (width, int(width * frame.height / frame.width / 2))
        )
        # Convert to ASCII
        ascii_frame = []
        pixel_data = list(frame.getdata())  # Ensure pixel data is list-like
        for y in range(frame.height):
            row = "".join(
                [
                    " .:-=+*#%@"[min(pixel // 25, 9)]
                    for pixel in pixel_data[y * frame.width : (y + 1) * frame.width]
                ]
            )
            ascii_frame.append(row)
        frames.append(ascii_frame)
    return frames


def display_banner(stdscr, y_offset):
    """Display the ASCII banner."""

    banner = [
        "          oooo  oooo                                         ",
        "          `888  `888                                         ",
        " .oooo.    888   888   .ooooo.   .oooo.   oooo d8b  .oooo.o  ",
        "P  )88b   888   888  d88' `88b `P  )88b  `888V" "8P d88(  L8 ",
        " .oPa888   888   888  888ooo888  .oP_888   888     ` Y88b.   ",
        "d8(  888   888   888  888    .o d8(  888   888     o.  )88b  ",
        "`Y888aaa8o o888o o888o Y8bod8P `Y888&^^8o d888b    8&&888P' ",
        "                                                             ",
        "                                                             ",
        "                                                             ",
    ]

    # width = stdscr.getmaxyx()
    width = 220
    for i, line in enumerate(banner):
        x = max(0, (width - len(line)) // 2)
        y = y_offset + i
        stdscr.addstr(y, x, line)


def display_gif_and_progress(stdscr, tasks):
    curses.curs_set(0)  # Hide cursor
    height, width = stdscr.getmaxyx()

    frame_delay = 0.1  # Adjust as needed

    bar_width = width - 4

    curses.start_color()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    for i, (task_name, duration) in enumerate(tasks):
        start_time = time.time()
        elapsed = 0
        while elapsed < duration:
            stdscr.clear()

            stdscr.bkgd(" ", curses.color_pair(1))

            # Display banner
            display_banner(stdscr, height // 2 - 5)

            # Display loading bar
            progress = int(((elapsed + (i / len(tasks))) / len(tasks)) * bar_width)
            bar = "=" * progress + " " * (bar_width - progress)
            stdscr.addstr(
                height - 3, 2, f"[{bar}] {i + 1}/{len(tasks)}", curses.color_pair(1)
            )
            stdscr.addstr(
                height - 2, 2, f" Current Task: {task_name}", curses.color_pair(1)
            )

            # Refresh screen
            stdscr.refresh()
            time.sleep(frame_delay)

            # Update time and frame index
            elapsed = time.time() - start_time

    stdscr.addstr(height - 1, 2, "(Press any key to continue)", curses.color_pair(1))
    stdscr.refresh()
    # stdscr.getch()


def loading(stdscr):
    """Main function to run the curses interface."""

    # Tasks for the loading bar
    tasks = [
        ("Initializing modules", 1),
        ("Loading resources", 2),
        ("Finalizing setup", 1.5),
    ]

    # Display GIF, banner, and progress bar simultaneously
    display_gif_and_progress(stdscr, tasks)
    return 0


if __name__ == "__main__":
    curses.wrapper(loading)
