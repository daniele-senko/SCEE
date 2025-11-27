import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.models.users.client_model import Cliente
from src.repositories.user_repository import UsuarioRepository
from src.utils.security.password_hasher import PasswordHasher

repo = UsuarioRepository()
senha = PasswordHasher.hash_password("cliente123")
try:
    # Cria cliente: Nome, Email, CPF, Senha
    cli = Cliente("João Cliente", "joao@email.com", "12345678900", senha)
    repo.salvar(cli)
    print("✅ Cliente criado: joao@email.com / cliente123")
except Exception as e:
    print(f"❌ Erro: {e}")