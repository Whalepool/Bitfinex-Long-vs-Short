import time 
import requests
from json import dumps as json_dumps, loads as json_loads
from math import log10, floor
from pprint import pprint 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import squarify
import os 

hide_api_request = 1 
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

endc      = '\033[0m'
bold      = '\033[1m'
spacerstr = '--------------------'

def minimise_ratio(ratio):
    min_num = min(ratio)
    ratio = [round(n / min_num, 2) for n in ratio]
    return ratio
    
def round_sig(x, sig=5):
	return round(x, sig-int(floor(log10(abs(x))))-1)

def spacer():
	green  = '\033[92m'
	print(green, spacerstr, endc)

def title(txt):
	x = '\033[93m' 
	print(x, bold, spacerstr, txt, spacerstr,  endc)


def error(txt, kill=0):
	red   = '\033[91m'
	print(red, txt, endc)

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
	if num == None:
		return 'None' 
	elif type(num) is str:
		return num
	else: 
		return str("{:,}".format(num))



def api_request(url):

	slow_api_time = 30 
	if hide_api_request != 1:
		print4( 'bfx api requesting: '+url ) 

	response = requests.get(url).text
	data     = json_loads(response)

	# Check we actually got the data back 
	# Not just an api error 
	completed = 0 
	while completed == 0:

		if isinstance(data, list):

			if str(data[0]) == 'error': 

				error('BFX API Error: '+str(data))
				error('Sleeping '+str(slow_api_time)+' seconds to calm down..')
				time.sleep(slow_api_time)
				
				# Re-request the data
				response = requests.get(url).text

				# Load the response
				data = json_loads(response)

				## Re-run

			else:
				# The response json does not contain error
				# Therefore we have the response we wanted
				# So api request actuall completed successfully
				completed = 1

		elif isinstance(data, dict):

			if 'error' in data:

				error('BFX API Error: '+str(data))
				error('Sleeping '+str(slow_api_time)+' seconds to calm down..')
				time.sleep(slow_api_time)
				
				# Re-request the data
				response = requests.get(url).text

				# Load the response
				data = json_loads(response)


		else:
			# WTF has the api returned then ? 
			lmsg = 'API error'
			error(data)
			error(lmsg)
			exit()		



	return data


def get_currencies( tdata ): 

	# Currency : [ Preformatter, Postformatter ]

	# Fiat pairs 
	fiats  = { 
		'USD': [ '$', ''], 
		'EUR': [ '€', ''], 
		'JPY': ['¥', ''] , 
		'GBP': ['$', ''] , 
		'UST': ['$', ' USDT']
	}

	def add_curr(key):
		if key in fiats:
			return fiats[key]
		else:
			return ['',  ' '+key]


	currs = {} 

	for t in tdata:  

		fpart = t[0][1:-3]
		lpart = t[0][-3:]
		currs[fpart] = add_curr(fpart)
		currs[lpart] = add_curr(lpart)

	return currs 


def get_cmc_data( tpairs ):

	ticker_list = [t[0][1:-3] for t in tpairs]

	overrides = { 
		'BCH': 'BAB'
	} 

	url = "https://api.coinmarketcap.com/v1/ticker/?limit=0"
	if hide_api_request != 1:
		print4("requesting coinmarketcap api: "+url)	
	response = json_loads(requests.get(url).text)
	tickers = {}
	for r in response:
		key = r['symbol']
		bfxticker = key 

		if key in overrides:
			bfxticker = overrides[key] 

		if bfxticker in ticker_list:

			max_supply = r['max_supply']
			if max_supply is not None:
				max_supply = float(max_supply)

			tickers[bfxticker] = {
				'id': r['id'],
				'rank': r['rank'],
				'marketcap': float(r['market_cap_usd']),
				'available_supply': float(r['available_supply']),
				'total_supply': float(r['total_supply']),
				'max_supply': max_supply
			}


	return tickers

