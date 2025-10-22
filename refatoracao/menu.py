import sys
import time
import os
from classes import Ebook
from facade import BibliotecaFacade
from datetime import datetime

#Define a senha de acesso para a área administrativa.
SENHA_ADMIN = "admin123"

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

#------------------------------- MENU PRINCIPAL ------------------------------------------
def menu_principal(biblioteca):
    #Exibe o menu principal e direciona o usuário com base na sua escolha.
    while True:
        time.sleep(2)
        limpar_tela()
        print("---- Sistema de gerenciamento da biblioteca ----")
        print("1. Entrar como administrador")
        print("2. Entrar como membro")
        print("3. Cadastrar novo membro")
        print("4. Sair do sistema")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            #Valida a senha do administrador antes de dar acesso.
            senha = input("Digite a senha de administrador: ")
            if senha == SENHA_ADMIN:
                print("\n✔ Login de administrador bem-sucedido!")
                time.sleep(1)
                menu_administrador(biblioteca)
            else:
                print("❗️ Senha incorreta.")
                time.sleep(0.5)
                
        elif escolha == '2':
            #Valida o e-mail do membro para login.
            email = input("Digite seu e-mail para login: ")
            membro = biblioteca.buscar_membro_por_email(email)
            if membro:
                print(f"\n✔ Login bem-sucedido! Bem-vindo(a), {membro.nome}.")
                time.sleep(1)
                menu_membro(biblioteca, membro)
            else:
                print("❗️ Membro não encontrado com este e-mail.")
                time.sleep(0.5)
                
        elif escolha == '3':
            #Chama a função de cadastro de membro.
            menu_cadastrar_membro(biblioteca)
        elif escolha == '4':
            #Encerra o programa.
            print("Saindo do sistema...")
            time.sleep(1)
            print("Até logo!")
            sys.exit(0)
        else:
            print("❗️ Opção inválida.")
            time.sleep(0.5)
            
#------------------------------------------------- MENU e SUBMENU ADMINISTRADOR --------------------------------------------------
def menu_administrador(biblioteca):
    while True:
        limpar_tela()
        print("\n--- 👑 Menu do administrador ---")
        print(f"Data atual do sistema: {biblioteca.data_atual.strftime('%d/%m/%Y')}")
        print("1. Gerenciar acervo")
        print("2. Gerenciar membros")
        print("3. Gerenciar eventos")
        print("4. Avançar o tempo no sistema")
        print("5. Ver relatório de uso")
        print("6. Persistência (Salvar / Carregar / Backup)")
        print("7. Logout")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_gerenciar_itens(biblioteca)
        elif escolha == '2':
            menu_gerenciar_membros(biblioteca)
        elif escolha == '3':
            menu_gerenciar_eventos(biblioteca)
                 
        elif escolha == '4':
            #Permite simular a passagem do tempo e verificar atrasos automaticamente.
            try:
                dias = int(input("Quantos dias você deseja avançar no tempo? "))
                mensagens = biblioteca.avancar_no_tempo(dias)
                for msg in mensagens:
                    print(msg)
                    time.sleep(0.5)
                input("\nPressione ENTER para continuar...")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")
                time.sleep(1.5)
                
        elif escolha == '5':
            #Gera e exibe um relatório de uso da biblioteca.
            relatorio = biblioteca.relatorio_uso()
            exibir_relatorio(relatorio)
            input("\nPressione ENTER para continuar...")
        elif escolha == '6':
            # Persistência (Salvar / Carregar / Backup)
            fac = BibliotecaFacade(biblioteca)
            menu_persistencia(biblioteca, fac)
        elif escolha == '7':
            #Retorna ao menu principal.
            print("Fazendo logout de administrador...")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)


            
def menu_gerenciar_itens(biblioteca):
    while True:
        limpar_tela()
        print("\n--- 📦 Gerenciamento de acervo (Admin) ---")
        print("1. Gerenciar catálogo da biblioteca")
        print("2. Gerenciar circulação")
        print("3. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_gerenciar_catalogo(biblioteca)
        elif escolha == '2':
            menu_gerenciar_circulacao(biblioteca)
        elif escolha == '3':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)

