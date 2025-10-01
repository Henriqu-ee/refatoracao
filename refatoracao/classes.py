from abc import ABC, abstractmethod

from datetime import datetime

VALOR_MULTA = 0.5

#------------------ CLASSE ABSTRATA ------------------
class Item(ABC):
    def __init__(self, titulo: str, autor: str, editora: str, genero: str, total_exemplares: int) -> None:
        self._titulo = titulo
        self._autor = autor
        self._editora = editora
        self._genero = genero
        self._total_exemplares = total_exemplares
        self._exemplares_disponiveis = total_exemplares #Começa com todos os exemplares disponíveis.

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def editora(self):
        return self._editora

    @property
    def genero(self):
        return self._genero

    @property
    def total_exemplares(self):
        return self._total_exemplares

    @property
    def exemplares_disponiveis(self):
        return self._exemplares_disponiveis

    def verificar_disponibilidade(self) -> bool:
        return self._exemplares_disponiveis > 0

    def emprestar(self) -> bool:
        #Decrementa o número de exemplares disponíveis se houver algum.
        if self.verificar_disponibilidade():
            self._exemplares_disponiveis -= 1
            return True
        return False

    def devolver(self) -> None:
        #Incrementa o número de exemplares disponíveis ao receber uma devolução.
        if self._exemplares_disponiveis < self._total_exemplares:
            self._exemplares_disponiveis += 1
        else:
            print(f"Todos os exemplares de '{self._titulo}' já se encontram no acervo.")

    @abstractmethod
    def __str__(self) -> str:
        #Método abstrato para forçar subclasses a implementar uma representação em string.
        pass

    @abstractmethod
    def info_basica(self) -> str:
        #Método abstrato para uma informação básica e rápida do item.
        pass

    # Compatibilidade: método `descricao()` usado pelo menu e pela fábrica refatorada.
    def descricao(self) -> str:
        return self.info_basica()


#------------------ SUBCLASSES ------------------
class Livro(Item):
    def __init__(self, titulo: str, autor: str, editora: str, genero: str, total_exemplares: int, isbn=None) -> None:
        super().__init__(titulo, autor, editora, genero, total_exemplares)
        self._isbn = isbn

    # Expor atributos com nomes públicos para compatibilidade com o restante do código
    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def genero(self):
        return self._genero

    @property
    def exemplares_disponiveis(self):
        return self._exemplares_disponiveis

    @property
    def total_exemplares(self):
        return self._total_exemplares

    def __str__(self) -> str:
        base = (
            f"{self.info_basica()}\n"
            f"   - Gênero: {self.genero}\n"
            f"   - Exemplares: {self.exemplares_disponiveis}/{self.total_exemplares}"
        )
        if self._isbn:
            base += f"\n   - ISBN: {self._isbn}"
        return base

    def info_basica(self) -> str:
        return f"📚 {self.titulo} ({self.autor})"


class Revista(Item):
    def __init__(self, titulo: str, autor: str, editora: str, genero: str, total_exemplares: int, edicao=None) -> None:
        super().__init__(titulo, autor, editora, genero, total_exemplares)
        self._edicao = edicao

    def __str__(self) -> str:
        base = (
            f"{self.info_basica()}\n"
            f"   - Gênero: {self.genero}\n"
            f"   - Exemplares: {self.exemplares_disponiveis}/{self.total_exemplares}"
        )
        if self._edicao:
            base += f"\n   - Edição: {self._edicao}"
        return base

    def info_basica(self) -> str:
        return f"📰 {self.titulo} - {self.editora}"

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def genero(self):
        return self._genero

    @property
    def exemplares_disponiveis(self):
        return self._exemplares_disponiveis

    @property
    def total_exemplares(self):
        return self._total_exemplares


class Ebook(Item):
    def __init__(self, titulo: str, autor: str, editora: str, genero: str, total_exemplares: int, formato: str, link_download: str) -> None:
        super().__init__(titulo, autor, editora, genero, total_exemplares)
        self._formato = formato
        self._link_download = link_download

    def verificar_disponibilidade(self) -> bool:
        #Sobrescreve o método original; ebooks estão sempre disponíveis.
        return True

    def emprestar(self) -> bool:
        #Sobrescreve o método original; emprestar um ebook não altera a disponibilidade.
        return True

    def devolver(self) -> None:
        #Sobrescreve o método original; a devolução de um ebook não é necessária.
        pass
    
    @property 
    def link_download(self) -> str:
        return self._link_download

    def __str__(self) -> str:
        return (
            f"{self.info_basica()} por {self.autor}\n"
            f"   - Gênero: {self.genero}"
        )

    def info_basica(self) -> str:
        return f"💻 {self.titulo} [{self._formato}]"

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def genero(self):
        return self._genero

    @property
    def exemplares_disponiveis(self):
        return self._exemplares_disponiveis

    @property
    def total_exemplares(self):
        return self._total_exemplares

    @property 
    def link_download(self) -> str:
        return self._link_download


