"""
components.py — Widgets reutilizados por várias telas: barra lateral
navegável, cartão de estilo de corte, cartão de métrica, cabeçalho de
página e campo de seleção (dropdown).
"""

import tkinter as tk
from tkinter import font as tkfont

from theme import (
    INK, INK_SOFT, PAPER, PAPER_DIM, BRASS, BRASS_DEEP,
    STONE, STONE_LIGHT, LINE, SIDEBAR_W,
)

MAIN_NAV = [
    ("Início", "inicio"),
    ("Catálogo", "catalogo"),
    ("Recomendações", "recomendacoes"),
    ("Informações", "informacoes"),
    ("Sair", "sair"),
]

ADMIN_NAV = [
    ("Catálogo", "catalogo"),
    ("Admin", "admin"),
    ("Sair", "sair"),
]

# Mapeia a chave do item de menu para o nome da classe do frame de destino.
# Chaves que não aparecem aqui (ex.: "sair") são tratadas separadamente.
NAV_ROUTES = {
    "inicio": "DashboardFrame",
    "catalogo": "CatalogoFrame",
    "recomendacoes": "RecomendacoesFrame",
    "informacoes": "InformacoesFrame",
    "admin": "AdminFrame",
}


def build_sidebar(parent, controller, active_key, nav_items=None,
                   brand_label="Catálogo de Cortes"):
    """Barra lateral escura com o item ativo destacado em latão.
    Cada item navega para o frame correspondente através do `controller`
    (que deve ter os métodos show_frame(nome) e logout())."""
    nav_items = nav_items or MAIN_NAV

    side = tk.Frame(parent, bg=INK, width=SIDEBAR_W)
    side.pack(side="left", fill="y")
    side.pack_propagate(False)

    mark = tk.Frame(side, bg=INK)
    mark.pack(fill="x", padx=18, pady=(22, 18))
    icon = tk.Canvas(mark, width=20, height=20, bg=INK, highlightthickness=0)
    icon.pack(side="left")
    icon.create_oval(1, 1, 8, 8, outline=BRASS, width=1.6)
    icon.create_oval(1, 12, 8, 19, outline=BRASS, width=1.6)
    icon.create_line(10, 10, 19, 19, fill=PAPER, width=1.6)
    icon.create_line(10, 11, 19, 2, fill=PAPER, width=1.6)
    tk.Label(
        mark, text=brand_label, bg=INK, fg=PAPER,
        font=tkfont.Font(family="Helvetica", size=10, weight="bold"),
        wraplength=120, justify="left"
    ).pack(side="left", padx=(8, 0))

    def make_handler(key):
        def handler(_event):
            if key == "sair":
                controller.logout()
            elif key in NAV_ROUTES:
                controller.show_frame(NAV_ROUTES[key])
        return handler

    for label, key in nav_items:
        is_active = key == active_key
        row_bg = BRASS_DEEP if is_active else INK
        fg = PAPER if is_active else STONE_LIGHT
        row = tk.Label(
            side, text=label, bg=row_bg, fg=fg,
            font=tkfont.Font(family="Helvetica", size=10),
            anchor="w", padx=18, pady=9, cursor="hand2"
        )
        row.pack(fill="x")
        if not is_active:
            row.bind("<Enter>", lambda e, r=row: r.config(bg=INK_SOFT))
            row.bind("<Leave>", lambda e, r=row: r.config(bg=INK))
        row.bind("<Button-1>", make_handler(key))

    return side


def build_topbar(parent, title, subtitle=None, action_text=None, action_cmd=None):
    """Cabeçalho de página: título + subtítulo opcional + botão de ação opcional."""
    bar = tk.Frame(parent, bg=PAPER)
    bar.pack(fill="x", pady=(0, 16))

    text_col = tk.Frame(bar, bg=PAPER)
    text_col.pack(side="left", anchor="w")
    tk.Label(
        text_col, text=title, bg=PAPER, fg=INK,
        font=tkfont.Font(family="Georgia", size=20, weight="bold")
    ).pack(anchor="w")
    if subtitle:
        tk.Label(
            text_col, text=subtitle, bg=PAPER, fg=STONE,
            font=tkfont.Font(family="Helvetica", size=10)
        ).pack(anchor="w", pady=(2, 0))

    if action_text:
        btn = tk.Label(
            bar, text=action_text, bg=INK, fg=PAPER,
            font=tkfont.Font(family="Helvetica", size=10, weight="bold"),
            padx=16, pady=8, cursor="hand2"
        )
        btn.pack(side="right", anchor="e")
        btn.bind("<Enter>", lambda e: btn.config(bg=BRASS_DEEP))
        btn.bind("<Leave>", lambda e: btn.config(bg=INK))
        if action_cmd:
            btn.bind("<Button-1>", lambda e: action_cmd())

    return bar


