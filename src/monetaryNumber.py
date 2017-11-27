#
#	Monetary Number
#

class MonetaryNumber:

	# Ex : 25 USD
	# Currency (ex : USD)
	# Amount = 25
	def __init__(self, s):
		
		sTmp = s.replace(',', '.')
		sArray = sTmp.split()
		
		self.currency = float(sArray[1])
		self.amount = sArray[0]

		
