"""Servidor HTTP mínimo para health check (Kubernetes probes). Roda em thread separada."""

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


HEALTH_PATH = "/health-check"


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == HEALTH_PATH:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Silencia logs do http.server


def start_health_check_server(port: int, host: str = "0.0.0.0") -> threading.Thread:
    server = HTTPServer((host, port), HealthCheckHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return thread