def make_chart( cmc_data, cdata, mdata ):


	cmcdf = pd.DataFrame( { k:[ round(v['marketcap']/1000000000) ] for k,v in cmc_data.items() } )
	
	columns = [
		'fpart', 'marketcap', 'available_supply', 'max_supply', 
		'as_percent_long', 'as_percent_short', 
		'total_longs_usd', 'total_shorts_usd'
	]
	cdf = pd.DataFrame(cdata, columns=columns ).set_index('fpart').iloc[::-1]

	columns = [
		'ticker', 'fpart', 'lpart', 'fpart_usd_price', 'lpart_usd_price', 
		'total_longs', 'total_longs_usd',
		'total_shorts', 'total_shorts_usd',
		'long_funding', 'long_funding_usd',
		'short_funding', 'short_funding_usd',
		'overall_ls_ratio',
		'as_percent_long', 'as_percent_short',
		'long_funding_rate', 'short_funding_rate',
		'long_funding_charge', 'short_funding_charge'
	]
	mdf = pd.DataFrame(mdata, columns=columns ).set_index('ticker').iloc[::-1]


	fig, ( ax1, ax2, ax3, ax4 ) =  plt.subplots(4,1, figsize=(8,12), gridspec_kw = {'hspace':0.6, 'height_ratios':[3, 4, 4, 5]})
	fig.suptitle('Bitfinex Margin Usage Analysis by whalepool.io', fontsize=16, fontweight='bold')

	# Coinmarket cap
	# cmc_data, cmcdf
	squarify.plot(sizes=cmcdf.iloc[0], label=cmcdf.columns.tolist(), value=[ '$'+str(k)+'bn' for k in cmcdf.iloc[0].tolist() ], alpha=.8, ax=ax1 ) 
	ax1.set_title('Market Cap Sizes')
	ax1.get_xaxis().set_visible(False)
	ax1.get_yaxis().set_visible(False)
	ax1.axis('off')

	# Cumulative data as USD value of margin positions 
	# cdata, cdf 
	ax2.barh(np.arange(len(cdf)), cdf["total_longs_usd"], color="g", align="center", alpha=0.25, linewidth=0)
	ax2.barh(np.arange(len(cdf)), 0-cdf["total_shorts_usd"], color="r", align="center", alpha=0.25, linewidth=0)
	ax2.set_title('$ valuation of margin positions ')
	ax2.set_yticks(np.arange(len(cdf)))
	ax2.set_yticklabels(cdf.index.tolist(), minor=False)
	ax2.axvline(x=0, color='k', linewidth=0.75, ymax=0.94)
	ax2.spines['top'].set_visible(False)
	ax2.spines['right'].set_visible(False)
	ax2.spines['bottom'].set_visible(False)

	# ax2.set_xlim(cdf['total_shorts_usd'].min(), cdf['total_longs_usd'].max())

	for i, v in enumerate(cdf["total_longs_usd"].tolist()):
		txt = '$'+(f(round(v/1000000)))+'m'
		ax2.text(v+0.04, i-0.05, txt, color='g', fontweight='bold')

	for i, v in enumerate(cdf["total_shorts_usd"].tolist()):
		txt = '$'+(f(round(v/1000000)))+'m'
		ax2.text((0-v)-0.23, i-0.05, txt, color='r', fontweight='bold')

	# Cumulative data as Percent of circulating supply
	# cdata, cdf 
	ax3.barh(np.arange(len(cdf)), cdf["as_percent_long"], color="g", align="center", alpha=0.25, linewidth=0)
	ax3.barh(np.arange(len(cdf)), 0-cdf["as_percent_short"], color="r", align="center", alpha=0.25, linewidth=0)
	ax3.set_title('% of Circulating supply that is margin long/short')
	ax3.set_yticks(np.arange(len(cdf)))
	ax3.set_yticklabels(cdf.index.tolist(), minor=False)
	ax3.axvline(x=0, color='k', linewidth=0.75, ymax=0.94)
	ax3.spines['top'].set_visible(False)
	ax3.spines['right'].set_visible(False)
	ax3.spines['bottom'].set_visible(False)



	# Individual ticker margin breakdown
	# mdata, mdf  
	ax4.barh(np.arange(len(mdf)), mdf["as_percent_long"], color="g", align="center", alpha=0.25, linewidth=0)
	ax4.barh(np.arange(len(mdf)), 0-mdf["as_percent_short"], color="r", align="center", alpha=0.25, linewidth=0)
	ax4.set_title('Individial ticker breakdown % of Circulating supply that is margin long/short')
	ax4.set_yticks(np.arange(len(mdf)))
	ax4.set_yticklabels(mdf.index.tolist(), minor=False)
	ax4.axvline(x=0, color='k', linewidth=0.75, ymax=0.94)
	ax4.spines['top'].set_visible(False)
	ax4.spines['right'].set_visible(False)
	ax4.spines['bottom'].set_visible(False)


	plt.savefig(ROOT_PATH+'/chart.png', pad_inches=1)

	print2('Chart made: '+ROOT_PATH+'/chart.png')



