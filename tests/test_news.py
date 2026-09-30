import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from news import (  # noqa: E402
    NewsItem,
    NewsValidationError,
    build_google_search_url,
    google_slug,
    validate_http_url,
    validate_iso_date,
    validate_news_collection,
    validate_news_item,
)


def item(title: str = "Notícia de teste") -> NewsItem:
    return NewsItem(title, "Fonte", "2025-01-15", "Resumo demonstrativo.", "https://fonte.example/noticia", build_google_search_url(title))


class NewsValidationTests(unittest.TestCase):
    def test_rejects_fewer_than_three_news(self):
        with self.assertRaisesRegex(NewsValidationError, "exatamente 3"):
            validate_news_collection([item(), item("Outra notícia")])

    def test_rejects_more_than_three_news(self):
        with self.assertRaisesRegex(NewsValidationError, "exatamente 3"):
            validate_news_collection([item(), item("2"), item("3"), item("4")])

    def test_rejects_missing_required_field(self):
        invalid = NewsItem("", "Fonte", "2025-01-15", "Resumo", "https://fonte.example/a", "https://www.google.com/search?q=x")
        with self.assertRaisesRegex(NewsValidationError, "title"):
            validate_news_item(invalid)

    def test_accepts_iso_date(self):
        self.assertEqual("2025-01-15", validate_iso_date("2025-01-15"))

    def test_rejects_invalid_date(self):
        with self.assertRaisesRegex(NewsValidationError, "YYYY-MM-DD"):
            validate_iso_date("15/01/2025")

    def test_accepts_http_and_https_urls(self):
        self.assertEqual("http://fonte.example/a", validate_http_url("http://fonte.example/a", "original_url"))
        self.assertEqual("https://fonte.example/a", validate_http_url("https://fonte.example/a", "original_url"))

    def test_rejects_invalid_url(self):
        with self.assertRaisesRegex(NewsValidationError, "http/https"):
            validate_http_url("fonte.example/a", "original_url")

    def test_slug_removes_accents(self):
        self.assertEqual("prefeitura-apresenta-uso-de-tecnologia", google_slug("Prefeitura apresenta uso de tecnologia"))

    def test_slug_removes_punctuation(self):
        self.assertEqual("ia-negocios-2025", google_slug("IA, negócios! 2025?"))

    def test_builds_google_search_url(self):
        self.assertEqual(
            "https://www.google.com/search?q=prefeitura-apresenta-uso-de-tecnologia-na-expo-manaus",
            build_google_search_url("Prefeitura apresenta uso de tecnologia na Expo Manaus"),
        )


if __name__ == "__main__":
    unittest.main()
