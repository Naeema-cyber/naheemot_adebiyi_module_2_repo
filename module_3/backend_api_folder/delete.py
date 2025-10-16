from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

DATA_FILE = "data.json"

def load_data():
    """Load data from the JSON file (or create it if missing)."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    """Save updated data back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)



class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status=200):
        """Helper to send JSON response."""
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def parse_request_body(self):
        """Helper to read and parse JSON body."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            return json.loads(post_data)
        return {}
    
    
    def do_DELETE(self):
        """Delete a record by id."""
        data = load_data()
        body = self.parse_request_body()
        record_id = body.get("id")

        if not record_id:
            self.send_data({"error": "Missing 'id' field"}, 400)
            return

        new_data = [item for item in data if item["id"] != record_id]
        if len(new_data) == len(data):
            self.send_data({"error": "Record not found"}, 404)
        else:
            save_data(new_data)
            self.send_data({"message": f"Record with id {record_id} deleted successfully"})



def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, BasicAPI)
    print("Starting server on port 8000...")
    httpd.serve_forever()


if __name__ == "__main__":
    print("Running server...")
    run()