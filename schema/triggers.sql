-- Triggers MySQL para SCEE
-- Executar após criar o schema

-- Limpar triggers existentes (se houver)
DROP TRIGGER IF EXISTS validate_estoque_carrinho;
DROP TRIGGER IF EXISTS abater_estoque_pedido;
DROP TRIGGER IF EXISTS devolver_estoque_pedido;

-- Trigger para validar estoque ao adicionar item no carrinho
CREATE TRIGGER validate_estoque_carrinho
BEFORE INSERT ON itens_carrinho
FOR EACH ROW
BEGIN
    DECLARE estoque_disponivel INT;
    
    SELECT estoque INTO estoque_disponivel
    FROM produtos
    WHERE id = NEW.produto_id;
    
    IF estoque_disponivel < NEW.quantidade THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Estoque insuficiente para o produto';
    END IF;
END;

-- Trigger para abater estoque ao criar pedido
CREATE TRIGGER abater_estoque_pedido
AFTER INSERT ON itens_pedido
FOR EACH ROW
BEGIN
    UPDATE produtos 
    SET estoque = estoque - NEW.quantidade 
    WHERE id = NEW.produto_id;
END;

-- Trigger para devolver estoque ao cancelar pedido
CREATE TRIGGER devolver_estoque_pedido
AFTER UPDATE ON pedidos
FOR EACH ROW
BEGIN
    IF NEW.status = 'CANCELADO' AND OLD.status != 'CANCELADO' THEN
        UPDATE produtos p
        INNER JOIN itens_pedido ip ON p.id = ip.produto_id
        SET p.estoque = p.estoque + ip.quantidade
        WHERE ip.pedido_id = NEW.id;
    END IF;
END;
