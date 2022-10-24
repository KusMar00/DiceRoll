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
connection, address = tls.accept()

print("Connection from: " + str(address) + " (Alice)")

# Establish TSL is configured correctly
clientCert = connection.getpeercert()
if clientCert != None:
	print("Alice's certificate verified")
else:
	print("Alice's certificate is not valid. Termintaing connection.")
	connection.close()

shake = connection.do_handshake()
if shake == None:
	print("TLS handshake successful")

print("Starting dice roll simulation...\n\n")

counter = 0

while True:
	counter += 1
	
	# Receive commitment from Alice
	aliceCommit = connection.recv(1024).decode()

	# Simulate dice roll
	bobDice = Dice.roll_dice()

	# Send dice roll to Alice
	connection.send(str(bobDice).encode())

	# Receive Alice's dice roll and bit-string
	aliceDice, aliceBitString = connection.recv(1024).decode().split()

	# Verify Alice's commitment
	if aliceCommit == Dice.commit(aliceDice, aliceBitString):
		# Calculate result
		result = Dice.result(int(aliceDice), bobDice)
		# Print result
		print(f"Result of dice roll #{counter}: {result}")
	else:
		print("Alice is cheating. Terminating connection.")
		break

connection.close()