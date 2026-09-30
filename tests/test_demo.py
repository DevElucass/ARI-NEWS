import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from demo import get_demo_news  # noqa: E402
from providers import RealTimeNotConfiguredError, get_real_time_news  # noqa: E402


class DemoTests(unittest.TestCase):
    def test_demo_has_exactly_three_valid_news(self):
        news = get_demo_news()
        self.assertEqual(3, len(news))
        self.assertTrue(all(item.original_url.endswith(("inovacao-setorial", "operacoes-regionais", "decisoes-negocios")) for item in news))
        self.assertTrue(all(".example/" in item.original_url for item in news))

    def test_realtime_mode_is_not_configured(self):
        with self.assertRaisesRegex(RealTimeNotConfiguredError, "Modo tempo real não configurado"):
            get_real_time_news("Tecnologia", "Brasil", "2025-01-01")


if __name__ == "__main__":
    unittest.main()