def menu_gerenciar_catalogo(biblioteca):
    #Submenu para cadastrar, listar e buscar itens no catálogo.
    while True:
        limpar_tela()
        print("\n--- 📚 Gerenciamento de catálogo ---")
        print("1. Cadastrar novo livro")
        print("2. Cadastrar nova revista")
        print("3. Cadastrar novo Ebook")
        print("4. Listar todos os itens")
        print("5. Buscar item")
        print("6. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha in ('1', '2', '3'):
            #Coleta dados comuns a todos os tipos de itens.
            tipo = "livro" if escolha == '1' else ("revista" if escolha == '2' else "ebook")
            titulo = input("Título: ")
            autor = input("Autor/Editor: ")
            editora = input("Editora: ")
            genero = input("Gênero: ")
            try:
                total_exemplares = int(input("Total de exemplares: "))
                kwargs = {}
                #Coleta dados específicos para cada tipo de item.
                if tipo == 'livro':
                    kwargs['isbn'] = input("ISBN (opcional): ")
                elif tipo == 'revista':
                    kwargs['edicao'] = input("Edição (opcional): ")
                else:
                    # Validação do link para ebook: não vazio e começa com http/https
                    while True:
                        link = input("Link para download: ").strip()
                        if not link:
                            print("❗️ O link não pode ficar vazio. Por favor insira um link válido.")
                            continue
                        if not (link.startswith('http://') or link.startswith('https://')):
                            print("❗️ O link deve começar com http:// ou https://. Tente novamente.")
                            continue
                        break
                    kwargs['link_download'] = link
                    kwargs['formato'] = input("Formato do ebook: ")
                
                #Chama o método de cadastro da biblioteca.
                sucesso, msg, _ = biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares, tipo=tipo, **kwargs)
                print(msg)
            except ValueError:
                print("❗️ Número de exemplares deve ser um número inteiro.")
            time.sleep(1.5)
            
        elif escolha == '4':
            #Lista as informações básicas de todos os itens do acervo.
            print("\n--- 📚 Lista de itens no acervo ---")
            itens = biblioteca.listar_itens()
            if not itens:
                print("Nenhum item cadastrado.")
            else:
                for item in itens:
                    print(item.descricao())
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '5':
            #Busca itens por um critério específico (título, autor, etc.).
            criterio = input("Escolha o critério que deseja buscar (titulo\\autor\editora\genero): ").lower().strip()
            if criterio in ['titulo', 'autor', 'editora', 'genero']:
                valor = input(f"Digite o {criterio} que deseja buscar: ")
                resultados = biblioteca.buscar_item(criterio, valor)
                if not resultados:
                    print("\nNenhum item encontrado com esse critério.")
                else:
                    print("\n--- Resultados da busca ---")
                    for item in resultados:
                        print(item.descricao())
            else:
                print("Critério de busca inválido.")
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '6':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)

def menu_gerenciar_circulacao(biblioteca):
    #Submenu para gerenciar empréstimos, devoluções e reservas.
    while True:
        limpar_tela()
        print("\n--- 🔄 Gerenciamento de circulação ---")
        print("1. Realizar empréstimo")
        print("2. Realizar devolução")
        print("3. Ver reservas")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            email = input("Email do membro: ")
            titulo = input("Título do item: ")
            sucesso, msg, _ = biblioteca.realizar_emprestimo(email, titulo)
            #Se o item estiver indisponível, oferece a opção de reserva.
            if not sucesso and msg == "ITEM_INDISPONIVEL":
                print(f"❗️ Item '{titulo}' não está disponível para empréstimo no momento.")
                opcao = input("Deseja reservar o item para retirada posterior? (sim/não): ").strip().lower()
                if opcao == 'sim':
                    sucesso_reserva, msg_reserva, _ = biblioteca.realizar_emprestimo(email, titulo, para_reserva=True)
                    print(msg_reserva)
                else:
                    print("Empréstimo não realizado.")
            else:
                print(msg)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '2':
            email = input("Email do membro: ")
            titulo = input("Título do item: ")
            membro = biblioteca.buscar_membro_por_email(email)
            if not membro:
               print(f"❗️ Membro com email {email} não encontrado.")
            else:
               #Verifica se há multas pendentes antes de permitir a devolução.
               multas_pendentes = biblioteca.listar_multas_do_membro(membro)
               pagamento_ok = True
               if multas_pendentes:
                   print(f"\n❗️ O membro {membro.nome} possui multas pendentes. É necessário quitá-las para devolver o item.")
                   pagamento_ok = pagamento_multas(biblioteca, membro)
              
               if pagamento_ok:
                   sucesso, msg = biblioteca.realizar_devolucao(email, titulo)
                   print(msg)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            #Lista todas as reservas ativas no sistema.
            reservas = biblioteca.listar_reservas()
            if not reservas:
                print("Nenhuma reserva de livro ativa no momento.")
            else:
                print("\n--- Lista de reservas ativas ---")
                for reserva in reservas:
                    print(reserva)
                    print("-" * 25)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)

