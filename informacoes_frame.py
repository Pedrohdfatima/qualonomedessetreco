"""
informacoes_frame.py — Tela 6: Informações do Usuário

Mostra os dados da conta logada (nome, e-mail, usuário), lidos de
storage.py. Antes essa tela era um questionário de cabelo/rosto —
esse conteúdo foi movido para a tela de Recomendações.
"""

import tkinter as tk
from tkinter import font as tkfont

import storage
from theme import INK, PAPER, PAPER_DIM, STONE, LINE
from components import build_sidebar, build_topbar


class InformacoesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=PAPER)
        self.controller = controller
        self._build_layout()

    def _build_layout(self):
        build_sidebar(self, self.controller, active_key="informacoes")

        content = tk.Frame(self, bg=PAPER)
        content.pack(side="left", fill="both", expand=True, padx=28, pady=24)

        build_topbar(content, "Informações do usuário", "Dados da sua conta no sistema.")

        card = tk.Frame(content, bg=PAPER_DIM, width=420, highlightthickness=1,
                          highlightbackground=LINE)
        card.pack(anchor="w")

        self.rows = {}
        for label in ("Nome completo", "Usuário", "E-mail"):
            row = tk.Frame(card, bg=PAPER_DIM)
            row.pack(fill="x", padx=24, pady=(18, 0))
            tk.Label(row, text=label, bg=PAPER_DIM, fg=STONE,
                      font=tkfont.Font(family="Helvetica", size=9, weight="bold")
                      ).pack(anchor="w")
            value_lbl = tk.Label(row, text="—", bg=PAPER_DIM, fg=INK,
                                   font=tkfont.Font(family="Helvetica", size=13))
            value_lbl.pack(anchor="w", pady=(2, 0))
            self.rows[label] = value_lbl

        tk.Frame(card, bg=PAPER_DIM, height=18).pack()  # respiro inferior

    def on_show(self):
        usuario = self.controller.current_user
        dados = storage.get_user(usuario) if usuario else None
        self.rows["Nome completo"].config(text=(dados or {}).get("nome", "—"))
        self.rows["Usuário"].config(text=(dados or {}).get("usuario", usuario or "—"))
        self.rows["E-mail"].config(text=(dados or {}).get("email", "—"))
