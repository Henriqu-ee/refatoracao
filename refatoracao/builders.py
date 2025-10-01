"""Builders para criação de itens do acervo.

Fornece builders para Livro, Revista e Ebook, com validações e API fluente.
Os builders retornam instâncias das classes definidas em `classes.py`.
"""
from __future__ import annotations
from typing import Optional
import re

from classes import Livro, Revista, Ebook


class ItemBuilder:
    def __init__(self) -> None:
        self._titulo: Optional[str] = None
        self._autor: Optional[str] = None
        self._editora: Optional[str] = None
        self._genero: Optional[str] = None
        self._total_exemplares: Optional[int] = None

    def with_titulo(self, titulo: str):
        self._titulo = titulo.strip()
        return self

    def with_autor(self, autor: str):
        self._autor = autor.strip()
        return self

    def with_editora(self, editora: str):
        self._editora = editora.strip()
        return self

    def with_genero(self, genero: str):
        self._genero = genero.strip()
        return self

    def with_total_exemplares(self, total: int):
        if not isinstance(total, int) or total < 0:
            raise ValueError("total_exemplares deve ser inteiro não-negativo")
        self._total_exemplares = total
        return self

    def _validate_base(self):
        if not self._titulo:
            raise ValueError("O título é obrigatório")
        if not self._autor:
            raise ValueError("O autor/editora é obrigatório")
        if self._total_exemplares is None:
            raise ValueError("Total de exemplares é obrigatório")


class LivroBuilder(ItemBuilder):
    def __init__(self) -> None:
        super().__init__()
        self._isbn: Optional[str] = None

    def with_isbn(self, isbn: Optional[str]):
        self._isbn = isbn.strip() if isbn else None
        return self

    def build(self) -> Livro:
        self._validate_base()
        return Livro(self._titulo, self._autor, self._editora, self._genero, self._total_exemplares, self._isbn)


class RevistaBuilder(ItemBuilder):
    def __init__(self) -> None:
        super().__init__()
        self._edicao: Optional[str] = None

    def with_edicao(self, edicao: Optional[str]):
        self._edicao = edicao.strip() if edicao else None
        return self

    def build(self) -> Revista:
        self._validate_base()
        return Revista(self._titulo, self._autor, self._editora, self._genero, self._total_exemplares, self._edicao)


class EbookBuilder(ItemBuilder):
    LINK_PATTERN = re.compile(r"^https?://")

    def __init__(self) -> None:
        super().__init__()
        self._formato: str = "PDF"
        self._link_download: Optional[str] = None

    def with_formato(self, formato: Optional[str]):
        if formato:
            self._formato = formato.strip()
        return self

    def with_link_download(self, link: str):
        self._link_download = link.strip()
        return self

    def build(self) -> Ebook:
        self._validate_base()
        if not self._link_download:
            raise ValueError("O campo 'link_download' é obrigatório para ebooks.")
        if not EbookBuilder.LINK_PATTERN.match(self._link_download):
            raise ValueError("O link para download deve começar com http:// ou https://")
        return Ebook(self._titulo, self._autor, self._editora, self._genero, self._total_exemplares, self._formato, self._link_download)


def create_builder(tipo: str):
    tipo = tipo.lower() if tipo else ''
    if tipo == 'livro':
        return LivroBuilder()
    if tipo == 'revista':
        return RevistaBuilder()
    if tipo == 'ebook':
        return EbookBuilder()
    raise ValueError(f"Tipo desconhecido para builder: {tipo}")
