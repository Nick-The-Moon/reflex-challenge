import tkinter as tk
from .base_screen import ScreenComponent
from .theme import (
    COR_BRANCO, COR_FUNDO, COR_VERDE_ESCURO, COR_VERMELHO,
)
from .futuristic_button import BotaoFuturista

class MenuScreen(ScreenComponent):
    """Individually constructible menu screen."""

    def __init__(self, app):
        super().__init__(app)
        self.build()

    def build(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.register_screen("menu", tela)

        canvas_bg = tk.Canvas(tela, bg=COR_FUNDO, highlightthickness=0)
        canvas_bg.pack(fill="both", expand=True)
        canvas_bg.bind("<Configure>", lambda e: self.create_background(canvas_bg, "assets/fundo_menu.png", "img_bg_menu"))

        # Frame de botões TOTALMENTE CENTRALIZADO (relx=0.5, rely=0.5)
        frame_botoes = tk.Frame(tela, bg="#0A0A0E")
        frame_botoes.place(relx=0.5, rely=0.75, anchor="center")

        # Caixa invisível (fundo mesclado) para agrupar botões e dar contraste
        box = tk.Frame(frame_botoes, bg="#0A0A0E", padx=20, pady=20, highlightbackground=COR_VERDE_ESCURO, highlightthickness=1)
        box.pack()

        BotaoFuturista(box, "▶ JOGAR AGORA", self._ir_para_nome, largura=320, altura=60).pack(pady=8)
        BotaoFuturista(box, "🏆 RANKING TEMPORÁRIO", self._ir_para_ranking, largura=320, altura=50, cor_borda=COR_BRANCO).pack(pady=8)
        BotaoFuturista(box, "💡 CURIOSIDADES", self._ir_para_curiosidades, largura=320, altura=50, cor_borda=COR_BRANCO).pack(pady=8)
        BotaoFuturista(box, "⚙ COMO JOGAR", self._ir_para_como_jogar, largura=320, altura=50, cor_borda=COR_BRANCO).pack(pady=8)
        BotaoFuturista(box, "🚪 SAIR", self.raiz.destroy, largura=320, altura=50, cor_borda=COR_VERMELHO).pack(pady=8)
