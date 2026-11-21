# -*- coding: utf-8 -*-
import random
import time
import tkinter as tk
from tkinter import messagebox
import math
import os
from PIL import Image, ImageTk
from tkinter import ttk

DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))

# =================================================================== #
#  PALETA DE CORES E FONTES                                           #
# =================================================================== #
COR_FUNDO          = "#0A0A0E"
COR_PAINEL         = "#12121A"
COR_NEON           = "#39FF88"
COR_NEON_HOVER     = "#8AFFBB"
COR_VERDE_ESCURO   = "#123D2A"
COR_BRANCO         = "#FFFFFF"
COR_CINZA          = "#A0A0A0"
COR_CINZA_ESCURO   = "#555555"
COR_VERMELHO       = "#FF4545"
COR_AMARELO        = "#FFD447"

FAMILIA = "Segoe UI"

TOTAL_RODADAS     = 5
ATRASO_MIN_MS     = 1000
ATRASO_MAX_MS     = 5000
RAIO_MEDIO        = 70
RAIO_DIFICIL      = 22
PAUSA_RODADA_MS   = 1300

NOMES_NIVEIS = {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}

TABELA_CURIOSIDADES = [
    ("1000 ms ou mais", "Bicho-preguiça", "Você demorou mais de um segundo inteiro. Nesse tempo, uma preguiça já teria bocejado e decidido se mexer."),
    ("500 ms – 599 ms", "Tartaruga / Internet Discada", "Seu cérebro ainda está carregando a página. Ótimo para relaxar, péssimo para desviar de bolas de queimada."),
    ("300 ms – 499 ms", "Humano com Sono", "Você reagiu mais devagar do que o tempo necessário para um humano piscar os olhos."),
    ("215 ms – 299 ms", "Ser Humano Comum", "A média global. Você está no padrão, mas perde uma briga de tapas para um gato."),
    ("160 ms – 214 ms", "Gamer / Motorista Atento", "Seus dedos têm memória muscular. Você freia o carro antes do susto passar."),
    ("120 ms – 159 ms", "Pro-Player / Piloto F1", "Reflexos de elite. Você clicou antes da maioria perceber a mudança."),
    ("100 ms – 119 ms", "Velocista (Limite Humano)", "No atletismo, menos de 100 ms é considerado queima de largada."),
    ("70 ms – 99 ms", "Cachorro / Pombo", "Pombos enxergam em 'câmera lenta'. Escapam dos carros no último segundo."),
    ("40 ms – 69 ms", "Cobra / Gato Doméstico", "Bote de víbora e agilidade felina. Gatos são 10x mais rápidos que humanos."),
    ("15 ms – 39 ms", "Mosca Doméstica", "Por isso é difícil acertar uma mosca. Sua mão parece em câmera lenta."),
    ("8 ms – 14 ms", "Toupeira-estrelada", "Recorde dos mamíferos. Identifica e come a presa antes de um piscar."),
    ("Menos de 8 ms", "Trapaça ou Sorte Pura", "Impossível para humanos. Você adivinhou ou usou um robô.")
]

# =================================================================== #
#  COMPONENTES CUSTOMIZADOS                                           #
# =================================================================== #
class BotaoFuturista(tk.Canvas):
    def __init__(self, mestre, texto, comando, largura=300, altura=50,
                 cor_texto=COR_BRANCO, cor_borda=COR_NEON, bg_cor="#0A0A0E"):
        # bg_cor="#0A0A0E" (fundo escuro) para fingir transparência
        super().__init__(mestre, width=largura, height=altura, bg=bg_cor,
                         highlightthickness=0, bd=0, cursor="hand2")
        self._comando = comando
        self._bg_cor = bg_cor
        
        corte = 15
        self.pontos = [corte, 0, largura, 0, largura - corte, altura, 0, altura, corte, 0]
        self.id_borda = self.create_polygon(self.pontos, fill="", outline=cor_borda, width=2)
        # Fundo interno
        self.id_fundo = self.create_polygon([corte+2, 2, largura-2, 2, largura-corte-2, altura-2, 2, altura-2], fill=bg_cor, outline="")
        self.create_text(largura/2, altura/2, text=texto, fill=cor_texto, font=(FAMILIA, 14, "bold"))

        self.bind("<Enter>", lambda e: self.itemconfig(self.id_fundo, fill=COR_VERDE_ESCURO))
        self.bind("<Leave>", lambda e: self.itemconfig(self.id_fundo, fill=self._bg_cor))
        self.bind("<Button-1>", lambda e: self._comando() if callable(self._comando) else None)

