#
#   EncodeJson
#
#   Take the portfolio structure and encode it in JSON

from portfolio import PortFolio
from asset import Asset

def encode_asset(asset):

    return '{\"asset\":' + str(asset.id) +
        ',\"label\":\"' + str(asset.label) + '\"' +
        ',\"sharpe\":' + str(asset.sharpe) +
        ',\"return\":' + str(asset.rendement) +
        ',\"volatity\":' + str(asset.volatility) +
        '}'

def encode_pf(portFolio):
    
    pr = ''

    #for asset in portFolio:
        
