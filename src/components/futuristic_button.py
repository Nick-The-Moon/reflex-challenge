"""Reusable neon-styled Tkinter button."""

import tkinter as tk

from .theme import COR_BRANCO, COR_NEON, COR_VERDE_ESCURO, FAMILIA


class BotaoFuturista(tk.Canvas):
    """Canvas button with an optional callback and configurable styling."""

    def __init__(
        self,
        mestre,
        texto,
        comando,
        largura=300,
        altura=50,
        cor_texto=COR_BRANCO,
        cor_borda=COR_NEON,
        bg_cor="#0A0A0E",
    ):
        super().__init__(
            mestre,
            width=largura,
            height=altura,
            bg=bg_cor,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self._comando = comando
        self._bg_cor = bg_cor

        corte = 15
        self.pontos = [
            corte,
            0,
            largura,
            0,
            largura - corte,
            altura,
            0,
            altura,
            corte,
            0,
        ]
        self.id_borda = self.create_polygon(
            self.pontos, fill="", outline=cor_borda, width=2
        )
        self.id_fundo = self.create_polygon(
            [
                corte + 2,
                2,
                largura - 2,
                2,
                largura - corte - 2,
                altura - 2,
                2,
                altura - 2,
            ],
            fill=bg_cor,
            outline="",
        )
        self.create_text(
            largura / 2,
            altura / 2,
            text=texto,
            fill=cor_texto,
            font=(FAMILIA, 14, "bold"),
        )

        self.bind(
            "<Enter>",
            lambda _event: self.itemconfig(self.id_fundo, fill=COR_VERDE_ESCURO),
        )
        self.bind(
            "<Leave>",
            lambda _event: self.itemconfig(self.id_fundo, fill=self._bg_cor),
        )
        self.bind(
            "<Button-1>",
            lambda _event: self._comando() if callable(self._comando) else None,
        )
