"""
admin_frame.py — Tela 9: Administrativa (Gerenciar Cortes)
"""

import tkinter as tk
from tkinter import font as tkfont

from theme import INK, INK_SOFT, PAPER, PAPER_DIM, BRASS_DEEP, RUST
from components import build_sidebar, build_topbar, ADMIN_NAV

CORTES = [
    (1, "Taper Fade", "Degradê"),
    (2, "Low Fade", "Degradê"),
    (3, "Mid Fade", "Degradê"),
    (4, "Undercut", "Clássico"),
]

COLS = ["ID", "Imagem", "Nome", "Categoria", "Ações"]


class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=PAPER)
        self.controller = controller
        self._build_layout()

    def _build_layout(self):
        build_sidebar(self, self.controller, active_key="admin", nav_items=ADMIN_NAV)

        content = tk.Frame(self, bg=PAPER)
        content.pack(side="left", fill="both", expand=True, padx=28, pady=24)

        build_topbar(content, "Gerenciar Cortes", action_text="+ Novo corte")

        table = tk.Frame(content, bg=PAPER)
        table.pack(fill="both", expand=True)
        for c in range(len(COLS)):
            table.grid_columnconfigure(c, weight=1)

        for c, header in enumerate(COLS):
            tk.Label(table, text=header, bg=PAPER_DIM, fg=INK,
                      font=tkfont.Font(family="Helvetica", size=9, weight="bold"),
                      anchor="w", padx=10, pady=8, bd=1, relief="solid"
                      ).grid(row=0, column=c, sticky="ew")

        for r, (cid, nome, categoria) in enumerate(CORTES, start=1):
            row_vals = [str(cid), None, nome, categoria, None]
            for c, val in enumerate(row_vals):
                cell = tk.Frame(table, bg="#ffffff", bd=1, relief="solid")
                cell.grid(row=r, column=c, sticky="nsew")
                if c == 1:
                    canvas = tk.Canvas(cell, width=30, height=30, bg="#ffffff", highlightthickness=0)
                    canvas.pack(padx=10, pady=6)
                    canvas.create_oval(4, 2, 26, 24, fill=INK_SOFT, outline=INK_SOFT)
                elif c == 4:
                    actions = tk.Frame(cell, bg="#ffffff")
                    actions.pack(padx=8, pady=6)
                    tk.Label(actions, text="✎", bg=BRASS_DEEP, fg=PAPER, padx=8, pady=2,
                              cursor="hand2").pack(side="left", padx=(0, 4))
                    tk.Label(actions, text="🗑", bg=RUST, fg=PAPER, padx=8, pady=2,
                              cursor="hand2").pack(side="left")
                else:
                    tk.Label(cell, text=val, bg="#ffffff", fg=INK,
                              font=tkfont.Font(family="Helvetica", size=9),
                              anchor="w", padx=10, pady=8).pack(fill="both")
