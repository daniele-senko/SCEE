from typing import Optional, List
from src.repositories.base_repository import BaseRepository
from src.models.users.user_model import Usuario
from src.models.users.client_model import Cliente
from src.models.users.admin_model import Administrador

class UsuarioRepository(BaseRepository[Usuario]):
    """
    Repositório especializado em persistência de Usuários.
    """

    def __init__(self):
        # Chama o construtor do Pai (BaseRepository) que agora não pede nada
        super().__init__()

    def salvar(self, usuario: Usuario) -> Usuario:
        # Usa o self.db herdado da Base
        conn = self.db.get_connection() 
        cursor = conn.cursor()
        
        # Define valores padrão
        tipo = 'padrao'
        cpf = None
        nivel_acesso = None

        # Polimorfismo: verifica o tipo da classe
        if isinstance(usuario, Cliente):
            tipo = 'cliente'
            cpf = usuario.cpf
        elif isinstance(usuario, Administrador):
            tipo = 'admin'
            nivel_acesso = usuario.nivel_acesso

        query = """
            INSERT INTO usuarios (nome, email, senha_hash, cpf, nivel_acesso, tipo)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        try:
            cursor.execute(query, (
                usuario.nome, 
                usuario.email, 
                usuario.senha_hash, 
                cpf, 
                nivel_acesso, 
                tipo
            ))
            conn.commit()
            usuario._id = cursor.lastrowid
            return usuario
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Erro ao salvar usuário: {e}")

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nome, email, senha_hash, cpf, nivel_acesso, tipo FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        
        if not row:
            return None
            
        return self._mapear_tupla_para_objeto(row)

    def _mapear_tupla_para_objeto(self, row: tuple) -> Usuario:
        u_id, nome, email, senha, cpf, nivel, tipo = row
        
        if tipo == 'cliente':
            return Cliente(nome, email, cpf, senha, id=u_id)
        elif tipo == 'admin':
            return Administrador(nome, email, senha, nivel_acesso=nivel, id=u_id)
        else:
            return Usuario(nome, email, senha, id=u_id)

    # Métodos obrigatórios da interface (Implementação básica)
    def buscar_por_id(self, id: int) -> Optional[Usuario]:
        pass
    def listar(self) -> List[Usuario]:
        pass
    def deletar(self, id: int) -> bool:
        pass