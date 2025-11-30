import tkinter as tk
from tkinter import messagebox
from src.config.settings import Config
from src.controllers.admin_controller import AdminController
from src.views.components.custom_button import CustomButton
from src.views.components.data_table import DataTable

# Importamos as funções específicas de modal que já existem
from src.views.components.modal_message import show_success, show_error, show_confirm


class ManageCategoriesView(tk.Frame):
    """
    Tela de gerenciamento de categorias (Admin).
    Permite listar, adicionar, editar e desativar categorias.
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.admin_usuario = data
        self.admin_controller = AdminController(controller)

        # Configurar admin no controller
        if self.admin_usuario and hasattr(self.admin_usuario, "id"):
            self.admin_controller.set_current_admin(self.admin_usuario.id)

        self._build_ui()
        self._load_categories()

    def _build_ui(self):
        """Constrói a interface."""
        self._build_header()

        main_container = tk.Frame(self, bg=Config.COLOR_BG)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self._build_title_section(main_container)
        self._build_table(main_container)

    def _build_header(self):
        """Barra superior com navegação."""
        header = tk.Frame(self, bg=Config.COLOR_PRIMARY, padx=20, pady=15)
        header.pack(fill="x")

        # Título
        tk.Label(
            header,
            text="Gerenciar Categorias",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_PRIMARY,
            fg=Config.COLOR_WHITE,
        ).pack(side="left")

        # Botão Voltar
        CustomButton(
            header,
            text="← Voltar ao Dashboard",
            command=lambda: self.controller.show_view(
                "AdminDashboard", data=self.admin_usuario
            ),
            variant="secondary",  # CORREÇÃO: 'style' alterado para 'variant'
        ).pack(side="right")

    def _build_title_section(self, parent):
        """Seção com título e botão adicionar."""
        title_frame = tk.Frame(parent, bg=Config.COLOR_BG)
        title_frame.pack(fill="x", pady=(0, 20))

        # Título
        tk.Label(
            title_frame,
            text="📂 Categorias Cadastradas",
            font=Config.FONT_TITLE,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT,
        ).pack(side="left")

        # Botão Adicionar
        CustomButton(
            title_frame,
            text="➕ Nova Categoria",
            command=self._open_add_form,
            variant="primary",  # CORREÇÃO: 'style' alterado para 'variant'
        ).pack(side="right")

    def _build_table(self, parent):
        """Tabela de categorias."""
        # Frame da tabela
        table_frame = tk.Frame(parent, bg=Config.COLOR_WHITE, relief="solid", bd=1)
        table_frame.pack(fill="both", expand=True)

        # Cabeçalho
        header_frame = tk.Frame(table_frame, bg=Config.COLOR_PRIMARY)
        header_frame.pack(fill="x")

        headers = [
            ("ID", 8),
            ("Nome", 25),
            ("Descrição", 40),
            ("Status", 12),
            ("Ações", 15),
        ]

        for text, width in headers:
            tk.Label(
                header_frame,
                text=text,
                font=Config.FONT_BODY,
                bg=Config.COLOR_PRIMARY,
                fg=Config.COLOR_WHITE,
                width=width,
                anchor="w",
            ).pack(side="left", padx=5, pady=10)

        # Container com scroll para as linhas
        canvas = tk.Canvas(table_frame, bg=Config.COLOR_WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas, bg=Config.COLOR_WHITE)

        self.rows_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _load_categories(self):
        """Carrega categorias do banco."""
        # Limpar linhas existentes
        for widget in self.rows_frame.winfo_children():
            widget.destroy()

        try:
            # Buscar categorias
            resultado = self.admin_controller.list_all_categories()

            if not resultado["success"]:
                show_error(self, "Erro", resultado["message"])
                return

            categorias = resultado.get("data", [])

            if not categorias:
                tk.Label(
                    self.rows_frame,
                    text="Nenhuma categoria cadastrada",
                    font=Config.FONT_BODY,
                    bg=Config.COLOR_WHITE,
                    fg=Config.COLOR_TEXT_LIGHT,
                ).pack(pady=20)
                return

            # Criar linhas
            for i, cat in enumerate(categorias):
                self._create_category_row(cat, i)

        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
            show_error(self, "Erro Crítico", f"Falha ao carregar categorias: {e}")

    def _create_category_row(self, categoria, index):
        """Cria uma linha da tabela."""
        bg_color = Config.COLOR_WHITE if index % 2 == 0 else "#F5F5F5"

        row = tk.Frame(self.rows_frame, bg=bg_color)
        row.pack(fill="x", pady=1)

        # ID
        tk.Label(
            row,
            text=str(categoria["id"]),
            font=Config.FONT_BODY,
            bg=bg_color,
            fg=Config.COLOR_TEXT,
            width=8,
            anchor="w",
        ).pack(side="left", padx=5, pady=8)

        # Nome
        tk.Label(
            row,
            text=categoria["nome"],
            font=Config.FONT_BODY,
            bg=bg_color,
            fg=Config.COLOR_TEXT,
            width=25,
            anchor="w",
        ).pack(side="left", padx=5, pady=8)

        # Descrição
        descricao = categoria.get("descricao", "")
        if len(descricao) > 45:
            descricao = descricao[:42] + "..."

        tk.Label(
            row,
            text=descricao or "-",
            font=Config.FONT_BODY,
            bg=bg_color,
            fg=Config.COLOR_TEXT_LIGHT,
            width=40,
            anchor="w",
        ).pack(side="left", padx=5, pady=8)

        # Status
        status = "Ativo" if categoria.get("ativo", 1) else "Inativo"
        status_color = (
            Config.COLOR_ACCENT if categoria.get("ativo", 1) else Config.COLOR_SECONDARY
        )

        tk.Label(
            row,
            text=status,
            font=Config.FONT_BODY,
            bg=bg_color,
            fg=status_color,
            width=12,
            anchor="w",
        ).pack(side="left", padx=5, pady=8)

        # Ações
        actions_frame = tk.Frame(row, bg=bg_color)
        actions_frame.pack(side="left", padx=5)

        # Botão Editar
        tk.Button(
            actions_frame,
            text="✏️",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_ACCENT,
            fg=Config.COLOR_WHITE,
            bd=0,
            cursor="hand2",
            width=3,
            command=lambda: self._open_edit_form(categoria),
        ).pack(side="left", padx=2)

        # Botão Ativar/Desativar
        toggle_text = "🔴" if categoria.get("ativo", 1) else "🟢"

        tk.Button(
            actions_frame,
            text=toggle_text,
            font=Config.FONT_SMALL,
            bg=(
                Config.COLOR_SECONDARY
                if categoria.get("ativo", 1)
                else Config.COLOR_ACCENT
            ),
            fg=Config.COLOR_WHITE,
            bd=0,
            cursor="hand2",
            width=3,
            command=lambda: self._toggle_category(
                categoria["id"], not categoria.get("ativo", 1)
            ),
        ).pack(side="left", padx=2)

    def _open_add_form(self):
        """Abre formulário de adicionar categoria."""
        CategoryFormDialog(self, self.admin_controller, on_save=self._load_categories)

    def _open_edit_form(self, categoria):
        """Abre formulário de editar categoria."""
        CategoryFormDialog(
            self,
            self.admin_controller,
            categoria=categoria,
            on_save=self._load_categories,
        )

    def _toggle_category(self, categoria_id, novo_status):
        """Ativa ou desativa uma categoria."""
        acao = "ativar" if novo_status else "desativar"

        if not show_confirm(
            self, "Confirmar", f"Deseja realmente {acao} esta categoria?"
        ):
            return

        resultado = self.admin_controller.toggle_category(categoria_id, novo_status)

        if resultado["success"]:
            show_success(self, "Sucesso", resultado["message"])
            self._load_categories()
        else:
            show_error(self, "Erro", resultado["message"])


class CategoryFormDialog(tk.Toplevel):
    """
    Dialog para adicionar ou editar categoria.
    """

    def __init__(self, parent, controller, categoria=None, on_save=None):
        super().__init__(parent)
        self.controller = controller
        self.categoria = categoria
        self.on_save = on_save

        self.title("Editar Categoria" if categoria else "Nova Categoria")

        self.geometry("500x450")

        self.configure(bg=Config.COLOR_BG)
        self.transient(parent)
        self.grab_set()

        self._build_form()

        # Centralizar
        self.update_idletasks()
        try:
            x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (500 // 2)
            y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (450 // 2)
            self.geometry(f"+{x}+{y}")
        except:
            # Fallback se não conseguir calcular posição relativa
            pass

    def _build_form(self):
        # Container principal com scroll se necessário, mas aqui fixo deve bastar
        container = tk.Frame(self, bg=Config.COLOR_WHITE, padx=30, pady=30)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = "Editar Categoria" if self.categoria else "Nova Categoria"
        tk.Label(
            container,
            text=titulo,
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT,
        ).pack(pady=(0, 20))

        # Nome
        tk.Label(
            container, text="Nome *", font=Config.FONT_BODY, bg=Config.COLOR_WHITE
        ).pack(anchor="w")
        self.nome_entry = tk.Entry(
            container, font=Config.FONT_BODY, bd=1, relief="solid"
        )
        self.nome_entry.pack(fill="x", pady=(0, 15))
        if self.categoria:
            self.nome_entry.insert(0, self.categoria["nome"])

        # Descrição
        tk.Label(
            container, text="Descrição", font=Config.FONT_BODY, bg=Config.COLOR_WHITE
        ).pack(anchor="w")
        self.descricao_text = tk.Text(
            container, font=Config.FONT_BODY, bd=1, relief="solid", height=4
        )
        self.descricao_text.pack(fill="x", pady=(0, 20))
        if self.categoria:
            self.descricao_text.insert("1.0", self.categoria.get("descricao", ""))

        # Botões (Garantindo que apareçam no final)
        btns = tk.Frame(container, bg=Config.COLOR_WHITE)
        btns.pack(fill="x", side="bottom", pady=10)

        CustomButton(btns, text="Salvar", command=self._save, variant="primary").pack(
            side="right"
        )

        CustomButton(
            btns, text="Cancelar", command=self.destroy, variant="secondary"
        ).pack(side="right", padx=(0, 10))

    def _save(self):
        nome = self.nome_entry.get().strip()
        descricao = self.descricao_text.get("1.0", "end-1c").strip()

        if not nome or len(nome) < 3:
            messagebox.showerror("Erro", "Nome deve ter no mínimo 3 caracteres")
            return

        try:
            if self.categoria:
                res = self.controller.update_category(
                    self.categoria["id"], nome, descricao
                )
            else:
                res = self.controller.add_category(nome, descricao)

            if res["success"]:
                messagebox.showinfo("Sucesso", res["message"])
                if self.on_save:
                    self.on_save()
                self.destroy()
            else:
                messagebox.showerror("Erro", res["message"])

        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha ao salvar: {e}")
