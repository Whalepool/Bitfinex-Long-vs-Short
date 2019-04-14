from pprint import pprint
import requests
import time
from tabulate import tabulate
from math import log10, floor


endc      = '\033[0m'
bold      = '\033[1m'
spacerstr = '--------------------'


def round_sig(x, sig=5):
	return round(x, sig-int(floor(log10(abs(x))))-1)

def spacer():
	green  = '\033[92m'
	print(green, spacerstr, endc)

###################
# BLUE 
def print1(txt):
	x   = '\033[94m'
	print(x, txt, endc)

###################
# PURPLE  
def print2(txt):
	x  = '\033[95m'
	print(x, txt, endc)

###################
# CYAN 
def print3(txt):
	x  = '\033[96m'
	print(x, txt, endc)

###################
# GREEN 
def print4(txt):
	x  = '\033[92m'
	print(x, txt, endc)

def f(num):
	return str("{:,}".format(num))


print('\033[93m', bold, spacerstr, 'The be all & end all of the finex long/short data', spacerstr,  endc)

# Prices
r = requests.get("https://api.bitfinex.com/v2/tickers?symbols=tBTCUSD,tETHUSD,tETHBTC")
btc_price = round(r.json()[0][7])
eth_price = round(r.json()[1][7])
ethbtc_price = r.json()[2][7]

print1('BTCUSD price: $'+str(btc_price))
print1('ETHUSD price: $'+str(eth_price))
print1('ETHBTC price: '+str(ethbtc_price))
spacer()

time.sleep(1)

# Rates
r = requests.get("https://api.bitfinex.com/v2/tickers?symbols=fBTC,fETH,fUSD")
btc_rate = round_sig(r.json()[0][1])
eth_rate = round_sig(r.json()[1][1])
usd_rate = round_sig(r.json()[2][1])

print1('BTC FRR '+str(round_sig(btc_rate*100)))
print1('ETH FRR '+str(round_sig(eth_rate*100)))
print1('USD FRR '+str(round_sig(usd_rate*100)))
spacer()

time.sleep(1)

# BTC USD 
# Total longs
r = requests.get("https://api.bitfinex.com/v2/stats1/pos.size:1m:tBTCUSD:long/last") 
btc_total_long = round(r.json()[1])
btc_total_long_usd_value = round(btc_total_long*btc_price)


# Total short 
r = requests.get('https://api.bitfinex.com/v2/stats1/pos.size:1m:tBTCUSD:short/last')
btc_total_short = round(r.json()[1])
btc_total_short_usd_value = round(btc_total_short*btc_price)


# Total USD Used 
r = requests.get('https://api.bitfinex.com/v2/stats1/credits.size.sym:1m:fUSD:tBTCUSD/last')
btc_total_usd_used = round(r.json()[1])


# Total BTC Used 
r = requests.get('https://api.bitfinex.com/v2/stats1/credits.size.sym:1m:fBTC:tBTCUSD/last')
btc_total_btc_used = round(r.json()[1])


total = btc_total_short + btc_total_long
percent_short = str(int(( btc_total_short / total ) * 100))
percent_long = str(int(( btc_total_long / total ) * 100))

print3('BTC, long:short, '+str(percent_long)+':'+str(percent_short))
print2(f(btc_total_long)+' BTC long ( $'+f(btc_total_long_usd_value)+' ) consuming $'+f(btc_total_usd_used)+' of USD margin')
print2(f(btc_total_short)+' BTC short ( $'+f(btc_total_short_usd_value)+' ), consuming '+f(btc_total_btc_used)+' of funded BTC margin')
spacer()


time.sleep(3)


# ETH USD 
# Total longs
r = requests.get("https://api.bitfinex.com/v2/stats1/pos.size:1m:tETHUSD:long/last") 
eth_total_long = round(r.json()[1])
eth_total_long_usd_value = round(eth_total_long*eth_price)

# Total short 
r = requests.get('https://api.bitfinex.com/v2/stats1/pos.size:1m:tETHUSD:short/last')
eth_total_short = round(r.json()[1])
eth_short_usd_value = round(eth_total_short*eth_price)

# Total USD Used 
r = requests.get('https://api.bitfinex.com/v2/stats1/credits.size.sym:1m:fUSD:tETHUSD/last')
eth_total_usd_used = round(r.json()[1])

# Total ETH Used 
r = requests.get('https://api.bitfinex.com/v2/stats1/credits.size.sym:1m:fETH:tETHUSD/last')
eth_total_eth_used = round(r.json()[1])


total = eth_total_short + eth_total_long
percent_short1 = str(int(( eth_total_short / total ) * 100))
percent_long1 = str(int(( eth_total_long / total ) * 100))

print3('ETH USD, long:short, '+str(percent_long1)+':'+str(percent_short1))
print2(f(eth_total_long)+' ETH long ( $'+f(eth_total_long_usd_value)+' ) consuming $'+f(eth_total_usd_used)+' of USD margin')
print2(f(eth_total_short)+' ETH short ( $'+f(eth_short_usd_value)+' ), consuming '+f(eth_total_eth_used)+' of funded ETH margin')
spacer()

time.sleep(3)


# ETHBTC USD 
# Total longs
r = requests.get("https://api.bitfinex.com/v2/stats1/pos.size:1m:tETHBTC:long/last") 
ethbtc_total_long = round(r.json()[1])
ethbtc_total_long_usd_value = round(ethbtc_total_long*eth_price)

