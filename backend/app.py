"""Servidor HTTP local do MVP ARI NEWS, baseado apenas na biblioteca padrão."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from demo import get_demo_news
from news import NewsValidationError, validate_request_context
from providers import RealTimeNotConfiguredError, get_real_time_news


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


class AriNewsHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - assinatura exigida pela biblioteca padrão
        parsed = urlparse(self.path)
        if parsed.path == "/api/news":
            self._handle_news(parsed.query)
            return
        static_files = {
            "/": (FRONTEND / "index.html", "text/html; charset=utf-8"),
            "/index.html": (FRONTEND / "index.html", "text/html; charset=utf-8"),
            "/app.js": (FRONTEND / "app.js", "application/javascript; charset=utf-8"),
            "/assets/hero-demo.svg": (FRONTEND / "assets" / "hero-demo.svg", "image/svg+xml"),
        }
        requested = static_files.get(parsed.path)
        if requested is None:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Recurso não encontrado."})
            return
        path, content_type = requested
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(path.stat().st_size))
        self.end_headers()
        self.wfile.write(path.read_bytes())

    def _handle_news(self, query: str) -> None:
        values = parse_qs(query)
        mode = values.get("mode", ["demo"])[0]
        try:
            sector, region, news_date = validate_request_context(
                values.get("sector", [""])[0],
                values.get("region", [""])[0],
                values.get("date", [""])[0],
            )
            if mode == "demo":
                items = get_demo_news()
                self._send_json(
                    HTTPStatus.OK,
                    {
                        "mode": "demo",
                        "notice": "Dados demonstrativos locais: não representam notícias atuais nem busca em tempo real.",
                        "sector": sector,
                        "region": region,
                        "date": news_date,
                        "hero_image": "/assets/hero-demo.svg",
                        "news": [item.to_dict() for item in items],
                    },
                )
                return
            if mode == "realtime":
                items = get_real_time_news(sector, region, news_date)
                self._send_json(HTTPStatus.OK, {"mode": "realtime", "news": [item.to_dict() for item in items]})
                return
            raise NewsValidationError("Modo inválido. Use DEMO ou TEMPO REAL.")
        except RealTimeNotConfiguredError as error:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": str(error)})
        except NewsValidationError as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})

    def _send_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format: str, *args: object) -> None:
        """Mantém o terminal local sem logs de acesso a cada recurso estático."""


def run(port: int = 8000) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), AriNewsHandler)
    print(f"ARI NEWS disponível em http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
