"""Módulo simples para implementar o padrão Observer para notificações de reserva.

Fornece uma API para registrar observadores (objetos com método `update(reserva)`)
e notificar quando uma reserva precisa ser comunicada.
"""
from typing import List, Protocol


class ReservationObserver(Protocol):
    def update(self, reserva) -> None:
        ...


_observers: List[ReservationObserver] = []


def register_observer(observer: ReservationObserver) -> None:
    """Registra um observador. Observadores devem implementar update(reserva)."""
    _observers.append(observer)


def clear_observers() -> None:
    _observers.clear()


def notify_reservation(reserva) -> None:
    """Notifica todos os observadores sobre a reserva.

    Falhas em um observador são logadas (print) e não interrompem a notificação.
    """
    for obs in list(_observers):
        try:
            obs.update(reserva)
        except Exception as e:
            print(f"Erro ao notificar observador {obs}: {e}")


# Implementação padrão simples: print de notificação.
class SimplePrintObserver:
    def update(self, reserva) -> None:
        try:
            titulo = reserva.livro.titulo
            membro = reserva.membro
            print(f"\n🔔 Notificação (Observer): O livro '{titulo}' ficou disponível para {membro.nome} ({membro.email}).")
        except Exception:
            print("🔔 Notificação: reserva disponível (detalhes indisponíveis)")


# Registra um observador padrão ao importar o módulo para manter comportamento atual.
register_observer(SimplePrintObserver())
