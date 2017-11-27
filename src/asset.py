
from monetaryNumber import MonetaryNumber

#
#   asset.py
#

#
#   Used to get informations on every assets
#

class Asset:

  def __init__(self, id, label, priceValue, typeValue,
  		volatility, sharpe, rendement, rendementAnnuel,
		varHistorique):
    # ASSET_DATABASE_ID
    self.id = id
    
    # LABEL
    self.label = label

    # LAST_CLOSE_VALUE_IN_CURR
    self.priceValue = priceValue
    
    # TYPE
    self.typeValue = typeValue

    self.volatility = volatility
    self.sharpe = sharpe
    self.rendement = rendement
    self.rendementAnnuel = rendementAnnuel
    self.varHistorique = varHistorique


  # Used to compute the NAV. NAV = asset PTF / portfolio PTF
  def getPTF(self, quantity, changeRate):
      return quantity * self.monetaryPrice.amount * changeRate

  def toString(self):
    s = (str(self.id) + " : S(" + str(self.sharpe) + ") V(" + str(self.volatility) + ") R(" + str(self.rendement) + ")")
    return s