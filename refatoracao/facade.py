"""Facade simples para operações de persistência e conveniência sobre a `Biblioteca`.

Fornece métodos para salvar/carregar o estado (acervo, membros, eventos) em JSON e
operações auxiliares úteis para o `menu.py` ou scripts administrativos.
"""
from __future__ import annotations
import json
from datetime import datetime
from typing import Any, Dict
import os
import tempfile
import shutil
import logging

logger = logging.getLogger(__name__)

from classes import Livro, Revista, Ebook
from adapters import CsvCatalogAdapter


class BibliotecaFacade:
    def __init__(self, biblioteca) -> None:
        """Recebe uma instância existente de `Biblioteca` e fornece operações de alto nível."""
        self.biblioteca = biblioteca

    # -------------------- Serialização helpers --------------------
    def _serialize_item(self, item) -> Dict[str, Any]: 
        if isinstance(item, Livro):
            return ["livro", item.titulo, item.autor, item.editora, item.genero, item.total_exemplares, getattr(item, '_isbn', None), None]
        if isinstance(item, Revista):
            return ["revista", item.titulo, item.autor, item.editora, item.genero, item.total_exemplares, getattr(item, '_edicao', None), None]
        if isinstance(item, Ebook):
            return ["ebook", item.titulo, item.autor, item.editora, item.genero, item.total_exemplares, getattr(item, '_formato', None), getattr(item, '_link_download', None)]
        # Fallback: try to read common attributes
        return ["item", getattr(item, 'titulo', None), getattr(item, 'autor', None), getattr(item, 'editora', None), getattr(item, 'genero', None), getattr(item, 'total_exemplares', None), None, None]

    def _serialize_membro(self, membro) -> Dict[str, Any]:
        return [membro.nome, membro.endereco, membro.email]

    def _serialize_evento(self, evento) -> Dict[str, Any]:
        # Evento armazena data como string dd/mm/yyyy
        return [evento._nome if hasattr(evento, '_nome') else getattr(evento, 'nome', None),
                getattr(evento, '_descricao', None) or getattr(evento, 'descricao', None),
                getattr(evento, '_data', None) or getattr(evento, 'data', None),
                getattr(evento, '_local', None) or getattr(evento, 'local', None)]

    # -------------------- Public API --------------------
    def save(self, path: str) -> (bool, str, str | None):
        """Salva acervo, membros e eventos em JSON no caminho `path`. Retorna (ok, msg)."""
        data = {
            'meta': {
                'saved_at': datetime.now().isoformat(),
                'version': 1
            },
            'acervo': [self._serialize_item(i) for i in self.biblioteca.listar_itens()],
            'membros': [self._serialize_membro(m) for m in self.biblioteca.listar_membros()],
            'eventos': [self._serialize_evento(e) for e in self.biblioteca.listar_eventos()]
        }
        try:
            # Garante que o diretório existe
            dirpath = os.path.dirname(path)
            if dirpath:
                os.makedirs(dirpath, exist_ok=True)

            # Se o arquivo já existir, cria um backup com timestamp antes de sobrescrever
            backup_path = None
            if os.path.exists(path):
                try:
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    backup_path = f"{path}.backup.{timestamp}"
                    shutil.copy2(path, backup_path)
                except Exception:
                    # Não falha todo o save se o backup não puder ser criado; continua, mas registra
                    logger.exception("Falha ao criar backup para %s", path)

            # Escrita atômica: escreve em arquivo temporário no mesmo diretório e faz replace
            tmp_dir = dirpath or '.'
            fd, tmp_path = tempfile.mkstemp(prefix='tmp_save_', dir=tmp_dir)
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                # Substitui de forma atômica no nível do sistema operacional
                os.replace(tmp_path, path)
            finally:
                # Assegura limpeza do temporário caso algo dê errado e o arquivo ainda exista
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        logger.exception("Falha ao remover arquivo temporário %s", tmp_path)

            # Retorna o caminho do backup (ou None quando não criado)
            return True, f"✔ Estado salvo em {path}", backup_path
        except Exception as e:
            logger.exception("Falha ao salvar estado em %s", path)
            return False, f"❗️ Erro ao salvar: {e}", None

    def load(self, path: str, replace: bool = False) -> (bool, str):
        """Carrega dados do JSON e popula a biblioteca.

        Se replace=True, limpa acervo/membros/eventos antes de importar.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.exception("Falha ao abrir/ler arquivo %s", path)
            return False, f"❗️ Erro ao abrir arquivo: {e}"

        try:
            acervo = data.get('acervo', [])
            membros = data.get('membros', [])
            eventos = data.get('eventos', [])

            if replace:
                # reinicializa os gerenciadores substituindo listas internas
                self.biblioteca.acervo._item.clear()
                self.biblioteca.membros._membros.clear()
                self.biblioteca.eventos._eventos.clear()

            for tipo, titulo, autor, editora, genero, total_exemplares, extra1, extra2 in acervo:
                kwargs = {}
                if tipo == 'livro':
                    kwargs['isbn'] = extra1
                elif tipo == 'revista':
                    kwargs['edicao'] = extra1
                elif tipo == 'ebook':
                    kwargs['formato'] = extra1
                    kwargs['link_download'] = extra2
                self.biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares, tipo=tipo, **kwargs)

            for nome, endereco, email in membros:
                try:
                    self.biblioteca.cadastrar_membro(nome, endereco, email)
                except Exception:
                    # ignora membros problemáticos e continua, mas registra o erro
                    logger.exception("Falha ao cadastrar membro durante load: %s <%s>", nome, email)

            for nome, descricao, data_evt, local in eventos:
                try:
                    self.biblioteca.agendar_evento(nome, descricao, data_evt, local)
                except Exception:
                    logger.exception("Falha ao agendar evento durante load: %s (%s)", nome, data_evt)

            return True, f"✔ Estado carregado a partir de {path}"
        except Exception as e:
            logger.exception("Falha ao importar dados do arquivo %s", path)
            return False, f"❗️ Erro ao importar dados: {e}"

    def export_acervo(self, path: str) -> (bool, str):
        # Alias para save com apenas acervo
        try:
            data = {'meta': {'exported_at': datetime.now().isoformat()}, 'acervo': [self._serialize_item(i) for i in self.biblioteca.listar_itens()]}
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, f"✔ Acervo exportado para {path}"
        except Exception as e:
            logger.exception("Falha ao exportar acervo para %s", path)
            return False, f"❗️ Erro ao exportar acervo: {e}"

    def import_acervo(self, path: str, merge: bool = True) -> (bool, str):
        # If CSV file, delegate to CsvCatalogAdapter
        try:
            if path.lower().endswith('.csv'):
                adapter = CsvCatalogAdapter(self.biblioteca)
                return adapter.import_file(path, merge=merge)

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.exception("Falha ao abrir/ler arquivo %s", path)
            return False, f"❗️ Erro ao abrir arquivo: {e}"

        try:
            acervo = data.get('acervo', [])
            if not merge:
                self.biblioteca.acervo._item.clear()
            for tipo, titulo, autor, editora, genero, total_exemplares, extra1, extra2 in acervo:
                kwargs = {}
                if tipo == 'livro':
                    kwargs['isbn'] = extra1
                elif tipo == 'revista':
                    kwargs['edicao'] = extra1
                elif tipo == 'ebook':
                    kwargs['formato'] = extra1
                    kwargs['link_download'] = extra2
                self.biblioteca.cadastrar_item(titulo, autor, editora, genero, total_exemplares, tipo=tipo, **kwargs)
            return True, f"✔ Acervo importado de {path}"
        except Exception as e:
            logger.exception("Falha ao importar acervo de %s", path)
            return False, f"❗️ Erro ao importar acervo: {e}"
