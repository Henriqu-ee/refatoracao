Biblioteca - Persistência e Importação
=====================================

Breve guia de uso das funções de persistência e importação incluídas no projeto.

1) Objetivo
 - Permitir salvar o estado (acervo, membros, eventos) em JSON.
 - Restaurar a partir de arquivos JSON ou CSV (catálogos).
 - Criar backups automáticos antes de sobrescrever arquivos existentes.

2) Onde acessar
 - No menu administrativo, escolha "Persistência e Backup".
 - Opções: Salvar, Restaurar (adicionar), Restaurar (substituir), Exportar catálogo, Importar catálogo, Listar backups, Ajuda.

3) Formatos suportados
 - JSON: arquivo criado por "Salvar estado" ou por exportação do sistema. Estrutura esperada:
   - Chave `acervo`: lista de itens no formato interno (tipo, título, autor, editora, gênero, total_exemplares, extra1, extra2)
   - Chave `membros`: lista de membros (nome, endereco, email)
   - Chave `eventos`: lista de eventos (nome, descricao, data, local)

 - CSV: usado apenas para importação de catálogos (apenas acervo). Cada linha do CSV deve ter os campos:

   tipo,titulo,autor,editora,genero,total_exemplares,extra1,extra2

   Onde `tipo` é um dos: `livro`, `revista`, `ebook`.
   - Para `livro`: extra1 = isbn
   - Para `revista`: extra1 = edicao
   - Para `ebook`: extra1 = formato, extra2 = link_download (URL completa, ex: https://...)

   Exemplo de linha CSV (3 itens):

   livro,Csv Livro,Autor X,Editora Y,Ficcao,2,9781234567890,
   revista,Revista Z,Editor A,Editora B,Estudos,1,Edicao 5,
   ebook,Ebook Exemplo,Autor E,Editora E,Digital,1,EPUB,https://example.com/ebook

4) Recomendações
 - Sempre salve/backup antes de usar "Restaurar (substituir)".
 - Use "Restaurar (adicionar)" se não tiver certeza — ele apenas acrescenta dados.
 - Se um CSV tiver cabeçalho, remova-o ou converta para o formato esperado (o importador atual espera linhas de dados sem cabeçalho).

5) Erros e relatórios
 - O importador CSV ignora linhas inválidas e tenta continuar. O retorno indica quantos registros foram importados/ignorados/geraram erro.
 - Em caso de problema ao salvar/carregar, verifique permissões de arquivo e caminho informado.

6) Próximos passos
 - Podemos adicionar importador que aceita cabeçalho automaticamente e mapeamento interativo de colunas (opcional). Se quiser, posso implementar.

---
Gerado automaticamente para ajudar administradores leigos a usar o menu de persistência.
