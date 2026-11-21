# -*- coding: utf-8 -*-
import math
import random
import time
import tkinter as tk
from tkinter import messagebox

from src.components import (
    DifficultyScreen,
    FactsScreen,
    GameScreen,
    HowToPlayScreen,
    MenuScreen,
    NameScreen,
    RankingScreen,
    ResultsScreen,
)
from src.components.theme import (
    ATRASO_MAX_MS,
    ATRASO_MIN_MS,
    COR_AMARELO,
    COR_BRANCO,
    COR_CINZA,
    COR_FUNDO,
    COR_NEON,
    COR_PAINEL,
    COR_VERDE_ESCURO,
    COR_VERMELHO,
    NOMES_NIVEIS,
    PAUSA_RODADA_MS,
    RAIO_DIFICIL,
    RAIO_MEDIO,
    TOTAL_RODADAS,
)


class ReflexChallenge:
    """Owns game state, input handlers, and navigation between screens."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("REFLEX CHALLENGE")
        self.raiz.geometry("1920x1080")
        self.raiz.configure(bg=COR_FUNDO)

        
        try: self.raiz.state('zoomed')
        except: pass

        self.raiz.bind("<F11>", self._alternar_tela_cheia)
        self.raiz.bind("<Escape>", self._sair_tela_cheia)
        
        self.banco_dados = {}
        self.usuario_atual = ""
        self.dificuldade = "facil"
        self.rodada_atual = 0
        self.tempos = []
        self.estado = "menu"
        self.alvo = None
        self.inicio_estimulo = 0.0
        self.eventos_agendados = []

        self.img_bg_menu = None
        self.img_bg_como_jogar = None
        self.img_bg_curiosidades = None
        self.img_bg_ranking = None

        self.container = tk.Frame(self.raiz, bg=COR_FUNDO)
        self.container.pack(fill="both", expand=True)

        # Screens register their frames and expose the widgets used by gameplay.
        self.telas = {}
        self.components = {
            "menu": MenuScreen(self),
            "nome": NameScreen(self),
            "dificuldade": DifficultyScreen(self),
            "jogo": GameScreen(self),
            "resultados": ResultsScreen(self),
            "ranking": RankingScreen(self),
            "curiosidades": FactsScreen(self),
            "como_jogar": HowToPlayScreen(self),
        }
        self._mostrar_tela("menu")

    def _alternar_tela_cheia(self, _=None):
        em_tela_cheia = self.raiz.attributes("-fullscreen")
        self.raiz.attributes("-fullscreen", not em_tela_cheia)

    def _sair_tela_cheia(self, _=None):
        self.raiz.attributes("-fullscreen", False)

    def _agendar(self, atraso_ms, funcao):
        id_ev = self.raiz.after(atraso_ms, funcao)
        self.eventos_agendados.append(id_ev)
        return id_ev

    def _cancelar_eventos(self):
        for id_ev in self.eventos_agendados:
            try: self.raiz.after_cancel(id_ev)
            except tk.TclError: pass
        self.eventos_agendados.clear()

    def _mostrar_tela(self, nome):
        self._cancelar_eventos()
        for tela in self.telas.values():
            tela.pack_forget()
        self.telas[nome].pack(fill="both", expand=True)
        # update_idletasks força o Tkinter a calcular o layout antes de desenhar
        self.raiz.update_idletasks()

    # =============================================================== #
    #  NAVEGAÇÃO E LÓGICA                                             #
    # =============================================================== #
    def _ir_para_menu(self): self._mostrar_tela("menu")
    
    def _ir_para_nome(self):
        self.entry_nome.delete(0, tk.END)
        if self.usuario_atual: self.entry_nome.insert(0, self.usuario_atual)
        self._mostrar_tela("nome")
        self.entry_nome.focus_set()
    
    def _confirmar_nome(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite um nome para jogar.")
            return
        self.usuario_atual = nome
        if nome not in self.banco_dados: self.banco_dados[nome] = {"facil": [], "medio": [], "dificil": []}
        self.lbl_dificuldade_nome.config(text=f"JOGADOR: {self.usuario_atual.upper()}")
        self._mostrar_tela("dificuldade")

    def _ir_para_ranking(self): 
        self.components["ranking"].update_ranking_table()
        self._mostrar_tela("ranking")
    
    def _ir_para_curiosidades(self): self._mostrar_tela("curiosidades")
    def _ir_para_como_jogar(self): self._mostrar_tela("como_jogar")

    def iniciar_partida(self, nivel):
        self.dificuldade, self.tempos, self.rodada_atual, self.alvo, self.inicio_estimulo = nivel, [], 0, None, 0.0
        self._mostrar_tela("jogo")
        self._avancar_rodada()

    def _avancar_rodada(self):
        self.rodada_atual += 1
        if self.rodada_atual > TOTAL_RODADAS:
            self.components["resultados"].show_results()
        else: self._iniciar_rodada()

    def _repetir_rodada(self):
        self.btn_repetir.place_forget()
        self._iniciar_rodada()

    def _abandonar_partida(self):
        self._cancelar_eventos()
        self._mostrar_tela("dificuldade")

    def _iniciar_rodada(self):
        self._cancelar_eventos()
        self.estado, self.alvo, self.inicio_estimulo = "espera", None, 0.0
        self.btn_repetir.place_forget()
        self.lbl_nivel.config(text=f"NÍVEL: {NOMES_NIVEIS[self.dificuldade].upper()}")
        self.lbl_rodada.config(text=f"RODADA {self.rodada_atual} / {TOTAL_RODADAS}")

        self.canvas_jogo.delete("all")
        if self.dificuldade == "facil":
            self.canvas_jogo.configure(bg=COR_VERMELHO)
            self.components["jogo"].draw_text("AGUARDE...", COR_BRANCO, 50, 0)
            self.components["jogo"].define_status("Aguarde o verde aparecer...", COR_BRANCO)
        else:
            self.canvas_jogo.configure(bg=COR_PAINEL)
            self.components["jogo"].draw_text("AGUARDE...", COR_CINZA, 40, 0)
            self.components["jogo"].define_status("O alvo vai aparecer. Não clique antes!", COR_CINZA)

        self._agendar(random.randint(ATRASO_MIN_MS, ATRASO_MAX_MS), self._mostrar_estimulo)

    def _mostrar_estimulo(self):
        if self.estado != "espera": return
        self.estado = "estimulo"
        if self.dificuldade == "facil":
            self.canvas_jogo.delete("all")
            self.canvas_jogo.configure(bg=COR_NEON)
            self.components["jogo"].define_status("CLIQUE AGORA!", COR_NEON)
        else:
            self._desenhar_alvo()
            self.components["jogo"].define_status("CLIQUE NO ALVO!", COR_NEON)
        self.raiz.update_idletasks()
        self.inicio_estimulo = time.perf_counter()

    def _desenhar_alvo(self):
        self.canvas_jogo.delete("all")
        self.canvas_jogo.configure(bg=COR_PAINEL)
        w, h = self.canvas_jogo.winfo_width(), self.canvas_jogo.winfo_height()
        if w <= 1: w, h = 1000, 420
        r = RAIO_MEDIO if self.dificuldade == "medio" else RAIO_DIFICIL
        margem = r + 20
        x = random.randint(margem, max(margem, w - margem))
        y = random.randint(margem, max(margem, h - margem))
        self.alvo = (x, y, r)
        self.canvas_jogo.create_oval(x-r-10, y-r-10, x+r+10, y+r+10, outline=COR_VERDE_ESCURO, width=3)
        self.canvas_jogo.create_oval(x-r, y-r, x+r, y+r, fill=COR_NEON, outline=COR_BRANCO, width=2)

    def _ao_clicar_area(self, e):
        if self.estado == "espera": self._registrar_falso_inicio()
        elif self.estado == "estimulo":
            if self.dificuldade == "facil": self._registrar_tempo()
            else:
                if self.alvo:
                    x, y, r = self.alvo
                    if math.hypot(e.x - x, e.y - y) <= r: self._registrar_tempo()
                    else: self._feedback_erro(e.x, e.y)

    def _feedback_erro(self, x, y):
        m1 = self.canvas_jogo.create_line(x-15, y-15, x+15, y+15, fill=COR_VERMELHO, width=4)
        m2 = self.canvas_jogo.create_line(x-15, y+15, x+15, y-15, fill=COR_VERMELHO, width=4)
        self.raiz.after(200, lambda: [self.canvas_jogo.delete(m1), self.canvas_jogo.delete(m2)])
        game_screen = self.components["jogo"]
        game_screen.define_status("Fora do alvo! Continue tentando.", COR_VERMELHO)
        self.raiz.after(
            600,
            lambda: game_screen.define_status("CLIQUE NO ALVO!", COR_NEON)
            if self.estado == "estimulo"
            else None,
        )

    def _registrar_tempo(self):
        t = (time.perf_counter() - self.inicio_estimulo) * 1000.0
        self.estado = "resultado"
        self.tempos.append(t)
        self.canvas_jogo.delete("all")
        self.canvas_jogo.configure(bg=COR_VERDE_ESCURO)
        game_screen = self.components["jogo"]
        game_screen.draw_text(f"{t:.0f} ms", COR_NEON, 70, -20)
        game_screen.draw_text(
            f"Rodada {self.rodada_atual} de {TOTAL_RODADAS}", COR_BRANCO, 20, 50
        )
        game_screen.define_status(f"{t:.0f} ms", COR_AMARELO)
        self._agendar(PAUSA_RODADA_MS, self._avancar_rodada)

    def _registrar_falso_inicio(self):
        self._cancelar_eventos()
        self.estado = "falso_inicio"
        self.canvas_jogo.delete("all")
        self.canvas_jogo.configure(bg=COR_VERMELHO)
        game_screen = self.components["jogo"]
        game_screen.draw_text("FALSO INÍCIO!", COR_BRANCO, 55, -50)
        game_screen.draw_text("Você clicou antes da hora.", COR_BRANCO, 20, 10)
        game_screen.define_status("Rodada não contabilizada.", COR_AMARELO)
        self.btn_repetir.place(relx=0.5, rely=0.70, anchor="center")