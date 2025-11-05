"""Módulo simples para implementar o padrão Observer para notificações de reserva.

Fornece uma API para registrar observadores (objetos com método `update(reserva)`)
e notificar quando uma reserva precisa ser comunicada.
"""
from typing import List, Protocol
import logging

logger = logging.getLogger(__name__)


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
        except Exception:
            # Log the observer failure but continue notifying others
            logger.exception("Erro ao notificar observador %r", obs)


# Implementação padrão simples: print de notificação.
class SimplePrintObserver:
    def update(self, reserva) -> None:
        try:
            titulo = reserva.livro.titulo
            membro = reserva.membro
            print(f"\n🔔 Notificação (Observer): O livro '{titulo}' ficou disponível para {membro.nome} ({membro.email}).")
        except Exception:
            logger.exception("Erro ao formatar notificação de reserva: %r", reserva)
            print("🔔 Notificação: reserva disponível (detalhes indisponíveis)")


# Registra um observador padrão ao importar o módulo para manter comportamento atual.
register_observer(SimplePrintObserver())
