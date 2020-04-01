from pprint import pprint
import argparse
import requests
import time
from tabulate import tabulate
from utils.chart import *
from utils.apis import *
from utils.formatting import *
from utils.mongo import *
import csv 
import os 
from datetime import datetime 

parser = argparse.ArgumentParser()
parser.add_argument('-t','--tpairs', nargs='+', help='Ticker pairs to check data for')
args = parser.parse_args()
if args.tpairs is None:
    parser.error("please specify pairs, eg: long-vs-short.py -t BTCUSD ETHUSD ETHBTC")


title('The be all & end all of the finex long/short data') 

# Example input: 
# python long-vs-short.py -t ETHBTC 
# ['ETHBTC']
tpairs = args.tpairs


# tpairs = ['ETHBTC', 'ETHUSD', 'BTCUSD']
# currs  = {'BTC': ['', ' BTC'], 'ETH': ['', ' ETH'], 'USD': ['$', '']}
tpairs, currs = get_currencies( tpairs ) 


# Get Ticker + Currency data 
# 'ETHBTC,tETHUSD,tBTCUSD'
query = ",t".join(tpairs)
# [['tETHBTC',
#   0.017308,
#   1147.92595856,
#   0.017309,
#   87.37486794,
#   -0.000131,
#   -0.0075,
#   0.017309,
#   6421.90684597,
#   0.01782,
#   0.017273],
#  ['tETHUSD',
tdata = api_request("https://api-pub.bitfinex.com/v2/tickers?symbols=t"+query)

# Get Funding data 
# 'BTG,fUSD,fETH,fBTC'
query = ",f".join(currs)
fdata = api_request("https://api-pub.bitfinex.com/v2/tickers?symbols=f"+query)


# Get the coin market cap data for the tickers 
# {'BTG': {'available_supply': 17513924.0,
#          'id': 'bitcoin-gold',
#          'marketcap': 91255189.0,
#          'max_supply': 21000000.0,
#          'rank': '57',
#          'total_supply': 17513924.0},
#  'ETH': {'available_supply': 109047945.0,
# cmc_data = get_cmc_data( tdata  )
cmc_data = {}

spacer()

# Individual margin data
mdata_headers = [
	'ticker', 'ticker_price', 'fpart', 'lpart', 'fpart_usd_price', 'lpart_usd_price',
	'total_longs','total_longs_usd',
	'total_shorts', 'total_shorts_usd',
	'long_funding', 'long_funding_usd',
	'short_funding', 'short_funding_usd',
	'overall_ls_ratio', 
	'as_percent_long', 'as_percent_short',
	'long_funding_rate', 'short_funding_rate',
	'long_funding_charge', 'short_funding_charge'
]
mdata = [] 

# Cumulative data 
cdata_headers = [ 
	'fpart', 'marketcap', 'available_supply', 'max_supply', 
	'as_percent_long', 'as_percent_short', 'total_longs_usd', 'total_shorts_usd'
]
cdata = []
cdata_keys = {} 
cdata_index = 0 

