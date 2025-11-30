"""
Testes para Controllers
=======================

Conftest para testes de controllers.
"""
import pytest
import sys
import os

# Adiciona diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset automático de mocks entre testes."""
    yield
    # Cleanup após cada teste
