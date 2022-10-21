import socket
import ssl
import Dice

# Create a SSL socket
hostname = 'www.python.org'
context = ssl.create_default_context()

with socket.create_connection((hostname, 443)) as sock:
    context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())