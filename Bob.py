import socket
import time
import Dice
from ssl import CERT_REQUIRED, SSLContext, PROTOCOL_TLS_SERVER

# Acts as server for Alice
host = socket.gethostname()
port = 5001

# Set SSL Context as server. Verify mode is CERT_REQUIRED, which means client must also have cert.
context = SSLContext(PROTOCOL_TLS_SERVER)
context.verify_mode = CERT_REQUIRED

# Load Bob cert and key, and store location of Alice cert
context.load_cert_chain('./certificates/bob.cert.pem', './certificates/bob.key.pem')
context.load_verify_locations("./certificates/alice.cert.pem")

server = socket.socket()

server.bind((host, port)) 
server.listen()

tls = context.wrap_socket(server, server_side=True)
conn, address = tls.accept()

print("Connection from: " + str(address))

# Establish TSL is configured correctly
clientCert = conn.getpeercert()
print(f"Certificate verified: {clientCert != None}")

shake = conn.do_handshake()

# Receive message from Alice
message = conn.recv(1024).decode()
print("Message from Alice: " + message)

while True:
	