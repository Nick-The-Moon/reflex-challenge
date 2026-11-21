import tkinter as tk
from .base_screen import ScreenComponent
from .theme import (
    COR_BRANCO, COR_CINZA, COR_FUNDO, COR_NEON, COR_PAINEL, COR_VERDE_ESCURO, FAMILIA, TABELA_CURIOSIDADES,
)
from .futuristic_button import BotaoFuturista
from .scrollable_table import TabelaComScroll

class FactsScreen(ScreenComponent):
    """Individually constructible facts screen."""

    def __init__(self, app):
        super().__init__(app)
        self.build()

    def build(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.register_screen("curiosidades", tela)
        
        # Fundo
        canvas_bg = tk.Canvas(tela, bg=COR_FUNDO, highlightthickness=0)
        canvas_bg.pack(fill="both", expand=True)
        canvas_bg.bind("<Configure>", lambda e: self.create_background(canvas_bg, "assets/fundo_padrao.png", "img_bg_curiosidades"))

        # Moldura Principal (ocupa 95% da tela inteira)
        box_principal = tk.Frame(tela, bg="#0A0A0E", highlightbackground=COR_NEON, highlightthickness=2, padx=30, pady=30)
        box_principal.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

        # Título
        frame_titulo = tk.Frame(box_principal, bg="#0A0A0E")
        frame_titulo.pack(fill="x", pady=(0, 20))
        tk.Label(frame_titulo, text="💡 CURIOSIDADES DO TEMPO DE REAÇÃO", font=(FAMILIA, 26, "bold"), fg=COR_BRANCO, bg="#0A0A0E").pack(side="left", padx=10)
        
        lbl_detalhe = tk.Frame(frame_titulo, bg=COR_NEON, height=4)
        lbl_detalhe.pack(side="left", fill="x", expand=True, padx=(20, 0))

        # Tabela (Agora com fill="both" e expand=True para ocupar todo o espaço restante)
        frame_tabela_scroll = TabelaComScroll(box_principal, bg="#0A0A0E")
        frame_tabela_scroll.pack(fill="both", expand=True, pady=(0, 20))

        tabela = frame_tabela_scroll.frame_interno
        # Ajuste dos pesos das colunas (a última coluna ficou bem maior)
        tabela.columnconfigure(0, weight=1, uniform="col")
        tabela.columnconfigure(1, weight=2, uniform="col")
        tabela.columnconfigure(2, weight=6, uniform="col")

        # Cabeçalho
        headers = ["Faixa de Tempo", "Nível / Criatura", "Fato Curioso e Engraçado"]
        for col, h in enumerate(headers):
            tk.Label(tabela, text=h, font=(FAMILIA, 15, "bold"), fg=COR_NEON, bg=COR_VERDE_ESCURO, pady=15).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        # Linhas
        for i, (tempo, nivel, fato) in enumerate(TABELA_CURIOSIDADES, start=1):
            # Aumentei o wraplength de 550 para 1000 para o texto espalhar mais na horizontal
            tk.Label(tabela, text=tempo, font=(FAMILIA, 14, "bold"), fg=COR_NEON, bg=COR_PAINEL, pady=12, padx=10).grid(row=i, column=0, sticky="nsew", padx=1, pady=1)
            tk.Label(tabela, text=nivel, font=(FAMILIA, 13, "bold"), fg=COR_BRANCO, bg=COR_PAINEL, pady=12, padx=10, wraplength=300).grid(row=i, column=1, sticky="nsew", padx=1, pady=1)
            tk.Label(tabela, text=fato, font=(FAMILIA, 12), fg=COR_CINZA, bg=COR_PAINEL, pady=12, padx=15, wraplength=1000, justify="left").grid(row=i, column=2, sticky="nsew", padx=1, pady=1)

        # Botão
        BotaoFuturista(box_principal, "<< VOLTAR AO MENU >>", self._ir_para_menu, largura=300, altura=55).pack()