# Itterate through ticker data 
for data in tdata:

	o = {}

	# Ticker breakdown 
	o['ticker'] = data[0]		# tBTGUSD  - Actual Ticker
	o['ticker_price'] = data[1]  # 5.1423   - Ticker fpartlpart price 
	o['fpart'] 	= o['ticker'][1:-3]	# BTG  	   - First part of  the ticker
	o['fcd'] 	= currs[ o['fpart'] ]	# ['', ' BTG']  - Firt part currency data
	o['lpart'] 	= o['ticker'][-3:]		# USD  	   - Last part of the ticker
	o['lcd'] 	= currs[ o['lpart'] ]	# ['$', '']- Last part currency data 


	# Get USD price for fpart (eg: ETH in the ETHBTC) 
	o['fpart_usd_price'] = next((t for t in tdata if t[0]=='t'+o['fpart']+'USD'), [1,1])[1]
	o['lpart_usd_price'] = next((t for t in tdata if t[0]=='t'+o['lpart']+'USD'), [1,1])[1]


	# Total longs 
	o['total_longs']       = round( api_request("https://api-pub.bitfinex.com/v2/stats1/pos.size:1m:"+o['ticker']+":long/last")[1] )
	o['total_longs_base']  = round( o['total_longs']  * o['ticker_price'] )
	o['total_longs_usd']   = round( o['total_longs']  * o['fpart_usd_price'] )

	# Total shorts
	o['total_shorts']      = round( api_request("https://api-pub.bitfinex.com/v2/stats1/pos.size:1m:"+o['ticker']+":short/last")[1] )
	o['total_shorts_base'] = round( o['total_shorts']  * o['ticker_price'] ) 
	o['total_shorts_usd']  = round( o['total_shorts']  * o['fpart_usd_price'] )


	# Long funding 
	o['long_funding']      = round( api_request("https://api-pub.bitfinex.com/v2/stats1/credits.size.sym:1m:f"+o['lpart']+":"+o['ticker']+"/last")[1] )
	o['long_funding_usd']  = round( o['long_funding'] * o['lpart_usd_price'] )

	# Short funding  
	o['short_funding']     = round( api_request("https://api-pub.bitfinex.com/v2/stats1/credits.size.sym:1m:f"+o['fpart']+":"+o['ticker']+"/last")[1] )
	o['short_funding_usd'] = round( o['short_funding'] * o['fpart_usd_price'] )


	# L/S Ratios
	total = o['total_longs'] + o['total_shorts']
	percent_long     		= int(( o['total_longs']  / total ) * 100)
	percent_short    		= int(( o['total_shorts'] / total ) * 100)
	o['overall_ls_ratio'] 	= str(percent_long)+':'+str(percent_short)

	# L/S relative to available supply
	o['as_percent_long']  = 0
	o['as_percent_short'] = 0

	if o['fpart'] in cmc_data: 
		marketcap 		 = cmc_data[o['fpart']]['marketcap']
		available_supply = cmc_data[o['fpart']]['available_supply']
		max_supply		 = cmc_data[o['fpart']]['max_supply']
		o['as_percent_long']  = round_sig( ( o['total_longs']  / available_supply ) * 100, 2)
		o['as_percent_short'] = round_sig( ( o['total_shorts'] / available_supply ) * 100, 2)
	

	o['long_funding_rate']    = round_sig( next((t for t in fdata if t[0]=='f'+o['lpart']), [1,1])[1], 2 )
	o['short_funding_rate']   = round_sig( next((t for t in fdata if t[0]=='f'+o['fpart']), [1,1])[1], 2 )


	# Interest amounts 
	o['long_funding_charge']  = round_sig( o['long_funding']  * o['long_funding_rate']  )
	o['short_funding_charge'] = round_sig( o['short_funding'] * o['short_funding_rate'] )

	print3(o['ticker'][1:]+", "+str(o['ticker_price']))
	print2("Overall long:short ratio "+str(o['overall_ls_ratio'])+", % of circulating supply L/S on bfx: "+str(o['as_percent_long'])+"/"+str(o['as_percent_short'])+"")
	print2("Longs: ")

	if o['lpart'] == 'USD':
		print2("- Total \"margin\" long: "+f(o['total_longs'])+" "+o['fpart'])
		print2("- Longs currently worth: $"+f(o['total_longs_base']))
		print2("- Longs are borrowing "+o['lcd'][0]+f(o['long_funding'])+" "+o['lpart'])

		if o['total_longs_base'] > o['long_funding']: 
			print2("- Longs are in the money: +$"+f(o['total_longs_base'] - o['long_funding']))
		else:
			print2("- Longs are rekt: -$"+f(o['long_funding'] - o['total_longs_base']))

	else: 
		print2("- Total \"margin\" long: "+f(o['total_longs'])+" "+o['fpart']+" ($"+f(o['total_longs_usd'])+")")
		print2("- Longs currently worth: "+o['lcd'][0]+f(o['total_longs_base'])+o['lcd'][1])
		print2("- Longs are borrowing "+o['lcd'][0]+f(o['long_funding'])+" "+o['lpart'])

		if o['total_longs_base'] > o['long_funding']: 
			print2("- Longs are in the money: +"+o['lcd'][0]+f(o['total_longs_base'] - o['long_funding'])+o['lcd'][1]+" (+$"+f(o['total_longs_usd'] - o['long_funding_usd'])+")")
		else:
			print2("- Longs are rekt: -"+o['lcd'][0]+f(o['long_funding'] - o['total_longs_base'])+o['lcd'][1]+" (-$"+f(o['long_funding_usd'] - o['total_longs_usd'])+")")

	print2("- Longs are paying "+o['lcd'][0]+f(o['long_funding_charge'])+o['lcd'][1]+" per day in interest")
	
	# print2(f(total_shorts)+" "+fpart+" short ( worth $"+f(total_shorts_usd)+" ) consuming "+lcd[0]+f(short_funding)+" of "+fpart+" margin paying "+fcd[0]+f(short_funding_charge)+fcd[1]+" per day to be short")
	
	print2("Shorts: ")

	print2("- Total \"margin\" short: "+f(o['total_shorts'])+" "+o['fpart']+" ($"+f(o['total_shorts_usd'])+")")
	print2("- Shorts are borrowing "+o['fcd'][0]+f(o['short_funding'])+" "+o['fpart'])
	print2("- Shorts are paying "+o['fcd'][0]+f(o['short_funding_charge'])+o['fcd'][1]+" per day in interest")
	


	# Cumulative data 
	if o['fpart'] not in cdata_keys:
		cdata_keys[ o['fpart'] ] = cdata_index 
		cdata.append( {
			'fpart': o['fpart'],
			# 'marketcap': marketcap,
			# 'available_supply': available_supply,
			# 'max_supply': max_supply,
			'as_percent_long': o['as_percent_long'],
			'as_percent_short': o['as_percent_short'],
			'total_longs_usd': o['total_longs_usd'],
			'total_shorts_usd': o['total_shorts_usd']
		})
		cdata_index += 1 
	else:
		index = cdata_keys[o['fpart']] 
		cdata[index]['as_percent_long'] += o['as_percent_long']
		cdata[index]['as_percent_short'] += o['as_percent_short']
		cdata[index]['total_longs_usd'] += o['total_longs_usd']
		cdata[index]['total_shorts_usd'] += o['total_shorts_usd']


	mdata.append(o)
	spacer()
	# time.sleep(12)


