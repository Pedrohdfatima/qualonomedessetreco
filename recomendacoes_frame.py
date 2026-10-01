"""
recomendacoes_frame.py — Tela 7: Recomendações

Agora reúne o que antes era a tela de Perfil (questionário de tipo de
cabelo, formato do rosto, estilo e manutenção) com a lista de cortes
recomendados, que aparece depois que o questionário é respondido.
"""

import tkinter as tk
from tkinter import font as tkfont

from theme import INK, PAPER, PAPER_DIM, STONE, BRASS_DEEP
from components import build_sidebar, build_topbar, dropdown_field, style_card

RECOMENDADOS = [
    ("Taper Fade", "90% compatibilidade"),
    ("Low Fade", "90% compatibilidade"),
    ("Curly Crop", "80% compatibilidade"),
    ("French Crop", "80% compatibilidade"),
]


class RecomendacoesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=PAPER)
        self.controller = controller
        self._build_layout()

    def _build_layout(self):
        build_sidebar(self, self.controller, active_key="recomendacoes")

        content = tk.Frame(self, bg=PAPER)
        content.pack(side="left", fill="both", expand=True, padx=28, pady=24)

        build_topbar(content, "Recomendações",
                     "Responda ao questionário para receber sugestões de cortes.")

        form = tk.Frame(content, bg=PAPER, width=420)
        form.pack(anchor="w")

        dropdown_field(form, "Tipo de cabelo", ["Liso", "Ondulado", "Cacheado", "Crespo"])
        dropdown_field(form, "Formato do rosto", ["Oval", "Quadrado", "Redondo", "Triangular"])
        dropdown_field(form, "Estilo que o cliente prefere", ["Clássico", "Moderno", "Ousado", "Discreto"])
        dropdown_field(form, "Nível de manutenção desejado", ["Baixa", "Média", "Alta"])

        self.ver_btn = tk.Label(form, text="Ver recomendações", bg=INK, fg=PAPER,
                                  font=tkfont.Font(family="Helvetica", size=10, weight="bold"),
                                  cursor="hand2", pady=11)
        self.ver_btn.pack(fill="x", pady=(16, 0))
        self.ver_btn.bind("<Enter>", lambda e: self.ver_btn.config(bg=BRASS_DEEP))
        self.ver_btn.bind("<Leave>", lambda e: self.ver_btn.config(bg=INK))
        self.ver_btn.bind("<Button-1>", lambda e: self._mostrar_resultados())

        # Área de resultados — começa vazia e só aparece depois do clique.
        self.results_frame = tk.Frame(content, bg=PAPER)
        self.results_frame.pack(fill="both", expand=True, pady=(26, 0))

    def _mostrar_resultados(self):
        for w in self.results_frame.winfo_children():
            w.destroy()

        tk.Label(self.results_frame, text="Cortes recomendados", bg=PAPER, fg=INK,
                  font=tkfont.Font(family="Georgia", size=15, weight="bold")
                  ).pack(anchor="w", pady=(0, 10))

        row = tk.Frame(self.results_frame, bg=PAPER)
        row.pack(anchor="w", pady=(0, 16))
        for name, tag in RECOMENDADOS:
            style_card(row, name, tag=tag, accent=PAPER_DIM, on_click=self._open_detail)

        refazer = tk.Label(self.results_frame, text="Refazer questionário", bg="#ffffff", fg=INK,
                             bd=1, relief="solid",
                             font=tkfont.Font(family="Helvetica", size=10, weight="bold"),
                             cursor="hand2", padx=16, pady=9)
        refazer.pack(anchor="w")
        refazer.bind("<Button-1>", lambda e: self._limpar_resultados())

    def _limpar_resultados(self):
        for w in self.results_frame.winfo_children():
            w.destroy()

    def _open_detail(self, name):
        self.controller.frames["DetalheFrame"].set_cut(name)
        self.controller.show_frame("DetalheFrame")
