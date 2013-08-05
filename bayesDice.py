##############################################################
#### Beyes Dice program
#### Author: Nathan N.
#### Date Created: 8.4.2013
#### Last Updated: 8.4.2013
#### Notes: Bayesian probability methods attempt to make
####		decisions based on degrees of belief or confidence.
####		As a result, it allows for decision-making in the
####		face of incomplete information, which is often what
####		people encounter in the real world. This program
####		models a scenario in which there are 5 multisided
####		dice in a box. One die is picked out at random.
####		It's type is unknown at the start. The goal of this
####		program is to use Bayesian probability as a model
####		for machine learning in order to make an decision
####		in the face of incomplete information--in this case,
####		a guess at the die type that was selected based on
####		the random die roll results.
##############################################################

#### PROGRAM IS MODELED OFF OF BAYESIAN PROBABILITY TABLE BELOW ####
#### In this example there are 5 types of dice.
####
#### H (Hypthesis) is the guess that a particular die was selected.
####
#### P(H) (Prior) is the probabity of having picked that particular die
#### out of the total dice types available to select from.
####
#### D (Data) is the roll result.
####
#### P(D|H) (Likelihood) is the probability of the stated roll result (6)
#### occuring (D; data), given that the hypothesis (H) is True.
####
#### P(H) * P(D|H) is the non normalized probability that the
#### Hypothesis is True, given the roll result (data).
####
#### P(H|D) (Posterior) is the normalized probability that H is True, given
#### the data. This is our objective. P(H)P(D|H) / SUM(ALL P(H)P(D|H))
#### Note that this term becomes the Prior on future rolls.

# H 		P(H)	D 	P(D|H)	P(H)*P(D|H)		P(H|D)
# 4			.2 		6	.00000		.0000		.00000
# 6			.2		6	.16667		.03333		.39216
# 8			.2		6	.125		.025		.29412
# 12		.2		6	.08333		.08333		.19608
# 20		.2		6	.025		.11765		.11765

import random
import sys


class Dice:
	def __init__(self):
		self.data = []
		self.singleRollResult = 0
		self.diceTypes = [4, 6, 8, 12, 20]
		self.guess = None
		self.r = random
		self.r.seed()
		self.priors = [1.0 / len(self.diceTypes) for x in self.diceTypes]
		self.dieType = None
		self.likelihoods = [1.0 / x for x in self.diceTypes]
		self.prePosteriors = [a * b for a,b in zip(self.priors, self.likelihoods)]
		self.sumPrePosteriors = sum(x for x in self.prePosteriors)
		self.posteriors = [x / self.sumPrePosteriors for x in self.prePosteriors]

	def selectRandomDie(self):
		self.dieType = self.diceTypes[self.r.randrange(len(self.diceTypes))]

	def roll(self):
		rollResult = self.r.randrange(1, self.dieType)
		self.singleRollResult = rollResult
		self.data.append(rollResult)

	def updatePriors(self):
		self.priors = [x for x in self.posteriors]

	def updateLikelihoods(self):
		for i in xrange(len(self.diceTypes) - 1):
			for roll in self.data:
				if roll > self.diceTypes[i]:
					self.likelihoods[i] = 0

	def updatePrePosteriors(self):
		self.prePosteriors = [a * b for a,b in zip(self.priors, self.likelihoods)]

	def updatePosteriors(self):
		self.sumPrePosteriors = 0
		self.sumPrePosteriors = sum(x for x in self.prePosteriors)
		self.posteriors = [x / self.sumPrePosteriors for x in self.prePosteriors]

	def updateGuess(self):
		self.updatePriors()
		self.updateLikelihoods()
		self.updatePrePosteriors()
		self.updatePosteriors()


def printGuess():
	i = 0
	print 'Best guess:'
	for die in dice.diceTypes:
		asterisk = ''
		if dice.posteriors[i] >= .8:
			asterisk = '*'
			dice.guess = die
		print '{0}{1}-sided die: {2} percent probability.'.format(asterisk, die, round(dice.posteriors[i] * 100, 2))
		i += 1


def main():
	promptAnyKey = None
	rollagain = 'y'
	i = 0
	print '\n-------------------------------------\n'
	print 'There are {0} dice in a box full of multisided dice: {1}.'.format(len(dice.diceTypes), dice.diceTypes)
	print 'You have selected one at random.'
	print 'This program will attempt to guess which die was picked based on your rolls.\n'

	dice.selectRandomDie()

	while promptAnyKey is None:
		promptAnyKey = raw_input('Press enter to roll.\n')

	while rollagain != 'x':
		i += 1
		dice.roll()
		print '\nYou rolled a {0}.\n'.format(dice.singleRollResult)
		dice.updateGuess()
		printGuess()
		rollagain = raw_input('\nPress ENTER to roll. (x to exit)\n')
		rollagain = rollagain.lower()

	if dice.guess == dice.dieType:
		status = 'The program guessed CORRECTLY!'
	else:
		status = 'The program did NOT guess correctly!'

	print 'The die selected was a {0}-sided die! {1} {2} total rolls'.format(dice.dieType, status, i)
	sys.exit()

if __name__ == '__main__':
	dice = Dice()
	main()
