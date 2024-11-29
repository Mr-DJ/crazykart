import random
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import threading
import socket

db = SQLAlchemy()

class HextechCipher:
    def __init__(self, seed):
        self.state = seed
        self.length = len(seed)
        
    def step(self):
        # Flawed but functional feedback function
        # Uses only first 3 bits, making it predictable
        feedback = (self.state[0] ^ self.state[1] ^ self.state[2]) & 1
        self.state = self.state[1:] + [feedback]
        return feedback

    def generate_keystream(self, length):
        keystream = []
        for _ in range(length):
            bit = self.step()
            keystream.append(bit)
        return keystream


class HextechCipherCommunication:
    def __init__(self, flag):
        self.key = 0b1010000000000000  # Example polynomial
        self.lfsr = HextechCipher([1, 0, 1, 0])  # Initial state
        self.messages = [
            "HEXTECH{test_message_1}",
            "HEXTECH{updating_security_protocols}",
            flag  # Use the flag passed from config
        ]

    def handle_client(self, client):
        try:
            while True:
                message = random.choice(self.messages)
                keystream = self.lfsr.generate_keystream(len(message))
                encrypted = ''.join(chr(ord(char) ^ k) for char, k in zip(message, keystream))
                client.send((encrypted + '\n').encode())
                time.sleep(2)
        except:
            client.close()

    def run_server(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind(('localhost', port))
            server.listen(5)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client,)).start()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server.close()

def run_secret_server(port, flag):
    comm = HextechCipherCommunication(flag)  # Pass flag to HextechCipherCommunication
    comm.run_server(port)  # Pass port to run_server


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    from app import routes
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()
        from app.routes import init_db
        init_db()

    # Start the secret server with configuration
    server_thread = threading.Thread(
        target=run_secret_server,
        args=(app.config['PORT'], app.config['FLAG']),  # Pass config values
        daemon=True
    )
    server_thread.start()

    return app

