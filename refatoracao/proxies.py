"""Objetos proxy para controlar o acesso a recursos como e-books.

EbookProxy envolve um `Ebook` e aplica regras de autorização (ex.: bloqueio por multas)
e permite contabilizar acessos (contador simples) sem modificar a classe `Ebook`.
"""
from __future__ import annotations
from typing import Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EbookProxy:
    def __init__(self, ebook, biblioteca) -> None:
        self._ebook = ebook
        self._biblioteca = biblioteca

    def get_link(self, membro=None) -> Tuple[bool, str]:
        """Retorna (True, link) se o membro pode acessar o ebook,
        ou (False, mensagem) quando o acesso é bloqueado.

        Regras aplicadas atualmente:
        - Se `membro` tiver multas pendentes (via `biblioteca.listar_multas_do_membro`), negar acesso.
        - Caso contrário, retorna o link de download.
        """
        # Se não houver um membro especificado, retorna o link (uso público)
        if membro is None:
            return True, getattr(self._ebook, 'link_download', '')

        try:
            multas = self._biblioteca.listar_multas_do_membro(membro)
            if multas:
                return False, f"❗️ Acesso negado. O membro '{membro.nome}' possui multas pendentes."
        except Exception:
            # Se não for possível verificar multas, negar por segurança e logar
            logger.exception("Falha ao verificar multas para membro %s", getattr(membro, 'email', None))
            return False, "❗️ Não foi possível verificar o status do membro. Contate o administrador."

        # Registra acesso simples (contador) sem alterar a classe original
        try:
            count = getattr(self._ebook, '_access_count', 0) + 1
            setattr(self._ebook, '_access_count', count)
        except Exception:
            logger.exception("Falha ao incrementar contador de acessos para ebook %s", getattr(self._ebook, 'titulo', None))

        return True, getattr(self._ebook, 'link_download', '')

    def descricao(self) -> str:
        # Delegar para o ebook para manter compatibilidade com menus
        try:
            return self._ebook.descricao()
        except Exception:
            logger.exception("Falha ao obter descricao do ebook %s", getattr(self._ebook, 'titulo', None))
            return str(self._ebook)

    @property
    def titulo(self):
        return getattr(self._ebook, 'titulo', '')

    def __str__(self):
        return self.descricao()
