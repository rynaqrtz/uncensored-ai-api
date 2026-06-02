from http.server import BaseHTTPRequestHandler
import json, urllib.parse, sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unces import chat, CREATOR

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        prompt = " ".join(params.get("prompt", []))
        if not prompt:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "creator": CREATOR, "error": 'Parameter "prompt" diperlukan'}).encode())
            return

        try:
            result = chat(
                prompt=prompt,
                temperature=float(params.get("temp", [0.9])[0]),
                max_tokens=int(params.get("max", [100000])[0]),
                new_chat=("new" in params or "n" in params),
                stream=False
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "creator": CREATOR, "error": str(e)}).encode())
PYEOF
