"""
catalogo_frame.py — Tela 4: Catálogo (busca funcional + grade de cortes)

A busca filtra a grade em tempo real conforme o texto digitado,
comparando com o nome e a categoria de cada corte (sem diferenciar
maiúsculas/minúsculas).
"""

import tkinter as tk
from tkinter import font as tkfont

from theme import INK, PAPER, PAPER_DIM, STONE
from components import build_sidebar, style_card

CORTES = [
    ("Low Fade", "Degradê"), ("Taper Fade", "Degradê"),
    ("Mid Fade", "Degradê"), ("Undercut", "Clássico"),
    ("Buzz Cut", "Clássico"), ("French Crop", "Clássico"),
    ("Curly Crop", "Cacheado"), ("Pompadour", "Clássico"),
]

FILTROS = ["Tipo de cabelo", "Formato do rosto", "Estilo", "Manutenção"]


class CatalogoFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=PAPER)
        self.controller = controller
        self._build_layout()

    def _build_layout(self):
        build_sidebar(self, self.controller, active_key="catalogo")

        content = tk.Frame(self, bg=PAPER)
        content.pack(side="left", fill="both", expand=True, padx=28, pady=24)

        header = tk.Frame(content, bg=PAPER)
        header.pack(fill="x", pady=(0, 16))
        tk.Label(header, text="Catálogo de Cortes", bg=PAPER, fg=INK,
                  font=tkfont.Font(family="Georgia", size=20, weight="bold")).pack(side="left")

        search_box = tk.Frame(header, bg="#ffffff", bd=1, relief="solid")
        search_box.pack(side="right")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_box, width=24, bd=0, textvariable=self.search_var,
                                  font=tkfont.Font(family="Helvetica", size=10))
        search_entry.pack(side="left", padx=8, pady=6)
        tk.Label(search_box, text="🔍", bg="#ffffff").pack(side="left", padx=(0, 8))
        self.search_var.trace_add("write", lambda *args: self._render_grid())

        filtros = tk.Frame(content, bg=PAPER)
        filtros.pack(fill="x", pady=(0, 20))
        for label in FILTROS:
            box = tk.Frame(filtros, bg="#ffffff", bd=1, relief="solid")
            box.pack(side="left", expand=True, fill="x", padx=4)
            tk.Label(box, text=f"{label}  ▾", bg="#ffffff", fg=INK,
                      font=tkfont.Font(family="Helvetica", size=9), anchor="w"
                      ).pack(fill="x", padx=10, pady=6)

        self.grid_container = tk.Frame(content, bg=PAPER)
        self.grid_container.pack(fill="both", expand=True)
        self._render_grid()

    def _render_grid(self):
        for w in self.grid_container.winfo_children():
            w.destroy()

        termo = self.search_var.get().strip().lower()
        filtrados = [
            (name, tag) for name, tag in CORTES
            if termo in name.lower() or termo in tag.lower()
        ] if termo else CORTES

        if not filtrados:
            tk.Label(self.grid_container, text="Nenhum corte encontrado para essa busca.",
                      bg=PAPER, fg=STONE, font=tkfont.Font(family="Helvetica", size=10)
                      ).pack(anchor="w", pady=20)
            return

        row = None
        for i, (name, tag) in enumerate(filtrados):
            if i % 4 == 0:
                row = tk.Frame(self.grid_container, bg=PAPER)
                row.pack(anchor="w")
            style_card(row, name, tag=tag, accent=PAPER_DIM, on_click=self._open_detail)

    def _open_detail(self, name):
        self.controller.frames["DetalheFrame"].set_cut(name)
        self.controller.show_frame("DetalheFrame")
