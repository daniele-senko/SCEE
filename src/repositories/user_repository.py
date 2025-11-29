from typing import Optional, List
from src.repositories.base_repository import BaseRepository
from src.models.users.user_model import Usuario
from src.models.users.client_model import Cliente
from src.models.users.admin_model import Administrador

class UsuarioRepository(BaseRepository[Usuario]):
    """
    Repositório especializado em persistência de Usuários.
    Adaptado para trabalhar com SQLite e tabelas separadas.
    """

    def __init__(self):
        super().__init__()

    def salvar(self, usuario: Usuario) -> Usuario:
        conn = self.db.get_connection() 
        cursor = conn.cursor()
        
        try:
            # 1. Insere na tabela usuarios
            if isinstance(usuario, Cliente):
                tipo = 'cliente'
            elif isinstance(usuario, Administrador):
                tipo = 'administrador'
            else:
                tipo = 'cliente'
            
            query = """
                INSERT INTO usuarios (nome, email, senha_hash, tipo)
                VALUES (?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                usuario.nome, 
                usuario.email, 
                usuario.senha_hash, 
                tipo
            ))
            
            usuario._id = cursor.lastrowid
            
            # 2. Insere dados específicos conforme o tipo
            if isinstance(usuario, Cliente):
                cursor.execute("""
                    INSERT INTO clientes_info (usuario_id, cpf, telefone, data_nascimento)
                    VALUES (?, ?, ?, ?)
                """, (usuario._id, usuario.cpf, getattr(usuario, 'telefone', None), 
                      getattr(usuario, 'data_nascimento', None)))
                      
            elif isinstance(usuario, Administrador):
                # Converte string para INTEGER (1-3) ao salvar
                nivel_str = getattr(usuario, 'nivel_acesso', 'padrao')
                nivel_map = {"padrao": 1, "estoquista": 2, "gerente": 3, "admin": 3}
                nivel_int = nivel_map.get(nivel_str, 1)
                
                cursor.execute("""
                    INSERT INTO administradores (usuario_id, cargo, nivel_acesso)
                    VALUES (?, ?, ?)
                """, (usuario._id, getattr(usuario, 'cargo', None), nivel_int))
            
            conn.commit()
            return usuario
            
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Erro ao salvar usuário: {e}")

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Busca usuário básico
        cursor.execute("""
            SELECT id, nome, email, senha_hash, tipo 
            FROM usuarios 
            WHERE email = ?
        """, (email,))
        
        row = cursor.fetchone()
        
        if not row:
            return None
        
        u_id, nome, email, senha_hash, tipo = row
        
        # Busca dados específicos conforme o tipo
        if tipo == 'cliente':
            cursor.execute("""
                SELECT cpf, telefone, data_nascimento 
                FROM clientes_info 
                WHERE usuario_id = ?
            """, (u_id,))
            
            cliente_row = cursor.fetchone()
            if cliente_row:
                cpf, telefone, data_nascimento = cliente_row
                return Cliente(nome, email, cpf, senha_hash, id=u_id)
            
        elif tipo == 'administrador':
            cursor.execute("""
                SELECT cargo, nivel_acesso 
                FROM administradores 
                WHERE usuario_id = ?
            """, (u_id,))
            
            admin_row = cursor.fetchone()
            if admin_row:
                cargo, nivel_acesso_int = admin_row
                # Converte INTEGER (1-3) para string esperada pelo modelo
                nivel_map = {1: "padrao", 2: "estoquista", 3: "gerente"}
                nivel_acesso = nivel_map.get(nivel_acesso_int, "padrao")
                admin = Administrador(nome, email, senha_hash, nivel_acesso=nivel_acesso, id=u_id)
                if cargo:
                    admin.cargo = cargo
                return admin
        
        # Retorna usuário básico se não encontrar dados específicos
        return Usuario(nome, email, senha_hash, id=u_id)

    def buscar_por_id(self, id: int) -> Optional[Usuario]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Busca usuário básico
        cursor.execute("""
            SELECT id, nome, email, senha_hash, tipo 
            FROM usuarios 
            WHERE id = ?
        """, (id,))
        
        row = cursor.fetchone()
        
        if not row:
            return None
        
        u_id, nome, email, senha_hash, tipo = row
        
        # Busca dados específicos conforme o tipo
        if tipo == 'cliente':
            cursor.execute("""
                SELECT cpf, telefone, data_nascimento 
                FROM clientes_info 
                WHERE usuario_id = ?
            """, (u_id,))
            
            cliente_row = cursor.fetchone()
            if cliente_row:
                cpf, telefone, data_nascimento = cliente_row
                return Cliente(nome, email, cpf, senha_hash, id=u_id)
            
        elif tipo == 'administrador':
            cursor.execute("""
                SELECT cargo, nivel_acesso 
                FROM administradores 
                WHERE usuario_id = ?
            """, (u_id,))
            
            admin_row = cursor.fetchone()
            if admin_row:
                cargo, nivel_acesso_int = admin_row
                # Converte INTEGER (1-3) para string esperada pelo modelo
                nivel_map = {1: "padrao", 2: "estoquista", 3: "gerente"}
                nivel_acesso = nivel_map.get(nivel_acesso_int, "padrao")
                admin = Administrador(nome, email, senha_hash, nivel_acesso=nivel_acesso, id=u_id)
                if cargo:
                    admin.cargo = cargo
                return admin
        
        return Usuario(nome, email, senha_hash, id=u_id)
    
    def listar(self) -> List[Usuario]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM usuarios")
        rows = cursor.fetchall()
        
        usuarios = []
        for row in rows:
            usuario = self.buscar_por_id(row[0])
            if usuario:
                usuarios.append(usuario)
        
        return usuarios
    
    def deletar(self, id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # O CASCADE vai deletar automaticamente de clientes_info ou administradores
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Erro ao deletar usuário: {e}")
