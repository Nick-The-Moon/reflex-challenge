"""Scrollable frame widget with the project's neon scrollbar style."""

import tkinter as tk
from tkinter import ttk

from .theme import COR_BRANCO, COR_FUNDO, COR_NEON


class TabelaComScroll(tk.Frame):
    """Frame that provides an independently scrollable content area."""

    def __init__(self, mestre, bg="#0A0A0E"):
        super().__init__(mestre, bg=bg)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Neon.Vertical.TScrollbar",
            background=COR_NEON,
            troughcolor=COR_FUNDO,
            bordercolor=COR_FUNDO,
            arrowcolor=COR_BRANCO,
            lightcolor=COR_NEON,
            darkcolor=COR_NEON,
        )

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            style="Neon.Vertical.TScrollbar",
        )
        self.frame_interno = tk.Frame(self.canvas, bg=bg)

        self.frame_interno.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.frame_interno, anchor="nw"
        )
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(
                self.canvas_window, width=event.width
            ),
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda event: self.canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units"
            )
            if self.canvas.winfo_exists()
            else None,
        )
