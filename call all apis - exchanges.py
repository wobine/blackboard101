# Python 2.7.6. WBN Calling exchange APIs. 
import time, json, requests
"""
Some api pages
https://bitpay.com/bitcoin-payment-gateway-api
https://blockchain.info/api
https://localbitcoins.com/api-docs/public/
https://www.bitstamp.net/api/
https://coinbase.com/docs/api/overview
https://coinbase.com/api/doc/1.0/prices/buy.html
https://coinbase.com/api/v1/prices/spot_rate
https://www.kraken.com/help/api
https://www.bitfinex.com/pages/api
https://www.cryptsy.com/pages/api
http://bitcoincharts.com/about/markets-api/
https://www.bitfinex.com/pages/api
"""

def btstamp():
    bitStampTick = requests.get('https://www.bitstamp.net/api/ticker/')
    return bitStampTick.json()['last'] # replace last with timestamp etc

def btceBU():
    btceBtcTick = requests.get('https://btc-e.com/api/2/btc_usd/ticker')
    return btceBtcTick.json()['ticker']['last'] # replace last with updated etc

def btceBL():
    btceLtcTick = requests.get('https://btc-e.com/api/2/ltc_btc/ticker')
    return btceLtcTick.json()['ticker']['last'] # replace last with updated etc

def bitfinex(): 
    bitFinexTick = requests.get("https://api.bitfinex.com/v1/ticker/btcusd")
    return bitFinexTick.json()['last_price']

def coinbase():
    coinBaseTick = requests.get('https://coinbase.com/api/v1/prices/buy') # replace buy with spot_rate, sell etc
    return coinBaseTick.json()['amount'] # replace amount with currency etc

def kraken():
    krakenTick = requests.post('https://api.kraken.com/0/public/Ticker',data=json.dumps({"pair":"XXBTZUSD"}),
        headers={"content-type":"application/json"})
    return krakenTick.json()['result']['XXBTZUSD']['c'][0]

while True:
    btstampUSDLive = float(btstamp())
    btceUSDLive = float(btceBU())
    btceLTCinBTCLive = float(btceBL())
    coinbUSDLive = float(coinbase())
    krakenUSDLive = float(kraken())
    bitfinexUSDLive = float(bitfinex())

    print "Bitstamp Price in USD =", btstampUSDLive
    print "BTC-e Price in USD =", btceUSDLive
    print "Coinbase Price in USD =", coinbUSDLive
    print "Kraken Price in USD =", krakenUSDLive
    print "Bitfinex Price in USD =", bitfinexUSDLive
    print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
    print "BTC USD Average = ", 
    print (krakenUSDLive + coinbUSDLive + btceUSDLive + btstampUSDLive + bitfinexUSDLive) / 5
    print "difference betweeen coinbase and bitstamp", (coinbUSDLive - btstampUSDLive)
    print "BTC-e LTC Price in BTC", btceLTCinBTCLive
    print "BTC-e LTC Price in USD =", btceLTCinBTCLive * btceUSDLive, "USD"
    print; print; print "=-=-=-=-=-=-=--=-=-=-"; print;
    time.sleep(2) # 120 equals two minutes, you can ping it every second by putting a 1 in here