def menu_gerenciar_membros(biblioteca):
    #Submenu para cadastrar, listar membros e visualizar multas.
    while True:
        limpar_tela()
        print("\n--- 👤 Gerenciamento de membros (Admin) ---")
        print("1. Cadastrar novo membro")
        print("2. Listar todos os membros")
        print("3. Ver todas as multas")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_cadastrar_membro(biblioteca)
            
        elif escolha == '2':
            #Lista todos os membros cadastrados no sistema.
            print("\n--- 👥 Lista de membros ---")
            membros = biblioteca.listar_membros()
            if not membros:
                print("Nenhum membro cadastrado.")
            else:
                for membro in membros:
                    print(membro)
                    print("-" * 25)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            menu_gerenciar_multas(biblioteca)
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)
            
def menu_gerenciar_multas(biblioteca):
    print("\n--- 💰 Todas as multas do sistema ---")
    multas = biblioteca.listar_multas()
    if not multas:
        print("Nenhuma multa registrada no sistema.")
    else:
        for multa in multas:
            print(multa)
            print("-" * 25)
    input("\nPressione ENTER para continuar...")
            
def menu_gerenciar_eventos(biblioteca):
    while True:
        limpar_tela()
        print("\n--- 🎉 Gerenciamento de eventos (Admin) ---")
        print("1. Agendar evento")
        print("2. Divulgar eventos")
        print("3. Cancelar evento")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            #Coleta os dados e agenda um novo evento.
            nome = input("Nome: ")
            descricao = input("Descrição: ")
            data = input("Data (DD/MM/AAAA): ")
            local = input("Local: ")
            sucesso, msg, _ = biblioteca.agendar_evento(nome, descricao, data, local)
            print(msg)
            time.sleep(1.5)
            
        elif escolha == '2':
            #Exibe os próximos eventos agendados.
            eventos_para_divulgar = biblioteca.divulgar_eventos()
            if not eventos_para_divulgar:
                print("Nenhum evento agendado para divulgar.")
            else:
                print(f"\nDivulgando {len(eventos_para_divulgar)} evento(s)...")
                print("-" * 40)
                for evento in eventos_para_divulgar:
                    print(evento)
                    print("-" * 20)
                    time.sleep(0.7)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            #Cancela um evento com base no nome.
            nome_evento = input("Digite o nome do evento a ser cancelado: ")
            sucesso, msg = biblioteca.cancelar_evento(nome_evento)
            print(msg)
            
            time.sleep(1.5)
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)
  
                        
#--------------------- ADMIN E PRINCIPAL --------------------------------------------
def menu_cadastrar_membro(biblioteca):
    limpar_tela()
    print("\n--- Cadastro de novo Membro ---")
    try:
        nome = input("Digite o nome do membro: ")
        endereco = input("Digite o endereço do membro: ")
        email = input("Digite o email do membro: ")
        sucesso, msg, _ = biblioteca.cadastrar_membro(nome, endereco, email)
        print(msg)

    except ValueError as e:
        print(f"\n❗️ Erro no cadastro: {e}")
        print("Por favor, tente novamente com os dados corretos.")

    finally:
        time.sleep(2.5)


