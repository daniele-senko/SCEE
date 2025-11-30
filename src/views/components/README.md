# Componentes Reutilizáveis do Sistema

Este diretório contém componentes visuais customizados para uso em todo o sistema.

## 📦 Componentes Disponíveis

### 1. **Botões** (`custom_button.py`)

#### CustomButton
Botão estilizado com variantes predefinidas:
```python
from src.views.components import CustomButton

# Botão primário (azul)
btn = CustomButton(parent, text="Salvar", variant="primary", command=salvar)

# Botão secundário (vermelho)
btn = CustomButton(parent, text="Cancelar", variant="secondary")

# Botão de sucesso (verde)
btn = CustomButton(parent, text="Confirmar", variant="accent")

# Botão outline
btn = CustomButton(parent, text="Detalhes", variant="outline")
```

**Variantes disponíveis:**
- `primary`: Azul (ações principais)
- `secondary`: Vermelho (cancelar/excluir)
- `accent`: Verde (sucesso/confirmar)
- `outline`: Borda colorida, fundo transparente
- `light`: Cinza claro

#### IconButton
Botão compacto com ícones:
```python
from src.views.components import IconButton

# Com ícone predefinido
btn = IconButton(parent, icon='edit', command=editar, tooltip="Editar produto")
btn = IconButton(parent, icon='delete', command=excluir, tooltip="Excluir")

# Com caractere customizado
btn = IconButton(parent, icon='★', command=favoritar)
```

**Ícones disponíveis:**
`edit`, `delete`, `add`, `remove`, `check`, `close`, `search`, `refresh`, `save`, `download`, `upload`, `settings`, `info`, `warning`, `cart`, `user`

---

### 2. **Campos de Formulário** (`form_field.py`)

#### FormField
Campo de entrada com label e validação:
```python
from src.views.components import FormField

# Campo de texto obrigatório
nome_field = FormField(parent, label="Nome", required=True)

# Campo de senha
senha_field = FormField(parent, label="Senha", field_type="password")

# Campo de número
preco_field = FormField(parent, label="Preço", field_type="number")

# Campo de email com validação
email_field = FormField(parent, label="E-mail", field_type="email")

# Validar campo
if nome_field.validate():
    valor = nome_field.get()

# Mostrar erro customizado
nome_field.show_error("Nome muito curto")

# Limpar erro
nome_field.clear_error()
```

**Tipos de campo:**
- `text`: Texto padrão
- `password`: Senha (oculta caracteres)
- `number`: Apenas números
- `email`: Email com validação

#### SearchField
Campo de busca com ícone e botão limpar:
```python
from src.views.components import SearchField

def on_search(texto):
    print(f"Buscando: {texto}")

search = SearchField(parent, placeholder="Buscar produtos...", on_search=on_search)

# Obter valor
texto = search.get()
```

#### SelectField
Combobox estilizado:
```python
from src.views.components import SelectField

categorias = SelectField(parent, label="Categoria", required=True)
categorias.set_options(["Eletrônicos", "Roupas", "Livros"])

# Obter selecionado
valor = categorias.get()

# Validar
if categorias.validate():
    print("Válido!")
```

---

### 3. **Modais e Notificações** (`modal_message.py`)

#### Funções de Conveniência
```python
from src.views.components import (
    show_info,
    show_success,
    show_warning,
    show_error,
    show_confirm
)

# Informação
show_info(parent, "Aviso", "Operação realizada")

# Sucesso
show_success(parent, "Sucesso!", "Produto cadastrado")

# Aviso
show_warning(parent, "Atenção", "Estoque baixo")

# Erro
show_error(parent, "Erro", "Falha ao conectar")

# Confirmação
result = show_confirm(parent, "Confirmar", "Deseja excluir?")
if result:
    print("Confirmado!")
```

#### Modal Customizado
```python
from src.views.components import Modal

modal = Modal(
    parent,
    title="Título",
    message="Mensagem",
    modal_type="info",  # info, success, warning, error, confirm
    buttons=[
        {'text': 'OK', 'command': lambda: print('OK'), 'bg': '#3B82F6'},
        {'text': 'Cancelar', 'bg': '#9CA3AF'}
    ]
)
result = modal.show()
```

#### LoadingModal
```python
from src.views.components import LoadingModal

loading = LoadingModal(parent, message="Processando...")
# ... operação demorada ...
loading.close()
```

#### ToastNotification
```python
from src.views.components import ToastNotification

# Toast de sucesso (desaparece em 3s)
ToastNotification.show(
    parent,
    "Produto adicionado ao carrinho!",
    duration=3000,
    position='bottom',  # top ou bottom
    toast_type='success'  # info, success, warning, error
)
```

---

### 4. **Cards** (`card.py`)

