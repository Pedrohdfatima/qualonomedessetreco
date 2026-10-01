"""
detalhe_frame.py — Tela 5: Detalhes do Corte
"""

import tkinter as tk
from tkinter import font as tkfont

from theme import INK, INK_SOFT, PAPER, PAPER_DIM, BRASS_DEEP, STONE, LINE
from components import build_sidebar

CARACTERISTICAS = [
    ("Tipo de cabelo", "Liso, Ondulado, Cacheado"),
    ("Formato do rosto", "Oval, Quadrado, Redondo"),
    ("Estilo", "Moderno, Clássico"),
    ("Manutenção", "Média"),
    ("Tempo médio", "40 min"),
]
PRODUTOS = ["Pomada", "Leave-in", "Spray Texturizador"]


class DetalheFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=PAPER)
        self.controller = controller
        self._build_layout()

    def _build_layout(self):
        build_sidebar(self, self.controller, active_key="catalogo")

        content = tk.Frame(self, bg=PAPER)
        content.pack(side="left", fill="both", expand=True, padx=28, pady=24)

        back = tk.Label(content, text="← Voltar", bg=PAPER, fg=STONE,
                          font=tkfont.Font(family="Helvetica", size=10), cursor="hand2")
        back.pack(anchor="w", pady=(0, 14))
        back.bind("<Button-1>", lambda e: self.controller.show_frame("CatalogoFrame"))

        body = tk.Frame(content, bg=PAPER)
        body.pack(fill="both", expand=True)

        preview = tk.Frame(body, bg=PAPER_DIM, width=420, height=460)
        preview.pack(side="left", fill="y")
        preview.pack_propagate(False)
        canvas = tk.Canvas(preview, width=260, height=260, bg=PAPER_DIM, highlightthickness=0)
        canvas.pack(pady=(50, 10))
        self._draw_big_silhouette(canvas)

        thumbs = tk.Frame(preview, bg=PAPER_DIM)
        thumbs.pack()
        for _ in range(4):
            c = tk.Canvas(thumbs, width=50, height=50, bg="#ffffff", highlightthickness=1,
                          highlightbackground=LINE)
            c.pack(side="left", padx=4)
            c.create_oval(14, 8, 36, 30, fill=INK_SOFT, outline=INK_SOFT)

        info = tk.Frame(body, bg=PAPER)
        info.pack(side="left", fill="both", expand=True, padx=(28, 0))

        title_row = tk.Frame(info, bg=PAPER)
        title_row.pack(anchor="w", pady=(0, 4))
        self.title_label = tk.Label(title_row, text="Taper Fade", bg=PAPER, fg=INK,
                                      font=tkfont.Font(family="Georgia", size=22, weight="bold"))
        self.title_label.pack(side="left")
        tk.Label(title_row, text=" Degradê ", bg="#dfeaf6", fg=INK,
                  font=tkfont.Font(family="Helvetica", size=9), padx=6, pady=2
                  ).pack(side="left", padx=(10, 0))

        tk.Label(info, text="Descrição", bg=PAPER, fg=INK,
                  font=tkfont.Font(family="Helvetica", size=11, weight="bold")
                  ).pack(anchor="w", pady=(16, 4))
        tk.Label(info, text="Degradê clássico e versátil que combina com diversos estilos.",
                  bg=PAPER, fg=STONE, wraplength=380, justify="left",
                  font=tkfont.Font(family="Helvetica", size=10)).pack(anchor="w")

        tk.Label(info, text="Características", bg=PAPER, fg=INK,
                  font=tkfont.Font(family="Helvetica", size=11, weight="bold")
                  ).pack(anchor="w", pady=(18, 6))
        for label, value in CARACTERISTICAS:
            tk.Label(info, text=f"•  {label}: {value}", bg=PAPER, fg=INK_SOFT,
                      font=tkfont.Font(family="Helvetica", size=9)).pack(anchor="w", pady=1)

        tk.Label(info, text="Produtos recomendados", bg=PAPER, fg=INK,
                  font=tkfont.Font(family="Helvetica", size=11, weight="bold")
                  ).pack(anchor="w", pady=(18, 8))
        chips = tk.Frame(info, bg=PAPER)
        chips.pack(anchor="w")
        for produto in PRODUTOS:
            tk.Label(chips, text=produto, bg="#ffffff", fg=INK, bd=1, relief="solid",
                      font=tkfont.Font(family="Helvetica", size=9), padx=10, pady=4
                      ).pack(side="left", padx=(0, 6))

        self.indicar_btn = tk.Label(info, text="Indicar para cliente", bg=INK, fg=PAPER,
                                      font=tkfont.Font(family="Helvetica", size=10, weight="bold"),
                                      cursor="hand2", padx=16, pady=9)
        self.indicar_btn.pack(anchor="w", pady=(22, 0))
        self.indicar_btn.bind("<Enter>", lambda e: self.indicar_btn.config(bg=BRASS_DEEP))
        self.indicar_btn.bind("<Leave>", lambda e: self.indicar_btn.config(bg=INK))

    def set_cut(self, name):
        """Atualiza o título ao abrir os detalhes vindo de um cartão específico."""
        self.title_label.config(text=name)

    @staticmethod
    def _draw_big_silhouette(canvas):
        canvas.create_oval(70, 20, 190, 140, fill=INK_SOFT, outline=INK_SOFT)
        canvas.create_arc(70, 10, 190, 90, start=0, extent=180, fill=INK, outline=INK)
        canvas.create_polygon(85, 140, 100, 200, 160, 200, 175, 140, fill="#d8cdb8", outline="")
