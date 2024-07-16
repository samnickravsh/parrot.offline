import os
import time
import threading
import curses
from http.server import SimpleHTTPRequestHandler, HTTPServer


frames_dir = 'frames'
frame_files = sorted(os.listdir(frames_dir))


frames = []
for frame_file in frame_files:
    with open(os.path.join(frames_dir, frame_file), 'r') as file:
        frames.append(file.read())


color_pairs = [
    curses.COLOR_RED,
    curses.COLOR_YELLOW,
    curses.COLOR_GREEN,
    curses.COLOR_BLUE,
    curses.COLOR_MAGENTA,
    curses.COLOR_CYAN,
    curses.COLOR_WHITE,
]


delay = 0.05


def handle_input(stdscr):
    global delay
    stdscr.nodelay(True)
    while True:
        key = stdscr.getch()
        if key == ord('1'):
            delay = 0.01
        elif key == ord('2'):
            delay = 0.02
        elif key == ord('3'):
            delay = 0.03
        elif key == ord('4'):
            delay = 0.04
        elif key == ord('5'):
            delay = 0.05
        elif key == ord('6'):
            delay = 0.06
        elif key == ord('7'):
            delay = 0.07
        elif key == ord('8'):
            delay = 0.08
        elif key == ord('9'):
            delay = 0.09
        elif key == ord('0'):
            delay = 2
        time.sleep(0.25)


def display_frames(stdscr):
    try:
        curses.curs_set(0)
        color_index = 0
        while True:
            for frame in frames:
                stdscr.clear()
                stdscr.addstr(0, 0, frame, curses.color_pair(color_index % len(color_pairs) + 1))
                stdscr.refresh()
                color_index += 1
                time.sleep(delay)
    except KeyboardInterrupt:
        curses.curs_set(1)  # Show cursor


class ParrotHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <head><title>Parrot Live</title></head>
                <body><pre id="parrot"></pre></body>
                <script>
                const frames = """ + str(frames).encode() + b""";
                const colors = ['red', 'yellow', 'green', 'blue', 'magenta', 'cyan', 'white'];
                let index = 0;
                let colorIndex = 0;
                setInterval(() => {
                    const frame = frames[index];
                    const color = colors[colorIndex % colors.length];
                    document.getElementById('parrot').style.color = color;
                    document.getElementById('parrot').innerText = frame;
                    index = (index + 1) % frames.length;
                    colorIndex++;
                }, 50);  // Adjusted the interval to 50 milliseconds for a faster animation
                </script>
                </html>
            """)
        else:
            self.send_error(404)
            self.end_headers()


def start_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ParrotHandler)
    print("Serving on port 8000...")
    httpd.serve_forever()


def main(stdscr):
    os.system('printf "\033[48;2;0;0;0m\033[2J\033[H"')

    
    threading.Thread(target=start_server, daemon=True).start()


    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)


    stdscr.bkgd(' ', curses.color_pair(7))  # Use color pair 7 as default background color (black)
    stdscr.clear()
    stdscr.refresh()


    threading.Thread(target=display_frames, args=(stdscr,), daemon=True).start()


    handle_input(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
