"""Contrato para futuros adaptadores de busca, sem implementação de rede."""

from __future__ import annotations

from typing import Protocol

from news import NewsItem


class NewsSearchAdapter(Protocol):
    def search(self, sector: str, region: str, news_date: str) -> list[NewsItem]:
        """Retorna três notícias segundo o contrato local."""


class RealTimeNotConfiguredError(RuntimeError):
    pass


def get_real_time_news(sector: str, region: str, news_date: str) -> list[NewsItem]:
    """Ponto de extensão explícito: nenhum provedor real existe nesta etapa."""
    raise RealTimeNotConfiguredError("Modo tempo real não configurado.")
