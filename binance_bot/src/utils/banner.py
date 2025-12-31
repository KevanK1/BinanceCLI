#!/usr/bin/env python3
"""
ASCII Art Banner for Binance CLI.
Displays a stylish gradient banner when the CLI starts.
"""

# ANSI color codes for gradient effect (blue to pink/magenta)
COLORS = [
    "\033[38;5;75m",   # Light blue
    "\033[38;5;111m",  # Sky blue
    "\033[38;5;147m",  # Light purple
    "\033[38;5;183m",  # Light magenta
    "\033[38;5;219m",  # Pink
    "\033[38;5;218m",  # Light pink
]

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
YELLOW = "\033[38;5;220m"
CYAN = "\033[38;5;51m"
WHITE = "\033[38;5;255m"
BOX_BORDER = "\033[38;5;245m"

# ASCII Art for "BINANCE CLI" - block-style letters (large)
ASCII_ART = [
    "██████╗ ██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗",
    "██╔══██╗██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝",
    "██████╔╝██║██╔██╗ ██║███████║██╔██╗ ██║██║     █████╗  ",
    "██╔══██╗██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██╔══╝  ",
    "██████╔╝██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗███████╗",
    "╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝",
    "                                                        ",
    " ██████╗██╗     ██╗                                     ",
    "██╔════╝██║     ██║                                     ",
    "██║     ██║     ██║                                     ",
    "██║     ██║     ██║                                     ",
    "╚██████╗███████╗██║                                     ",
    " ╚═════╝╚══════╝╚═╝                                     ",
]

# Signature text
SIGNATURE = "Made with ❤️  by Kevan"


def get_gradient_color(line_index: int, total_lines: int) -> str:
    """Get gradient color based on line position."""
    if total_lines <= 1:
        return COLORS[0]
    # Map line index to color index
    color_index = int((line_index / (total_lines - 1)) * (len(COLORS) - 1))
    return COLORS[min(color_index, len(COLORS) - 1)]


def apply_horizontal_gradient(line: str, start_color_idx: int = 0) -> str:
    """Apply horizontal gradient across a single line."""
    if not line:
        return line
    
    result = []
    chars_per_color = max(1, len(line) // len(COLORS))
    
    for i, char in enumerate(line):
        color_idx = min(i // chars_per_color + start_color_idx, len(COLORS) - 1)
        result.append(f"{COLORS[color_idx]}{char}")
    
    return "".join(result) + RESET


def print_banner():
    """Print the stylish ASCII art banner."""
    # Enable Windows terminal colors
    try:
        import os
        os.system('')  # Enable ANSI escape sequences on Windows
    except:
        pass
    
    print()
    
    # Welcome message box
    welcome_msg = "Welcome to the Binance CLI research preview!"
    box_width = len(welcome_msg) + 6
    
    print(f"  {BOX_BORDER}╭{'─' * box_width}╮{RESET}")
    print(f"  {BOX_BORDER}│{RESET}  {YELLOW}✳ {RESET} {WHITE}{welcome_msg}{RESET} {BOX_BORDER}│{RESET}")
    print(f"  {BOX_BORDER}╰{'─' * box_width}╯{RESET}")
    print()
    
    # ASCII Art with gradient
    total_lines = len(ASCII_ART)
    for i, line in enumerate(ASCII_ART):
        # Apply both vertical and horizontal gradient
        colored_line = apply_horizontal_gradient(line, start_color_idx=i % 2)
        print(f"  {colored_line}")
    
    # "Made with ❤️ by Kevan" signature box
    print()
    sig_box_width = len(SIGNATURE) + 6
    print(f"  {BOX_BORDER}╭{'─' * sig_box_width}╮{RESET}")
    print(f"  {BOX_BORDER}│{RESET}  {apply_horizontal_gradient(SIGNATURE, start_color_idx=2)}  {BOX_BORDER}  │{RESET}")
    print(f"  {BOX_BORDER}╰{'─' * sig_box_width}╯{RESET}")
    
    print()
    print(f"  {DIM}{'─' * 70}{RESET}")
    print()


def print_simple_banner():
    """Print a simplified banner for non-interactive use."""
    print()
    print(f"  {CYAN}═══════════════════════════════════════════════{RESET}")
    print(f"  {BOLD}{WHITE}  BINANCE CLI{RESET} {DIM}| SPOT Trading Bot{RESET}")
    print(f"  {CYAN}═══════════════════════════════════════════════{RESET}")
    print()


if __name__ == "__main__":
    # Test the banner ✳ 
    print_banner()
