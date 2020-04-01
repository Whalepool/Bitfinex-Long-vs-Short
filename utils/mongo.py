from json import dumps as json_dumps, loads as json_loads
from pprint import pprint 
from pymongo import MongoClient
from datetime import datetime 
from utils.formatting import *

mclient 	= MongoClient('mongodb://localhost:27017')
db 			= mclient.bfxstats
minute_ts   = datetime.utcnow().strftime('%Y-%m-%d %H:%M')

def log_marketdata(mdata):

	print3('Logging individual ticker data to mongodb')

	for m in mdata:


		print2('- '+str(minute_ts)+' '+m['ticker'])

		ins = {
			'timestamp': minute_ts,
			'ticker': m['ticker'],

			'as_percent_long': m['as_percent_long'],
			'as_percent_short': m['as_percent_short'],
			'fpart_usd_price': 8096.1,
			'long_funding': m['long_funding'],
			'long_funding_charge': m['long_funding_charge'],
			'long_funding_rate': m['long_funding_rate'],
			'long_funding_usd': m['long_funding_usd'],
			'lpart_usd_price': 1,
			'short_funding': m['short_funding'],
			'short_funding_charge': m['short_funding_charge'],
			'short_funding_rate': m['short_funding_rate'],
			'short_funding_usd': m['short_funding_usd'],
			'ticker_price': m['ticker_price'],
			'total_longs': m['total_longs'],
			'total_longs_base': m['total_longs_base'],
			'total_longs_usd': m['total_longs_usd'],
			'total_shorts': m['total_shorts'],
			'total_shorts_base': m['total_shorts_base'],
			'total_shorts_usd': m['total_shorts_usd']
		}

		
		db['longshort_granular'].update( 
			{'timestamp': minute_ts, 'ticker': ins['ticker']}, 
			{
				"$set" : ins
			}, upsert=True )



def log_cumulativedata(cdata):

	print3('Logging cumulative ticker data to mongodb')

	for m in cdata:


		print2('- '+str(minute_ts)+' '+m['fpart'])

		ins = {
			'timestamp': minute_ts,
			'ticker': m['fpart'],

			'as_percent_long': m['as_percent_long'],
			'as_percent_short': m['as_percent_short'],
			# 'available_supply': m['available_supply'],
			# 'marketcap': m['marketcap'],
			# 'max_supply': m['max_supply'],
			'total_longs_usd': m['total_longs_usd'],
			'total_shorts_usd': m['total_shorts_usd'],
		}

		db['longshort_cum'].update( 
			{'timestamp': minute_ts, 'ticker': ins['ticker']}, 
			{
				"$set" : ins
			}, upsert=True )