-- Dados de seed para o projeto SCEE
-- Dados iniciais para desenvolvimento e testes

-- Inserir categorias
INSERT OR IGNORE INTO categorias (id, nome, descricao, ativo) VALUES
(1, 'Eletrônicos', 'Produtos eletrônicos e tecnologia', 1),
(2, 'Roupas', 'Vestuário masculino e feminino', 1),
(3, 'Livros', 'Livros e publicações', 1),
(4, 'Casa e Decoração', 'Produtos para casa e decoração', 1),
(5, 'Esportes', 'Artigos esportivos e fitness', 1);

-- Inserir produtos de exemplo
INSERT OR IGNORE INTO produtos (id, nome, descricao, preco, sku, categoria_id, estoque, ativo) VALUES
-- Eletrônicos
(1, 'Fone de Ouvido Bluetooth', 'Fone sem fio com cancelamento de ruído', 199.90, 'ELET-FONE-001', 1, 50, 1),
(2, 'Mouse Gamer RGB', 'Mouse óptico com iluminação RGB e 7 botões programáveis', 129.90, 'ELET-MOUSE-001', 1, 30, 1),
(3, 'Teclado Mecânico', 'Teclado mecânico com switches blue', 299.90, 'ELET-TEC-001', 1, 25, 1),
(4, 'Webcam Full HD', 'Webcam 1080p com microfone integrado', 249.90, 'ELET-WEB-001', 1, 15, 1),

-- Roupas
(5, 'Camiseta Básica Preta', 'Camiseta 100% algodão tamanho M', 39.90, 'ROUPA-CAM-001', 2, 100, 1),
(6, 'Calça Jeans Masculina', 'Calça jeans slim fit azul escuro', 149.90, 'ROUPA-CALCA-001', 2, 60, 1),
(7, 'Jaqueta Corta-Vento', 'Jaqueta impermeável com capuz', 189.90, 'ROUPA-JAQ-001', 2, 40, 1),

-- Livros
(8, 'Clean Code', 'Guia de boas práticas de programação', 89.90, 'LIVRO-PROG-001', 3, 20, 1),
(9, 'Design Patterns', 'Padrões de projeto orientados a objetos', 95.90, 'LIVRO-PROG-002', 3, 15, 1),
(10, 'Python Cookbook', 'Receitas práticas de Python', 79.90, 'LIVRO-PROG-003', 3, 25, 1),

-- Casa e Decoração
(11, 'Luminária LED', 'Luminária de mesa com regulagem de intensidade', 69.90, 'CASA-LUM-001', 4, 35, 1),
(12, 'Quadro Decorativo', 'Quadro abstrato 40x60cm', 129.90, 'CASA-QUAD-001', 4, 20, 1),

-- Esportes
(13, 'Garrafa Térmica 1L', 'Garrafa térmica de aço inoxidável', 59.90, 'ESP-GARR-001', 5, 80, 1),
(14, 'Tapete de Yoga', 'Tapete antiderrapante para yoga e pilates', 99.90, 'ESP-TAP-001', 5, 45, 1),
(15, 'Halteres 5kg (Par)', 'Par de halteres emborrachados', 119.90, 'ESP-HALT-001', 5, 30, 1);

-- Inserir imagens de produtos (URLs de exemplo)
INSERT OR IGNORE INTO imagens_produto (produto_id, url, prioridade) VALUES
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
(15, '/images/produtos/halteres-1.jpg', 1);

-- Inserir usuário administrador padrão (senha: admin123)
-- Hash bcrypt de 'admin123': $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqW.6NMjaa
INSERT OR IGNORE INTO usuarios (id, nome, email, senha_hash, tipo) VALUES
(1, 'Administrador', 'admin@scee.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqW.6NMjaa', 'administrador');

INSERT OR IGNORE INTO administradores (usuario_id, cargo, nivel_acesso) VALUES
(1, 'Administrador Geral', 3);

-- Inserir usuário cliente de exemplo (senha: cliente123)
-- Hash bcrypt de 'cliente123': $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW
INSERT OR IGNORE INTO usuarios (id, nome, email, senha_hash, tipo) VALUES
(2, 'João Silva', 'joao@email.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'cliente');

INSERT OR IGNORE INTO clientes_info (usuario_id, cpf, telefone, data_nascimento) VALUES
(2, '123.456.789-00', '(11) 98765-4321', '1990-05-15');

INSERT OR IGNORE INTO enderecos (usuario_id, logradouro, numero, complemento, bairro, cidade, estado, cep, principal) VALUES
(2, 'Rua das Flores', '123', 'Apto 45', 'Centro', 'São Paulo', 'SP', '01234-567', 1);
