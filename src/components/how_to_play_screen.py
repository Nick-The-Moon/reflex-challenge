import tkinter as tk
from .base_screen import ScreenComponent
from .theme import (
    COR_FUNDO,
)
from .futuristic_button import BotaoFuturista

class HowToPlayScreen(ScreenComponent):
    """Individually constructible how to play screen."""

    def __init__(self, app):
        super().__init__(app)
        self.build()

    def build(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.register_screen("como_jogar", tela)

        canvas_bg = tk.Canvas(tela, bg=COR_FUNDO, highlightthickness=0)
        canvas_bg.pack(fill="both", expand=True)
        canvas_bg.bind("<Configure>", lambda e: self.create_background(canvas_bg, "assets/como_jogar.png", "img_bg_como_jogar"))

        frame_btn = tk.Frame(tela, bg="#0A0A0E")
        frame_btn.place(relx=0.5, rely=0.92, anchor="center")
        BotaoFuturista(frame_btn, "VOLTAR AO MENU", self._ir_para_menu, largura=280, altura=55).pack()
