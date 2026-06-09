from http.server import BaseHTTPRequestHandler, HTTPServer
import json

tasks = []

class Handler(BaseHTTPRequestHandler):

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == "/":
            self._send(200, {"message": "Service is running"})

        elif self.path == "/tasks":
            self._send(200, tasks)

        else:
            self._send(404, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/tasks":
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            data = json.loads(body)

            task = data.get("title", "No title")
            tasks.append(task)

            self._send(201, {
                "message": "Task added",
                "task": task
            })
        else:
            self._send(404, {"error": "Not found"})

server = HTTPServer(("0.0.0.0", 5000), Handler)
server.serve_forever()