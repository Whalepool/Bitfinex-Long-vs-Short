from pprint import pprint
import requests
import time
from tabulate import tabulate
from utils import *

title('The be all & end all of the finex long/short data') 

# Ticker pairs
tpairs = [
	'BTCUSD',
	'ETHUSD','ETHBTC',
	'XRPUSD','XRPBTC',
	'EOSUSD','EOSBTC',
	'LTCUSD','LTCBTC'
]

# Get the coin market cap data for the tickers 
cmc_data = get_cmc_data( [t[0:-3] for t in tpairs]  )

# Currencies / Funding 
currs  = { 
	# Currency : [ Preformatter, Postformatter ]
	'USD': [ '$', '',   ], 
	'EUR': [ '€', '',   ],
	'BTC': [ '',  ' BTC' ], 
	'ETH': [ '',  ' ETH' ],
	'XRP': [ '',  ' XRP' ],
	'EOS': [ '',  ' EOS' ],
	'LTC': [ '',  ' LTC' ],
}


# Get ticker data
query = ",t".join(tpairs)
tdata = api_request("https://api.bitfinex.com/v2/tickers?symbols=t"+query)
for data in tdata:
	cd = currs[ data[0][-3:] ]
	print1( data[0][1:] +' price: '+cd[0]+str(data[7])+cd[1]  )

spacer()
time.sleep(1)

# Get funding data 
query = ",f".join(currs)
fdata = api_request("https://api.bitfinex.com/v2/tickers?symbols=f"+query)
for data in fdata: 
	cd = currs[ data[0][-3:] ]
	print1( data[0][1:]+' FRR: '+str(round_sig(data[1]*100)))

spacer()
time.sleep(1)

# Get margin data
mdata = [] 
for data in tdata:

	# Ticker breakdown 
	ticker = data[0]
	fpart = ticker[1:-3]
	fcd = currs[ fpart ]
	lpart = ticker[-3:]
	lcd = currs[ lpart ]

	# Get USD price for fpart (eg: ETH in the ETHBTC) 
	fpart_usd_price = next((t for t in tdata if t[0]=='t'+fpart+'USD'), [1,1])[1]
	lpart_usd_price = next((t for t in tdata if t[0]=='t'+fpart+'USD'), [1,1])[1]


	output = [] 
	output.extend([ ticker, fpart, lpart, fpart_usd_price, lpart_usd_price ])

	# Total longs 
	total_longs       = round( api_request("https://api.bitfinex.com/v2/stats1/pos.size:1m:"+ticker+":long/last")[1] )
	total_longs_usd   = round( total_longs * fpart_usd_price )
	output.extend([total_longs,total_longs_usd ]) 

	# Total shorts
	total_shorts      = round( api_request("https://api.bitfinex.com/v2/stats1/pos.size:1m:"+ticker+":short/last")[1] )
	total_shorts_usd  = round( total_shorts * fpart_usd_price )
	output.extend([ total_shorts, total_shorts_usd ]) 

	# Long funding 
	long_funding      = round( api_request("https://api.bitfinex.com/v2/stats1/credits.size.sym:1m:f"+lpart+":"+ticker+"/last")[1] )
	long_funding_usd  = round( long_funding * lpart_usd_price )
	output.extend([ long_funding, long_funding_usd ]) 

	# Short funding  
	short_funding     = round( api_request("https://api.bitfinex.com/v2/stats1/credits.size.sym:1m:f"+fpart+":"+ticker+"/last")[1] )
	short_funding_usd = round( short_funding * fpart_usd_price )
	output.extend([ short_funding, short_funding_usd ])

	# L/S Ratios
	total = total_longs + total_shorts
	percent_long     = int(( total_longs  / total ) * 100)
	percent_short    = int(( total_shorts / total ) * 100)
	overall_ls_ratio = str(percent_long)+':'+str(percent_short)
	output.append( overall_ls_ratio )

	# L/S relative to available supply
	as_percent_long  = round_sig( ( total_longs  / cmc_data[fpart]['available_supply'] ) * 100, 2)
	as_percent_short = round_sig( ( total_shorts / cmc_data[fpart]['available_supply'] ) * 100, 2)
	output.extend([ as_percent_long, as_percent_short ])

	# Interest rates
	long_funding_rate    = round_sig( next((t for t in fdata if t[0]=='f'+lpart), [1,1])[1], 2 )
	short_funding_rate   = round_sig( next((t for t in fdata if t[0]=='f'+fpart), [1,1])[1], 2 )
	output.extend([ long_funding_rate, short_funding_rate ])

	# Interest amounts 
	long_funding_charge  = round_sig( long_funding *long_funding_rate  )
	short_funding_charge = round_sig( short_funding*short_funding_rate )
	output.extend([ long_funding_charge, short_funding_charge ])

	print3(ticker[1:])
	print2("Overall long:short ratio "+str(overall_ls_ratio))
	print2(str(as_percent_long)+"% of available supply is margin long")
	print2(str(as_percent_short)+"% of available supply is margin short")
	print2(f(total_longs)+" "+fpart+" long ( $"+f(total_longs_usd)+" ) consuming "+lcd[0]+f(long_funding)+" of "+lpart+" margin")
	print2(f(total_shorts)+" "+fpart+" short ( $"+f(total_shorts_usd)+" ) consuming "+fcd[0]+f(short_funding)+" of "+fpart+" margin")
	print2('Funded longs are paying '+lcd[0]+f(long_funding_charge)+lcd[1]+" per day to be long")
	print2('Funded shorts are paying '+fcd[0]+f(short_funding_charge)+fcd[1]+" per day to be short")

	spacer()
	mdata.append(output)
	time.sleep(3)


table = []
for data in mdata:

	table.append([
		data[0], data[13], str(data[14])+':'+str(data[15]),
		f(data[5])+' ($'+f(data[6])+')', currs[data[2]][0]+f(data[9])+currs[data[2]][1], '-',
		f(data[7])+' ($'+f(data[8])+')', currs[data[1]][0]+f(data[11])+currs[data[1]][1], '-',
		currs[data[2]][0]+f(data[18])+currs[data[2]][1], currs[data[1]][0]+f(data[19])+currs[data[1]][1]
		])


print(tabulate(table, headers=[
		"Pair", "L/S ratio","% of supply long:short",
		'Total Long','Funded Longs','-',
		'Total Short', 'Funded Shorts','-',
		'Long Daily Charge', 'Short Daily Charge'
	]))




spacer()
print3('Making chart visualisations...')
make_chart( cmc_data, mdata ) 

print2('Done..')
exit() 



