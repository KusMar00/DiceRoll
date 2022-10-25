import random
import hashlib

# Hash based commitment
def commit(m, r):
	cm = (str(m)+str(r)).encode()
	return hashlib.sha256(cm).hexdigest()

# Simulate a dice roll
def roll_dice():
	return random.randint(1,6)

# Calculate result of inputs from Alice and Bob
def result(dice1, dice2):
	return ((dice1 ^ dice2)%6)+1

# Random bit-string of length 256
def bit_string():
	return ''.join([str(random.randint(0,1)) for i in range(256)])