# Output Margin Data table 
table = []
for o in mdata:

	if o['lpart'] == 'USD':
		total_longs  = o['fcd'][0]+f(o['total_longs'])+o['fcd'][1]+' (worth $'+f(o['total_longs_usd'])+')'
		total_shorts = o['fcd'][0]+f(o['total_shorts'])+o['fcd'][1]+' (worth $'+f(o['total_shorts_usd'])+')'
	else:
		total_longs  = o['fcd'][0]+f(o['total_longs'])+o['fcd'][1]+' (worth '+o['lcd'][0]+f(o['total_longs_base'])+o['lcd'][1]+')'
		total_shorts = o['fcd'][0]+f(o['total_shorts'])+o['fcd'][1]+' (worth '+o['lcd'][0]+f(o['total_shorts_base'])+o['lcd'][1]+')'

	table.append([
		o['ticker'], 
		total_longs, 
		o['lcd'][0]+f(o['long_funding'])+o['lcd'][1], 
		o['lcd'][0]+f(o['long_funding_charge'])+o['lcd'][1],
		total_shorts, 
		o['fcd'][0]+f(o['short_funding'])+o['fcd'][1], 
		o['fcd'][0]+f(o['short_funding_charge'])+o['fcd'][1]
		])

print3('Ticker pair margin usage breakdown')
print(tabulate(table, headers=[
		"Pair",
		'Total Long','Longs borrowing', 
		'Long Daily Charge',
		'Total Short', 'Shorts borrowing',
		'Short Daily Charge'
	]))


spacer()


# Output Cumulative Data table 
error('Disabled Cumulative Ticker margin usage breakdown')
# table = []
# for data in cdata:

# 	table.append([
# 		data['fpart'], '$'+f(data['marketcap']), f(data['available_supply']), f(data['max_supply']), 
# 		str(round_sig(data['as_percent_long']))+':'+str(round_sig(data['as_percent_short'])),
# 		'$'+f(data['total_longs_usd']),'$'+f(data['total_shorts_usd']),
# 		])

# print(tabulate(table, headers=[
# 		"Crypto", "Market Cap","Available Supply","Max Supply",
# 		"% of supply long:short",
# 		'Total Long USD Value','Total Short USD Value'
# 	]))


spacer()

error('Disableed Making chart visualisations ...')

# make_chart( cmc_data, cdata, mdata ) 

spacer()

log_marketdata(mdata)

log_cumulativedata(cdata)

print3('Done..')

exit() 



