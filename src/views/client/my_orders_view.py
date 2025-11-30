import tkinter as tk
from tkinter import messagebox
from src.config.settings import Config
from src.controllers.order_controller import OrderController
from datetime import datetime


class MyOrdersView(tk.Frame):
    """
    Tela de Histórico de Pedidos do Cliente.
    Exibe todos os pedidos realizados com status e detalhes.
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data  # Usuário logado
        self.order_controller = OrderController(controller)
        
        if self.usuario:
            self.order_controller.set_current_user(self.usuario.id)
        
        self._setup_header()
        self._setup_content()
        self._load_orders()

    def _setup_header(self):
        """Barra superior."""
        header = tk.Frame(self, bg=Config.COLOR_PRIMARY, padx=20, pady=15)
        header.pack(fill="x")
        
        tk.Label(
            header, 
            text="Meus Pedidos", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_PRIMARY, 
            fg="white"
        ).pack(side="left")

        tk.Button(
            header, 
            text="← Voltar", 
            bg=Config.COLOR_ACCENT, 
            fg="white",
            font=Config.FONT_SMALL,
            command=lambda: self.controller.show_view("HomeView", data=self.usuario)
        ).pack(side="right")

    def _setup_content(self):
        """Área principal para lista de pedidos."""
        self.main_container = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)

    def _load_orders(self):
        """Carrega os pedidos do usuário."""
        if not self.usuario:
            tk.Label(
                self.main_container,
                text="Você precisa estar logado para ver seus pedidos.",
                font=Config.FONT_BODY,
                bg=Config.COLOR_BG
            ).pack(pady=20)
            return
        
        # Busca pedidos
        resultado = self.order_controller.get_my_orders()
        
        if not resultado['success']:
            tk.Label(
                self.main_container,
                text="Erro ao carregar pedidos.",
                font=Config.FONT_BODY,
                bg=Config.COLOR_BG,
                fg=Config.COLOR_SECONDARY
            ).pack(pady=20)
            return
        
        pedidos = resultado.get('data', [])
        
        if not pedidos:
            # Sem pedidos
            tk.Label(
                self.main_container,
                text="Você ainda não fez nenhum pedido",
                font=Config.FONT_HEADER,
                bg=Config.COLOR_BG
            ).pack(pady=40)
            
            tk.Label(
                self.main_container,
                text="Explore nossos produtos e faça seu primeiro pedido!",
                font=Config.FONT_BODY,
                bg=Config.COLOR_BG,
                fg=Config.COLOR_TEXT_LIGHT
            ).pack()
            
            tk.Button(
                self.main_container,
                text="Ver Produtos",
                font=Config.FONT_HEADER,
                bg=Config.COLOR_PRIMARY,
                fg="white",
                cursor="hand2",
                command=lambda: self.controller.show_view("HomeView", data=self.usuario)
            ).pack(pady=20)
            return
        
        # Título
        tk.Label(
            self.main_container,
            text=f"Total de {len(pedidos)} pedido(s) encontrado(s)",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BG
        ).pack(anchor="w", pady=(0, 15))
        
        # Frame com scroll para pedidos
        canvas = tk.Canvas(self.main_container, bg=Config.COLOR_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Config.COLOR_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Renderiza cada pedido
        for pedido in pedidos:
            self._create_order_card(scrollable_frame, pedido)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _create_order_card(self, parent, pedido: dict):
        """Cria um card para cada pedido."""
        card = tk.Frame(parent, bg=Config.COLOR_WHITE, padx=20, pady=15)
        card.pack(fill="x", pady=8)
        
        # Cabeçalho do pedido
        header_frame = tk.Frame(card, bg=Config.COLOR_WHITE)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # ID do pedido
        tk.Label(
            header_frame,
            text=f"Pedido #{pedido.get('id', 'N/A')}",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY
        ).pack(side="left")
        
        # Status
        status = pedido.get('status', 'DESCONHECIDO')
        status_color = self._get_status_color(status)
        
        tk.Label(
            header_frame,
            text=self._format_status(status),
            font=Config.FONT_BODY,
            bg=status_color,
            fg="white",
            padx=10,
            pady=3
        ).pack(side="right")
        
        # Informações do pedido
        info_frame = tk.Frame(card, bg=Config.COLOR_WHITE)
        info_frame.pack(fill="x", pady=5)
        
        # Data
        data_pedido = pedido.get('created_at', datetime.now())
        if isinstance(data_pedido, str):
            try:
                data_pedido = datetime.fromisoformat(data_pedido)
            except:
                data_pedido = datetime.now()
        
        tk.Label(
            info_frame,
            text=f"📅 Data: {data_pedido.strftime('%d/%m/%Y %H:%M')}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(side="left", padx=(0, 20))
        
        # Total
        total = pedido.get('total', 0.0)
        tk.Label(
            info_frame,
            text=f"💰 Total: R$ {total:.2f}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(side="left", padx=(0, 20))
        
        # Quantidade de itens
        qtd_itens = len(pedido.get('itens', []))
        tk.Label(
            info_frame,
            text=f"📦 {qtd_itens} item(ns)",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(side="left")
        
        # Linha divisória
        tk.Frame(card, height=1, bg=Config.COLOR_BG).pack(fill="x", pady=10)
        
        # Botões de ação
        actions_frame = tk.Frame(card, bg=Config.COLOR_WHITE)
        actions_frame.pack(fill="x")
        
        # Botão Ver Detalhes
        tk.Button(
            actions_frame,
            text="Ver Detalhes",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_ACCENT,
            fg="white",
            cursor="hand2",
            command=lambda: self._view_order_details(pedido.get('id'))
        ).pack(side="left", padx=(0, 10))
        
        # Botão Cancelar (apenas se status permitir)
        if status in ['PROCESSANDO', 'PAGAMENTO_CONFIRMADO']:
            tk.Button(
                actions_frame,
                text="Cancelar Pedido",
                font=Config.FONT_SMALL,
                bg=Config.COLOR_SECONDARY,
                fg="white",
                cursor="hand2",
                command=lambda: self._cancel_order(pedido.get('id'))
            ).pack(side="left")

    def _get_status_color(self, status: str) -> str:
        """Retorna a cor de acordo com o status."""
        colors = {
            'PROCESSANDO': '#3498DB',       # Azul
            'PAGAMENTO_CONFIRMADO': '#2ECC71',  # Verde
            'PAGAMENTO_PENDENTE': '#F39C12',    # Laranja
            'SEPARANDO': '#9B59B6',         # Roxo
            'ENVIADO': '#1ABC9C',           # Verde água
            'ENTREGUE': '#27AE60',          # Verde escuro
            'CANCELADO': '#E74C3C',         # Vermelho
            'DEVOLVIDO': '#95A5A6'          # Cinza
        }
        return colors.get(status, Config.COLOR_TEXT_LIGHT)

    def _format_status(self, status: str) -> str:
        """Formata o status para exibição."""
        formats = {
            'PROCESSANDO': 'Processando',
            'PAGAMENTO_CONFIRMADO': 'Pagamento Confirmado',
            'PAGAMENTO_PENDENTE': 'Aguardando Pagamento',
            'SEPARANDO': 'Em Separação',
            'ENVIADO': 'Enviado',
            'ENTREGUE': 'Entregue',
            'CANCELADO': 'Cancelado',
            'DEVOLVIDO': 'Devolvido'
        }
        return formats.get(status, status)

    def _view_order_details(self, order_id: int):
        """Exibe detalhes do pedido."""
        resultado = self.order_controller.get_order_details(order_id)
        
        if resultado['success']:
            pedido = resultado['data']
            
            # Monta mensagem com detalhes
            itens_text = "\n".join([
                f"• {item.get('nome_produto', 'Produto')} - "
                f"{item.get('quantidade')}x R$ {item.get('preco_unitario', 0):.2f} = "
                f"R$ {item.get('subtotal', 0):.2f}"
                for item in pedido.get('itens', [])
            ])
            
            detalhes = f"""
Pedido #{pedido.get('id')}
Status: {self._format_status(pedido.get('status', ''))}

Itens:
{itens_text}

Subtotal: R$ {pedido.get('subtotal', 0):.2f}
Frete: R$ {pedido.get('frete', 0):.2f}
Total: R$ {pedido.get('total', 0):.2f}

Forma de Pagamento: {pedido.get('forma_pagamento', 'N/A')}
"""
            
            messagebox.showinfo("Detalhes do Pedido", detalhes)
        else:
            messagebox.showerror("Erro", resultado['message'])

    def _cancel_order(self, order_id: int):
        """Cancela um pedido."""
        if messagebox.askyesno("Confirmar", "Deseja realmente cancelar este pedido?"):
            resultado = self.order_controller.cancel_order(order_id)
            
            if resultado['success']:
                messagebox.showinfo("Sucesso", "Pedido cancelado com sucesso!")
                self._reload_orders()
            else:
                messagebox.showerror("Erro", resultado['message'])

    def _reload_orders(self):
        """Recarrega a lista de pedidos."""
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        self._load_orders()
