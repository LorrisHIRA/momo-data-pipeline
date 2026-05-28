import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.auth import check_auth
from api.data import load_transactions, save_transactions

class MoMoAPIHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_GET(self):
        if not check_auth(self.headers):
            self.send_json(401, {"error": "Unauthorized. Invalid or missing credentials."})
            return

        parsed = urlparse(self.path)
        path = parsed.path

        transactions = load_transactions()

        if path == "/transactions":
            params = parse_qs(parsed.query)
            limit = int(params.get("limit", [len(transactions)])[0])
            offset = int(params.get("offset", [0])[0])
            page = transactions[offset:offset + limit]
            self.send_json(200, {
                "total": len(transactions),
                "limit": limit,
                "offset": offset,
                "transactions": page
            })

        elif path.startswith("/transactions/"):
            try:
                tx_id = int(path.split("/")[-1])
                tx = next((t for t in transactions if t["id"] == tx_id), None)
                if tx:
                    self.send_json(200, tx)
                else:
                    self.send_json(404, {"error": f"Transaction with id {tx_id} not found."})
            except ValueError:
                self.send_json(400, {"error": "Invalid transaction ID."})

        else:
            self.send_json(404, {"error": "Endpoint not found."})

    def do_POST(self):
        if not check_auth(self.headers):
            self.send_json(401, {"error": "Unauthorized. Invalid or missing credentials."})
            return

        if self.path == "/transactions":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                new_tx = json.loads(body)
            except json.JSONDecodeError:
                self.send_json(400, {"error": "Invalid JSON body."})
                return

            transactions = load_transactions()
            new_tx["id"] = max((t["id"] for t in transactions), default=0) + 1
            transactions.append(new_tx)
            save_transactions(transactions)
            self.send_json(201, {"message": "Transaction created.", "transaction": new_tx})
        else:
            self.send_json(404, {"error": "Endpoint not found."})

    def do_PUT(self):
        if not check_auth(self.headers):
            self.send_json(401, {"error": "Unauthorized. Invalid or missing credentials."})
            return

        if self.path.startswith("/transactions/"):
            try:
                tx_id = int(self.path.split("/")[-1])
            except ValueError:
                self.send_json(400, {"error": "Invalid transaction ID."})
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                updated_data = json.loads(body)
            except json.JSONDecodeError:
                self.send_json(400, {"error": "Invalid JSON body."})
                return

            transactions = load_transactions()
            for i, tx in enumerate(transactions):
                if tx["id"] == tx_id:
                    transactions[i].update(updated_data)
                    save_transactions(transactions)
                    self.send_json(200, {"message": "Transaction updated.", "transaction": transactions[i]})
                    return

            self.send_json(404, {"error": f"Transaction with id {tx_id} not found."})
        else:
            self.send_json(404, {"error": "Endpoint not found."})

    def do_DELETE(self):
        if not check_auth(self.headers):
            self.send_json(401, {"error": "Unauthorized. Invalid or missing credentials."})
            return

        if self.path.startswith("/transactions/"):
            try:
                tx_id = int(self.path.split("/")[-1])
            except ValueError:
                self.send_json(400, {"error": "Invalid transaction ID."})
                return

            transactions = load_transactions()
            new_transactions = [t for t in transactions if t["id"] != tx_id]

            if len(new_transactions) == len(transactions):
                self.send_json(404, {"error": f"Transaction with id {tx_id} not found."})
                return

            save_transactions(new_transactions)
            self.send_json(200, {"message": f"Transaction {tx_id} deleted."})
        else:
            self.send_json(404, {"error": "Endpoint not found."})

    def log_message(self, format, *args):
        pass


def run(host="0.0.0.0", port=8080):
    server = HTTPServer((host, port), MoMoAPIHandler)
    print(f"MoMo API running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    run()