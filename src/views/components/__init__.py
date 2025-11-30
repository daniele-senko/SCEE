"""
Componentes reutilizáveis para a interface Tkinter.

Este módulo contém componentes visuais customizados que podem ser usados
em todo o sistema, facilitando a construção de interfaces consistentes.
"""

# Botões
from src.views.components.custom_button import CustomButton, IconButton

# Campos de formulário
from src.views.components.form_field import FormField, SearchField, SelectField

# Modais e notificações
from src.views.components.modal_message import (
    Modal, 
    LoadingModal, 
    ToastNotification,
    show_info,
    show_success,
    show_warning,
    show_error,
    show_confirm
)

# Cards
from src.views.components.card import (
    Card,
    StatCard,
    InfoCard,
    CollapsibleCard
)

# Tabelas
from src.views.components.data_table import DataTable, SimpleTable

# Produtos
from src.views.components.product_card import ProductCard

__all__ = [
    # Botões
    'CustomButton',
    'IconButton',
    
    # Formulários
    'FormField',
    'SearchField',
    'SelectField',
    
    # Modais
    'Modal',
    'LoadingModal',
    'ToastNotification',
    'show_info',
    'show_success',
    'show_warning',
    'show_error',
    'show_confirm',
    
    # Cards
    'Card',
    'StatCard',
    'InfoCard',
    'CollapsibleCard',
    
    # Tabelas
    'DataTable',
    'SimpleTable',
    
    # Produtos
    'ProductCard'
]
