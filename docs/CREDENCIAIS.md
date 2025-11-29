# Credenciais de Acesso - Dados Seed

## Usuários Padrão

### Administrador
- **Email:** admin@scee.com
- **Senha:** admin123
- **Tipo:** Administrador
- **Nível de Acesso:** 3 (Total)
- **Cargo:** Administrador Geral

### Cliente Exemplo
- **Email:** joao@email.com
- **Senha:** cliente123
- **Tipo:** Cliente
- **Nome:** João Silva
- **CPF:** 123.456.789-00
- **Telefone:** (11) 98765-4321
- **Endereço:** Rua das Flores, 123 - Apto 45, Centro, São Paulo/SP, CEP: 01234-567

## Dados Populados

### Categorias (5)
- Eletrônicos
- Roupas
- Livros
- Casa e Decoração
- Esportes

### Produtos (15)
#### Eletrônicos (4 produtos)
- Fone de Ouvido Bluetooth - R$ 199,90
- Mouse Gamer RGB - R$ 129,90
- Teclado Mecânico - R$ 299,90
- Webcam Full HD - R$ 249,90

#### Roupas (3 produtos)
- Camiseta Básica Preta - R$ 39,90
- Calça Jeans Masculina - R$ 149,90
- Jaqueta Corta-Vento - R$ 189,90

#### Livros (3 produtos)
- Clean Code - R$ 89,90
- Design Patterns - R$ 95,90
- Python Cookbook - R$ 79,90

#### Casa e Decoração (2 produtos)
- Luminária LED - R$ 69,90
- Quadro Decorativo - R$ 129,90

#### Esportes (3 produtos)
- Garrafa Térmica 1L - R$ 59,90
- Tapete de Yoga - R$ 99,90
- Halteres 5kg (Par) - R$ 119,90

### Imagens (16)
Cada produto possui ao menos uma imagem associada.

## Notas de Segurança

- As senhas são armazenadas usando hash bcrypt
- Em produção, altere imediatamente as credenciais padrão
- O nível de acesso do administrador é 3 (máximo)
