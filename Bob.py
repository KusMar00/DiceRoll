import socket
import Dice
from ssl import CERT_REQUIRED, SSLContext, PROTOCOL_TLS_SERVER

host = socket.gethostname()
port = 5001

# Create SSL context
context = SSLContext(PROTOCOL_TLS_SERVER)
context.verify_mode = CERT_REQUIRED
context.load_cert_chain('./certificates/bob.cert.pem', './certificates/bob.key.pem')
context.load_verify_locations("./certificates/alice.cert.pem")

# Create socket
sock = socket.socket()
sock.bind((host, port)) 
sock.listen()

tls = context.wrap_socket(sock, server_side=True, do_handshake_on_connect=True)

# Accept connection from Alice
connection, address = tls.accept()
print("Connection from: " + str(address) + " (Alice)")

# Verify Alice's certificate
clientCert = connection.getpeercert()
if clientCert != None:
	print("Alice's certificate verified")
else:
	print("Alice's certificate is not valid. Termintaing connection.")
	connection.close()

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