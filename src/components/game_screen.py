import tkinter as tk
from .base_screen import ScreenComponent
from .theme import (
    COR_AMARELO, COR_BRANCO, COR_FUNDO, COR_NEON, COR_PAINEL, COR_VERDE_ESCURO, COR_VERMELHO, FAMILIA,
)
from .futuristic_button import BotaoFuturista

class GameScreen(ScreenComponent):
    """Individually constructible game screen."""

    def __init__(self, app):
        super().__init__(app)
        self.build()

    def build(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.register_screen("jogo", tela)
        
        cabecalho = tk.Frame(tela, bg=COR_FUNDO)
        cabecalho.pack(fill="x", padx=60, pady=(30, 10))
        self.lbl_nivel = tk.Label(cabecalho, text="", font=(FAMILIA, 18, "bold"), fg=COR_NEON, bg=COR_FUNDO)
        self.lbl_nivel.pack(side="left")
        self.lbl_rodada = tk.Label(cabecalho, text="", font=(FAMILIA, 18, "bold"), fg=COR_BRANCO, bg=COR_FUNDO)
        self.lbl_rodada.pack(side="right")

        self.canvas_jogo = tk.Canvas(tela, bg=COR_PAINEL, highlightthickness=2, highlightbackground=COR_VERDE_ESCURO, cursor="hand2")
        self.canvas_jogo.pack(fill="both", expand=True, padx=60, pady=10)
        self.canvas_jogo.bind("<Button-1>", self._ao_clicar_area)

        rodape = tk.Frame(tela, bg=COR_FUNDO)
        rodape.pack(fill="x", padx=60, pady=(10, 30))
        self.lbl_status = tk.Label(rodape, text="", font=(FAMILIA, 22, "bold"), fg=COR_BRANCO, bg=COR_FUNDO)
        self.lbl_status.pack(side="left")

        BotaoFuturista(rodape, "SAIR DA PARTIDA", self._abandonar_partida, largura=220, altura=50, cor_borda=COR_VERMELHO).pack(side="right")

        self.btn_repetir = BotaoFuturista(self.canvas_jogo, "TENTAR NOVAMENTE", self._repetir_rodada, largura=300, altura=60, cor_borda=COR_AMARELO)

    def define_status(self, texto, cor): self.lbl_status.config(text=texto, fg=cor)

    def draw_text(self, texto, cor, tamanho, dy):
        self.canvas_jogo.update_idletasks() # Garante que o tamanho do canvas foi calculado
        w = self.canvas_jogo.winfo_width()
        h = self.canvas_jogo.winfo_height()
        self.canvas_jogo.create_text(w/2, h/2 + dy, text=texto, fill=cor, font=(FAMILIA, tamanho, "bold"))
