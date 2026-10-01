"""
cadastro_frame.py — Tela 2: Cadastro de Usuário

Fluxo:
- Valida os campos (todos obrigatórios, senha == confirmar senha).
- Verifica se o usuário já existe (storage.user_exists).
- Salva o novo usuário (storage.save_user) — isso cria a pasta LOGINS/
  na primeira vez que alguém se cadastra.
- NÃO loga automaticamente: manda de volta para a tela de Login com uma
  mensagem, e o usuário precisa entrar com a senha para confirmar.
"""

import tkinter as tk
from tkinter import font as tkfont

import storage
from theme import INK, PAPER, BRASS, BRASS_DEEP, RUST, STONE, LINE


class CadastroFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=PAPER)
        self.controller = controller

        serif_candidates = ["Georgia", "Times New Roman", "Times"]
        available = set(tkfont.families())
        self.serif = next((f for f in serif_candidates if f in available), "Times")

        self.entries = {}
        self._build_layout()

    def _build_layout(self):
        self._build_form()

    def _build_form(self):
        wrap = tk.Frame(self, bg=PAPER)
        wrap.pack(fill="both", expand=True)
        wrap.grid_rowconfigure(0, weight=1)
        wrap.grid_columnconfigure(0, weight=1)

        form = tk.Frame(wrap, bg=PAPER)
        form.grid(row=0, column=0)

        tk.Label(form, text="Cadastro de Usuário", bg=PAPER, fg=INK,
                  font=tkfont.Font(family=self.serif, size=24)).pack(pady=(0, 6))

        self.msg_label = tk.Label(form, text="", bg=PAPER, fg=RUST,
                                    font=tkfont.Font(family="Helvetica", size=9, weight="bold"),
                                    wraplength=380, justify="left")
        # empacotado sob demanda

        fields = [
            ("Nome completo", "Digite seu nome completo", ""),
            ("E-mail", "Digite seu e-mail", ""),
            ("Usuário", "Digite seu usuário", ""),
            ("Senha", "Digite sua senha", "•"),
            ("Confirmar senha", "Confirme sua senha", "•"),
        ]
        for label, placeholder, show in fields:
            entry, underline = self._build_field(form, label, placeholder, show)
            self.entries[label] = (entry, placeholder, underline)

        btn = tk.Label(form, text="Cadastrar", bg=INK, fg=PAPER,
                         font=tkfont.Font(family="Helvetica", size=11, weight="bold"),
                         cursor="hand2", pady=12, width=36)
        btn.pack(pady=(16, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg=BRASS_DEEP))
        btn.bind("<Leave>", lambda e: btn.config(bg=INK))
        btn.bind("<Button-1>", lambda e: self._submit())

        login_row = tk.Frame(form, bg=PAPER)
        login_row.pack(pady=(14, 0))
        tk.Label(login_row, text="Já tem conta? ", bg=PAPER, fg=STONE,
                  font=tkfont.Font(family="Helvetica", size=9)).pack(side="left")
        link = tk.Label(login_row, text="Faça login", bg=PAPER, fg=INK,
                          font=tkfont.Font(family="Helvetica", size=9, weight="bold"),
                          cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: self.controller.show_frame("LoginFrame"))

    def _build_field(self, parent, label, placeholder, show):
        wrap = tk.Frame(parent, bg=PAPER, width=380)
        wrap.pack(fill="x", pady=(0, 14))

        tk.Label(wrap, text=label, bg=PAPER, fg=INK,
                  font=tkfont.Font(family="Helvetica", size=10, weight="bold")).pack(anchor="w", pady=(0, 6))

        entry = tk.Entry(wrap, font=tkfont.Font(family="Helvetica", size=12),
                          bd=0, bg=PAPER, fg=STONE, insertbackground=INK, relief="flat")
        entry.pack(fill="x", ipady=6)
        entry.insert(0, placeholder)
        entry._is_placeholder = True

        underline = tk.Frame(wrap, bg=LINE, height=1.5)
        underline.pack(fill="x", pady=(4, 0))

        def on_focus_in(_e):
            underline.config(bg=BRASS)
            if entry._is_placeholder:
                entry.delete(0, "end")
                entry.config(fg=INK, show=show)
                entry._is_placeholder = False

        def on_focus_out(_e):
            underline.config(bg=LINE)
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=STONE, show="")
                entry._is_placeholder = True

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<Return>", lambda e: self._submit())

        return entry, underline

    def _value(self, label):
        entry, placeholder, _underline = self.entries[label]
        return "" if entry._is_placeholder else entry.get().strip()

    def _show_error(self, text, fields_to_mark=()):
        self.msg_label.config(text=text)
        self.msg_label.pack(anchor="w", pady=(0, 14), before=list(self.entries.values())[0][0].master)
        for label in fields_to_mark:
            self.entries[label][2].config(bg=RUST)

    def _clear_error(self):
        self.msg_label.pack_forget()
        for _entry, _ph, underline in self.entries.values():
            underline.config(bg=LINE)

    def clear_fields(self):
        for label, (entry, placeholder, underline) in self.entries.items():
            entry.delete(0, "end")
            entry.insert(0, placeholder)
            entry.config(fg=STONE, show="")
            entry._is_placeholder = True
            underline.config(bg=LINE)
        self._clear_error()

    def _submit(self):
        self._clear_error()

        nome = self._value("Nome completo")
        email = self._value("E-mail")
        usuario = self._value("Usuário")
        senha = self._value("Senha")
        confirmar = self._value("Confirmar senha")

        campos_vazios = [l for l in ("Nome completo", "E-mail", "Usuário", "Senha", "Confirmar senha")
                          if not self._value(l)]
        if campos_vazios:
            self._show_error("Preencha todos os campos para continuar.", campos_vazios)
            return

        if senha != confirmar:
            self._show_error("As senhas não coincidem.", ["Senha", "Confirmar senha"])
            return

        if storage.user_exists(usuario):
            self._show_error("Esse usuário já existe. Escolha outro ou faça login.", ["Usuário"])
            return

        storage.save_user(nome, email, usuario, senha)

        # cadastro salvo — agora o login é obrigatório para confirmar
        login_frame = self.controller.frames["LoginFrame"]
        login_frame.set_message("Cadastro realizado! Faça login para continuar.")
        login_frame.prefill_username(usuario)
        self.clear_fields()
        self.controller.show_frame("LoginFrame")


if __name__ == "__main__":
    # Permite visualizar esta tela isoladamente durante o desenvolvimento,
    # mas o fluxo completo (login -> cadastro -> dashboard) roda pelo main.py.
    from main import App
    App().mainloop()
