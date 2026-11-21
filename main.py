"""Application entry point and Tkinter event-loop pipeline."""

import tkinter as tk

from src.reflex_challenge import ReflexChallenge


def main():
    """Create the root window, load the game, and start processing events."""
    root = tk.Tk()
    ReflexChallenge(root)
    root.mainloop()


if __name__ == "__main__":
    main()
