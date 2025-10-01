from biblioteca import Biblioteca
from acervo_padrao import item_padrao, eventos_padrao, membros_padrao

b = Biblioteca()

# Carrega itens padrão
for tipo, titulo, autor, editora, genero, total_exemplares, extra1, extra2 in item_padrao:
    b.cadastrar_item(titulo, autor, editora, genero, total_exemplares, tipo=tipo, isbn=extra1, edicao=extra1, formato=extra1, link_download=extra2)

# Carrega eventos padrão
for nome, descricao, data, local in eventos_padrao:
    b.agendar_evento(nome, descricao, data, local)

# Carrega membros padrão
for nome, endereco, email in membros_padrao:
    try:
        b.cadastrar_membro(nome, endereco, email)
    except Exception as e:
        print(f"Erro ao cadastrar membro {nome}: {e}")

print("Dados carregados. Data do sistema:", b.data_atual.strftime('%d/%m/%Y'))

email = "joao@email.com"
titulo = "Dom Casmurro"

sucesso, msg, emprestimo = b.realizar_emprestimo(email, titulo)
print("sucesso:", sucesso)
print("mensagem:", msg)
if emprestimo:
    print("emprestimo:", emprestimo)
