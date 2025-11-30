import tkinter as tk
from tkinter import ttk, messagebox
from src.config.settings import Config
from src.controllers.checkout_controller import CheckoutController


class AddressFormView(tk.Frame):
    """
    Formulário para cadastro de novos endereços.
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data

        # Reutiliza o CheckoutController pois ele tem a lógica de endereços
        self.checkout_controller = CheckoutController(controller)
        if self.usuario:
            self.checkout_controller.set_current_user(self.usuario.id)

        self._setup_ui()

    def _setup_ui(self):
        # Card Central
        card = tk.Frame(self, bg=Config.COLOR_WHITE, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card,
            text="Novo Endereço",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY,
        ).pack(pady=(0, 20))

        # Campos
        self.ent_cep = self._create_field(card, "CEP (somente números)")
        self.ent_logradouro = self._create_field(
            card, "Logradouro (Rua, Av.)", width=40
        )

        row1 = tk.Frame(card, bg=Config.COLOR_WHITE)
        row1.pack(fill="x")
        self.ent_numero = self._create_field(row1, "Número", side="left", width=10)
        self.ent_compl = self._create_field(row1, "Complemento", side="right", width=25)

        self.ent_bairro = self._create_field(card, "Bairro")

        row2 = tk.Frame(card, bg=Config.COLOR_WHITE)
        row2.pack(fill="x")
        self.ent_cidade = self._create_field(row2, "Cidade", side="left", width=25)

        # Estado (Combobox)
        tk.Label(row2, text="UF", bg=Config.COLOR_WHITE, font=Config.FONT_BODY).pack(
            anchor="w", padx=(10, 0)
        )
        self.combo_uf = ttk.Combobox(
            row2,
            values=[
                "AC",
                "AL",
                "AP",
                "AM",
                "BA",
                "CE",
                "DF",
                "ES",
                "GO",
                "MA",
                "MT",
                "MS",
                "MG",
                "PA",
                "PB",
                "PR",
                "PE",
                "PI",
                "RJ",
                "RN",
                "RS",
                "RO",
                "RR",
                "SC",
                "SP",
                "SE",
                "TO",
            ],
            width=5,
            state="readonly",
        )
        self.combo_uf.pack(side="right", fill="x", pady=(0, 15))

        # Botões
        btn_frame = tk.Frame(card, bg=Config.COLOR_WHITE)
        btn_frame.pack(pady=20, fill="x")

        # Botão Cancelar -> Volta para o Checkout
        tk.Button(
            btn_frame,
            text="Cancelar",
            bg=Config.COLOR_SECONDARY,
            fg="white",
            width=12,
            command=lambda: self.controller.show_view(
                "CheckoutView", data=self.usuario
            ),
        ).pack(side="left")

        # Botão Salvar
        tk.Button(
            btn_frame,
            text="Salvar Endereço",
            bg=Config.COLOR_PRIMARY,
            fg="white",
            width=15,
            command=self._handle_save,
        ).pack(side="right")

    def _create_field(self, parent, label, side=None, width=30):
        container = tk.Frame(parent, bg=Config.COLOR_WHITE)
        if side:
            container.pack(side=side, padx=(0 if side == "left" else 10, 0))
        else:
            container.pack(fill="x")

        tk.Label(
            container, text=label, bg=Config.COLOR_WHITE, font=Config.FONT_BODY
        ).pack(anchor="w")
        entry = tk.Entry(container, width=width, font=Config.FONT_BODY, bg="#F8F9FA")
        entry.pack(pady=(0, 15))
        return entry

    def _handle_save(self):
        # Coleta dados da tela
        dados = {
            "cep": self.ent_cep.get(),
            "logradouro": self.ent_logradouro.get(),
            "numero": self.ent_numero.get(),
            "complemento": self.ent_compl.get(),
            "bairro": self.ent_bairro.get(),
            "cidade": self.ent_cidade.get(),
            "estado": self.combo_uf.get(),
        }

        # Chama o Controller
        resultado = self.checkout_controller.add_address(dados)

        if resultado["success"]:
            messagebox.showinfo("Sucesso", resultado["message"])
            # Redireciona de volta para o Checkout para continuar a compra
            self.controller.show_view("CheckoutView", data=self.usuario)
        else:
            messagebox.showerror("Erro", resultado["message"])
