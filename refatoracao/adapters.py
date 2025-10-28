"""Adapters para importar catálogos em formatos diversos (CSV, XML, etc.).

Atualmente implementa um CsvCatalogAdapter que aceita um CSV com colunas:
tipo,titulo,autor,editora,genero,total_exemplares,extra1,extra2

O adapter tenta normalizar cada linha e chamar `biblioteca.cadastrar_item`.
"""
from __future__ import annotations
import csv
from typing import Tuple


class CsvCatalogAdapter:
    def __init__(self, biblioteca) -> None:
        self.biblioteca = biblioteca

    def import_file(self, path: str, merge: bool = True) -> Tuple[bool, str]:
        """Importa itens de um CSV. Retorna (ok, mensagem resumida).

        Espera linhas com 8 campos: tipo,titulo,autor,editora,genero,total_exemplares,extra1,extra2
        Campos extras dependem do tipo (isbn/edicao/formato/link)
        """
        imported = 0
        skipped = 0
        errors = 0

        try:
            if not merge:
                # remove itens atuais
                try:
                    self.biblioteca.acervo._item.clear()
                except Exception:
                    pass

            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    # Skip empty/comment lines
                    if not row or (len(row) == 1 and not row[0].strip()):
                        continue
                    try:
                        # Normalize to 8 columns
                        cols = row + [None] * (8 - len(row))
                        tipo, titulo, autor, editora, genero, total_exemplares, extra1, extra2 = cols[:8]
                        # Convert total_exemplares to int when possible
                        try:
                            total_exemplares = int(total_exemplares) if total_exemplares not in (None, '') else 1
                        except Exception:
                            total_exemplares = 1

                        kwargs = {}
                        if tipo == 'livro':
                            kwargs['isbn'] = extra1
                        elif tipo == 'revista':
                            kwargs['edicao'] = extra1
                        elif tipo == 'ebook':
                            kwargs['formato'] = extra1
                            kwargs['link_download'] = extra2

                        self.biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares, tipo=tipo, **kwargs)
                        imported += 1
                    except Exception:
                        errors += 1
                        continue

            msg = f"✔ Importação concluída. Importados: {imported}. Ignorados: {skipped}. Erros: {errors}."
            return True, msg
        except FileNotFoundError:
            return False, f"❗️ Arquivo CSV não encontrado: {path}"
        except Exception as e:
            return False, f"❗️ Erro ao importar CSV: {e}"
