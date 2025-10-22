# 📖 Sistema de Gestão de Biblioteca  

Projeto acadêmico desenvolvido em Python para a disciplina de Projeto de Software, com foco na aplicação de Padrões de Projeto (Design Patterns), boas práticas de arquitetura e orientação a objetos.
---

## 🚀 Funcionalidades  

### ✅ Implementadas  
- 🔍 Busca no Catálogo – Pesquisa por título, autor, gênero, editora e outros filtros.
- 📚 Empréstimo e Devolução de Itens – Controle completo de circulação de livros, revistas e e-books.
- ⏳ Reservas Automáticas – Usuários podem reservar itens indisponíveis.
- ⚠️ Notificações de Atraso e Disponibilidade – Implementadas com o padrão Observer.
- 👤 Gestão de Membros – Cadastro, consulta e validação de membros.
- 💸 Multas Automáticas – Geração e atualização de multas por atraso, com cálculo via Strategy.
- 📦 Gestão de Acervo – Cadastro, edição e rastreamento de itens físicos e digitais.
- 📅 Eventos da Biblioteca – Agendamento, divulgação e cancelamento de eventos.
- 💾 Persistência de Dados – Exportação e importação do acervo e do estado geral em formato JSON.
- 📊 Relatórios de Uso – Estatísticas sobre empréstimos, membros e multas.

---

## 🧠 Padrões de Projeto Utilizados
### 🏗️ Criação (Creational)
- Factory Method → Criação de diferentes tipos de itens (livros, revistas, e-books).
- Abstract Factory → Criação de fábricas específicas (biblioteca física e digital).
- Builder → Construção fluente e validada de objetos do acervo.
### 🔄 Comportamento (Behavioral)
- Strategy → Políticas de cálculo para prazos de devolução e multas.
- Observer → Notificações automáticas de reservas e atrasos.
- Chain of Responsibility → Validação flexível de campos (membros e itens).
### 🧰 Estrutural (Structural)
- Facade → Interface simplificada para persistência e operações administrativas.
   
---

## ⚠️ Limitações e Implementação Parcial
- 🌐 Interface Web/Mobile: Ainda não implementada.
- 🗄️ Banco de Dados: Dados são mantidos em memória (persistência opcional via arquivos JSON).
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
    
## 🏗️ Estrutura do Projeto
``` bash
  📁 sistema-biblioteca/
  │
  ├── biblioteca.py        # Classes principais e gerenciadores (acervo, membros, eventos, operações)
  ├── builders.py          # Builders para criação de itens do acervo
  ├── classes.py           # Modelos de domínio (Livro, Revista, Ebook, Membro, etc.)
  ├── facade.py            # Interface de persistência (salvar/carregar estado)
  ├── menu.py              # Interface textual interativa
  ├── notifications.py     # Implementação do padrão Observer
  ├── policies.py          # Estratégias para prazos e multas
  ├── validators.py        # Validação com Chain of Responsibility
  ├── main.py              # Ponto de entrada do sistema
  └── acervo_padrao.py     # Dados iniciais de exemplo
```

## 💻 Como Usar

- Execute o sistema com python main.py.
- Navegue pelo menu interativo para:
 - Gerenciar acervo, eventos e membros.
 - Realizar empréstimos, devoluções e reservas.
 - Gerar relatórios e salvar o estado atual da biblioteca.

## 👥 Perfis de Usuário

-Administrador: Acesso total ao acervo, membros, eventos, relatórios e persistência de dados
-Membro: Consulta, empréstimo, reserva e acesso a e-books.

## 💾 Persistência

A persistência é feita por meio da Facade, salvando os dados em JSON com backup automático.

Exemplo:
  ``` bash
  from facade import BibliotecaFacade
  facade = BibliotecaFacade(biblioteca)
  facade.save("dados/biblioteca.json")
  facade.load("dados/biblioteca.json", replace=True)
  ```

## 📌 Sobre

### 📚 Projeto acadêmico sem fins comerciais.
Projeto acadêmico sem fins comerciais, desenvolvido com foco em aprendizado e aplicação prática de princípios de Engenharia de Software.

Recursos

- 🐍 Python
- 🧩 Padrões de Projeto
- ⚙️ Arquitetura modular e extensível
- 💾 Persistência simples em JSON
