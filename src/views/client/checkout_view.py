import tkinter as tk
from tkinter import messagebox, ttk
from src.config.settings import Config
from src.controllers.checkout_controller import CheckoutController
from src.controllers.cart_controller import CartController
from decimal import Decimal


class CheckoutView(tk.Frame):
    """
    Tela de Finalização de Compra.
    Permite selecionar endereço, método de pagamento e confirmar pedido.
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data  # Usuário logado
        self.checkout_controller = CheckoutController(controller)
        self.cart_controller = CartController(controller)
        
        if self.usuario:
            self.checkout_controller.set_current_user(self.usuario.id)
            self.cart_controller.set_current_user(self.usuario.id)
        
        self.selected_address_id = None
        self.selected_payment_method = None
        self.cart_total = Decimal('0.00')
        
        self._setup_header()
        self._setup_content()
        self._load_data()

    def _setup_header(self):
        """Barra superior."""
        header = tk.Frame(self, bg=Config.COLOR_PRIMARY, padx=20, pady=15)
        header.pack(fill="x")
        
        tk.Label(
            header, 
            text="Finalizar Compra", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_PRIMARY, 
            fg="white"
        ).pack(side="left")

        tk.Button(
            header, 
            text="← Voltar ao Carrinho", 
            bg=Config.COLOR_ACCENT, 
            fg="white",
            font=Config.FONT_SMALL,
            command=lambda: self.controller.show_view("CartView", data=self.usuario)
        ).pack(side="right")

    def _setup_content(self):
        """Layout principal com formulário e resumo."""
        # Container principal
        main = tk.Frame(self, bg=Config.COLOR_BG, padx=30, pady=20)
        main.pack(fill="both", expand=True)
        
        # Frame esquerdo (formulário)
        self.form_frame = tk.Frame(main, bg=Config.COLOR_BG)
        self.form_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Frame direito (resumo)
        self.summary_frame = tk.Frame(main, bg=Config.COLOR_WHITE, width=300, padx=20, pady=20)
        self.summary_frame.pack(side="right", fill="y")
        self.summary_frame.pack_propagate(False)

    def _load_data(self):
        """Carrega dados do carrinho e endereços."""
        if not self.usuario:
            tk.Label(
                self.form_frame,
                text="Você precisa estar logado",
                font=Config.FONT_BODY,
                bg=Config.COLOR_BG
            ).pack()
            return
        
        # Busca carrinho
        cart_result = self.cart_controller.get_cart()
        if cart_result['success']:
            carrinho = cart_result.get('data', {})
            self.cart_total = carrinho.get('total', Decimal('0.00'))
            
            if not carrinho.get('itens'):
                messagebox.showwarning("Aviso", "Seu carrinho está vazio!")
                self.controller.show_view("HomeView", data=self.usuario)
                return
        
        # Monta o formulário
        self._setup_address_section()
        self._setup_payment_section()
        self._setup_summary()

    def _setup_address_section(self):
        """Seção de seleção de endereço."""
        # Título
        tk.Label(
            self.form_frame,
            text="1. Endereço de Entrega",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_PRIMARY
        ).pack(anchor="w", pady=(0, 10))
        
        # Busca endereços
        result = self.checkout_controller.get_shipping_addresses()
        
        if not result['success'] or not result.get('data'):
            # Sem endereços cadastrados
            no_address_frame = tk.Frame(self.form_frame, bg=Config.COLOR_WHITE, padx=15, pady=15)
            no_address_frame.pack(fill="x", pady=(0, 20))
            
            tk.Label(
                no_address_frame,
                text="Você ainda não possui endereços cadastrados.",
                font=Config.FONT_BODY,
                bg=Config.COLOR_WHITE
            ).pack()
            
            tk.Label(
                no_address_frame,
                text="Por favor, cadastre um endereço para continuar.",
                font=Config.FONT_SMALL,
                bg=Config.COLOR_WHITE,
                fg=Config.COLOR_TEXT_LIGHT
            ).pack()
            return
        
        enderecos = result['data']
        
        # Frame com scroll para endereços
        address_container = tk.Frame(self.form_frame, bg=Config.COLOR_BG)
        address_container.pack(fill="x", pady=(0, 20))
        
        self.address_var = tk.IntVar()
        
        for endereco in enderecos:
            self._create_address_card(address_container, endereco)
        
        # Seleciona o primeiro ou principal por padrão
        if enderecos:
            principal = next((e for e in enderecos if e.get('principal')), enderecos[0])
            self.address_var.set(principal['id'])
            self.selected_address_id = principal['id']

    def _create_address_card(self, parent, endereco: dict):
        """Cria um card de endereço selecionável."""
        card = tk.Frame(parent, bg=Config.COLOR_WHITE, padx=15, pady=10)
        card.pack(fill="x", pady=5)
        
        # Radiobutton
        rb = tk.Radiobutton(
            card,
            text="",
            variable=self.address_var,
            value=endereco['id'],
            bg=Config.COLOR_WHITE,
            command=lambda: self._select_address(endereco['id'])
        )
        rb.pack(side="left")
        
        # Info do endereço
        info_frame = tk.Frame(card, bg=Config.COLOR_WHITE)
        info_frame.pack(side="left", fill="x", expand=True)
        
        principal_tag = " (Principal)" if endereco.get('principal') else ""
        
        tk.Label(
            info_frame,
            text=f"{endereco.get('rua', '')}, {endereco.get('numero', '')}{principal_tag}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            anchor="w"
        ).pack(anchor="w")
        
        tk.Label(
            info_frame,
            text=f"{endereco.get('cidade', '')} - {endereco.get('estado', '')} | CEP: {endereco.get('cep', '')}",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT,
            anchor="w"
        ).pack(anchor="w")

    def _select_address(self, address_id: int):
        """Callback ao selecionar endereço."""
        self.selected_address_id = address_id

    def _setup_payment_section(self):
        """Seção de seleção de método de pagamento."""
        tk.Label(
            self.form_frame,
            text="2. Forma de Pagamento",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_PRIMARY
        ).pack(anchor="w", pady=(10, 10))
        
        payment_frame = tk.Frame(self.form_frame, bg=Config.COLOR_WHITE, padx=15, pady=15)
        payment_frame.pack(fill="x", pady=(0, 20))
        
        self.payment_var = tk.StringVar(value="cartao")
        self.selected_payment_method = "cartao"
        
        # Opção Cartão
        tk.Radiobutton(
            payment_frame,
            text="💳 Cartão de Crédito",
            variable=self.payment_var,
            value="cartao",
            bg=Config.COLOR_WHITE,
            font=Config.FONT_BODY,
            command=lambda: self._select_payment("cartao")
        ).pack(anchor="w", pady=5)
        
        # Opção PIX
        tk.Radiobutton(
            payment_frame,
            text="📱 PIX (Pagamento pendente após gerar QR Code)",
            variable=self.payment_var,
            value="pix",
            bg=Config.COLOR_WHITE,
            font=Config.FONT_BODY,
            command=lambda: self._select_payment("pix")
        ).pack(anchor="w", pady=5)
        
        # Frame para campos específicos do cartão
        self.card_fields_frame = tk.Frame(payment_frame, bg=Config.COLOR_WHITE)
        self.card_fields_frame.pack(fill="x", pady=(10, 0))
        
        self._setup_card_fields()

    def _setup_card_fields(self):
        """Campos específicos para pagamento com cartão."""
        tk.Label(
            self.card_fields_frame,
            text="Número do Cartão:",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE
        ).pack(anchor="w", pady=(5, 0))
        
        self.entry_card_number = tk.Entry(self.card_fields_frame, font=Config.FONT_BODY, width=30)
        self.entry_card_number.pack(anchor="w", pady=(0, 5))
        self.entry_card_number.insert(0, "4111111111111111")  # Número de teste
        
        row_frame = tk.Frame(self.card_fields_frame, bg=Config.COLOR_WHITE)
        row_frame.pack(fill="x", pady=5)
        
        # Validade
        tk.Label(
            row_frame,
            text="Validade (MM/AA):",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE
        ).pack(side="left", padx=(0, 5))
        
        self.entry_validade = tk.Entry(row_frame, font=Config.FONT_BODY, width=8)
        self.entry_validade.pack(side="left", padx=(0, 20))
        self.entry_validade.insert(0, "12/25")
        
        # CVV
        tk.Label(
            row_frame,
            text="CVV:",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE
        ).pack(side="left", padx=(0, 5))
        
        self.entry_cvv = tk.Entry(row_frame, font=Config.FONT_BODY, width=6, show="*")
        self.entry_cvv.pack(side="left")
        self.entry_cvv.insert(0, "123")

    def _select_payment(self, method: str):
        """Callback ao selecionar método de pagamento."""
        self.selected_payment_method = method
        
        # Mostra/esconde campos do cartão
        if method == "cartao":
            self.card_fields_frame.pack(fill="x", pady=(10, 0))
        else:
            self.card_fields_frame.pack_forget()

    def _setup_summary(self):
        """Resumo do pedido no painel lateral."""
        tk.Label(
            self.summary_frame,
            text="Resumo do Pedido",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT
        ).pack(anchor="w", pady=(0, 20))
        
        # Subtotal
        tk.Label(
            self.summary_frame,
            text=f"Subtotal: R$ {self.cart_total:.2f}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE
        ).pack(anchor="w", pady=5)
        
        # Frete (simulado)
        frete = Decimal('15.00')
        tk.Label(
            self.summary_frame,
            text=f"Frete: R$ {frete:.2f}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE
        ).pack(anchor="w", pady=5)
        
        # Linha divisória
        tk.Frame(self.summary_frame, height=1, bg=Config.COLOR_BG).pack(fill="x", pady=10)
        
        # Total
        total = self.cart_total + frete
        tk.Label(
            self.summary_frame,
            text=f"Total: R$ {total:.2f}",
            font=Config.FONT_TITLE,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY
        ).pack(anchor="w", pady=(10, 20))
        
        # Botão Finalizar
        tk.Button(
            self.summary_frame,
            text="FINALIZAR PEDIDO",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_PRIMARY,
            fg="white",
            width=20,
            cursor="hand2",
            command=self._finalize_order
        ).pack(pady=10)

    def _finalize_order(self):
        """Processa a finalização do pedido."""
        # Validações
        if not self.selected_address_id:
            messagebox.showwarning("Atenção", "Selecione um endereço de entrega!")
            return
        
        if not self.selected_payment_method:
            messagebox.showwarning("Atenção", "Selecione uma forma de pagamento!")
            return
        
        # Prepara dados de pagamento
        dados_pagamento = {}
        
        if self.selected_payment_method == "cartao":
            numero = self.entry_card_number.get().strip()
            cvv = self.entry_cvv.get().strip()
            validade = self.entry_validade.get().strip()
            
            if not numero or not cvv or not validade:
                messagebox.showwarning("Atenção", "Preencha todos os dados do cartão!")
                return
            
            dados_pagamento = {
                'numero': numero,
                'cvv': cvv,
                'validade': validade
            }
        else:  # PIX
            dados_pagamento = {
                'chave_pix': self.usuario.email
            }
        
        # Processa o pedido
        resultado = self.checkout_controller.process_order(
            endereco_id=self.selected_address_id,
            metodo_pagamento=self.selected_payment_method,
            dados_pagamento=dados_pagamento
        )
        
        if resultado['success']:
            if self.selected_payment_method == 'pix':
                messagebox.showinfo(
                    "Pedido Criado", 
                    "Pedido criado com sucesso!\n\nGere o QR Code PIX para concluir o pagamento."
                )
            else:
                messagebox.showinfo("Sucesso", resultado['message'])
        else:
            messagebox.showerror("Erro", resultado['message'])
