import sqlite3
import os
from typing import Optional
from src.config.database import DatabaseConnection
from src.config.settings import Config


class DatabaseInitializer:
    """
    Classe responsável por criar e inicializar o banco de dados SQLite.
    """
    
    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        """
        Inicializa o DatabaseInitializer.
        
        Args:
            db_connection: Instância de DatabaseConnection (opcional).
                          Se não fornecida, cria uma nova instância.
        """
        self.db = db_connection if db_connection else DatabaseConnection()
        self.conn = self.db.get_connection()
    
    def create_schema(self):
        """
        Cria todas as tabelas do sistema no banco SQLite.
        """
        cursor = self.conn.cursor()
        
        try:
            # Habilita chaves estrangeiras
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Tabela de usuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    senha_hash TEXT NOT NULL,
                    tipo TEXT NOT NULL CHECK(tipo IN ('cliente', 'administrador')),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_tipo ON usuarios(tipo);")
            
            # Informações específicas de clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL UNIQUE,
                    cpf TEXT UNIQUE NOT NULL,
                    telefone TEXT,
                    data_nascimento DATE,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_clientes_cpf ON clientes_info(cpf);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_clientes_usuario_id ON clientes_info(usuario_id);")
            
            # Informações específicas de administradores
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS administradores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL UNIQUE,
                    cargo TEXT,
                    nivel_acesso INTEGER DEFAULT 1 CHECK(nivel_acesso >= 1 AND nivel_acesso <= 3),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_administradores_usuario_id ON administradores(usuario_id);")
            
            # Endereços dos clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS enderecos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    logradouro TEXT NOT NULL,
                    numero TEXT NOT NULL,
                    complemento TEXT,
                    bairro TEXT NOT NULL,
                    cidade TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    cep TEXT NOT NULL,
                    principal INTEGER DEFAULT 0,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_enderecos_usuario_id ON enderecos(usuario_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_enderecos_cep ON enderecos(cep);")
            
            # Categorias de produtos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
                    descricao TEXT,
                    ativo INTEGER DEFAULT 1,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_categorias_nome ON categorias(nome);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_categorias_ativo ON categorias(ativo);")
            
            # Produtos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    preco REAL NOT NULL CHECK(preco >= 0),
                    sku TEXT UNIQUE NOT NULL,
                    categoria_id INTEGER,
                    estoque INTEGER DEFAULT 0 CHECK(estoque >= 0),
                    ativo INTEGER DEFAULT 1,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_produtos_sku ON produtos(sku);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_produtos_categoria_id ON produtos(categoria_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_produtos_nome ON produtos(nome);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_produtos_ativo ON produtos(ativo);")
            
            # Imagens dos produtos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS imagens_produto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER NOT NULL,
                    url TEXT NOT NULL,
                    prioridade INTEGER DEFAULT 0,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_imagens_produto_id ON imagens_produto(produto_id);")
            
            # Carrinhos de compras
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS carrinhos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL UNIQUE,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_carrinhos_usuario_id ON carrinhos(usuario_id);")
            
            # Itens do carrinho
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS itens_carrinho (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    carrinho_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
                    preco_unitario REAL NOT NULL CHECK(preco_unitario >= 0),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (carrinho_id) REFERENCES carrinhos(id) ON DELETE CASCADE,
                    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
                    UNIQUE(carrinho_id, produto_id)
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_itens_carrinho_carrinho_id ON itens_carrinho(carrinho_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_itens_carrinho_produto_id ON itens_carrinho(produto_id);")
            
            # Pedidos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    endereco_id INTEGER NOT NULL,
                    subtotal REAL NOT NULL CHECK(subtotal >= 0),
                    frete REAL NOT NULL CHECK(frete >= 0),
                    total REAL NOT NULL CHECK(total >= 0),
                    status TEXT DEFAULT 'PENDENTE' CHECK(status IN ('PENDENTE', 'PROCESSANDO', 'ENVIADO', 'ENTREGUE', 'CANCELADO')),
                    tipo_pagamento TEXT NOT NULL CHECK(tipo_pagamento IN ('CARTAO', 'PIX', 'BOLETO')),
                    observacoes TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
                    FOREIGN KEY (endereco_id) REFERENCES enderecos(id) ON DELETE RESTRICT
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_usuario_id ON pedidos(usuario_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_status ON pedidos(status);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_criado_em ON pedidos(criado_em);")
            
            # Itens do pedido
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS itens_pedido (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pedido_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    nome_produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
                    preco_unitario REAL NOT NULL CHECK(preco_unitario >= 0),
                    subtotal REAL NOT NULL CHECK(subtotal >= 0),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
                    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE RESTRICT
                );
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_itens_pedido_pedido_id ON itens_pedido(pedido_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_itens_pedido_produto_id ON itens_pedido(produto_id);")
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao criar schema: {e}")
            raise
    
    def create_triggers(self):
        """
        Cria os triggers do sistema (validação de estoque, etc).
        SQLite tem limitações em triggers, então alguns serão simplificados.
        """
        cursor = self.conn.cursor()
        
        try:
            # Trigger para validar estoque ao adicionar item no carrinho
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS validate_estoque_carrinho
                BEFORE INSERT ON itens_carrinho
                FOR EACH ROW
                WHEN (SELECT estoque FROM produtos WHERE id = NEW.produto_id) < NEW.quantidade
                BEGIN
                    SELECT RAISE(ABORT, 'Estoque insuficiente para o produto');
                END;
            """)
            
            # Trigger para abater estoque ao criar pedido
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS abater_estoque_pedido
                AFTER INSERT ON itens_pedido
                FOR EACH ROW
                BEGIN
                    UPDATE produtos 
                    SET estoque = estoque - NEW.quantidade 
                    WHERE id = NEW.produto_id;
                END;
            """)
            
            # Trigger para devolver estoque ao cancelar pedido
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS devolver_estoque_pedido
                AFTER UPDATE ON pedidos
                FOR EACH ROW
                WHEN NEW.status = 'CANCELADO' AND OLD.status != 'CANCELADO'
                BEGIN
                    UPDATE produtos
                    SET estoque = estoque + (
                        SELECT quantidade 
                        FROM itens_pedido 
                        WHERE pedido_id = NEW.id AND produto_id = produtos.id
                    )
                    WHERE id IN (
                        SELECT produto_id 
                        FROM itens_pedido 
                        WHERE pedido_id = NEW.id
                    );
                END;
            """)
            
            # Trigger para atualizar timestamp de atualização em usuarios
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS update_usuarios_timestamp
                AFTER UPDATE ON usuarios
                FOR EACH ROW
                BEGIN
                    UPDATE usuarios SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END;
            """)
            
            # Trigger para atualizar timestamp de atualização em produtos
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS update_produtos_timestamp
                AFTER UPDATE ON produtos
                FOR EACH ROW
                BEGIN
                    UPDATE produtos SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END;
            """)
            
            # Trigger para atualizar timestamp de atualização em carrinhos
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS update_carrinhos_timestamp
                AFTER UPDATE ON carrinhos
                FOR EACH ROW
                BEGIN
                    UPDATE carrinhos SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END;
            """)
            
            # Trigger para atualizar timestamp de atualização em pedidos
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS update_pedidos_timestamp
                AFTER UPDATE ON pedidos
                FOR EACH ROW
                BEGIN
                    UPDATE pedidos SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END;
            """)
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao criar triggers: {e}")
            raise
    
    def create_views(self):
        """
        Cria as views do sistema para consultas otimizadas.
        """
        cursor = self.conn.cursor()
        
        try:
            # View de produtos com categoria
            cursor.execute("""
                CREATE VIEW IF NOT EXISTS vw_produtos_completos AS
                SELECT 
                    p.*,
                    c.nome AS categoria_nome,
                    c.descricao AS categoria_descricao,
                    (SELECT url FROM imagens_produto WHERE produto_id = p.id ORDER BY prioridade LIMIT 1) AS imagem_principal
                FROM produtos p
                LEFT JOIN categorias c ON p.categoria_id = c.id;
            """)
            
            # View de clientes completos
            cursor.execute("""
                CREATE VIEW IF NOT EXISTS vw_clientes_completos AS
                SELECT 
                    u.id,
                    u.nome,
                    u.email,
                    u.tipo,
                    u.criado_em,
                    c.cpf,
                    c.telefone,
                    c.data_nascimento
                FROM usuarios u
                INNER JOIN clientes_info c ON u.id = c.usuario_id
                WHERE u.tipo = 'cliente';
            """)
            
            # View de pedidos com detalhes
            cursor.execute("""
                CREATE VIEW IF NOT EXISTS vw_pedidos_detalhados AS
                SELECT 
                    p.*,
                    u.nome AS cliente_nome,
                    u.email AS cliente_email,
                    (e.logradouro || ', ' || e.numero || ' - ' || e.bairro || ', ' || e.cidade || '/' || e.estado) AS endereco_completo,
                    (SELECT COUNT(*) FROM itens_pedido WHERE pedido_id = p.id) AS total_itens
                FROM pedidos p
                INNER JOIN usuarios u ON p.usuario_id = u.id
                INNER JOIN enderecos e ON p.endereco_id = e.id;
            """)
            
            # View de carrinho com totais
            cursor.execute("""
                CREATE VIEW IF NOT EXISTS vw_carrinhos_totais AS
                SELECT 
                    c.id AS carrinho_id,
                    c.usuario_id,
                    u.nome AS cliente_nome,
                    COUNT(ic.id) AS total_itens,
                    SUM(ic.quantidade) AS total_quantidade,
                    SUM(ic.quantidade * ic.preco_unitario) AS valor_total,
                    c.atualizado_em
                FROM carrinhos c
                INNER JOIN usuarios u ON c.usuario_id = u.id
                LEFT JOIN itens_carrinho ic ON c.id = ic.carrinho_id
                GROUP BY c.id, c.usuario_id, u.nome, c.atualizado_em;
            """)
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao criar views: {e}")
            raise
    
    def initialize_database(self):
        """
        Executa a inicialização completa do banco de dados.
        """
        self.create_schema()
        self.create_triggers()
        self.create_views()
    
    def drop_all_tables(self):
        """
        Remove todas as tabelas do banco (use com cuidado!).
        Útil para resetar o banco em ambiente de desenvolvimento.
        """
        cursor = self.conn.cursor()
        
        try:
            # Desabilita temporariamente as foreign keys
            cursor.execute("PRAGMA foreign_keys = OFF;")
            
            # Lista todas as tabelas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()
            
            # Remove todas as tabelas
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
            
            # Lista todas as views
            cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
            views = cursor.fetchall()
            
            # Remove todas as views
            for view in views:
                cursor.execute(f"DROP VIEW IF EXISTS {view[0]};")
            
            # Reabilita foreign keys
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Erro ao remover tabelas: {e}")
            raise
    
    def check_database_exists(self) -> bool:
        """
        Verifica se o banco de dados já está inicializado.
        
        Returns:
            bool: True se o banco existe e tem tabelas, False caso contrário.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios';")
        return cursor.fetchone() is not None
