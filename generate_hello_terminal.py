# -*- coding: utf-8 -*-
"""
Hacker Hello Terminal Animation SVG Generator
Creates a styled terminal mockup in SVG that simulates typing a command and receiving
a big glowing block-text "HELLO" response.
"""
import os

def generate_svg():
    # Hello ASCII Art (38 characters wide per line) using ONLY solid blocks
    hello_lines = [
        "██  ██  ██████  ██      ██      ██████",
        "██  ██  ██      ██      ██      ██  ██",
        "██████  ████    ██      ██      ██  ██",
        "██  ██  ██      ██      ██      ██  ██",
        "██  ██  ██████  ██████  ██████  ██████"
    ]

    # Terminal size: 590x310 (leaves 15px margin in 620x340 viewport for drop shadow)
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 340" width="620" height="340">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;display=swap');
      .terminal-window {
        font-family: 'Fira Code', 'JetBrains Mono', 'Courier New', monospace;
        font-size: 12px;
        fill: #c9d1d9;
      }
      .window-bg {
        fill: #0d1117;
        stroke: #30363d;
        stroke-width: 1.5;
        rx: 10px;
        ry: 10px;
      }
      .header-bg {
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1.5;
        rx: 10px;
        ry: 10px;
      }
      .dot {
        stroke-width: 0;
      }
      .terminal-title {
        fill: #8b949e;
        font-size: 11px;
        font-weight: 700;
        text-anchor: middle;
      }
      .prompt-user {
        fill: #58a6ff;
        font-weight: bold;
      }
      .prompt-symbol {
        fill: #c9d1d9;
      }
      .prompt-cmd {
        fill: #f0883e;
        font-weight: bold;
      }
      .status-text {
        fill: #8b949e;
      }
      .status-ok {
        fill: #58a6ff;
        font-weight: bold;
      }
      .status-ready {
        fill: #00ff87;
        font-weight: bold;
        filter: url(#glow);
      }
      .cursor {
        fill: #00ff87;
      }
    </style>
    
    <!-- Glow filter for hacker aesthetic (used for fallback renderers) -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Gradient for HELLO text (Green to Cyan) -->
    <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00FF87" />
      <stop offset="100%" stop-color="#60EFFF" />
    </linearGradient>
  </defs>
  
  <g class="terminal-window">
    <!-- Whole terminal fades out at 8.5s and fades in at 9.0s to restart loop -->
    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.85;0.90;0.98;1" dur="10.0s" repeatCount="indefinite" />
    
    <!-- Vector Drop Shadow (Soft dark rect offset by +6px to avoid sanitizer stripping) -->
    <rect x="21" y="21" width="590" height="310" fill="#010409" opacity="0.6" rx="10" ry="10" />
    
    <!-- Window Body -->
    <rect class="window-bg" x="15" y="15" width="590" height="310" />
    
    <!-- Header Bar (Top Rounded) -->
    <rect class="header-bg" x="15" y="15" width="590" height="35" />
    <!-- Cover bottom corners of header to make them flat -->
    <rect x="15.75" y="35" width="588.5" height="15" fill="#161b22" />
    
    <!-- Window Controls -->
    <circle class="dot" cx="35" cy="32" r="6" fill="#ff5f56" />
    <circle class="dot" cx="55" cy="32" r="6" fill="#ffbd2e" />
    <circle class="dot" cx="75" cy="32" r="6" fill="#27c93f" />
    <text class="terminal-title" x="310.0" y="36">jay-magar ~ hello_secure</text>
    
    <!-- Line 1: Command Typing -->
    <g>
      <text x="40" y="75"><tspan class="prompt-user">jay@magar</tspan><tspan class="prompt-symbol">:~$ </tspan></text>
      <!-- Typing animation for command -->
      <clipPath id="clip-cmd">
        <rect x="140" y="63" width="0" height="20">
          <animate attributeName="width" values="0;0;101;101;0" keyTimes="0;0.02;0.08;0.85;1" dur="10.0s" repeatCount="indefinite" />
        </rect>
      </clipPath>
      <text x="140" y="75" class="prompt-cmd" clip-path="url(#clip-cmd)">./say_hello.sh</text>
      
      <!-- Command Typing Cursor -->
      <rect class="cursor" x="140" y="63" width="8" height="15">
        <animate attributeName="x" values="140;140;241;241;140;140" keyTimes="0;0.02;0.08;0.085;0.85;1" dur="10.0s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="1;0;1;0;1;1;0;0" keyTimes="0;0.005;0.01;0.015;0.02;0.085;0.086;1" dur="10.0s" repeatCount="indefinite" />
      </rect>
    </g>

    <!-- Line 2: Decrypting status -->
    <g>
      <clipPath id="clip-status-1">
        <rect x="40" y="83" width="0" height="20">
          <animate attributeName="width" values="0;0;260;260;0" keyTimes="0;0.09;0.11;0.85;1" dur="10.0s" repeatCount="indefinite" />
        </rect>
      </clipPath>
      <text x="40" y="95" class="status-text" clip-path="url(#clip-status-1)">[+] Decrypting cyber uplink... <tspan class="status-ok">[OK]</tspan></text>
    </g>

    <!-- Line 3: Establishing status -->
    <g>
      <clipPath id="clip-status-2">
        <rect x="40" y="103" width="0" height="20">
          <animate attributeName="width" values="0;0;300;300;0" keyTimes="0;0.11;0.13;0.85;1" dur="10.0s" repeatCount="indefinite" />
        </rect>
      </clipPath>
      <text x="40" y="115" class="status-text" clip-path="url(#clip-status-2)">[+] Establishing secure handshake... <tspan class="status-ok">[OK]</tspan></text>
    </g>

    <!-- Line 4: Kernel interface status -->
    <g>
      <clipPath id="clip-status-3">
        <rect x="40" y="123" width="0" height="20">
          <animate attributeName="width" values="0;0;290;290;0" keyTimes="0;0.13;0.15;0.85;1" dur="10.0s" repeatCount="indefinite" />
        </rect>
      </clipPath>
      <text x="40" y="135" class="status-text" clip-path="url(#clip-status-3)">[+] Loading kernel interface... <tspan class="status-ready">[READY]</tspan></text>
    </g>

    <!-- Big HELLO Block Text Section (Centered at x=173, width=273.6) -->
"""

    # Add the 5 lines of HELLO ASCII art as solid vector rectangles
    def get_segments(line_str):
        segments = []
        in_block = False
        start = 0
        for char_idx, char in enumerate(line_str):
            if char == '█' and not in_block:
                in_block = True
                start = char_idx
            elif char != '█' and in_block:
                in_block = False
                segments.append((start, char_idx - start))
        if in_block:
            segments.append((start, len(line_str) - start))
        return segments

    y_start = 175
    y_gap = 20
    for idx, line in enumerate(hello_lines):
        line_num = idx + 1
        y_pos = y_start + (idx * y_gap)
        
        # Start and end times for each line typing
        t_start = 0.17 + (idx * 0.02)
        t_end = t_start + 0.02
        
        # Format times for SMIL keyTimes
        kt_width = f"0;{t_start:.4f};{t_end:.4f};0.8500;1"
        kt_cursor = f"0;{t_start:.4f};{t_end:.4f};1"
        kt_opacity = f"0;{t_start:.4f};{t_start+0.0001:.4f};{t_end-0.0001:.4f};{t_end:.4f};1"
        
        rects_html = ""
        for start, length in get_segments(line):
            x_coord = 173 + start * 7.2
            width = length * 7.2
            rects_html += f'<rect x="{x_coord:.2f}" y="{y_pos - 12}" width="{width:.2f}" height="15" fill="url(#text-grad)" filter="url(#glow)" />'
        
        svg_content += f"""
    <!-- HELLO Line {line_num} -->
    <g>
      <clipPath id="clip-hello-{line_num}">
        <rect x="173" y="{y_pos - 12}" width="0" height="20">
          <animate attributeName="width" values="0;0;274;274;0" keyTimes="{kt_width}" dur="10.0s" repeatCount="indefinite" />
        </rect>
      </clipPath>
      <g clip-path="url(#clip-hello-{line_num})">
        {rects_html}
      </g>
      
      <!-- Slide cursor for Line {line_num} -->
      <rect class="cursor" x="173" y="{y_pos - 12}" width="8" height="15">
        <animate attributeName="x" values="173;173;447;447" keyTimes="{kt_cursor}" dur="10.0s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt_opacity}" dur="10.0s" repeatCount="indefinite" />
      </rect>
    </g>"""

    # Add final command prompt and blinking cursor at the bottom (Y = 295)
    svg_content += """

    <!-- Bottom Command Prompt -->
    <g>
      <text x="40" y="295">
        <animate attributeName="visibility" values="hidden;hidden;visible;visible;hidden" keyTimes="0;0.30;0.30;0.85;1" dur="10.0s" repeatCount="indefinite" />
        <tspan class="prompt-user">jay@magar</tspan><tspan class="prompt-symbol">:~$ </tspan>
      </text>
      
      <!-- Blinking Cursor -->
      <rect class="cursor" x="140" y="283" width="8" height="15">
        <animate attributeName="opacity" values="0;0;1;0;1;0;1;0;1;0;1;0;1;0;1;0;1;0;1;0;1;0;1;0;0;0" 
                 keyTimes="0.000;0.299;0.300;0.325;0.350;0.375;0.400;0.425;0.450;0.475;0.500;0.525;0.550;0.575;0.600;0.625;0.650;0.675;0.700;0.725;0.750;0.775;0.800;0.825;0.850;1.000" 
                 dur="10.0s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>
</svg>
"""

    output_path = "hello_terminal.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print(f"Generated hacker secure hello terminal visual successfully: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_svg()
