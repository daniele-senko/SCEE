"""Configurações do projeto SCEE.

Utiliza Pydantic BaseSettings para gerenciar variáveis de ambiente
e configurações do sistema.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configurações principais do projeto."""
    
    # Configurações gerais
    project_name: str = "SCEE - Sistema de Comércio Eletrônico"
    version: str = "1.0.0"
    debug: bool = True
    
    # Configurações de segurança
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 horas
    
    # Configurações do banco de dados
    database_url: str = "sqlite:///./data/scee.db"
    
    # Configurações de API
    api_prefix: str = "/api"
    cors_origins: list = ["*"]  # Em produção, especificar domínios permitidos
    
    # Configurações de paginação
    default_page_size: int = 20
    max_page_size: int = 100
    
    # Configurações de upload
    max_upload_size: int = 5 * 1024 * 1024  # 5MB
    allowed_image_extensions: list = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instância global de configurações
settings = Settings()
