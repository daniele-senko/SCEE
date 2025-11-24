import hashlib
import secrets

class PasswordHasher:
    """
    Responsável pela criptografia e verificação de senhas.
    Utiliza PBKDF2 (padrão robusto) com SHA256 e Salt aleatório.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Cria um hash seguro da senha com um salt aleatório.
        :param password: Senha em texto plano
        :return: String no formato 'salt$hash_hex'
        """
        # Gera um salt aleatório de 16 bytes
        salt = secrets.token_hex(16)
        
        # Cria o hash usando PBKDF2 (100.000 iterações)
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        
        # Retorna salt e hash juntos separados por $
        return f"{salt}${hash_obj.hex()}"

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """
        Verifica se a senha fornecida bate com o hash armazenado.
        :param stored_password: O hash completo salvo no banco (salt$hash)
        :param provided_password: A senha que o usuário digitou no login
        :return: True se conferir
        """
        try:
            salt, stored_hash = stored_password.split('$')
            
            # Recalcula o hash com o mesmo salt e senha fornecida
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                provided_password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            
            # Compara os hashes de forma segura
            return secrets.compare_digest(stored_hash, new_hash.hex())
        except ValueError:
            return False