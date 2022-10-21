import random

def rollDice():
	return random.randint(1,6)

def calcDice(dice1, dice2):
	return (dice1 ^ dice2) + 1