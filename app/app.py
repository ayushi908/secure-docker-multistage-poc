import http.server
import socketserver
import os
import socket
import json

PORT = 5000

class Handler(http.server.BaseHTTPRequestHandler):

    def _send_response(self, content, content_type="text/html"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(content.encode())

    def do_GET(self):

        # ROOT ENDPOINT
        if self.path == "/":
            content = f"""
            <html>
            <head><title>Secure App</title></head>
            <body>
                <h1>🚀 Secure Docker App</h1>
                <p><b>User ID:</b> {os.getuid()}</p>
                <p><b>Hostname:</b> {socket.gethostname()}</p>
                <p><b>Working Directory:</b> {os.getcwd()}</p>

                <h3>Available Endpoints:</h3>
                <ul>
                    <li><a href="/health">/health</a></li>
                    <li><a href="/env">/env</a></li>
                </ul>
            </body>
            </html>
            """
            self._send_response(content)

        # HEALTH ENDPOINT
        elif self.path == "/health":
            content = """
            <html>
            <body>
                <h1 style="color:green;">✅ HEALTH: OK</h1>
            </body>
            </html>
            """
            self._send_response(content)

        # ENV ENDPOINT (JSON FORMAT)
        elif self.path == "/env":
            env_data = dict(os.environ)
            json_data = json.dumps(env_data, indent=2)

            self._send_response(json_data, content_type="application/json")

        # DEFAULT
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Not Found")


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Running on port {PORT} as UID {os.getuid()}")
        httpd.serve_forever()