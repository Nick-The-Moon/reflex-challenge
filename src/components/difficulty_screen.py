import tkinter as tk
from .base_screen import ScreenComponent
from .theme import (
    COR_AMARELO, COR_CINZA, COR_FUNDO, COR_NEON, COR_PAINEL, COR_VERMELHO, FAMILIA,
)
from .futuristic_button import BotaoFuturista

class DifficultyScreen(ScreenComponent):
    """Individually constructible difficulty screen."""

    def __init__(self, app):
        super().__init__(app)
        self.build()

    def build(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.register_screen("dificuldade", tela)
        centro = tk.Frame(tela, bg=COR_FUNDO)
        centro.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_dificuldade_nome = tk.Label(centro, text="ESCOLHA A DIFICULDADE", font=(FAMILIA, 32, "bold"), fg=COR_NEON, bg=COR_FUNDO)
        self.lbl_dificuldade_nome.pack(pady=(0, 40))

        area = tk.Frame(centro, bg=COR_FUNDO)
        area.pack()

        configs = [("FÁCIL", COR_NEON, "facil"), ("MÉDIO", COR_AMARELO, "medio"), ("DIFÍCIL", COR_VERMELHO, "dificil")]
        for col, (nome, cor, nivel) in enumerate(configs):
            cartao = tk.Frame(area, bg=COR_PAINEL, highlightbackground=cor, highlightthickness=2, padx=30, pady=40)
            cartao.grid(row=0, column=col, padx=20, sticky="nsew")

            tk.Label(cartao, text=nome, font=(FAMILIA, 24, "bold"), fg=cor, bg=COR_PAINEL).pack(pady=(0, 25))
            BotaoFuturista(cartao, "JOGAR", lambda n=nivel: self.iniciar_partida(n), largura=200, altura=55, cor_borda=cor).pack()

        BotaoFuturista(centro, "VOLTAR", self._ir_para_nome, largura=260, altura=50, cor_borda=COR_CINZA).pack(pady=50)
