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
from utils.formatting import *

hide_api_request = 1 


def api_request(url):

	slow_api_time = 30 
	if hide_api_request != 1:
		print4( 'bfx api requesting: '+url ) 


	print4('Requesting: '+url)
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
				print4('Requesting: '+url)	
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
				print4('Requesting: '+url)
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



def get_cmc_data( tpairs ):

	ticker_list = [t[0][1:-3] for t in tpairs]

	overrides = { 
		'BCH': 'BAB',
		'USDT': 'UST',
		'IOTA': 'IOT'
	} 

	url = "https://api.coinmarketcap.com/v1/ticker/?limit=0"
	if hide_api_request != 1:
		print4("requesting coinmarketcap api: "+url)

	print4('Requesting: '+url)	
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