#-------------------------------- MENU MEMBRO ------------------------------------------  
def menu_membro(biblioteca, membro):
    #Exibe o menu de opções para um membro logado.
    while True:
        limpar_tela()
        print(f"\n--- 🤗 Menu do membro: {membro.nome} ---")
        print(f"Data atual do sistema: {biblioteca.data_atual.strftime('%d/%m/%Y')}")
        print("1. Buscar item no acervo")
        print("2. Meus empréstimos e devoluções")
        print("3. Minhas multas pendentes")
        print("4. Acessar eBook")
        print("5. Ver eventos")
        print("6. Logout")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            #Permite que o membro busque itens no acervo.
            criterio = input("Buscar por (titulo\\autor\editora\genero): ").lower().strip()
            if criterio in ['titulo', 'autor', 'editora', 'genero']:
                valor = input(f"Digite o {criterio} que deseja buscar: ")
                resultados = biblioteca.buscar_item(criterio, valor)
                if not resultados:
                    print("\nNenhum item encontrado.")
                else:
                    print("\n--- Resultados da busca ---")
                    for item in resultados:
                        print(item.descricao())
            else:
                print("Critério de busca inválido.")
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '2':
            #Exibe os empréstimos ativos do membro e oferece a opção de devolução.
            print("\n--- Meus empréstimos ativos ---")
            emprestimos_ativos = biblioteca.listar_emprestimos_do_membro(membro)
            if not emprestimos_ativos:
                print("Você não possui empréstimos ativos.")
            else:
                for emprestimo in emprestimos_ativos:
                    print(emprestimo)
                    print("-" * 25)
                
                devolver = input("\nDeseja devolver um item? (sim/não): ").lower()
                if devolver == 'sim':
                    titulo_item = input("Digite o título do item para devolver: ")
                    #Verifica multas antes de permitir a devolução.
                    multas_pendentes = biblioteca.listar_multas_do_membro(membro)
                    pagamento_ok = True
                    if multas_pendentes:
                       print("\n❗️ Você possui multas pendentes. É necessário quitá-las para devolver o item.")
                       pagamento_ok = pagamento_multas(biblioteca, membro)
                       
                    if pagamento_ok:
                       sucesso, msg = biblioteca.realizar_devolucao(membro.email, titulo_item)
                       print(msg)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '3':
            #Exibe as multas pendentes do membro e oferece a opção de pagamento.
            print("\n--- Minhas multas pendentes ---")
            multas_pendentes = biblioteca.listar_multas_do_membro(membro)
            if not multas_pendentes:
                print("Nenhuma multa pendente.")
            else:
                for multa in multas_pendentes:
                    print(multa)
                    print("-" * 25)
                resposta = input("Deseja pagar todas as multas? (sim/não): ").lower()
                if resposta == 'sim':
                    for m in multas_pendentes:
                        m.pagar()
                    print("\n✔ Multas pagas com sucesso.")
                    time.sleep(1.5)
                else:
                    print("\n❌ Pagamento não efetuado.")
                    time.sleep(1.5)             
            input("\nPressione ENTER para continuar...")
                    
        elif escolha == '4':
            #Lista os ebooks disponíveis e fornece o link de acesso.
            print("\n--- 📖 Ebooks cadastrados ---")
            todos_os_itens = biblioteca.listar_itens() 
            
            ebooks = [item for item in todos_os_itens if isinstance(item, Ebook)]
            
            if not ebooks:
                print("Nenhum ebook cadastrado atualmente.\n")
            else:
                for ebook in ebooks:
                    print(ebook)
                    print("-" * 25)
                titulo = input("Digite o título do eBook que deseja acessar: ")
                ebook_encontrado = next(
                    (i for i in ebooks if biblioteca.normalizar(i.titulo) == biblioteca.normalizar(titulo)),
                    None
                )
                if ebook_encontrado:
                    print(f"Acesse o livro clicando aqui 👉 {ebook_encontrado.link_download}")
                else:
                    print("❗️ Ebook não encontrado.")
            input("\nPressione ENTER para continuar...")

        elif escolha == '5':
            #Exibe os próximos eventos da biblioteca.
            eventos = biblioteca.listar_eventos()
            if not eventos:
                print("Nenhum evento agendado no momento.")
            else:
                print("\n--- 🗓️ Eventos agendados ---\nMostrando os 5 próximos exemplos:")
                for evento in eventos[:5]:
                    print(evento)
                    print("-" * 25)
            input("\nPressione ENTER para continuar...")
            
        elif escolha == '6':
            #Faz logout e retorna ao menu principal.
            print("Fazendo logout...")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)
            