#### Card
Container estilizado básico:
```python
from src.views.components import Card

# Card simples
card = Card(parent, title="Informações", subtitle="Dados do usuário")
card.add_widget(tk.Label(card.content, text="Nome: João"))

# Card sem sombra
card = Card(parent, elevation=False)
```

#### StatCard
Card de estatística:
```python
from src.views.components import StatCard

# Card de estatística com ícone
stats = StatCard(
    parent,
    label="Total de Vendas",
    value="R$ 15.420,00",
    icon="💰",
    color="#22C55E"
)
```

#### InfoCard
Card informativo com ícone:
```python
from src.views.components import InfoCard

info = InfoCard(
    parent,
    title="Pedido #1234",
    description="Pendente - Aguardando pagamento",
    icon="📦",
    icon_bg="#3B82F6",
    clickable=True,
    on_click=lambda: print("Clicou!")
)
```

#### CollapsibleCard
Card expansível:
```python
from src.views.components import CollapsibleCard

card = CollapsibleCard(parent, title="Detalhes do Pedido")
card.add_content(tk.Label(card.content, text="Item 1"))
card.add_content(tk.Label(card.content, text="Item 2"))

# Programaticamente
card.expand()
card.collapse()
```

---

### 5. **Tabelas** (`data_table.py`)

#### DataTable
Tabela completa com ordenação e paginação:
```python
from src.views.components import DataTable

# Definir colunas
columns = [
    {'id': 'id', 'text': 'ID', 'width': 50},
    {'id': 'nome', 'text': 'Nome', 'width': 200},
    {'id': 'preco', 'text': 'Preço', 'width': 100, 'anchor': 'e'}
]

# Criar tabela
table = DataTable(
    parent,
    columns=columns,
    sortable=True,
    selectable=True,
    paginated=True,
    items_per_page=20
)

# Carregar dados
data = [
    {'id': 1, 'nome': 'Produto A', 'preco': 'R$ 100,00'},
    {'id': 2, 'nome': 'Produto B', 'preco': 'R$ 200,00'}
]
table.load_data(data)

# Obter selecionado
selected = table.get_selected()

# Adicionar linha
table.add_row({'id': 3, 'nome': 'Produto C', 'preco': 'R$ 300,00'})

# Filtrar
table.filter(lambda row: row['preco'] > 100)
```

#### SimpleTable
Tabela simples e leve:
```python
from src.views.components import SimpleTable

table = SimpleTable(parent, columns=["Nome", "Preço", "Estoque"], show_index=True)
table.add_row(["Produto A", "R$ 100", "10"])
table.add_row(["Produto B", "R$ 200", "5"])
```

---

### 6. **ProductCard** (`product_card.py`)

Card de produto para catálogo:
```python
from src.views.components import ProductCard

def adicionar_ao_carrinho(produto):
    print(f"Adicionando {produto.nome}")

card = ProductCard(parent, produto=produto_obj, on_add_click=adicionar_ao_carrinho)
```

---

## 🎨 Benefícios

1. **Consistência Visual**: Todos os componentes seguem o mesmo padrão de design
2. **Reutilização**: Escreva uma vez, use em qualquer lugar
3. **Manutenção Fácil**: Alterações em um lugar refletem em todo o sistema
4. **Validação Integrada**: Campos de formulário com validação automática
5. **Responsividade**: Componentes adaptáveis a diferentes tamanhos

## 📝 Exemplo Completo

```python
import tkinter as tk
from src.views.components import (
    Card,
    FormField,
    CustomButton,
    show_success,
    show_error
)

class MeuFormulario(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Card container
        card = Card(self, title="Cadastro de Produto", elevation=True)
        
        # Campos
        self.nome_field = FormField(
            card.content, 
            label="Nome do Produto", 
            required=True
        )
        
        self.preco_field = FormField(
            card.content,
            label="Preço",
            field_type="number",
            required=True
        )
        
        # Botões
        btn_frame = tk.Frame(card.content)
        btn_frame.pack(fill="x", pady=20)
        
        CustomButton(
            btn_frame,
            text="Cancelar",
            variant="secondary",
            command=self.cancelar
        ).pack(side="left", padx=5)
        
        CustomButton(
            btn_frame,
            text="Salvar",
            variant="accent",
            command=self.salvar
        ).pack(side="right", padx=5)
    
    def salvar(self):
        # Valida todos os campos
        if not self.nome_field.validate():
            return
        if not self.preco_field.validate():
            return
        
        # Salva...
        show_success(self, "Sucesso", "Produto cadastrado!")
    
    def cancelar(self):
        if show_confirm(self, "Confirmar", "Deseja cancelar?"):
            # Fecha formulário...
            pass
```

---

## 🔧 Customização

Todos os componentes aceitam argumentos adicionais do Tkinter via `**kwargs`:

```python
# Customizar aparência
btn = CustomButton(
    parent,
    text="Meu Botão",
    variant="primary",
    width=20,
    font=('Arial', 14),
    pady=15
)
```
