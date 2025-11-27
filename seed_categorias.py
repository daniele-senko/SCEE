import sys
import os

# Garante que o Python encontre a pasta src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.repositories.category_repository import CategoriaRepository
from src.models.products.category_model import Categoria

# Instancia a classe com o nome correto
repo = CategoriaRepository()

categorias_para_criar = ["Hardware", "Periféricos", "Games", "Smartphones", "Escritório"]

print("--- 📦 Populando Categorias ---")

for nome in categorias_para_criar:
    # 1. Verifica se já existe no banco
    # O método buscar_por_nome do repo dele retorna um Dict ou None
    try:
        existente = repo.buscar_por_nome(nome)
        
        if not existente:
            # 2. Se não existe, cria
            # O repo dele espera um Objeto ou Dict (com o nosso adaptador)
            nova_cat = Categoria(nome=nome)
            repo.salvar(nova_cat)
            print(f"Criada: {nome}")
        else:
            print(f"ℹJá existe: {nome}")
            
    except Exception as e:
        print(f"Erro ao processar {nome}: {e}")