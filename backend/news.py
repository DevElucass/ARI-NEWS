"""Contrato, validação e formatação local das notícias ARI NEWS."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
import re
import unicodedata
from urllib.parse import urlsplit


GOOGLE_SEARCH_PREFIX = "https://www.google.com/search?q="


class NewsValidationError(ValueError):
    """Os dados locais não atendem ao contrato ARI NEWS."""


@dataclass(frozen=True)
class NewsItem:
    title: str
    source: str
    published_date: str
    summary: str
    original_url: str
    google_search_url: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def google_slug(title: str) -> str:
    """Converte um título em slug de busca conforme o Nó 6 da Aula 1."""
    normalized = "".join(
        char for char in unicodedata.normalize("NFD", title.casefold())
        if unicodedata.category(char) != "Mn"
    )
    words = re.findall(r"[a-z0-9]+", normalized)
    return "-".join(words)


def build_google_search_url(title: str) -> str:
    slug = google_slug(title)
    if not slug:
        raise NewsValidationError("O título deve conter caracteres para gerar a URL Google.")
    return f"{GOOGLE_SEARCH_PREFIX}{slug}"


def validate_iso_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise NewsValidationError("A data deve estar no formato ISO YYYY-MM-DD.") from error
    if parsed.isoformat() != value:
        raise NewsValidationError("A data deve estar no formato ISO YYYY-MM-DD.")
    return value


def validate_http_url(value: str, field_name: str) -> str:
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise NewsValidationError(f"{field_name} deve ser uma URL http/https válida.")
    return value


def validate_news_item(item: NewsItem) -> NewsItem:
    for field_name in ("title", "source", "published_date", "summary", "original_url", "google_search_url"):
        if not getattr(item, field_name).strip():
            raise NewsValidationError(f"O campo obrigatório {field_name} está vazio.")
    validate_iso_date(item.published_date)
    validate_http_url(item.original_url, "original_url")
    validate_http_url(item.google_search_url, "google_search_url")
    expected_google_url = build_google_search_url(item.title)
    if item.google_search_url != expected_google_url:
        raise NewsValidationError("google_search_url deve ser gerada a partir do título.")
    return item


def validate_news_collection(items: list[NewsItem]) -> list[NewsItem]:
    if len(items) != 3:
        raise NewsValidationError("A ARI NEWS requer exatamente 3 notícias.")
    return [validate_news_item(item) for item in items]


def validate_request_context(sector: str, region: str, news_date: str) -> tuple[str, str, str]:
    if not sector.strip():
        raise NewsValidationError("Setor é obrigatório.")
    if not region.strip():
        raise NewsValidationError("Região é obrigatória.")
    return sector.strip(), region.strip(), validate_iso_date(news_date)
