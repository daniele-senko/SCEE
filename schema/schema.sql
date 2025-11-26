-- Schema completo do projeto SCEE
-- DEV 1 - Banco de Dados SQLite
-- Todas as 11 tabelas conforme especificação

-- Tabela de usuários (base para clientes e administradores)
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('cliente', 'administrador')),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Informações específicas de clientes
CREATE TABLE IF NOT EXISTS clientes_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL UNIQUE,
    cpf TEXT UNIQUE NOT NULL,
    telefone TEXT,
    data_nascimento DATE,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Informações específicas de administradores
CREATE TABLE IF NOT EXISTS administradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL UNIQUE,
    cargo TEXT,
    nivel_acesso INTEGER DEFAULT 1 CHECK(nivel_acesso >= 1 AND nivel_acesso <= 3),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Endereços dos clientes
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
    principal BOOLEAN DEFAULT 0,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Categorias de produtos
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    ativo BOOLEAN DEFAULT 1,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL CHECK(preco >= 0),
    sku TEXT UNIQUE NOT NULL,
    categoria_id INTEGER,
    estoque INTEGER DEFAULT 0 CHECK(estoque >= 0),
    ativo BOOLEAN DEFAULT 1,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- Imagens dos produtos
CREATE TABLE IF NOT EXISTS imagens_produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    prioridade INTEGER DEFAULT 0,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

-- Carrinhos de compras
CREATE TABLE IF NOT EXISTS carrinhos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL UNIQUE,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Itens do carrinho
CREATE TABLE IF NOT EXISTS itens_carrinho (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    carrinho_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
    preco_unitario REAL NOT NULL CHECK(preco_unitario >= 0),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(carrinho_id) REFERENCES carrinhos(id) ON DELETE CASCADE,
    FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
    UNIQUE(carrinho_id, produto_id)
);

-- Pedidos
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
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    FOREIGN KEY(endereco_id) REFERENCES enderecos(id) ON DELETE RESTRICT
);

-- Itens do pedido
CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    nome_produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
    preco_unitario REAL NOT NULL CHECK(preco_unitario >= 0),
    subtotal REAL NOT NULL CHECK(subtotal >= 0),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE RESTRICT
);

-- Índices para melhorar performance das queries

-- Índices em usuarios
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_tipo ON usuarios(tipo);

-- Índices em clientes_info
CREATE INDEX IF NOT EXISTS idx_clientes_cpf ON clientes_info(cpf);
CREATE INDEX IF NOT EXISTS idx_clientes_usuario_id ON clientes_info(usuario_id);

-- Índices em enderecos
CREATE INDEX IF NOT EXISTS idx_enderecos_usuario_id ON enderecos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_enderecos_cep ON enderecos(cep);

-- Índices em produtos
CREATE INDEX IF NOT EXISTS idx_produtos_sku ON produtos(sku);
CREATE INDEX IF NOT EXISTS idx_produtos_categoria_id ON produtos(categoria_id);
CREATE INDEX IF NOT EXISTS idx_produtos_nome ON produtos(nome);
CREATE INDEX IF NOT EXISTS idx_produtos_ativo ON produtos(ativo);

-- Índices em imagens_produto
CREATE INDEX IF NOT EXISTS idx_imagens_produto_id ON imagens_produto(produto_id);

-- Índices em carrinhos
CREATE INDEX IF NOT EXISTS idx_carrinhos_usuario_id ON carrinhos(usuario_id);

-- Índices em itens_carrinho
CREATE INDEX IF NOT EXISTS idx_itens_carrinho_carrinho_id ON itens_carrinho(carrinho_id);
CREATE INDEX IF NOT EXISTS idx_itens_carrinho_produto_id ON itens_carrinho(produto_id);

-- Índices em pedidos
CREATE INDEX IF NOT EXISTS idx_pedidos_usuario_id ON pedidos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_pedidos_status ON pedidos(status);
CREATE INDEX IF NOT EXISTS idx_pedidos_criado_em ON pedidos(criado_em);

-- Índices em itens_pedido
CREATE INDEX IF NOT EXISTS idx_itens_pedido_pedido_id ON itens_pedido(pedido_id);
CREATE INDEX IF NOT EXISTS idx_itens_pedido_produto_id ON itens_pedido(produto_id);

-- Triggers para atualizar timestamp automaticamente

-- Trigger para usuarios
CREATE TRIGGER IF NOT EXISTS update_usuarios_timestamp 
AFTER UPDATE ON usuarios
BEGIN
    UPDATE usuarios SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para produtos
CREATE TRIGGER IF NOT EXISTS update_produtos_timestamp 
AFTER UPDATE ON produtos
BEGIN
    UPDATE produtos SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para carrinhos
CREATE TRIGGER IF NOT EXISTS update_carrinhos_timestamp 
AFTER UPDATE ON carrinhos
BEGIN
    UPDATE carrinhos SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para pedidos
CREATE TRIGGER IF NOT EXISTS update_pedidos_timestamp 
AFTER UPDATE ON pedidos
BEGIN
    UPDATE pedidos SET atualizado_em = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para validar estoque ao adicionar item no carrinho
CREATE TRIGGER IF NOT EXISTS validate_estoque_carrinho
BEFORE INSERT ON itens_carrinho
BEGIN
    SELECT CASE
        WHEN (SELECT estoque FROM produtos WHERE id = NEW.produto_id) < NEW.quantidade
        THEN RAISE(ABORT, 'Estoque insuficiente para o produto')
    END;
END;

-- Trigger para abater estoque ao criar pedido
CREATE TRIGGER IF NOT EXISTS abater_estoque_pedido
AFTER INSERT ON itens_pedido
BEGIN
    UPDATE produtos 
    SET estoque = estoque - NEW.quantidade 
    WHERE id = NEW.produto_id;
END;
