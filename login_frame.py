"""
login_frame.py — Tela 1: Login

Fluxo:
- Usuário e senha são conferidos em storage.py (pasta LOGINS/).
- Se o usuário não existir, sugere ir para o cadastro.
- Se a senha estiver errada, mostra erro.
- Se estiver tudo certo, guarda o usuário logado no controller e vai
  para o Dashboard.
"""

import tkinter as tk
from tkinter import font as tkfont

import storage
from theme import INK, INK_SOFT, PAPER, BRASS, BRASS_DEEP, RUST, STONE, STONE_LIGHT, LINE

BRAND_W = 420


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=PAPER)
        self.controller = controller
        self._load_fonts()
        self._build_layout()

    def _load_fonts(self):
        serif_candidates = ["Georgia", "Times New Roman", "Times"]
        available = set(tkfont.families())
        serif = next((f for f in serif_candidates if f in available), "Times")

        self.font_wordmark = tkfont.Font(family="Helvetica", size=11)
        self.font_headline = tkfont.Font(family=serif, size=27)
        self.font_headline_em = tkfont.Font(family=serif, size=27, slant="italic")
        self.font_body = tkfont.Font(family="Helvetica", size=11)
        self.font_footer = tkfont.Font(family="Helvetica", size=9)
        self.font_eyebrow = tkfont.Font(family="Helvetica", size=10)
        self.font_h2 = tkfont.Font(family=serif, size=24)
        self.font_label = tkfont.Font(family="Helvetica", size=10, weight="bold")
        self.font_input = tkfont.Font(family="Helvetica", size=12)
        self.font_link = tkfont.Font(family="Helvetica", size=10)
        self.font_button = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.font_error = tkfont.Font(family="Helvetica", size=9)
        self.font_msg = tkfont.Font(family="Helvetica", size=9, weight="bold")

    def _build_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, minsize=BRAND_W, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self._build_brand_panel()
        self._build_form_panel()

    # ------------------------------------------------------------ marca
    def _build_brand_panel(self):
        panel = tk.Frame(self, bg=INK, width=BRAND_W)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.grid_propagate(False)
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        pad_x = 44

        mark = tk.Frame(panel, bg=INK)
        mark.grid(row=0, column=0, sticky="w", padx=pad_x, pady=(40, 0))
        icon = tk.Canvas(mark, width=34, height=34, bg=INK, highlightthickness=0)
        icon.pack(side="left")
        self._draw_scissors(icon)
        tk.Label(mark, text="Catálogo de Cortes", bg=INK, fg=STONE,
                  font=self.font_wordmark).pack(side="left", padx=(12, 0))

        copy = tk.Frame(panel, bg=INK)
        copy.grid(row=1, column=0, sticky="w", padx=pad_x, pady=(30, 0))

        headline = tk.Frame(copy, bg=INK)
        headline.pack(anchor="w")
        tk.Label(headline, text="Catálogo Digital\nInteligente\nde Cortes", bg=INK, fg=PAPER,
                  font=self.font_headline, justify="left").pack(anchor="w")
    

        tk.Label(
            copy,
            text=("Encontre o corte ideal para você."),
            bg=INK, fg=STONE_LIGHT, font=self.font_body,
            justify="left", wraplength=320
        ).pack(anchor="w", pady=(18, 0))

        footer = tk.Frame(panel, bg=INK)
        footer.grid(row=2, column=0, sticky="ew", padx=pad_x, pady=(0, 36))
        footer.grid_columnconfigure(0, weight=1)
        tk.Label(footer, text="Feito por Alunos da Fatec Ipiranga",
                  bg=INK, fg=STONE, font=self.font_footer).grid(row=0, column=0, sticky="w")


    @staticmethod
    def _draw_scissors(canvas):
        canvas.create_oval(2, 2, 14, 14, outline=BRASS, width=2)
        canvas.create_oval(2, 20, 14, 32, outline=BRASS, width=2)
        canvas.create_line(17, 16, 33, 30, fill=PAPER, width=2, capstyle="round")
        canvas.create_line(17, 18, 33, 4, fill=PAPER, width=2, capstyle="round")

    # ------------------------------------------------------------ form
    def _build_form_panel(self):
        panel = tk.Frame(self, bg=PAPER)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        form = tk.Frame(panel, bg=PAPER)
        form.grid(row=0, column=0)

        tk.Label(form, text="Acesse sua conta", bg=PAPER, fg=STONE,
                  font=self.font_eyebrow).pack(anchor="w")
        tk.Label(form, text="Login", bg=PAPER, fg=INK,
                  font=self.font_h2).pack(anchor="w", pady=(2, 8))

        # mensagem de contexto (ex.: "cadastro realizado, faça login")
        self.msg_label = tk.Label(form, text="", bg=PAPER, fg=BRASS_DEEP,
                                    font=self.font_msg, wraplength=340, justify="left")
        # empacotado sob demanda em set_message()

        self.user_var = tk.StringVar()
        self.user_entry, self.user_underline, self.user_error = self._build_field(
            form, "Usuário", "Digite seu usuário", self.user_var, None,
            "Usuário não encontrado. Cadastre-se primeiro."
        )

        self.pass_var = tk.StringVar()
        self.pass_visible = False
        self.pass_entry, self.pass_underline, self.pass_error = self._build_field(
            form, "Senha", "Digite sua senha", self.pass_var, "•",
            "Senha incorreta.", toggle=True
        )

        forgot_row = tk.Frame(form, bg=PAPER)
        forgot_row.pack(fill="x", pady=(0, 22))
        forgot = tk.Label(forgot_row, text="Esqueci minha senha", bg=PAPER, fg=BRASS_DEEP,
                            font=self.font_link, cursor="hand2")
        forgot.pack(side="right")
        self._bind_link_hover(forgot)

        self.enter_btn = tk.Label(form, text="Entrar", bg=INK, fg=PAPER,
                                    font=self.font_button, cursor="hand2", pady=12)
        self.enter_btn.pack(fill="x")
        self.enter_btn.bind("<Enter>", lambda e: self.enter_btn.config(bg=BRASS_DEEP))
        self.enter_btn.bind("<Leave>", lambda e: self.enter_btn.config(bg=INK))
        self.enter_btn.bind("<Button-1>", lambda e: self._submit())

        divider = tk.Frame(form, bg=PAPER)
        divider.pack(fill="x", pady=(26, 20))
        tk.Frame(divider, bg=LINE, height=1).pack(side="left", fill="x", expand=True)
        tk.Label(divider, text="  ou  ", bg=PAPER, fg=STONE, font=self.font_footer).pack(side="left")
        tk.Frame(divider, bg=LINE, height=1).pack(side="left", fill="x", expand=True)

        signup_row = tk.Frame(form, bg=PAPER)
        signup_row.pack()
        tk.Label(signup_row, text="Não tem conta? ", bg=PAPER, fg=STONE,
                  font=self.font_footer).pack(side="left")
        signup_link = tk.Label(
            signup_row, text="Cadastre-se", bg=PAPER, fg=INK,
            font=tkfont.Font(family="Helvetica", size=9, weight="bold"), cursor="hand2"
        )
        signup_link.pack(side="left")
        self._bind_link_hover(signup_link, hover_fg=BRASS_DEEP, base_fg=INK)
        signup_link.bind("<Button-1>", lambda e: self._go_to_cadastro(), add="+")

    def _build_field(self, parent, label, placeholder, textvariable, show, error_text, toggle=False):
        wrap = tk.Frame(parent, bg=PAPER, width=340)
        wrap.pack(fill="x", pady=(0, 6))

        tk.Label(wrap, text=label, bg=PAPER, fg=INK, font=self.font_label).pack(anchor="w", pady=(0, 6))

        input_row = tk.Frame(wrap, bg=PAPER)
        input_row.pack(fill="x")

        entry = tk.Entry(input_row, textvariable=textvariable, font=self.font_input,
                          bd=0, bg=PAPER, fg=INK, insertbackground=INK, relief="flat")
        entry.pack(side="left", fill="x", expand=True, ipady=6)
        self._apply_placeholder(entry, textvariable, placeholder, show)

        if toggle:
            toggle_btn = tk.Label(input_row, text="mostrar", bg=PAPER, fg=STONE,
                                    font=self.font_footer, cursor="hand2")
            toggle_btn.pack(side="right", padx=(8, 0))
            toggle_btn.bind("<Button-1>", lambda e: self._toggle_password(entry, toggle_btn))

        underline = tk.Frame(wrap, bg=LINE, height=1.5)
        underline.pack(fill="x", pady=(4, 0))

        error_lbl = tk.Label(wrap, text=error_text, bg=PAPER, fg=RUST, font=self.font_error)

        entry.bind("<FocusIn>", lambda e: underline.config(bg=BRASS), add="+")
        entry.bind("<FocusOut>", lambda e: underline.config(bg=LINE), add="+")
        entry.bind("<Return>", lambda e: self._submit())

        return entry, underline, error_lbl

    def _apply_placeholder(self, entry, var, placeholder, show):
        entry._placeholder = placeholder
        entry._real_show = show or ""
        entry._is_placeholder = True
        var.set(placeholder)
        entry.config(fg=STONE)

        def on_focus_in(_e):
            if entry._is_placeholder:
                var.set("")
                entry.config(fg=INK, show=entry._real_show)
                entry._is_placeholder = False

        def on_focus_out(_e):
            if not var.get():
                var.set(placeholder)
                entry.config(fg=STONE, show="")
                entry._is_placeholder = True

        entry.bind("<FocusIn>", on_focus_in, add="+")
        entry.bind("<FocusOut>", on_focus_out, add="+")

    def _toggle_password(self, entry, toggle_btn):
        if entry._is_placeholder:
            return
        self.pass_visible = not self.pass_visible
        entry.config(show="" if self.pass_visible else "•")
        toggle_btn.config(text="ocultar" if self.pass_visible else "mostrar")

    @staticmethod
    def _bind_link_hover(label, hover_fg=None, base_fg=None):
        base_fg = base_fg or label.cget("fg")
        hover_fg = hover_fg or base_fg
        f = tkfont.Font(font=label.cget("font"))
        f_underline = tkfont.Font(font=label.cget("font"))
        f_underline.configure(underline=True)
        label.bind("<Enter>", lambda e: label.config(font=f_underline, fg=hover_fg))
        label.bind("<Leave>", lambda e: label.config(font=f, fg=base_fg))

    # ---------------------------------------------------------- ações
    def set_message(self, text):
        """Mostra uma mensagem de contexto acima do formulário
        (ex.: 'Cadastro realizado! Faça login para continuar.')."""
        if text:
            self.msg_label.config(text=text)
            self.msg_label.pack(anchor="w", pady=(0, 16), before=self.user_entry.master.master)
        else:
            self.msg_label.pack_forget()

    def prefill_username(self, usuario):
        entry = self.user_entry
        entry.delete(0, "end")
        entry.insert(0, usuario)
        entry.config(fg=INK, show="")
        entry._is_placeholder = False

    def clear_fields(self):
        self.user_entry.delete(0, "end")
        self.user_entry.insert(0, self.user_entry._placeholder)
        self.user_entry.config(fg=STONE, show="")
        self.user_entry._is_placeholder = True

        self.pass_entry.delete(0, "end")
        self.pass_entry.insert(0, self.pass_entry._placeholder)
        self.pass_entry.config(fg=STONE, show="")
        self.pass_entry._is_placeholder = True

        self.user_underline.config(bg=LINE)
        self.pass_underline.config(bg=LINE)
        self.user_error.pack_forget()
        self.pass_error.pack_forget()
        self.set_message(None)

    def _go_to_cadastro(self):
        self.set_message(None)
        self.controller.show_frame("CadastroFrame")

    def _submit(self):
        valid = True
        user_ok = not self.user_entry._is_placeholder and self.user_var.get().strip()
        pass_ok = not self.pass_entry._is_placeholder and self.pass_var.get().strip()

        self.user_error.config(text="Digite seu usuário para continuar.")
        self.pass_error.config(text="Digite sua senha para continuar.")

        if not user_ok:
            self.user_underline.config(bg=RUST)
            self.user_error.pack(anchor="w", pady=(6, 0))
            valid = False
        else:
            self.user_underline.config(bg=LINE)
            self.user_error.pack_forget()

        if not pass_ok:
            self.pass_underline.config(bg=RUST)
            self.pass_error.pack(anchor="w", pady=(6, 0))
            valid = False
        else:
            self.pass_underline.config(bg=LINE)
            self.pass_error.pack_forget()

        if not valid:
            return

        usuario = self.user_var.get().strip()
        senha = self.pass_var.get().strip()

        if not storage.user_exists(usuario):
            self.user_underline.config(bg=RUST)
            self.user_error.config(text="Usuário não encontrado. Cadastre-se primeiro.")
            self.user_error.pack(anchor="w", pady=(6, 0))
            return

        if not storage.validate_login(usuario, senha):
            self.pass_underline.config(bg=RUST)
            self.pass_error.config(text="Senha incorreta.")
            self.pass_error.pack(anchor="w", pady=(6, 0))
            return

        # login válido
        self.controller.current_user = usuario
        self.clear_fields()
        self.controller.show_frame("DashboardFrame")
