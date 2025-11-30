import tkinter as tk
from tkinter import ttk
from src.config.settings import Config

class DataTable(tk.Frame):
    """
    Tabela de dados reutilizável com ordenação, paginação e seleção.
    """
    
    def __init__(self, parent, columns, data=None, sortable=True, 
                 selectable=True, paginated=False, items_per_page=20):
        """
        Args:
            parent: Widget pai
            columns: Lista de dicionários com configuração das colunas
                     Ex: [{'id': 'nome', 'text': 'Nome', 'width': 200}]
            data: Lista de dicionários com os dados
            sortable: Permite ordenar clicando nos cabeçalhos
            selectable: Permite selecionar linhas
            paginated: Habilita paginação
            items_per_page: Itens por página
        """
        super().__init__(parent, bg=Config.COLOR_WHITE)
        
        self.columns = columns
        self.data = data or []
        self.sortable = sortable
        self.selectable = selectable
        self.paginated = paginated
        self.items_per_page = items_per_page
        self.current_page = 0
        self.sort_column = None
        self.sort_reverse = False
        
        self._setup_ui()
        if data:
            self.load_data(data)
    
    def _setup_ui(self):
        """Configura a interface da tabela."""
        # Container da tabela
        table_container = tk.Frame(self, bg=Config.COLOR_WHITE)
        table_container.pack(fill="both", expand=True)
        
        # Treeview
        column_ids = [col['id'] for col in self.columns]
        
        self.tree = ttk.Treeview(
            table_container,
            columns=column_ids,
            show='headings',
            selectmode='browse' if self.selectable else 'none',
            height=15
        )
        
        # Configura colunas
        for col in self.columns:
            self.tree.heading(
                col['id'],
                text=col['text'],
                command=lambda c=col['id']: self._sort_by_column(c) if self.sortable else None
            )
            self.tree.column(
                col['id'],
                width=col.get('width', 100),
                anchor=col.get('anchor', 'w')
            )
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Paginação (se habilitada)
        if self.paginated:
            self._setup_pagination()
        
        # Estilo de linha alternada
        self.tree.tag_configure('oddrow', background='#F8F9FA')
        self.tree.tag_configure('evenrow', background='white')
    
    def _setup_pagination(self):
        """Configura controles de paginação."""
        self.pagination_frame = tk.Frame(self, bg=Config.COLOR_WHITE, pady=10)
        self.pagination_frame.pack(fill="x")
        
        # Botão anterior
        self.btn_prev = tk.Button(
            self.pagination_frame,
            text="◀ Anterior",
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT,
            font=Config.FONT_SMALL,
            command=self._prev_page,
            cursor='hand2',
            relief='flat',
            padx=10,
            pady=5
        )
        self.btn_prev.pack(side="left", padx=5)
        
        # Info de página
        self.page_label = tk.Label(
            self.pagination_frame,
            text="Página 1 de 1",
            bg=Config.COLOR_WHITE,
            font=Config.FONT_BODY
        )
        self.page_label.pack(side="left", expand=True)
        
        # Botão próximo
        self.btn_next = tk.Button(
            self.pagination_frame,
            text="Próximo ▶",
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT,
            font=Config.FONT_SMALL,
            command=self._next_page,
            cursor='hand2',
            relief='flat',
            padx=10,
            pady=5
        )
        self.btn_next.pack(side="right", padx=5)
    
    def load_data(self, data):
        """Carrega dados na tabela."""
        self.data = data
        self.current_page = 0
        self._refresh_table()
    
    def _refresh_table(self):
        """Atualiza a exibição da tabela."""
        # Limpa dados antigos
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Dados a exibir (com paginação se habilitada)
        if self.paginated:
            start = self.current_page * self.items_per_page
            end = start + self.items_per_page
            display_data = self.data[start:end]
        else:
            display_data = self.data
        
        # Insere dados
        for idx, row in enumerate(display_data):
            values = [row.get(col['id'], '') for col in self.columns]
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=values, tags=(tag,))
        
        # Atualiza paginação
        if self.paginated:
            self._update_pagination()
    
    def _update_pagination(self):
        """Atualiza controles de paginação."""
        total_pages = max(1, (len(self.data) + self.items_per_page - 1) // self.items_per_page)
        self.page_label.config(text=f"Página {self.current_page + 1} de {total_pages}")
        
        # Habilita/desabilita botões
        self.btn_prev.config(state='normal' if self.current_page > 0 else 'disabled')
        self.btn_next.config(state='normal' if self.current_page < total_pages - 1 else 'disabled')
    
    def _prev_page(self):
        """Vai para página anterior."""
        if self.current_page > 0:
            self.current_page -= 1
            self._refresh_table()
    
    def _next_page(self):
        """Vai para próxima página."""
        total_pages = (len(self.data) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self._refresh_table()
    
    def _sort_by_column(self, col_id):
        """Ordena dados por coluna."""
        # Alterna direção se clicar na mesma coluna
        if self.sort_column == col_id:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col_id
            self.sort_reverse = False
        
        # Ordena dados
        self.data.sort(key=lambda x: x.get(col_id, ''), reverse=self.sort_reverse)
        self._refresh_table()
    
    def get_selected(self):
        """Retorna os dados da linha selecionada."""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        # Reconstroi dicionário
        return {col['id']: values[idx] for idx, col in enumerate(self.columns)}
    
    def get_all_selected(self):
        """Retorna todas as linhas selecionadas."""
        selection = self.tree.selection()
        results = []
        
        for item_id in selection:
            item = self.tree.item(item_id)
            values = item['values']
            results.append({col['id']: values[idx] for idx, col in enumerate(self.columns)})
        
        return results
    
    def clear(self):
        """Limpa todos os dados."""
        self.data = []
        self._refresh_table()
    
    def add_row(self, row_data):
        """Adiciona uma linha."""
        self.data.append(row_data)
        self._refresh_table()
    
    def filter(self, predicate):
        """Filtra dados com uma função predicado."""
        filtered = [row for row in self.data if predicate(row)]
        self.data = filtered
        self._refresh_table()


class SimpleTable(tk.Frame):
    """
    Tabela simples sem recursos avançados (mais leve).
    """
    
    def __init__(self, parent, columns, show_index=False):
        """
        Args:
            parent: Widget pai
            columns: Lista de nomes de colunas
            show_index: Mostra índice numérico na primeira coluna
        """
        super().__init__(parent, bg=Config.COLOR_WHITE)
        
        self.columns = columns
        self.show_index = show_index
        self.rows = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a tabela."""
        # Cabeçalho
        header = tk.Frame(self, bg=Config.COLOR_PRIMARY, height=40)
        header.pack(fill="x")
        
        cols = ['#'] + self.columns if self.show_index else self.columns
        
        for idx, col in enumerate(cols):
            tk.Label(
                header,
                text=col,
                bg=Config.COLOR_PRIMARY,
                fg='white',
                font=Config.FONT_BODY,
                padx=10,
                pady=10
            ).grid(row=0, column=idx, sticky='ew')
        
        # Configura pesos das colunas
        for i in range(len(cols)):
            header.grid_columnconfigure(i, weight=1)
        
        # Container das linhas
        self.rows_container = tk.Frame(self, bg=Config.COLOR_WHITE)
        self.rows_container.pack(fill="both", expand=True)
    
    def add_row(self, values):
        """Adiciona uma linha."""
        row_idx = len(self.rows)
        bg_color = '#F8F9FA' if row_idx % 2 == 0 else 'white'
        
        row_frame = tk.Frame(self.rows_container, bg=bg_color)
        row_frame.pack(fill="x")
        
        if self.show_index:
            values = [str(row_idx + 1)] + values
        
        for idx, value in enumerate(values):
            tk.Label(
                row_frame,
                text=str(value),
                bg=bg_color,
                font=Config.FONT_BODY,
                padx=10,
                pady=8
            ).grid(row=0, column=idx, sticky='ew')
        
        # Configura pesos
        for i in range(len(values)):
            row_frame.grid_columnconfigure(i, weight=1)
        
        self.rows.append(row_frame)
    
    def clear(self):
        """Remove todas as linhas."""
        for row in self.rows:
            row.destroy()
        self.rows = []
