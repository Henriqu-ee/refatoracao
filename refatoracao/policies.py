"""Policies para empréstimo e multa (Strategy pattern).

Define interfaces simples e implementações padrão que podem ser injetadas
em `GerenciadorOperacoes` para alterar regras de negócio sem modificar a lógica.
"""
from abc import ABC, abstractmethod


class EmprestimoPolicy(ABC):
    @abstractmethod
    def dias_devolucao(self, item, membro) -> int:
        """Retorna número de dias para devolução para o dado item/membro."""
        pass


class DefaultEmprestimoPolicy(EmprestimoPolicy):
    def __init__(self, dias: int = 14):
        self.dias = dias

    def dias_devolucao(self, item, membro) -> int:
        # Política simples: sempre retorna um número fixo de dias.
        return self.dias


class MultaPolicy(ABC):
    @abstractmethod
    def valor_por_dia(self, item=None, membro=None) -> float:
        """Retorna o valor da multa por dia de atraso (pode depender de item/membro)."""
        pass


class DefaultMultaPolicy(MultaPolicy):
    def __init__(self, valor_por_dia: float = 0.5):
        self._valor = float(valor_por_dia)

    def valor_por_dia(self, item=None, membro=None) -> float:
        return self._valor