def _draw_hair_silhouette(canvas, w=110, h=80):
    """Ícone genérico de corte (silhueta simples), já que não há fotos
    reais disponíveis — mantém o cartão visualmente reconhecível."""
    cx = w / 2
    canvas.create_oval(cx - 26, 8, cx + 26, 54, fill=INK_SOFT, outline=INK_SOFT)
    canvas.create_arc(cx - 26, 4, cx + 26, 40, start=0, extent=180, fill=INK, outline=INK)
    canvas.create_polygon(
        cx - 20, 54, cx - 14, 74, cx + 14, 74, cx + 20, 54,
        fill="#d8cdb8", outline=""
    )


def style_card(parent, name, tag="", accent=PAPER_DIM, badge=None, on_click=None):
    """Cartão de estilo de corte. Se `on_click` for passado, recebe o
    nome do corte quando o cartão é clicado (usado para abrir os detalhes)."""
    card = tk.Frame(parent, bg=accent, width=150, height=168,
                     highlightthickness=1, highlightbackground="#d0c7b6",
                     cursor="hand2" if on_click else "")
    card.pack_propagate(False)
    card.pack(side="left", padx=6, pady=6)

    canvas = tk.Canvas(card, width=130, height=78, bg=accent, highlightthickness=0)
    canvas.pack(pady=(10, 4))
    _draw_hair_silhouette(canvas, w=130, h=78)

    tk.Label(
        card, text=name, bg=accent, fg=INK,
        font=tkfont.Font(family="Helvetica", size=10, weight="bold")
    ).pack()
    if tag:
        tk.Label(
            card, text=tag, bg=accent, fg=STONE,
            font=tkfont.Font(family="Helvetica", size=8)
        ).pack()
    if badge:
        tk.Label(
            card, text=badge, bg=BRASS, fg=PAPER,
            font=tkfont.Font(family="Helvetica", size=8, weight="bold"),
            padx=6, pady=1
        ).pack(pady=(4, 0))

    if on_click:
        for widget in (card, canvas):
            widget.bind("<Button-1>", lambda e, n=name: on_click(n))

    return card


def metric_card(parent, label, value, accent):
    box = tk.Frame(parent, bg=accent, width=150, height=88)
    box.pack_propagate(False)
    box.pack(side="left", expand=True, fill="x", padx=6)
    tk.Label(
        box, text=value, bg=accent, fg=INK,
        font=tkfont.Font(family="Helvetica", size=22, weight="bold")
    ).pack(anchor="w", padx=14, pady=(14, 0))
    tk.Label(
        box, text=label, bg=accent, fg=INK_SOFT,
        font=tkfont.Font(family="Helvetica", size=9)
    ).pack(anchor="w", padx=14)
    return box


def dropdown_field(parent, label, options, default="Selecione..."):
    row = tk.Frame(parent, bg=PAPER)
    row.pack(fill="x", pady=8)
    tk.Label(
        row, text=label, bg=PAPER, fg=INK,
        font=tkfont.Font(family="Helvetica", size=10, weight="bold")
    ).pack(anchor="w", pady=(0, 6))
    var = tk.StringVar(value=default)
    menu = tk.OptionMenu(row, var, default, *options)
    menu.config(
        bg=PAPER, fg=INK, activebackground=PAPER_DIM, bd=1,
        relief="solid", highlightthickness=0, anchor="w",
        font=tkfont.Font(family="Helvetica", size=10)
    )
    menu.pack(fill="x", ipady=4)
    return var
