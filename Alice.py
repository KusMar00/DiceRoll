import time
import Dice
import socket
from ssl import SSLContext, PROTOCOL_TLS_CLIENT

servername='bob'
host = socket.gethostname()
port = 5001

# Create SSL context
context = SSLContext(PROTOCOL_TLS_CLIENT)
context.load_verify_locations('./certificates/bob.cert.pem')
context.load_cert_chain('./certificates/alice.cert.pem', './certificates/alice.key.pem')

# Connect to Bob
connection = socket.create_connection((host, port))
tls = context.wrap_socket(connection, server_hostname=servername, do_handshake_on_connect=True)
print("Connected to: " + str(socket.getaddrinfo(host, port)[1][4]) + " (Bob)")

# Verify Bob's certificate
serverCertificate = tls.getpeercert()
if serverCertificate != None:
	print(f"Bob's certificate verified")
else:
	print(f"Bob's certificate is not valid. Termintaing connection.")
	connection.close()

print("Starting dice roll simulation...\n\n")

counter = 0

while True:
	counter += 1

	# Roll dice, generate random bit-string and hash commit
	aliceDice = Dice.roll_dice()
	aliceBitString = Dice.bit_string()
	aliceCommit = Dice.commit(aliceDice, aliceBitString)

	# Send commitment to Bob
	tls.send(str(aliceCommit).encode())

	# Receive Bob's dice roll
	bobDice = int(tls.recv(1024).decode())

	# Send Alice's dice roll and bit-string to Bob
	tls.send((str(aliceDice) + " " + aliceBitString).encode())

	# Calculate result
	result = Dice.result(aliceDice, bobDice)

	# Print result
	print(f"Result of dice roll #{counter}: {result}")

	time.sleep(2)