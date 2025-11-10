from config.database import DatabaseConfig
from models.cliente import Usuario
from typing import List, Optional

class UsuarioRepository:
    def __init__(self):
        self.db_config = DatabaseConfig()

    def create(self, usuario: Usuario) -> Optional[int]:
        """Insere um novo usuário no banco"""
        conn = self.db_config.connect()
        if not conn:
            return None

        cursor = conn.cursor()
        query = """
            INSERT INTO usuarios (username, email, password, full_name, is_active)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (
                usuario.username,
                usuario.email,
                usuario.password,
                usuario.full_name,
                usuario.is_active
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def find_by_id(self, user_id: int) -> Optional[Usuario]:
        """Busca um usuário pelo ID"""
        conn = self.db_config.connect()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE id = %s"
        try:
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            return self._map_to_usuario(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def find_by_username(self, username: str) -> Optional[Usuario]:
        """Busca um usuário pelo username"""
        conn = self.db_config.connect()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE username = %s"
        try:
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            return self._map_to_usuario(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def find_all(self) -> List[Usuario]:
        """Retorna todos os usuários"""
        conn = self.db_config.connect()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuarios"
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._map_to_usuario(row) for row in rows]
        finally:
            cursor.close()
            conn.close()

    def update(self, usuario: Usuario) -> bool:
        """Atualiza um usuário existente"""
        conn = self.db_config.connect()
        if not conn:
            return False

        cursor = conn.cursor()
        query = """
            UPDATE usuarios
            SET username = %s, email = %s, password = %s,
                full_name = %s, is_active = %s
            WHERE id = %s
        """
        try:
            cursor.execute(query, (
                usuario.username,
                usuario.email,
                usuario.password,
                usuario.full_name,
                usuario.is_active,
                usuario.id
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def delete(self, user_id: int) -> bool:
        """Remove um usuário pelo ID"""
        conn = self.db_config.connect()
        if not conn:
            return False

        cursor = conn.cursor()
        query = "DELETE FROM usuarios WHERE id = %s"
        try:
            cursor.execute(query, (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def _map_to_usuario(self, row: dict) -> Usuario:
        """Converte um dicionário do banco em objeto Usuario"""
        return Usuario(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password=row['password'],
            full_name=row['full_name'],
            is_active=row['is_active'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )