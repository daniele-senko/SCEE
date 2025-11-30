"""
BaseController - Controlador Base Abstrato
==========================================

Classe abstrata que define o contrato para todos os controllers.
"""
from abc import ABC
from typing import Dict, Any, Optional


class BaseController(ABC):
    """
    Classe base abstrata para todos os controllers.
    
    Responsabilidades:
    - Gerenciar referência à MainWindow (navegação)
    - Padronizar formato de respostas
    - Fornecer métodos utilitários comuns
    """
    
    def __init__(self, main_window):
        """
        Inicializa o controller com referência à janela principal.
        
        Args:
            main_window: Instância de MainWindow para navegação
        """
        self.main_window = main_window
    
    def _success_response(self, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Cria resposta de sucesso padronizada.
        
        Args:
            message: Mensagem de sucesso
            data: Dados opcionais para retornar
            
        Returns:
            Dicionário com success=True, message e data
        """
        return {
            'success': True,
            'message': message,
            'data': data
        }
    
    def _error_response(self, message: str, error: Optional[Exception] = None) -> Dict[str, Any]:
        """
        Cria resposta de erro padronizada.
        
        Args:
            message: Mensagem de erro amigável
            error: Exceção original (opcional)
            
        Returns:
            Dicionário com success=False, message e error
        """
        return {
            'success': False,
            'message': message,
            'error': str(error) if error else None
        }
    
    def _validate_not_empty(self, value: str, field_name: str) -> Optional[str]:
        """
        Valida se campo não está vazio.
        
        Args:
            value: Valor a validar
            field_name: Nome do campo (para mensagem)
            
        Returns:
            Mensagem de erro ou None se válido
        """
        if not value or not value.strip():
            return f"{field_name} não pode estar vazio"
        return None
    
    def _validate_min_length(self, value: str, field_name: str, min_length: int) -> Optional[str]:
        """
        Valida tamanho mínimo.
        
        Args:
            value: Valor a validar
            field_name: Nome do campo
            min_length: Tamanho mínimo
            
        Returns:
            Mensagem de erro ou None se válido
        """
        if len(value) < min_length:
            return f"{field_name} deve ter pelo menos {min_length} caracteres"
        return None
    
    def navigate_to(self, view_name: str, data: Optional[Any] = None) -> None:
        """
        Navega para outra view.
        
        Args:
            view_name: Nome da view de destino
            data: Dados opcionais para passar
        """
        self.main_window.show_view(view_name, data)