class TabelaComScroll(tk.Frame):
    def __init__(self, mestre, bg="#0A0A0E"):
        super().__init__(mestre, bg=bg)

        # Estilizando a barra de rolagem nativa para ficar com tema Neon
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Neon.Vertical.TScrollbar",
                        background=COR_NEON,
                        troughcolor=COR_FUNDO,
                        bordercolor=COR_FUNDO,
                        arrowcolor=COR_BRANCO,
                        lightcolor=COR_NEON,
                        darkcolor=COR_NEON)

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview, style="Neon.Vertical.TScrollbar")
        self.frame_interno = tk.Frame(self.canvas, bg=bg)

        self.frame_interno.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_interno, anchor="nw")
        
        # Faz o frame interno acompanhar a largura do canvas
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units") if self.canvas.winfo_exists() else None)

# =================================================================== #
#  CLASSE PRINCIPAL                                                   #
# =================================================================== #
class ReflexChallenge:
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

        self.telas = {}
        self._criar_telas()
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

    # --- CARREGAMENTO E REDIMENSIONAMENTO DA IMAGEM DE FUNDO ---
    def _renderizar_bg(self, canvas, caminho_img, ref_attr):
        try:
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            if w <= 1 or h <= 1: return
            
            # A MÁGICA ACONTECE AQUI: Ele monta o caminho absoluto
            caminho_completo = os.path.join(DIRETORIO_BASE, caminho_img)
            
            img_pil = Image.open(caminho_completo)
            img_pil = img_pil.resize((w, h), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_pil)
            
            canvas.delete("bg")
            canvas.create_image(0, 0, image=img_tk, anchor="nw", tags="bg")
            setattr(self, ref_attr, img_tk)
        except Exception as e:
            print(f"Erro ao carregar imagem {caminho_img}: {e}")

    # =============================================================== #
    #  CRIAÇÃO DAS TELAS                                              #
    # =============================================================== #
    def _criar_telas(self):
        self._criar_tela_menu()
        self._criar_tela_nome()
        self._criar_tela_dificuldade()
        self._criar_tela_jogo()
        self._criar_tela_resultados()
        self._criar_tela_ranking()
        self._criar_tela_curiosidades()
        self._criar_tela_como_jogar()

    def _criar_tela_menu(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.telas["menu"] = tela

        canvas_bg = tk.Canvas(tela, bg=COR_FUNDO, highlightthickness=0)
        canvas_bg.pack(fill="both", expand=True)
        canvas_bg.bind("<Configure>", lambda e: self._renderizar_bg(canvas_bg, "assets/fundo_menu.png", "img_bg_menu"))

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

    def _criar_tela_como_jogar(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.telas["como_jogar"] = tela

        canvas_bg = tk.Canvas(tela, bg=COR_FUNDO, highlightthickness=0)
        canvas_bg.pack(fill="both", expand=True)
        canvas_bg.bind("<Configure>", lambda e: self._renderizar_bg(canvas_bg, "assets/como_jogar.png", "img_bg_como_jogar"))

        frame_btn = tk.Frame(tela, bg="#0A0A0E")
        frame_btn.place(relx=0.5, rely=0.92, anchor="center")
        BotaoFuturista(frame_btn, "VOLTAR AO MENU", self._ir_para_menu, largura=280, altura=55).pack()

    def _criar_tela_nome(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.telas["nome"] = tela
        centro = tk.Frame(tela, bg=COR_FUNDO)
        centro.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(centro, text="QUEM ESTÁ JOGANDO?", font=(FAMILIA, 32, "bold"), fg=COR_NEON, bg=COR_FUNDO).pack(pady=(0, 10))
        self.entry_nome = tk.Entry(centro, font=(FAMILIA, 24), bg=COR_PAINEL, fg=COR_BRANCO, insertbackground=COR_NEON, width=20, justify="center", relief="flat", highlightthickness=2, highlightbackground=COR_NEON)
        self.entry_nome.pack(pady=20, ipady=10)
        self.entry_nome.bind("<Return>", lambda e: self._confirmar_nome())

        BotaoFuturista(centro, "CONFIRMAR E JOGAR", self._confirmar_nome, largura=320, altura=60).pack(pady=15)
        BotaoFuturista(centro, "VOLTAR", self._ir_para_menu, largura=320, altura=50, cor_borda=COR_CINZA).pack()

    def _criar_tela_dificuldade(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.telas["dificuldade"] = tela
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

    def _criar_tela_jogo(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.telas["jogo"] = tela
        
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

    def _criar_tela_resultados(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.telas["resultados"] = tela
        self.frame_res_conteudo = tk.Frame(tela, bg=COR_FUNDO)
        self.frame_res_conteudo.place(relx=0.5, rely=0.5, anchor="center")

    def _criar_tela_ranking(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.telas["ranking"] = tela
        
        # 1. Fundo
        canvas_bg = tk.Canvas(tela, bg=COR_FUNDO, highlightthickness=0)
        canvas_bg.pack(fill="both", expand=True)
        canvas_bg.bind("<Configure>", lambda e: self._renderizar_bg(canvas_bg, "assets/fundo_padrao.png", "img_bg_ranking"))

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

        # 4. Tabela com Scroll (criada vazia, será preenchida no _atualizar_tabela_ranking)
        frame_tabela_scroll = TabelaComScroll(box_principal, bg="#0A0A0E")
        frame_tabela_scroll.pack(fill="both", expand=True, pady=(0, 20))
        
        self.frame_tabela_ranking = frame_tabela_scroll.frame_interno
        self.frame_tabela_ranking.bg_color = "#0A0A0E" # Guarda a referência da cor de fundo

        # 5. Botão Voltar
        BotaoFuturista(box_principal, "<< VOLTAR AO MENU >>", self._ir_para_menu, largura=300, altura=55).pack()

    def _criar_tela_curiosidades(self):
        tela = tk.Frame(self.container, bg=COR_FUNDO)
        self.telas["curiosidades"] = tela
        
        # Fundo
        canvas_bg = tk.Canvas(tela, bg=COR_FUNDO, highlightthickness=0)
        canvas_bg.pack(fill="both", expand=True)
        canvas_bg.bind("<Configure>", lambda e: self._renderizar_bg(canvas_bg, "assets/fundo_padrao.png", "img_bg_curiosidades"))

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
        self._atualizar_tabela_ranking()
        self._mostrar_tela("ranking")
    
    def _ir_para_curiosidades(self): self._mostrar_tela("curiosidades")
    def _ir_para_como_jogar(self): self._mostrar_tela("como_jogar")

    def _atualizar_tabela_ranking(self):
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

    def iniciar_partida(self, nivel):
        self.dificuldade, self.tempos, self.rodada_atual, self.alvo, self.inicio_estimulo = nivel, [], 0, None, 0.0
        self._mostrar_tela("jogo")
        self._avancar_rodada()

    def _avancar_rodada(self):
        self.rodada_atual += 1
        if self.rodada_atual > TOTAL_RODADAS: self._exibir_resultados()
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
            self._texto_no_canvas("AGUARDE...", COR_BRANCO, 50, 0)
            self._definir_status("Aguarde o verde aparecer...", COR_BRANCO)
        else:
            self.canvas_jogo.configure(bg=COR_PAINEL)
            self._texto_no_canvas("AGUARDE...", COR_CINZA, 40, 0)
            self._definir_status("O alvo vai aparecer. Não clique antes!", COR_CINZA)

        self._agendar(random.randint(ATRASO_MIN_MS, ATRASO_MAX_MS), self._mostrar_estimulo)

    def _mostrar_estimulo(self):
        if self.estado != "espera": return
        self.estado = "estimulo"
        if self.dificuldade == "facil":
            self.canvas_jogo.delete("all")
            self.canvas_jogo.configure(bg=COR_NEON)
            self._definir_status("CLIQUE AGORA!", COR_NEON)
        else:
            self._desenhar_alvo()
            self._definir_status("CLIQUE NO ALVO!", COR_NEON)
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
        self._definir_status("Fora do alvo! Continue tentando.", COR_VERMELHO)
        self.raiz.after(600, lambda: self._definir_status("CLIQUE NO ALVO!", COR_NEON) if self.estado == "estimulo" else None)

    def _registrar_tempo(self):
        t = (time.perf_counter() - self.inicio_estimulo) * 1000.0
        self.estado = "resultado"
        self.tempos.append(t)
        self.canvas_jogo.delete("all")
        self.canvas_jogo.configure(bg=COR_VERDE_ESCURO)
        self._texto_no_canvas(f"{t:.0f} ms", COR_NEON, 70, -20)
        self._texto_no_canvas(f"Rodada {self.rodada_atual} de {TOTAL_RODADAS}", COR_BRANCO, 20, 50)
        self._definir_status(f"{t:.0f} ms", COR_AMARELO)
        self._agendar(PAUSA_RODADA_MS, self._avancar_rodada)

    def _registrar_falso_inicio(self):
        self._cancelar_eventos()
        self.estado = "falso_inicio"
        self.canvas_jogo.delete("all")
        self.canvas_jogo.configure(bg=COR_VERMELHO)
        self._texto_no_canvas("FALSO INÍCIO!", COR_BRANCO, 55, -50)
        self._texto_no_canvas("Você clicou antes da hora.", COR_BRANCO, 20, 10)
        self._definir_status("Rodada não contabilizada.", COR_AMARELO)
        self.btn_repetir.place(relx=0.5, rely=0.70, anchor="center")

    def _exibir_resultados(self):
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

    def _definir_status(self, texto, cor): self.lbl_status.config(text=texto, fg=cor)
    
    def _texto_no_canvas(self, texto, cor, tamanho, dy):
        self.canvas_jogo.update_idletasks() # Garante que o tamanho do canvas foi calculado
        w = self.canvas_jogo.winfo_width()
        h = self.canvas_jogo.winfo_height()
        self.canvas_jogo.create_text(w/2, h/2 + dy, text=texto, fill=cor, font=(FAMILIA, tamanho, "bold"))

if __name__ == "__main__":
    raiz = tk.Tk()
    ReflexChallenge(raiz)
    raiz.mainloop()