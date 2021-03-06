# API info link: http://www.robin-stocks.com/en/latest/functions.html
import json
import priceUpdater
import robin_stocks as r
import time
import BitcoinHelper


infoJSON = BitcoinHelper.getJSON('./accountInfo.json')
prevPriceJSON = BitcoinHelper.getJSON('./prices.json')
email = infoJSON["email"]
password = infoJSON["pass"]

givenConstantPrice = BitcoinHelper.getPrice()
priceUpdater.updateConstant(givenConstantPrice)

print("------------------------------------------------------------")
print("Welcome to the Charlemagne Bitcoin Trading Bot!")
print("To begin, please enter the authentication code\nsent to your phone.")
r.login(email, password)

BitcoinHelper.setCapital(input("Next, how much money would you like to invest? "))
print("Perfect!", flush=True)
loopBreaker = "go"
print("Please type 'Ctrl + C' to stop the trading bot.\n", flush=True)


sleep = 0

while loopBreaker != 'stop' and BitcoinHelper.getCapitalLeft() > 0:
    time.sleep(30)
    sleep += 30
    possibleBuy = BitcoinHelper.getPrice()
    print("Charlemagne is determining whether or not to buy or sell...", flush=True)

    #  if the current value is equal to 1% less than the constant
    if BitcoinHelper.getCapitalLeft() > 5:
        if possibleBuy <= (givenConstantPrice * 0.999):
            r.order_buy_crypto_by_quantity('BTC', BitcoinHelper.getBuyConstant())
            priceUpdater.updateBuy(possibleBuy)
            print("" + str(BitcoinHelper.getBuyConstant()) + " Bitcoin was bought at: " + str(possibleBuy), flush=True)

    # if the current value is equal to 1% more than the bought price
    for price in prevPriceJSON["boughtPrices"]:
        if possibleBuy >= price * 1.001:
            r.order_sell_crypto_by_quantity('BTC', BitcoinHelper.getBuyConstant())
            priceUpdater.updateSell(float(price), possibleBuy)
            print("" + str(BitcoinHelper.getBuyConstant()) + " Bitcoin was sold at: " + str(possibleBuy), flush=True)

    if (sleep % 10800) == 0:
        givenConstantPrice = BitcoinHelper.getPrice()
        priceUpdater.updateConstant(givenConstantPrice)
        BitcoinHelper.setBuyConstant()
