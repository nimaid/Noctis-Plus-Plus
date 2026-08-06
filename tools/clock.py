#!/usr/bin/env python3

import time
from modules.feltime import feltime

print("\033[H\033[2J", end="")

print("\n     Felesian Clock")
print(  " Press Ctrl+C to exit...")

print("\n  +------------------+")
print("\n  +------------------+")
print("\033[2A", end="\r")
try:
    while True:
        print(feltime.now().strftime("  | %c |"), end="")
        print("\033[2B", end="\r")
        time.sleep(1)
        print("\033[2A", end="\r")
except KeyboardInterrupt:
    print("\033[2A", end="\r")
    print(feltime.now().strftime("  | %c |"), end="\r")
    print("\033[2B")
    print("   Program has exited.")
    print("    Have a nice day!")
