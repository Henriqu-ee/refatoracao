# 📖 Sistema de Gestão de Biblioteca  

Sistema de Biblioteca desenvolvido em **Python** como projeto acadêmico da disciplina de **Projeto de Software**.  

---

## 🚀 Funcionalidades  

### ✅ Implementadas  
- 🔍 **Busca no Catálogo**: Pesquisa por título, autor, gênero, editora e outros filtros.  
- 📚 **Empréstimo e Devolução**: Usuários podem retirar e devolver livros.  
- ⏳ **Sistema de Reservas**: Reserva de livros indisponíveis.  
- ⚠️ **Notificações de Atraso**: Alertas automáticos para itens em atraso.  
- 👤 **Gestão de Membros**: Cadastro, edição e consulta de membros.  
- 💸 **Cálculo e Pagamento de Multas**: Multas automáticas por atraso e opção de pagamento.  
- 📦 **Gestão de Inventário**: Cadastro, consulta e rastreamento de itens do acervo.  
- 📅 **Gestão de Eventos**: Agendamento, divulgação e cancelamento de eventos.  
- 📲 **E-books e Recursos Online**: Cadastro e acesso a e-books e links digitais.  
- 📊 **Relatórios e Análises**: Geração de relatórios de uso, empréstimos e tendências.  

---

## 🆕 Refatoração  
- Padrões de Criação
  - Fábrica Abstrata
  - Construtor
  - Método de Fábrica
- Padrões de comportamento
  - Observador
  - Estratégia
   
---

## ⚠️ Implementação Parcial  
- 🌐 **Integração Web/Mobile**: Não implementado.  
- 💾 **Persistência em Banco de Dados**: Dados são mantidos apenas em memória durante a execução.  

---

## 🛠️ Instalação e Execução  

### 📌 Pré-requisitos  
- Python **3.8** ou superior instalado  

### ▶️ Como executar  
1. Clone o repositório:  
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ``
2. Instale as dependências (se houver):
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o sistema:
   ``` bash
   python main.py
   ```
4. Navegue pelo menu interativo:
   - Digite o número da opção desejada e pressione Enter.
   - Os dados são carregados automaticamente a partir dos arquivos padrão.

## 🧶 Design Patterns

### Creational

   - Singleton
      - Garante que a classe Biblioteca tenha apenas uma instância durante a execução.

   - Factory Method
      - Utilizado para criar diferentes tipos de itens do acervo (livros, e-books, etc).
    
## 🏗️ Estrutura do Projeto

### 📁 Estrutura modular e extensível, facilitando futuras adaptações:

   - Persistência em banco de dados

   - Interface web ou mobile

## 💻 Como Usar

- Execute:
   ``` bash
   python main.py
   ```
- Siga as instruções do menu para acessar todas as funcionalidades.
- Cadastre membros, livros, realize empréstimos, reservas e gere relatórios.

## 👥 Perfis de Usuário

-Administrador: Acesso completo a todas as funcionalidades.
-Membro: Consulta ao acervo, empréstimos, reservas e acesso a e-books.

## 📌 Sobre

### 📚 Projeto acadêmico sem fins comerciais.
Desenvolvido para fins de aprendizado e demonstração de boas práticas em Python e orientação a objetos.

Recursos

- 🐍 Python
- ⚙️ Estrutura modular e extensível
- 💾 Fácil adaptação para banco de dados ou interface web