# Total short 
r = requests.get('https://api.bitfinex.com/v2/stats1/pos.size:1m:tETHBTC:short/last')
ethbtc_total_short = round(r.json()[1])
ethbtc_short_usd_value = round(ethbtc_total_short*eth_price)

# Total BTC Used ( for longing eth btc )
r = requests.get('https://api.bitfinex.com/v2/stats1/credits.size.sym:1m:fBTC:tETHBTC/last')
ethbtc_total_btc_used = round(r.json()[1])
ethbtc_long_btcused_value = round(ethbtc_total_btc_used*btc_price)

# Total ETH Used ( for shorting eth btc ) 
r = requests.get('https://api.bitfinex.com/v2/stats1/credits.size.sym:1m:fETH:tETHBTC/last')
ethbtc_total_eth_used = round(r.json()[1])


total = ethbtc_total_short + ethbtc_total_long
percent_short2 = str(int(( ethbtc_total_short / total ) * 100))
percent_long2 = str(int(( ethbtc_total_long / total ) * 100))

print3('ETH BTC, long:short, '+str(percent_long2)+':'+str(percent_short2))
print2(f(ethbtc_total_long)+' ETH long ( $'+f(ethbtc_total_long_usd_value)+' ) consuming '+f(ethbtc_total_btc_used)+' BTC ( $'+f(ethbtc_long_btcused_value)+' ) of BTC margin')
print2(f(ethbtc_total_short)+' ETH short ( $'+f(ethbtc_short_usd_value)+' ), consuming '+f(ethbtc_total_eth_used)+' of funded ETH margin')
spacer()


total = ( eth_total_short + ethbtc_total_short) + ( eth_total_long + ethbtc_total_long)
percent_short3 = str(int(( ( eth_total_short + ethbtc_total_short) / total ) * 100))
percent_long3 = str(int(( ( eth_total_long + ethbtc_total_long) / total ) * 100))

print3('ETH USD + ETH BTC, long:short, '+str(percent_long3)+':'+str(percent_short3))

print2(f(eth_total_long+ethbtc_total_long)+' ETH long ( $'+f(eth_total_long_usd_value+ethbtc_total_long_usd_value)+' ) consuming $'+f(eth_total_usd_used+ethbtc_long_btcused_value)+' of USD margin')
print2(f(eth_total_short+ethbtc_total_short)+' ETH short ( $'+f(eth_short_usd_value+ethbtc_short_usd_value)+' )')
spacer()



table = []
table.append([
	'BTCUSD @ $'+f(btc_price), str(percent_long)+':'+str(percent_short),'-',
	f(btc_total_long)+' ($'+f(btc_total_long_usd_value)+')', '$'+f(btc_total_usd_used),'-',
	f(btc_total_short)+' ($'+f(btc_total_short_usd_value)+')', f(btc_total_btc_used),'-',
	'$'+f(round_sig(btc_total_usd_used*usd_rate)), f(round_sig(btc_total_btc_used*btc_rate))+' BTC'
	])
table.append([
	'ETHUSD @ $'+f(eth_price), str(percent_long1)+':'+str(percent_short1),'-',
	f(eth_total_long)+' ($'+f(eth_total_long_usd_value)+')', '$'+f(eth_total_usd_used),'-',
	f(eth_total_short)+' ($'+f(eth_short_usd_value)+')', f(eth_total_eth_used),'-',
	'$'+f(round_sig(eth_total_usd_used*usd_rate)), f(round_sig(eth_total_eth_used*eth_rate))+' ETH'
	])
table.append([
	'ETHBTC @ '+f(ethbtc_price), str(percent_long2)+':'+str(percent_short2),'-',
	f(ethbtc_total_long)+' ($'+f(ethbtc_total_long_usd_value)+')', '$'+f(ethbtc_total_long_usd_value),'-',
	f(ethbtc_total_short)+' ($'+f(ethbtc_short_usd_value)+')', f(ethbtc_total_eth_used),'-',
	f(round_sig(ethbtc_total_btc_used*btc_rate))+' BTC', f(round_sig(ethbtc_total_eth_used*eth_rate))+' ETH'
	])
table.append([
	'ETHUSD + ETHBTC', str(percent_long3)+':'+str(percent_short3),'-',
	f(eth_total_long+ethbtc_total_long)+' ($'+f(eth_total_long_usd_value+ethbtc_total_long_usd_value)+')', '$'+f(eth_total_usd_used+ethbtc_long_btcused_value),'-',
	f(eth_total_short+ethbtc_total_short)+' ($'+f(eth_short_usd_value+ethbtc_short_usd_value)+')',f(eth_total_eth_used+ethbtc_total_eth_used),'-',
	'$'+f(round_sig( (eth_total_usd_used*usd_rate) + ((ethbtc_total_btc_used*btc_rate)*btc_price) )), f(round_sig( (eth_total_eth_used*eth_rate) + (ethbtc_total_eth_used*eth_rate) ))+' ETH'
	])

print(tabulate(table, headers=[
		"Pair", "L/S ratio",'-',
		'Total Long','Funded Longs','-',
		'Total Short', 'Funded Shorts','-',
		'Long Daily Charge', 'Short Daily Charge'
	]))
exit() 



