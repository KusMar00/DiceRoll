import time
import Dice
import socket
from ssl import CERT_REQUIRED, SSLContext, PROTOCOL_TLS_CLIENT

# Client to Bob
hostname='bob'
host = socket.gethostname()
port = 5001

context = SSLContext(PROTOCOL_TLS_CLIENT)

context.load_verify_locations('./certificates/bob.cert.pem')
context.load_cert_chain('./certificates/alice.cert.pem', './certificates/alice.key.pem')

client = socket.create_connection((host, port))
tls = context.wrap_socket(client, server_hostname=hostname)

# Establish TLS is configured correctly
serverCertificate = tls.getpeercert()
print(f"Certificate verified: {serverCertificate != None}")

shake = tls.do_handshake()

# Send message to Bob
message = "Hello Bob"
tls.send(message.encode())