#------------------ OUTRAS CLASSES ------------------
class Membro:
    def __init__(self, nome: str, endereco: str, email: str) -> None:
        self._nome = nome
        self._endereco = endereco
        self.email = email #Utiliza o setter para validação

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def email(self) -> str:
        return self._email 
    
    @email.setter
    def email(self, novo_email: str) -> None:
        #Define o email do membro, com validação de formato.
        if not novo_email.endswith("@email.com"):
            raise ValueError("O email deve terminar com @email.com")
        self._email = novo_email
        
    def __str__(self) -> str:
        return (
            f"  👤 Membro: {self._nome}\n"
            f"   - Endereço: {self._endereco}\n"
            f"   - Email: {self._email}"
        )


class Emprestimo:
    def __init__(self, livro: Livro, membro: Membro, data_emprestimo: datetime, data_devolucao_prevista: datetime) -> None:
        self._livro = livro
        self._membro = membro
        self._data_emprestimo = data_emprestimo
        self._data_devolucao_prevista = data_devolucao_prevista

    @property
    def livro(self):
        return self._livro

    @property
    def membro(self):
        return self._membro

    @property
    def data_emprestimo(self):
        return self._data_emprestimo

    @property
    def data_devolucao_prevista(self):
        return self._data_devolucao_prevista

    def __str__(self) -> str:
        return (
            f"  - Empréstimo de {self._livro.info_basica()} para {self._membro.nome}:\n"
            f"  - Data de empréstimo: {self._data_emprestimo.strftime('%d/%m/%Y')}\n"
            f"  - Data prevista de devolução: {self._data_devolucao_prevista.strftime('%d/%m/%Y')}"
        )


class Evento:
    def __init__(self, nome: str, descricao: str, data: str, local: str) -> None:
        self._nome = nome
        self._descricao = descricao
        self.data = data #Utiliza o setter para validação
        self._local = local

    @property
    def nome(self):
        return self._nome
    
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, nova_data: str):
        #Define a data do evento, validando o formato (dd/mm/yyyy).
        try:
            datetime.strptime(nova_data, '%d/%m/%Y')
            self._data = nova_data
        except ValueError:
            raise ValueError("O formato da data deve ser dd/mm/yyyy")

    def __str__(self) -> str:
        return (
            f"  🗓️ Evento: {self._nome}\n"
            f"   - Descrição: {self._descricao}\n"
            f"   - Data: {self._data}\n"
            f"   - Local: {self._local}"
        )


class Reserva:
    def __init__(self, livro: Livro, membro: Membro, data_reserva: datetime) -> None: 
        self._livro = livro
        self._membro = membro
        self._data_reserva = data_reserva
        self._status = "pendente" #Status pode ser 'pendente', 'confirmada' ou 'cancelada'.
        
    @property
    def livro(self):
        return self._livro
    
    @property
    def membro(self):
        return self._membro

    def confirmar_reserva(self):
        self._status = "confirmada"

    def cancelar_reserva(self):
        self._status = "cancelada"
        
    def __str__(self):
        return (
            f"  - Reserva de {self._livro.info_basica()} por {self._membro.nome}:\n"
            f"  - Data da Reserva: {self._data_reserva.strftime('%d/%m/%Y')}\n"
            f"  - Status: {self._status}"
        )


class Multa:
    def __init__(self, emprestimo_atrasado: Emprestimo, valor: float) -> None:
        self._emprestimo_atrasado = emprestimo_atrasado
        self._valor = valor
        self._pago = False #A multa começa como não paga.
        self. _dias_atraso = 0

    @property
    def valor(self):
        return self._valor

    @property
    def pago(self):
        return self._pago
    
    @property
    def emprestimo_atrasado(self):
        return self._emprestimo_atrasado
    
    @property
    def dias_atraso(self):
        return self._dias_atraso

    def pagar(self) -> bool:
        if not self._pago:
            self._pago = True
            return True
        return False
    
    def atualizar_valor(self, data_atual: datetime):
        #Calcula os dias de atraso e atualiza o valor da multa.
        dias = (data_atual - self.emprestimo_atrasado.data_devolucao_prevista).days
        
        if dias > 0:
            self._dias_atraso = dias
            self._valor = self._dias_atraso * VALOR_MULTA
        else:
            self._dias_atraso = 0
            self._valor = 0

    def __str__(self) -> str:
        status_multa = "Paga" if self._pago else "Pendente"
        return (
            f"  - Multa {status_multa} para o item {self._emprestimo_atrasado.livro.info_basica()}:\n"
            f"  - Membro: {self._emprestimo_atrasado.membro.nome}\n"
            f"  - Valor: R$ {self._valor:.2f}"
        )
