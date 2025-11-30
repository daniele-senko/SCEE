"""
Camada de Controllers - SCEE
============================

Controllers orquestram o fluxo entre Views e Services, implementando
o padrão MVC (Model-View-Controller).

Responsabilidades:
- Receber eventos da View
- Validar inputs básicos
- Chamar Services apropriados
- Decidir navegação entre Views
- Tratar exceções e converter em mensagens de UI

Estrutura:
- BaseController: Classe abstrata base
- AuthController: Autenticação e registro
- CatalogController: Produtos e categorias
- CartController: Carrinho de compras
- OrderController: Pedidos
- AdminController: Administração
"""

from src.controllers.base_controller import BaseController
from src.controllers.auth_controller import AuthController
from src.controllers.catalog_controller import CatalogController
from src.controllers.cart_controller import CartController
from src.controllers.order_controller import OrderController
from src.controllers.admin_controller import AdminController

__all__ = [
    'BaseController',
    'AuthController',
    'CatalogController',
    'CartController',
    'OrderController',
    'AdminController',
]
