"""Shared colors, game settings, and asset locations."""

from pathlib import Path


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"

COR_FUNDO = "#0A0A0E"
COR_PAINEL = "#12121A"
COR_NEON = "#39FF88"
COR_NEON_HOVER = "#8AFFBB"
COR_VERDE_ESCURO = "#123D2A"
COR_BRANCO = "#FFFFFF"
COR_CINZA = "#A0A0A0"
COR_CINZA_ESCURO = "#555555"
COR_VERMELHO = "#FF4545"
COR_AMARELO = "#FFD447"

FAMILIA = "Segoe UI"

TOTAL_RODADAS = 5
ATRASO_MIN_MS = 1000
ATRASO_MAX_MS = 5000
RAIO_MEDIO = 70
RAIO_DIFICIL = 22
PAUSA_RODADA_MS = 1300

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
    ("Menos de 8 ms", "Trapaça ou Sorte Pura", "Impossível para humanos. Você adivinhou ou usou um robô."),
]
