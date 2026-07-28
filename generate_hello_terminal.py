# -*- coding: utf-8 -*-
"""
Hacker Hello Terminal - Figlet ANSI Shadow Style
Renders the classic figlet "HELLO" as raw SVG <rect> elements with 3D shadow depth.
Each cell from the figlet grid maps to a colored rectangle:
  1 = bright green (main block)
  2 = dark green (shadow/depth)
  0 = empty
"""
import os

def generate_svg():
    # Figlet ANSI Shadow grids for each letter
    # Mapped from:
    # ██╗  ██╗███████╗██╗     ██╗      ██████╗
    # ██║  ██║██╔════╝██║     ██║     ██╔═══██╗
    # ███████║█████╗  ██║     ██║     ██║   ██║
    # ██╔══██║██╔══╝  ██║     ██║     ██║   ██║
    # ██║  ██║███████╗███████╗███████╗╚██████╔╝
    # ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝

    H = [
        [1,1,2,0,0,1,1,2],
        [1,1,2,0,0,1,1,2],
        [1,1,1,1,1,1,1,2],
        [1,1,2,2,2,1,1,2],
        [1,1,2,0,0,1,1,2],
        [2,2,2,0,0,2,2,2],
    ]

    E = [
        [1,1,1,1,1,1,1,2],
        [1,1,2,2,2,2,2,2],
        [1,1,1,1,1,2,0,0],
        [1,1,2,2,2,2,0,0],
        [1,1,1,1,1,1,1,2],
        [2,2,2,2,2,2,2,2],
    ]

    L = [
        [1,1,2,0,0,0,0,0],
        [1,1,2,0,0,0,0,0],
        [1,1,2,0,0,0,0,0],
        [1,1,2,0,0,0,0,0],
        [1,1,1,1,1,1,1,2],
        [2,2,2,2,2,2,2,2],
    ]

    O = [
        [0,1,1,1,1,1,1,2,0],
        [1,1,2,2,2,2,1,1,2],
        [1,1,2,0,0,0,1,1,2],
        [1,1,2,0,0,0,1,1,2],
        [2,1,1,1,1,1,1,2,2],
        [0,2,2,2,2,2,2,2,0],
    ]

    word = [('H', H), ('E', E), ('L', L), ('L', L), ('O', O)]

    # Cell dimensions
    CW = 11   # cell width in px
    CH = 14   # cell height in px
    GAP = 1   # gap between letters in cells

    # Colors
    MAIN = "#00ff87"    # bright green
    SHADOW = "#005c32"  # dark green depth

    # Calculate total width to center in viewport
    total_cells = sum(len(grid[0]) for _, grid in word) + GAP * (len(word) - 1)
    total_w = total_cells * CW
    x_start = 15 + (590 - total_w) // 2
    y_start = 155

    # Build rect elements grouped by row
    rects_by_row = {i: [] for i in range(6)}
    cx = x_start
    for _, grid in word:
        for row_i, row in enumerate(grid):
            for col_i, val in enumerate(row):
                if val == 0:
                    continue
                x = cx + col_i * CW
                y = y_start + row_i * CH
                color = MAIN if val == 1 else SHADOW
                rects_by_row[row_i].append(
                    f'        <rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{color}" />'
                )
        cx += (len(grid[0]) + GAP) * CW

    # Total HELLO block dimensions for clip-path
    hello_w = total_w + 10
    hello_h = 6 * CH + 10
    clip_x = x_start - 5
    clip_y = y_start - 5

    # Generate the clip paths for each row
    clip_paths = []
    for i in range(6):
        start_key = round(0.17 + i * 0.02, 4)
        end_key = round(0.19 + i * 0.02, 4)
        clip_paths.append(f"""    <clipPath id="ch{i}">
      <rect x="{clip_x}" y="{y_start + i * CH}" width="0" height="{CH}">
        <animate attributeName="width" values="0;0;{hello_w};{hello_w};0;0" keyTimes="0;{start_key};{end_key};0.85;0.8501;1" dur="10s" repeatCount="indefinite" />
      </rect>
    </clipPath>""")
    clip_paths_content = "\n".join(clip_paths)

    # Format the groups for the template
    hello_rect_groups = []
    for i in range(6):
        row_rects = "\n".join(rects_by_row[i])
        hello_rect_groups.append(
            f'    <g clip-path="url(#ch{i})">\n{row_rects}\n    </g>'
        )
    hello_rects_content = "\n".join(hello_rect_groups)

    # Scanning cursor positions
    cursor_x_values = f"{clip_x};{clip_x};{clip_x + hello_w};{clip_x};{clip_x + hello_w};{clip_x};{clip_x + hello_w};{clip_x};{clip_x + hello_w};{clip_x};{clip_x + hello_w};{clip_x};{clip_x + hello_w};{clip_x};{clip_x};{clip_x}"
    cursor_x_keytimes = "0;0.17;0.19;0.1901;0.21;0.2101;0.23;0.2301;0.25;0.2501;0.27;0.2701;0.29;0.2901;0.85;1"
    cursor_y_values = f"{y_start};{y_start};{y_start};{y_start + CH};{y_start + CH};{y_start + 2*CH};{y_start + 2*CH};{y_start + 3*CH};{y_start + 3*CH};{y_start + 4*CH};{y_start + 4*CH};{y_start + 5*CH};{y_start + 5*CH};{y_start};{y_start};{y_start}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 340" width="620" height="340">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;display=swap');
      .tw {{ font-family: 'Fira Code', 'JetBrains Mono', 'Courier New', monospace; font-size: 12px; fill: #c9d1d9; }}
      .pu {{ fill: #58a6ff; font-weight: bold; }}
      .ps {{ fill: #c9d1d9; }}
      .pc {{ fill: #f0883e; font-weight: bold; }}
      .st {{ fill: #8b949e; }}
      .sok {{ fill: #58a6ff; font-weight: bold; }}
      .srd {{ fill: #00ff87; font-weight: bold; }}
    </style>
  </defs>

  <g class="tw">
    <!-- Shadow -->
    <rect x="21" y="21" width="590" height="310" rx="10" ry="10" fill="#010409" opacity="0.5" />

    <!-- Window body -->
    <rect x="15" y="15" width="590" height="310" rx="10" ry="10" fill="#0d1117" stroke="#30363d" stroke-width="1.5" />

    <!-- Header bar -->
    <rect x="15" y="15" width="590" height="35" rx="10" ry="10" fill="#161b22" stroke="#30363d" stroke-width="1.5" />
    <rect x="16" y="36" width="588" height="14" fill="#161b22" />

    <!-- Traffic light dots -->
    <circle cx="35" cy="32" r="6" fill="#ff5f56" />
    <circle cx="55" cy="32" r="6" fill="#ffbd2e" />
    <circle cx="75" cy="32" r="6" fill="#27c93f" />
    <text x="310" y="36" fill="#8b949e" font-size="11" font-weight="700" text-anchor="middle">jay-magar ~ terminal</text>

    <!-- Command line: jay@magar:~$ ./say_hello.sh -->
    <g>
      <text x="40" y="75"><tspan class="pu">jay@magar</tspan><tspan class="ps">:~$ </tspan></text>
      <clipPath id="c0"><rect x="140" y="63" width="0" height="20">
        <animate attributeName="width" values="0;0;101;101;0;0" keyTimes="0;0.02;0.08;0.85;0.8501;1" dur="10s" repeatCount="indefinite" />
      </rect></clipPath>
      <text x="140" y="75" class="pc" clip-path="url(#c0)">./say_hello.sh</text>
      <!-- Typing cursor -->
      <rect x="140" y="63" width="8" height="15" fill="#00ff87">
        <animate attributeName="x" values="140;140;241;241;140;140" keyTimes="0;0.02;0.08;0.85;0.8501;1" dur="10s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="1;0;1;0;1;1;0;0;0;0" keyTimes="0;0.005;0.01;0.015;0.02;0.085;0.086;0.85;0.8501;1" dur="10s" repeatCount="indefinite" />
      </rect>
    </g>

    <!-- Status line 1 -->
    <g>
      <clipPath id="c1"><rect x="40" y="83" width="0" height="20">
        <animate attributeName="width" values="0;0;280;280;0;0" keyTimes="0;0.09;0.11;0.85;0.8501;1" dur="10s" repeatCount="indefinite" />
      </rect></clipPath>
      <text x="40" y="95" class="st" clip-path="url(#c1)">[+] Decrypting cyber uplink... <tspan class="sok">[OK]</tspan></text>
    </g>

    <!-- Status line 2 -->
    <g>
      <clipPath id="c2"><rect x="40" y="103" width="0" height="20">
        <animate attributeName="width" values="0;0;320;320;0;0" keyTimes="0;0.11;0.13;0.85;0.8501;1" dur="10s" repeatCount="indefinite" />
      </rect></clipPath>
      <text x="40" y="115" class="st" clip-path="url(#c2)">[+] Establishing secure handshake... <tspan class="sok">[OK]</tspan></text>
    </g>

    <!-- Status line 3 -->
    <g>
      <clipPath id="c3"><rect x="40" y="123" width="0" height="20">
        <animate attributeName="width" values="0;0;300;300;0;0" keyTimes="0;0.13;0.15;0.85;0.8501;1" dur="10s" repeatCount="indefinite" />
      </rect></clipPath>
      <text x="40" y="135" class="st" clip-path="url(#c3)">[+] Loading kernel interface... <tspan class="srd">[READY]</tspan></text>
    </g>

    <!-- ===== HELLO FIGLET LETTERS (raw rects, ANSI Shadow style) ===== -->
    {clip_paths_content}
    <g>
{hello_rects_content}
      <!-- Scanning cursor beam -->
      <rect x="{clip_x}" y="{y_start}" width="8" height="{CH}" fill="#00ff87" opacity="0">
        <animate attributeName="x" values="{cursor_x_values}" keyTimes="{cursor_x_keytimes}" dur="10s" repeatCount="indefinite" />
        <animate attributeName="y" values="{cursor_y_values}" keyTimes="{cursor_x_keytimes}" dur="10s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0;0;0.8;0.8;0;0;0;0" keyTimes="0;0.17;0.1701;0.29;0.2901;0.85;0.8501;1" dur="10s" repeatCount="indefinite" />
      </rect>
    </g>

    <!-- Bottom prompt with blinking cursor -->
    <g>
      <text x="40" y="295">
        <animate attributeName="visibility" values="hidden;hidden;visible;visible;hidden;hidden" keyTimes="0;0.33;0.33;0.85;0.8501;1" dur="10s" repeatCount="indefinite" />
        <tspan class="pu">jay@magar</tspan><tspan class="ps">:~$ </tspan>
      </text>
      <rect x="140" y="283" width="8" height="15" fill="#00ff87">
        <animate attributeName="opacity" values="0;0;1;0;1;0;1;0;1;0;1;0;1;0;1;0;1;0;1;0;1;0;0;0;0"
                 keyTimes="0;0.329;0.33;0.36;0.39;0.42;0.45;0.48;0.51;0.54;0.57;0.60;0.63;0.66;0.69;0.72;0.75;0.78;0.81;0.84;0.845;0.846;0.85;0.8501;1"
                 dur="10s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>
</svg>
"""

    output_path = "hello_terminal.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated figlet ANSI Shadow HELLO: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_svg()
