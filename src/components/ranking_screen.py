import tkinter as tk
from .base_screen import ScreenComponent
from .theme import (
    COR_AMARELO, COR_BRANCO, COR_CINZA, COR_CINZA_ESCURO, COR_FUNDO, COR_NEON, COR_PAINEL, COR_VERDE_ESCURO, FAMILIA,
)
from .futuristic_button import BotaoFuturista
from .scrollable_table import TabelaComScroll

class RankingScreen(ScreenComponent):
    """Individually constructible ranking screen."""

    def __init__(self, app):
        super().__init__(app)
        self.build()

    def build(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.register_screen("ranking", tela)
        
        # 1. Fundo
        canvas_bg = tk.Canvas(tela, bg=COR_FUNDO, highlightthickness=0)
        canvas_bg.pack(fill="both", expand=True)
        canvas_bg.bind("<Configure>", lambda e: self.create_background(canvas_bg, "assets/fundo_padrao.png", "img_bg_ranking"))

        # 2. Moldura Principal (ocupando 95% da tela)
        box_principal = tk.Frame(tela, bg="#0A0A0E", highlightbackground=COR_NEON, highlightthickness=2, padx=20, pady=20)
        box_principal.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.90, anchor="center")

        # 3. Título
        frame_titulo = tk.Frame(box_principal, bg="#0A0A0E")
        frame_titulo.pack(fill="x", pady=(0, 15))
        tk.Label(frame_titulo, text="🏆 RANKING DA SESSÃO", font=(FAMILIA, 26, "bold"), fg=COR_NEON, bg="#0A0A0E").pack(side="left", padx=10)
        tk.Label(frame_titulo, text="Os dados são apagados ao fechar o programa.", font=(FAMILIA, 12), fg=COR_CINZA, bg="#0A0A0E").pack(side="left", padx=20, pady=10)
        
        lbl_detalhe = tk.Frame(frame_titulo, bg=COR_NEON, height=4)
        lbl_detalhe.pack(side="left", fill="x", expand=True, padx=(20, 0))

        # 4. Tabela com Scroll (criada vazia, será preenchida no update_ranking_table)
        frame_tabela_scroll = TabelaComScroll(box_principal, bg="#0A0A0E")
        frame_tabela_scroll.pack(fill="both", expand=True, pady=(0, 20))
        
        self.frame_tabela_ranking = frame_tabela_scroll.frame_interno
        self.frame_tabela_ranking.bg_color = "#0A0A0E" # Guarda a referência da cor de fundo

        # 5. Botão Voltar
        BotaoFuturista(box_principal, "<< VOLTAR AO MENU >>", self._ir_para_menu, largura=300, altura=55).pack()

    def update_ranking_table(self):
        # Limpa a tabela antes de desenhar
        for widget in self.frame_tabela_ranking.winfo_children(): 
            widget.destroy()

        if not self.banco_dados:
            tk.Label(self.frame_tabela_ranking, text="Ninguém jogou ainda. Seja o primeiro!", font=(FAMILIA, 16, "bold"), fg=COR_CINZA, bg="#0A0A0E").grid(row=0, column=0, padx=30, pady=50)
            return

        # Configuração das colunas (Nome, Fácil, Médio, Difícil) + Posição
        self.frame_tabela_ranking.columnconfigure(0, weight=1, uniform="col") # Posição
        self.frame_tabela_ranking.columnconfigure(1, weight=3, uniform="col") # Nome
        self.frame_tabela_ranking.columnconfigure(2, weight=2, uniform="col") # Fácil
        self.frame_tabela_ranking.columnconfigure(3, weight=2, uniform="col") # Médio
        self.frame_tabela_ranking.columnconfigure(4, weight=2, uniform="col") # Difícil

        # Função auxiliar para calcular a média geral de um jogador (para ordenar)
        def media_geral(dados):
            medias = []
            for nivel in ["facil", "medio", "dificil"]:
                if dados[nivel]:
                    medias.append(sum(dados[nivel]) / len(dados[nivel]))
            if not medias: return float('inf')
            return sum(medias) / len(medias)

        # Ordena os jogadores pela média geral (quem tem a menor média fica em 1º)
        jogadores_ordenados = sorted(self.banco_dados.items(), key=lambda x: media_geral(x[1]))

        # Cabeçalho
        headers = ["POSIÇÃO", "NOME", "MÉDIA FÁCIL", "MÉDIA MÉDIO", "MÉDIA DIFÍCIL"]
        for col, h in enumerate(headers):
            tk.Label(self.frame_tabela_ranking, text=h, font=(FAMILIA, 15, "bold"), fg=COR_NEON, bg=COR_VERDE_ESCURO, pady=15).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        # Linhas de Dados
        for i, (nome, dados) in enumerate(jogadores_ordenados, start=1):
            # Define a cor de fundo baseada na posição (Pódio)
            if i == 1:
                bg_cor = "#2A2000" # Fundo dourado escuro
                fg_pos = COR_AMARELO
                medalha = "🥇 1º"
            elif i == 2:
                bg_cor = "#1C1C1C" # Fundo prateado escuro
                fg_pos = "#C0C0C0"
                medalha = "🥈 2º"
            elif i == 3:
                bg_cor = "#201008" # Fundo bronze escuro
                fg_pos = "#CD7F32"
                medalha = "🥉 3º"
            else:
                bg_cor = COR_PAINEL
                fg_pos = COR_CINZA
                medalha = f"{i}º"

            # Coluna 0: Posição (Medalha)
            tk.Label(self.frame_tabela_ranking, text=medalha, font=(FAMILIA, 16, "bold"), fg=fg_pos, bg=bg_cor, pady=12).grid(row=i, column=0, sticky="nsew", padx=1, pady=1)

            # Coluna 1: Nome
            tk.Label(self.frame_tabela_ranking, text=nome, font=(FAMILIA, 14, "bold"), fg=COR_BRANCO, bg=bg_cor, pady=12).grid(row=i, column=1, sticky="nsew", padx=1, pady=1)

            # Colunas 2, 3 e 4: Médias
            for j, nv in enumerate(["facil", "medio", "dificil"], start=2):
                t = dados[nv]
                txt = f"{sum(t)/len(t):.0f} ms" if t else "-"
                # Cor do texto se tiver jogado
                cor_txt = COR_NEON if t else COR_CINZA_ESCURO
                tk.Label(self.frame_tabela_ranking, text=txt, font=(FAMILIA, 14), fg=cor_txt, bg=bg_cor, pady=12).grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
