"""
main.py — Catálogo Digital Inteligente de Cortes
Ponto de entrada único do app. Execute:

    python3 main.py

Fluxo:
    Login -> (se não tiver conta) Cadastro -> volta pro Login
    (obrigatório logar após cadastrar) -> Dashboard -> demais telas.

Todas as telas moram dentro da MESMA janela: este arquivo troca qual
frame fica visível (self.show_frame), então não abre janelas novas.
"""

import tkinter as tk

from theme import PAPER

from login_frame import LoginFrame
from cadastro_frame import CadastroFrame
from dashboard_frame import DashboardFrame
from catalogo_frame import CatalogoFrame
from detalhe_frame import DetalheFrame
from informacoes_frame import InformacoesFrame
from recomendacoes_frame import RecomendacoesFrame
from admin_frame import AdminFrame

FRAME_CLASSES = (
    LoginFrame, CadastroFrame, DashboardFrame, CatalogoFrame,
    DetalheFrame, InformacoesFrame, RecomendacoesFrame, AdminFrame,
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catálogo Digital Inteligente de Cortes")
        self.geometry("1200x780")
        self.minsize(980, 640)
        self.configure(bg=PAPER)

        # usuário logado no momento (nome de usuário) — None se ninguém logado
        self.current_user = None

        container = tk.Frame(self, bg=PAPER)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for FrameClass in FRAME_CLASSES:
            frame = FrameClass(parent=container, controller=self)
            self.frames[FrameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    def logout(self):
        self.current_user = None
        self.frames["LoginFrame"].clear_fields()
        self.show_frame("LoginFrame")


if __name__ == "__main__":
    app = App()
    app.mainloop()
