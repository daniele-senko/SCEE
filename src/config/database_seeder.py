import sqlite3
from typing import Optional
from src.config.database import DatabaseConnection
from src.utils.security.password_hasher import PasswordHasher


class DatabaseSeeder:
    """
    Classe responsável por popular o banco de dados com dados iniciais.
    """
    
    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        """
        Inicializa o DatabaseSeeder.
        
        Args:
            db_connection: Instância de DatabaseConnection (opcional).
        """
        self.db = db_connection if db_connection else DatabaseConnection()
        self.conn = self.db.get_connection()
    
    def seed_categorias(self):
        """Insere categorias iniciais."""
        cursor = self.conn.cursor()
        
        categorias = [
            (1, 'Eletrônicos', 'Produtos eletrônicos e tecnologia', 1),
            (2, 'Roupas', 'Vestuário masculino e feminino', 1),
            (3, 'Livros', 'Livros e publicações', 1),
            (4, 'Casa e Decoração', 'Produtos para casa e decoração', 1),
            (5, 'Esportes', 'Artigos esportivos e fitness', 1)
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO categorias (id, nome, descricao, ativo) VALUES (?, ?, ?, ?)",
            categorias
        )
        self.conn.commit()
    
    def seed_produtos(self):
        """Insere produtos iniciais."""
        cursor = self.conn.cursor()
        
        produtos = [
            # Eletrônicos
            (1, 'Fone de Ouvido Bluetooth', 'Fone sem fio com cancelamento de ruído', 199.90, 'ELET-FONE-001', 1, 50, 1),
            (2, 'Mouse Gamer RGB', 'Mouse óptico com iluminação RGB e 7 botões programáveis', 129.90, 'ELET-MOUSE-001', 1, 30, 1),
            (3, 'Teclado Mecânico', 'Teclado mecânico com switches blue', 299.90, 'ELET-TEC-001', 1, 25, 1),
            (4, 'Webcam Full HD', 'Webcam 1080p com microfone integrado', 249.90, 'ELET-WEB-001', 1, 15, 1),
            
            # Roupas
            (5, 'Camiseta Básica Preta', 'Camiseta 100% algodão tamanho M', 39.90, 'ROUPA-CAM-001', 2, 100, 1),
            (6, 'Calça Jeans Masculina', 'Calça jeans slim fit azul escuro', 149.90, 'ROUPA-CALCA-001', 2, 60, 1),
            (7, 'Jaqueta Corta-Vento', 'Jaqueta impermeável com capuz', 189.90, 'ROUPA-JAQ-001', 2, 40, 1),
            
            # Livros
            (8, 'Clean Code', 'Guia de boas práticas de programação', 89.90, 'LIVRO-PROG-001', 3, 20, 1),
            (9, 'Design Patterns', 'Padrões de projeto orientados a objetos', 95.90, 'LIVRO-PROG-002', 3, 15, 1),
            (10, 'Python Cookbook', 'Receitas práticas de Python', 79.90, 'LIVRO-PROG-003', 3, 25, 1),
            
            # Casa e Decoração
            (11, 'Luminária LED', 'Luminária de mesa com regulagem de intensidade', 69.90, 'CASA-LUM-001', 4, 35, 1),
            (12, 'Quadro Decorativo', 'Quadro abstrato 40x60cm', 129.90, 'CASA-QUAD-001', 4, 20, 1),
            
            # Esportes
            (13, 'Garrafa Térmica 1L', 'Garrafa térmica de aço inoxidável', 59.90, 'ESP-GARR-001', 5, 80, 1),
            (14, 'Tapete de Yoga', 'Tapete antiderrapante para yoga e pilates', 99.90, 'ESP-TAP-001', 5, 45, 1),
            (15, 'Halteres 5kg (Par)', 'Par de halteres emborrachados', 119.90, 'ESP-HALT-001', 5, 30, 1)
        ]
        
        cursor.executemany(
            """INSERT OR IGNORE INTO produtos 
               (id, nome, descricao, preco, sku, categoria_id, estoque, ativo) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            produtos
        )
        self.conn.commit()
    
    def seed_imagens_produto(self):
        """Insere URLs de imagens dos produtos."""
        cursor = self.conn.cursor()
        
        imagens = [
            (1, '/images/produtos/fone-bluetooth-1.jpg', 1),
            (1, '/images/produtos/fone-bluetooth-2.jpg', 2),
            (2, '/images/produtos/mouse-gamer-1.jpg', 1),
            (3, '/images/produtos/teclado-mecanico-1.jpg', 1),
            (4, '/images/produtos/webcam-1.jpg', 1),
            (5, '/images/produtos/camiseta-preta-1.jpg', 1),
            (6, '/images/produtos/calca-jeans-1.jpg', 1),
            (7, '/images/produtos/jaqueta-1.jpg', 1),
            (8, '/images/produtos/clean-code-1.jpg', 1),
            (9, '/images/produtos/design-patterns-1.jpg', 1),
            (10, '/images/produtos/python-cookbook-1.jpg', 1),
            (11, '/images/produtos/luminaria-1.jpg', 1),
            (12, '/images/produtos/quadro-1.jpg', 1),
            (13, '/images/produtos/garrafa-1.jpg', 1),
            (14, '/images/produtos/tapete-yoga-1.jpg', 1),
            (15, '/images/produtos/halteres-1.jpg', 1)
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO imagens_produto (produto_id, url, prioridade) VALUES (?, ?, ?)",
            imagens
        )
        self.conn.commit()
    
    def seed_usuario_admin(self):
        """Insere usuário administrador padrão."""
        cursor = self.conn.cursor()
        
        # Usuário: admin@scee.com | Senha: admin123
        senha_hash_admin = PasswordHasher.hash_password('admin123')
        cursor.execute(
            """INSERT OR IGNORE INTO usuarios (id, nome, email, senha_hash, tipo) 
               VALUES (?, ?, ?, ?, ?)""",
            (1, 'Administrador', 'admin@scee.com', senha_hash_admin, 'administrador')
        )
        
        cursor.execute(
            """INSERT OR IGNORE INTO administradores (usuario_id, cargo, nivel_acesso) 
               VALUES (?, ?, ?)""",
            (1, 'Administrador Geral', 3)
        )
        
        self.conn.commit()
    
    def seed_usuario_cliente(self):
        """Insere usuário cliente de exemplo."""
        cursor = self.conn.cursor()
        
        # Usuário: joao@email.com | Senha: cliente123
        senha_hash_cliente = PasswordHasher.hash_password('cliente123')
        cursor.execute(
            """INSERT OR IGNORE INTO usuarios (id, nome, email, senha_hash, tipo) 
               VALUES (?, ?, ?, ?, ?)""",
            (2, 'João Silva', 'joao@email.com', senha_hash_cliente, 'cliente')
        )
        
        cursor.execute(
            """INSERT OR IGNORE INTO clientes_info (usuario_id, cpf, telefone, data_nascimento) 
               VALUES (?, ?, ?, ?)""",
            (2, '123.456.789-00', '(11) 98765-4321', '1990-05-15')
        )
        
        cursor.execute(
            """INSERT OR IGNORE INTO enderecos 
               (usuario_id, logradouro, numero, complemento, bairro, cidade, estado, cep, principal) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (2, 'Rua das Flores', '123', 'Apto 45', 'Centro', 'São Paulo', 'SP', '01234-567', 1)
        )
        
        self.conn.commit()
    
    def seed_all(self):
        """Executa todos os seeds."""
        try:
            self.seed_categorias()
            self.seed_produtos()
            self.seed_imagens_produto()
            self.seed_usuario_admin()
            self.seed_usuario_cliente()
            
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao popular banco de dados: {e}")
            raise
    
    def check_if_seeded(self) -> bool:
        """
        Verifica se o banco já foi populado com dados iniciais.
        
        Returns:
            bool: True se já existe dados, False caso contrário.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM categorias")
        count = cursor.fetchone()[0]
        return count > 0
