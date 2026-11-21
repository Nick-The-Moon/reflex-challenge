"""Shared lifecycle and helpers for independently creatable screens."""

import tkinter as tk
from PIL import Image, ImageTk

from .theme import ASSET_DIR, COR_FUNDO


class ScreenComponent:
    """Base for screen widgets that call back into the game controller."""

    def __init__(self, app):
        object.__setattr__(self, "app", app)
        object.__setattr__(self, "frame", None)

    def __getattr__(self, name):
        return getattr(self.app, name)

    def __setattr__(self, name, value):
        if name in {"app", "frame"}:
            object.__setattr__(self, name, value)
        else:
            setattr(self.app, name, value)

    def register_screen(self, name, frame):
        """Store the screen frame and keep it available to the controller."""
        self.frame = frame
        self.telas[name] = frame

    def create_background(self, canvas, image_name, reference_name):
        """Render an asset at the canvas size and retain its Tk image reference."""
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 1 or height <= 1:
            return

        try:
            image_path = ASSET_DIR / image_name
            image = Image.open(image_path)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            image_tk = ImageTk.PhotoImage(image)

            canvas.delete("bg")
            canvas.create_image(0, 0, image=image_tk, anchor="nw", tags="bg")
            # Keep the image alive for Tkinter and share it with the controller.
            setattr(self, reference_name, image_tk)
        except (OSError, tk.TclError) as error:
            print(f"Erro ao carregar imagem {image_name}: {error}")
