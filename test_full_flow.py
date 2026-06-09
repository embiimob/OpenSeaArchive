from playwright.sync_api import sync_playwright
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.parse
import time

# Create a mock server
class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # suppress logs

    def do_POST(self):
        if self.path == '/api/v2/auth/keys':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "api_key": "mock_api_key",
                "expires_at": "2030-01-01T00:00:00Z"
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Handle CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        if path.startswith('/GetPublicMessagesByAddress'):
            self.wfile.write(json.dumps([]).encode())
            return

        if path.startswith('/api/v2/accounts/'):
            self.wfile.write(json.dumps({
                "account": {
                    "address": "0x95239f3e8f395bb787ec9a0f475e830c6848fdfd",
                    "username": "mock_user"
                }
            }).encode())
            return

        if path.startswith('/api/v2/chain/ethereum/account/'):
            # Mock owned NFTs
            self.wfile.write(json.dumps({
                "nfts": [
                    {
                        "identifier": "67457553150443021914092587022250176347061355639032054621716076114697793830913",
                        "collection": "robotdream",
                        "contract": "0x495f947276749ce646f68ac8c248420045cb7b5e",
                        "name": "bitcoin margaret hamilton",
                        "image_url": "https://i2c.seadn.io/mock.png",
                        "original_image_url": "https://raw2.seadn.io/ethereum/0x495f947276749ce646f68ac8c248420045cb7b5e/mock_orig.png",
                        "total_supply": 1
                    }
                ],
                "next": ""
            }).encode())
            return

        if path.startswith('/api/v2/chain/ethereum/contract/') and not path.startswith('/api/v2/events/chain/ethereum/contract/'):
            # Mock token details
            self.wfile.write(json.dumps({
                "nft": {
                    "identifier": "67457553150443021914092587022250176347061355639032054621716076114697793830913",
                    "collection": "robotdream",
                    "contract": "0x495f947276749ce646f68ac8c248420045cb7b5e",
                    "name": "bitcoin margaret hamilton",
                    "image_url": "https://i2c.seadn.io/mock.png",
                    "original_image_url": "https://raw2.seadn.io/ethereum/0x495f947276749ce646f68ac8c248420045cb7b5e/mock_orig.png",
                    "total_supply": 1
                }
            }).encode())
            return

        if path.startswith('/api/v2/events/chain/ethereum/contract/'):
            # Mock events (MINT)
            self.wfile.write(json.dumps({
                "asset_events": [
                    {
                        "event_type": "transfer",
                        "event_timestamp": 1631412662,
                        "transfer_type": "mint",
                        "from_address": "0x0000000000000000000000000000000000000000",
                        "to_address": "0x95239f3e8f395bb787ec9a0f475e830c6848fdfd"
                    }
                ],
                "next": None
            }).encode())
            return

        self.wfile.write(json.dumps({}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-API-KEY, Content-Type, Accept')
        self.end_headers()

server = HTTPServer(('127.0.0.1', 8080), MockHandler)
t = Thread(target=server.serve_forever)
t.daemon = True
t.start()


def run_cuj(page):
    cwd = os.getcwd()
    page.goto(f"file://{cwd}/index.html")
    page.wait_for_timeout(500)

    # Overwrite APIs to use localhost
    page.evaluate("""() => {
        document.getElementById('openSeaInput').value = 'http://127.0.0.1:8080/api/v2';
        document.getElementById('apiBaseInput').value = 'http://127.0.0.1:8080';
    }""")

    # Generate mock API key
    page.click("button#generateOpenSeaKeyBtn")
    page.wait_for_timeout(1000)

    # Input data
    page.fill("input#keywordInput", "#margaret")
    page.fill("input#userInput", "0x95239f3e8f395bb787ec9a0f475e830c6848fdfd")

    # Analyze
    page.click("button#analyzeBtn")
    page.wait_for_timeout(3000) # Wait for background processing

    # Capture the output
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    page.screenshot(path="/home/jules/verification/screenshots/verification_full.png", full_page=True)
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        os.makedirs("/home/jules/verification/videos", exist_ok=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
