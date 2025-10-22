"""Chain of Responsibility validadores para membros e itens.

Cada manipulador implementa handle(context) -> (True, None) em caso de sucesso ou (False, error_msg) em caso de falha.
Simples, leve e evita acoplamento profundo, aceitando funções de retorno de chamada quando necessário.
"""
from typing import Callable, Dict, Optional
import re


class Handler:
    def handle(self, context: Dict) -> (bool, Optional[str]):
        raise NotImplementedError()


class EmailFormatHandler(Handler):
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def handle(self, context: Dict) -> (bool, Optional[str]):
        email = context.get('email')
        if not email:
            return False, "O email é obrigatório." 
        if not EmailFormatHandler.EMAIL_RE.match(email):
            return False, "Formato de email inválido. Informe um email válido."
        return True, None


class DuplicateMemberHandler(Handler):
    def __init__(self, exists_fn: Callable[[str], bool]):
        self.exists_fn = exists_fn

    def handle(self, context: Dict) -> (bool, Optional[str]):
        email = context.get('email')
        if self.exists_fn(email):
            return False, f"Membro com email '{email}' já cadastrado."
        return True, None


class TipoHandler(Handler):
    def __init__(self, allowed: Optional[list] = None):
        self.allowed = allowed or ['livro', 'revista', 'ebook']

    def handle(self, context: Dict) -> (bool, Optional[str]):
        tipo = context.get('tipo')
        if not tipo:
            return False, "Tipo do item é obrigatório."
        if tipo not in self.allowed:
            return False, f"Tipo inválido: {tipo}. Tipos válidos: {', '.join(self.allowed)}"
        return True, None


class TotalExemplaresHandler(Handler):
    def handle(self, context: Dict) -> (bool, Optional[str]):
        total = context.get('total_exemplares')
        try:
            total_int = int(total)
            if total_int < 0:
                return False, "Total de exemplares deve ser não-negativo."
            return True, None
        except Exception:
            return False, "Total de exemplares deve ser um número inteiro."


class EbookLinkHandler(Handler):
    def handle(self, context: Dict) -> (bool, Optional[str]):
        tipo = context.get('tipo')
        if tipo != 'ebook':
            return True, None
        link = context.get('link_download')
        if not link:
            return False, "O campo 'link_download' é obrigatório para ebooks."
        if not (link.startswith('http://') or link.startswith('https://')):
            return False, "O link do ebook deve começar com http:// ou https://"
        return True, None


def run_chain(handlers, context: Dict) -> (bool, Optional[str]):
    for h in handlers:
        ok, msg = h.handle(context)
        if not ok:
            return False, msg
    return True, None
