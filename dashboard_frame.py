"""
dashboard_screen.py wasn't reused directly — this is dashboard_frame.py,
Tela 3: Tela Inicial (Dashboard). É a primeira tela depois do login.
"""

import tkinter as tk
from tkinter import font as tkfont

import storage
from theme import INK, PAPER, PAPER_DIM, STONE, CARD_BLUE, CARD_GREEN, CARD_ORANGE, CARD_PURPLE
from components import build_sidebar, build_topbar, style_card, metric_card

DESTAQUES = ["Low Fade", "Taper Fade", "Mid Fade", "Undercut", "Buzz Cut"]


class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=PAPER)
        self.controller = controller
        self._build_layout()

    def _build_layout(self):
        build_sidebar(self, self.controller, active_key="inicio")

        content = tk.Frame(self, bg=PAPER)
        content.pack(side="left", fill="both", expand=True, padx=28, pady=24)

        greeting = tk.Frame(content, bg=PAPER)
        greeting.pack(fill="x", pady=(0, 18))
        self.greeting_label = tk.Label(
            greeting, text="Olá, Usuário!", bg=PAPER, fg=INK,
            font=tkfont.Font(family="Georgia", size=22, weight="bold")
        )
        self.greeting_label.pack(anchor="w")
        tk.Label(greeting, text="Encontre o corte perfeito para você.", bg=PAPER, fg=STONE,
                  font=tkfont.Font(family="Helvetica", size=10)).pack(anchor="w", pady=(2, 0))

        metrics = tk.Frame(content, bg=PAPER)
        metrics.pack(fill="x", pady=(0, 26))
        for label, value, accent in [
            ("Cortes disponíveis", "48", CARD_BLUE),
            ("Clientes atendidos", "34", CARD_GREEN),
            ("Avaliações", "27", CARD_ORANGE),
            ("Recomendações", "5", CARD_PURPLE),
        ]:
            metric_card(metrics, label, value, accent)

        build_topbar(content, "Cortes em destaque", action_text="Ver todos ›",
                     action_cmd=lambda: self.controller.show_frame("CatalogoFrame"))

        row = tk.Frame(content, bg=PAPER)
        row.pack(anchor="w")
        for name in DESTAQUES:
            style_card(row, name, accent=PAPER_DIM, on_click=self._open_detail)

    def _open_detail(self, name):
        self.controller.frames["DetalheFrame"].set_cut(name)
        self.controller.show_frame("DetalheFrame")

    def on_show(self):
        """Chamado toda vez que a tela é exibida — atualiza a saudação
        com o nome de quem está logado."""
        usuario = self.controller.current_user
        dados = storage.get_user(usuario) if usuario else None
        nome = dados.get("nome") if dados else usuario
        self.greeting_label.config(text=f"Olá, {nome or 'Usuário'}!")
