import tkinter as tk
from .base_screen import ScreenComponent
from .theme import (
    COR_AMARELO, COR_BRANCO, COR_CINZA, COR_FUNDO, COR_NEON, COR_PAINEL, COR_VERDE_ESCURO, COR_VERMELHO, FAMILIA, NOMES_NIVEIS,
)
from .futuristic_button import BotaoFuturista

class ResultsScreen(ScreenComponent):
    """Individually constructible results screen."""

    def __init__(self, app):
        super().__init__(app)
        self.build()

    def build(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.register_screen("resultados", tela)
        self.frame_res_conteudo = tk.Frame(tela, bg=COR_FUNDO)
        self.frame_res_conteudo.place(relx=0.5, rely=0.5, anchor="center")

    def show_results(self):
        self.banco_dados[self.usuario_atual][self.dificuldade] = self.tempos[:]
        self._mostrar_tela("resultados")
        for f in self.frame_res_conteudo.winfo_children(): f.destroy()

        media, melhor, pior = sum(self.tempos)/len(self.tempos), min(self.tempos), max(self.tempos)
        
        if media <= 200: classif, cor_c = "REFLEXO INSANO!", COR_NEON
        elif media <= 300: classif, cor_c = "REFLEXO DE ELITE!", COR_NEON
        elif media <= 450: classif, cor_c = "MUITO BOM!", COR_AMARELO
        elif media <= 600: classif, cor_c = "EVOLUINDO!", COR_AMARELO
        else: classif, cor_c = "TREINE MAIS!", COR_VERMELHO

        tk.Label(self.frame_res_conteudo, text=f"NÍVEL {NOMES_NIVEIS[self.dificuldade].upper()}", font=(FAMILIA, 16, "bold"), fg=COR_CINZA, bg=COR_FUNDO).pack()
        tk.Label(self.frame_res_conteudo, text=classif, font=(FAMILIA, 40, "bold"), fg=cor_c, bg=COR_FUNDO).pack(pady=(4, 25))

        linha_info = tk.Frame(self.frame_res_conteudo, bg=COR_FUNDO)
        linha_info.pack(pady=(0, 20))
        
        for titulo, valor, cor in [("MÉDIA", f"{media:.0f} ms", COR_NEON), ("MELHOR", f"{melhor:.0f} ms", COR_AMARELO), ("PIOR", f"{pior:.0f} ms", COR_VERMELHO)]:
            c = tk.Frame(linha_info, bg=COR_PAINEL, highlightbackground=cor, highlightthickness=2, padx=40, pady=20)
            c.pack(side="left", padx=15)
            tk.Label(c, text=titulo, font=(FAMILIA, 12, "bold"), fg=COR_CINZA, bg=COR_PAINEL).pack()
            tk.Label(c, text=valor, font=(FAMILIA, 32, "bold"), fg=cor, bg=COR_PAINEL).pack()

        linha_rodadas = tk.Frame(self.frame_res_conteudo, bg=COR_FUNDO)
        linha_rodadas.pack(pady=(0, 30))
        for i, t in enumerate(self.tempos, 1):
            c = tk.Frame(linha_rodadas, bg=COR_PAINEL, highlightbackground=COR_VERDE_ESCURO, highlightthickness=2, padx=15, pady=10)
            c.pack(side="left", padx=8)
            tk.Label(c, text=f"R{i}", font=(FAMILIA, 10, "bold"), fg=COR_CINZA, bg=COR_PAINEL).pack()
            tk.Label(c, text=f"{t:.0f} ms", font=(FAMILIA, 16, "bold"), fg=COR_BRANCO, bg=COR_PAINEL).pack()

        linha_botoes = tk.Frame(self.frame_res_conteudo, bg=COR_FUNDO)
        linha_botoes.pack(pady=(10, 0))

        prox = "medio" if self.dificuldade == "facil" else ("dificil" if self.dificuldade == "medio" else None)
        if prox:
            BotaoFuturista(linha_botoes, f"IR PARA NÍVEL {NOMES_NIVEIS[prox].upper()}", lambda: self.iniciar_partida(prox), largura=320, altura=60).pack(side="left", padx=10)

        BotaoFuturista(linha_botoes, "JOGAR NOVAMENTE", lambda: self.iniciar_partida(self.dificuldade), largura=220, altura=56, cor_borda=COR_CINZA).pack(side="left", padx=10)
        BotaoFuturista(linha_botoes, "VER RANKING", self._ir_para_ranking, largura=220, altura=56, cor_borda=COR_AMARELO).pack(side="left", padx=10)
        
        tk.Label(self.frame_res_conteudo, text="Classificação recreativa. Não é avaliação médica.", font=(FAMILIA, 11), fg=COR_CINZA, bg=COR_FUNDO).pack(pady=(25, 0))
