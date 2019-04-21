import time 
import requests
from json import dumps as json_dumps, loads as json_loads
from math import log10, floor
from pprint import pprint 

hide_api_request = 1 

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


def get_cmc_data( ticker_list ):

	url = "https://api.coinmarketcap.com/v1/ticker/?limit=0"
	if hide_api_request != 1:
		print4("requesting coinmarketcap api: "+url)	
	response = json_loads(requests.get(url).text)
	tickers = {}
	for r in response:
		key = r['symbol']
		if key in ticker_list:
			tickers[key] = {
				'id': r['id'],
				'rank': r['rank'],
				'marketcap': float(r['market_cap_usd']),
				'available_supply': float(r['available_supply']),
				'total_supply': float(r['total_supply']),
				'max_supply': r['max_supply']
			}

	return tickers

