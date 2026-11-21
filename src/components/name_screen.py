import tkinter as tk
from .base_screen import ScreenComponent
from .theme import (
    COR_BRANCO, COR_CINZA, COR_FUNDO, COR_NEON, COR_PAINEL, FAMILIA,
)
from .futuristic_button import BotaoFuturista

class NameScreen(ScreenComponent):
    """Individually constructible name screen."""

    def __init__(self, app):
        super().__init__(app)
        self.build()

    def build(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.register_screen("nome", tela)
        centro = tk.Frame(tela, bg=COR_FUNDO)
        centro.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(centro, text="QUEM ESTÁ JOGANDO?", font=(FAMILIA, 32, "bold"), fg=COR_NEON, bg=COR_FUNDO).pack(pady=(0, 10))
        self.entry_nome = tk.Entry(centro, font=(FAMILIA, 24), bg=COR_PAINEL, fg=COR_BRANCO, insertbackground=COR_NEON, width=20, justify="center", relief="flat", highlightthickness=2, highlightbackground=COR_NEON)
        self.entry_nome.pack(pady=20, ipady=10)
        self.entry_nome.bind("<Return>", lambda e: self._confirmar_nome())

        BotaoFuturista(centro, "CONFIRMAR E JOGAR", self._confirmar_nome, largura=320, altura=60).pack(pady=15)
        BotaoFuturista(centro, "VOLTAR", self._ir_para_menu, largura=320, altura=50, cor_borda=COR_CINZA).pack()