def exibir_relatorio(relatorio):
    print("\n" + "=" * 30)
    print("📑 Relatório de uso da biblioteca")
    print("=" * 30 + "")
    
    if not relatorio:
        print("😩 Nenhuma atividade para gerar relatório")
        return

    print("\n--- Atividade dos itens ---\n")
    print("📖 Top 5 livros mais emprestados\n")
    if relatorio["top_livros"]:
        for livro, count in relatorio["top_livros"]:
            print(f" - {livro} ({count} vezes)")
    else:
        print("Nenhum livro emprestado ainda.")
        
    print("\n\n👀 Top 3 genêros mais populares\n")
    if relatorio["top_generos"]:
        for genero, count in relatorio["top_generos"]:
            print(f" - {genero} ({count} vezes)")
    else:
        print("Nenhum gênero popular ainda.")
    
    print("\n--- Atividade dos membros ---\n")
    print("🏆 Top 3 membros mais ativos:\n")
    if relatorio["membros_ativos"]:
        for membro, count in relatorio["membros_ativos"]:
            print(f"  - {membro} ({count} empréstimos)")
    else:
        print("Nenhum membro ativo ainda.")
            
    print("\n--- Análise de multas ---\n")
    print(f"  - 💰 Valor total de multas geradas: R$ {relatorio['total_multas_geradas']:.2f}")
    print(f"  - 🤑 Valor total de multas pagas: R$ {relatorio['total_multas_pagas']:.2f}")
    print(f"  - 🪙 Taxa de pagamento de multas: {relatorio['taxa_pagamento_multas']:.1f}%")

    print("\n\n--- Estatísticas Gerais ---")
    print(f"  - Número total de itens no acervo: {relatorio['total_livros_acervo']}")
    print(f"  - Número total de membros: {relatorio['total_membros']}")
    print(f"  - Total de empréstimos realizados (histórico): {relatorio['total_emprestimos_historico']}")
    print(f"  - Itens atualmente emprestados: {relatorio['emprestimos_atuais']}")

    print("\n" + "="*30)
    print("Relatório gerado com sucesso!")
    print("="*30)
    
    
    

def pagamento_multas(biblioteca, membro):
    #Função auxiliar para exibir e processar o pagamento de multas de um membro.
    multas_pendentes = biblioteca.listar_multas_do_membro(membro)
    
    print("\n--- 💰 Multas pendentes ---")
    total_a_pagar = 0
    for multa in multas_pendentes:
        print(multa)
        total_a_pagar += multa.valor
        print("-" * 25)
    print(f"Total a pagar: R$ {total_a_pagar:.2f}")

    pagar = input("\nDeseja pagar todas as multas agora? (sim/não): ").strip().lower()
    if pagar == 'sim':
        for m in multas_pendentes:
            m.pagar()
        print("\n✔ Multas pagas com sucesso.")
        time.sleep(1.5)
        return True #Retorna True se o pagamento foi efetuado.
    else:
        print("\n❌ Pagamento não efetuado. A devolução não pode ser concluída.")
        time.sleep(1.5)
        return False #Retorna False se o pagamento foi recusado.


