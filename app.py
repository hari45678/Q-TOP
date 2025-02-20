import http.server
import socketserver
import subprocess
import datetime
import pytz
import os

class HtopHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/htop':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # 1. Get name (replace with your full name)
            name = "Hariom Gupta"
            
            # 2. Get system username
            username = os.getenv('USER', subprocess.getoutput('whoami'))
            
            # 3. Get server time in IST
            ist_timezone = pytz.timezone('Asia/Kolkata')
            server_time = datetime.datetime.now(ist_timezone).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            
            # 4. Get top output
            top_output = subprocess.getoutput('top -b -n 1')
            
            # Create HTML response
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>HTOP Information</title>
                <style>
                    body {{ font-family: monospace; margin: 20px; line-height: 1.5; }}
                    pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                </style>
            </head>
            <body>
                <p><b>Name:</b> {name}</p>
                <p><b>User:</b> {username}</p>
                <p><b>Server Time (IST):</b> {server_time}</p>
                <p><b>TOP output:</b></p>
                <pre>{top_output}</pre>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Go to <a href="/htop">/htop</a> for system information.')

# Run the server on port 3000
port = 3000
handler = HtopHandler
httpd = socketserver.TCPServer(("", port), handler)

print(f"Server running at http://0.0.0.0:{port}")
httpd.serve_forever()