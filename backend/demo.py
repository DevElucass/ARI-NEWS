"""Dados demonstrativos, estáticos e versionados para execução local."""

from __future__ import annotations

from news import NewsItem, build_google_search_url, validate_news_collection


def _item(title: str, source: str, published_date: str, summary: str, original_url: str) -> NewsItem:
    return NewsItem(
        title=title,
        source=source,
        published_date=published_date,
        summary=summary,
        original_url=original_url,
        google_search_url=build_google_search_url(title),
    )


DEMO_NEWS: tuple[NewsItem, ...] = (
    _item(
        "Dados demonstrativos sobre inovação setorial",
        "Fonte demonstrativa A",
        "2025-01-15",
        "Exemplo local para demonstrar como o painel apresenta impactos de negócio sem representar uma notícia atual.",
        "https://noticias-demo.example/inovacao-setorial",
    ),
    _item(
        "Dados demonstrativos sobre operações regionais",
        "Fonte demonstrativa B",
        "2025-01-16",
        "Exemplo local para visualizar a combinação de setor, região e data com três cards padronizados.",
        "https://noticias-demo.example/operacoes-regionais",
    ),
    _item(
        "Dados demonstrativos sobre decisões de negócios",
        "Fonte demonstrativa C",
        "2025-01-17",
        "Exemplo local para evidenciar o resumo focado em negócios e a preservação da URL de origem demonstrativa.",
        "https://noticias-demo.example/decisoes-negocios",
    ),
)


def get_demo_news() -> list[NewsItem]:
    """Retorna exatamente três itens demonstrativos validados, sem acesso à rede."""
    return validate_news_collection(list(DEMO_NEWS))
