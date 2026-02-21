#!/usr/bin/env python3
import ssl
import http.server
import socketserver
import os
import sys
import tempfile
from pathlib import Path

# Configuration
PORT = 8443
CERT_FILE = r'D:\NoSync\misc\Comp\EdgeExtension\certificates\localhost.pfx'
CERT_PASSWORD = 'Extension@123'
SERVE_DIR = r'D:\NoSync\misc\Comp\EdgeExtension\output'

os.chdir(SERVE_DIR)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        super().end_headers()
    
    def log_message(self, format, *args):
        print(f'[{self.log_date_time_string()}] {format % args}')

def extract_pem_from_pfx(pfx_path, password):
    """Extract PEM certificate from PFX file"""
    try:
        from cryptography.hazmat.primitives.serialization import pkcs12
        from cryptography.hazmat.backends import default_backend
        
        # Read PFX file
        with open(pfx_path, 'rb') as f:
            pfx_data = f.read()
        
        # Load PFX
        private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
            pfx_data, 
            password.encode() if password else None,
            backend=default_backend()
        )
        
        # Create temporary files for cert and key
        temp_dir = tempfile.gettempdir()
        cert_pem_path = os.path.join(temp_dir, f'temp_cert_{os.getpid()}.pem')
        key_pem_path = os.path.join(temp_dir, f'temp_key_{os.getpid()}.pem')
        
        # Export certificate
        from cryptography.hazmat.primitives import serialization
        cert_pem = certificate.public_bytes(serialization.Encoding.PEM)
        with open(cert_pem_path, 'wb') as f:
            f.write(cert_pem)
        
        # Export private key
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(key_pem_path, 'wb') as f:
            f.write(key_pem)
        
        return cert_pem_path, key_pem_path
    except ImportError:
        print("Error: 'cryptography' library is required. Installing...")
        os.system(f'{sys.executable} -m pip install cryptography')
        return extract_pem_from_pfx(pfx_path, password)

def run_server():
    print(f'Starting HTTPS server on port {PORT}...')
    print(f'Serving files from: {SERVE_DIR}')
    print(f'Press Ctrl+C to stop')
    
    try:
        # Extract PEM files from PFX
        print('Extracting certificate from PFX file...')
        cert_pem_path, key_pem_path = extract_pem_from_pfx(CERT_FILE, CERT_PASSWORD)
        
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(cert_pem_path, key_pem_path)
        
        with socketserver.TCPServer(('', PORT), MyHTTPRequestHandler) as httpd:
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            print(f'Server is running on https://localhost:{PORT}/')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped by user')
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    run_server()