def menu_persistencia(biblioteca, facade: BibliotecaFacade):
    import glob
    import textwrap

    while True:
        limpar_tela()
        print("\n--- 💾 Persistência e Backup (Admin) ---")
        print("1. Salvar estado (criar arquivo .json)")
        print("2. Restaurar a partir de um arquivo (ADICIONAR dados ao atual)")
        print("3. Restaurar e SUBSTITUIR tudo (PERIGOSO)")
        print("4. Exportar somente o catálogo (acervo)")
        print("5. Importar catálogo (acrescentar itens ao acervo)")
        print("6. Listar backups disponíveis e restaurar")
        print("7. Ajuda (explicações rápidas)")
        print("8. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            default = 'state.json'
            path = input(f"Salvar em (ENTER para '{default}'): ").strip() or default
            if os.path.exists(path):
                sobrescrever = input(f"O arquivo '{path}' já existe. Deseja sobrescrever? (sim/não): ").strip().lower()
                if sobrescrever != 'sim':
                    print("Operação cancelada pelo usuário.")
                    input("\nPressione ENTER para continuar...")
                    continue

            ok, msg, backup = facade.save(path)
            print(msg)
            if ok:
                if backup:
                    print(f"Um backup do arquivo anterior foi criado em: {backup}")
                else:
                    print("Nenhum backup anterior foi criado (arquivo novo ou falha ao criar backup).")
            input("\nPressione ENTER para continuar...")

        elif escolha == '2':
            default = 'state.json'
            path = input(f"Arquivo para restaurar (acrescentar dados) (ENTER para '{default}'): ").strip() or default
            print("Isto irá ADICIONAR os dados do arquivo ao estado atual. Entradas duplicadas podem ocorrer.")
            confirmar = input("Deseja continuar? (sim/não): ").strip().lower()
            if confirmar != 'sim':
                print("Operação cancelada.")
                input("\nPressione ENTER para continuar...")
                continue
            ok, msg = facade.load(path, replace=False)
            print(msg)
            input("\nPressione ENTER para continuar...")

        elif escolha == '3':
            default = 'state.json'
            path = input(f"Arquivo para restaurar (SUBSTITUIR tudo) (ENTER para '{default}'): ").strip() or default
            print(textwrap.fill("ATENÇÃO: Esta operação irá APAGAR o estado atual e substituí-lo pelo conteúdo do arquivo. Faça um backup primeiro se não tiver certeza.", 70))
            confirmar = input("Confirmar substituição COMPLETA? (sim/não): ").strip().lower()
            if confirmar != 'sim':
                print("Operação de substituição cancelada.")
                input("\nPressione ENTER para continuar...")
                continue
            ok, msg = facade.load(path, replace=True)
            print(msg)
            input("\nPressione ENTER para continuar...")

        elif escolha == '4':
            default = 'acervo_export.json'
            path = input(f"Salvar catálogo em (ENTER para '{default}'): ").strip() or default
            ok, msg = facade.export_acervo(path)
            print(msg)
            input("\nPressione ENTER para continuar...")

        elif escolha == '5':
            default = 'acervo_export.json'
            path = input(f"Arquivo de catálogo para importar (acrescentar) (ENTER para '{default}'): ").strip() or default
            print("Isto irá tentar adicionar os itens do arquivo ao catálogo atual. Itens inválidos podem ser ignorados.")
            confirmar = input("Deseja continuar? (sim/não): ").strip().lower()
            if confirmar != 'sim':
                print("Importação cancelada.")
                input("\nPressione ENTER para continuar...")
                continue
            ok, msg = facade.import_acervo(path, merge=True)
            print(msg)
            input("\nPressione ENTER para continuar...")

        elif escolha == '6':
            # Lista backups no diretório corrente com padrão *.backup.*
            arquivos = sorted(glob.glob('*.backup.*'))
            if not arquivos:
                print("Nenhum arquivo de backup encontrado no diretório atual.")
                input("\nPressione ENTER para continuar...")
                continue
            print("Backups encontrados:")
            for i, a in enumerate(arquivos, start=1):
                print(f"{i}. {a}")
            selecionado = input("Escolha um número para restaurar ou ENTER para cancelar: ").strip()
            if not selecionado:
                continue
            try:
                idx = int(selecionado) - 1
                backup_path = arquivos[idx]
            except Exception:
                print("Seleção inválida.")
                input("\nPressione ENTER para continuar...")
                continue

            print("Você pode: 1) Adicionar (manter dados atuais) ou 2) Substituir tudo com este backup.")
            modo = input("Escolha 1 para adicionar ou 2 para substituir (ENTER para 1): ").strip() or '1'
            if modo not in ('1', '2'):
                print("Modo inválido. Cancelando.")
                input("\nPressione ENTER para continuar...")
                continue
            if modo == '2':
                confirmar = input("CONFIRMA substituir tudo com este backup? (sim/não): ").strip().lower()
                if confirmar != 'sim':
                    print("Operação cancelada.")
                    input("\nPressione ENTER para continuar...")
                    continue
                ok, msg = facade.load(backup_path, replace=True)
                print(msg)
            else:
                ok, msg = facade.load(backup_path, replace=False)
                print(msg)
            input("\nPressione ENTER para continuar...")

        elif escolha == '7':
            limpar_tela()
            print("Ajuda rápida - persistência e backups:\n")
            print("Salvar estado: cria um arquivo JSON com todos os dados (itens, membros, eventos). Use para guardar o trabalho antes de fechar o programa.")
            print("Restaurar (Adicionar): carrega os dados de um arquivo e adiciona ao que já existe no sistema. Útil para mesclar catálogos.")
            print("Restaurar e Substituir: APAGA o estado atual e carrega apenas o que estiver no arquivo. Perigoso sem backup.")
            print("Exportar catálogo: grava só o acervo (útil para compartilhar o catálogo).")
            print("Importar catálogo: adiciona itens ao acervo atual a partir de um arquivo de catálogo.")
            print("Listar backups: mostra arquivos de backup gerados anteriormente; permite restaurar a partir deles.")
            print('\nRecomendações: sempre salve/backup antes de substituir o estado. Se tiver dúvidas, escolha "Restaurar (Adicionar)".')
            input("\nPressione ENTER para continuar...")

        elif escolha == '8':
            break
        else:
            print("Opção inválida.")
            time.sleep(1.5)
