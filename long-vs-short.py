from pprint import pprint
import argparse
import requests
import time
from tabulate import tabulate
from utils import *
import csv 
import os 
from datetime import datetime 

parser = argparse.ArgumentParser()
parser.add_argument('-t','--tpairs', nargs='+', help='Ticker pairs to check data for', required=False)
args = parser.parse_args()


title('The be all & end all of the finex long/short data') 

# Ticker pairs
tpairs = args.tpairs

# Get Ticker + Currency data 
query = ",t".join(tpairs)
tdata = api_request("https://api.bitfinex.com/v2/tickers?symbols=t"+query)
currs = get_currencies( tdata ) 

# Get Funding data 
query = ",f".join(currs)
fdata = api_request("https://api.bitfinex.com/v2/tickers?symbols=f"+query)


# Get the coin market cap data for the tickers 
cmc_data = get_cmc_data( tdata  )

# Individual margin data
mdata_headers = [
	'ticker', 'fpart', 'lpart', 'fpart_usd_price', 'lpart_usd_price',
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
cdi = 0 

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
	marketcap 		 = cmc_data[fpart]['marketcap']
	available_supply = cmc_data[fpart]['available_supply']
	max_supply		 = cmc_data[fpart]['max_supply']
	as_percent_long  = round_sig( ( total_longs  / available_supply ) * 100, 2)
	as_percent_short = round_sig( ( total_shorts / available_supply ) * 100, 2)
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

	# Cumulative data 
	if fpart not in cdata_keys:
		cdata_keys[fpart] = cdi 
		cdata.append( [fpart, marketcap, available_supply, max_supply, as_percent_long, as_percent_short, total_longs_usd, total_shorts_usd ] )
		cdi += 1 
	else:
		index = cdata_keys[fpart] 
		cdata[index][4] += as_percent_long
		cdata[index][5] += as_percent_short
		cdata[index][6] += total_longs_usd
		cdata[index][7] += total_shorts_usd


	mdata.append(output)
	spacer()
	time.sleep(2)


# Output Margin Data table 
table = []
for data in mdata:

	table.append([
		data[0], data[13], str(data[14])+':'+str(data[15]),
		f(data[5])+' ($'+f(data[6])+')', currs[data[2]][0]+f(data[9])+currs[data[2]][1], '-',
		f(data[7])+' ($'+f(data[8])+')', currs[data[1]][0]+f(data[11])+currs[data[1]][1], '-',
		currs[data[2]][0]+f(data[18])+currs[data[2]][1], currs[data[1]][0]+f(data[19])+currs[data[1]][1]
		])

print3('Ticker pair margin usage breakdown')
print(tabulate(table, headers=[
		"Pair", "L/S ratio","% of supply long:short",
		'Total Long','Funded Longs','-',
		'Total Short', 'Funded Shorts','-',
		'Long Daily Charge', 'Short Daily Charge'
	]))

spacer()

# Output Cumulative Data table 
print3('Cumulative Ticker margin usage breakdown')
table = []
for data in cdata:

	table.append([
		data[0], '$'+f(data[1]), f(data[2]), f(data[3]), 
		str(round_sig(data[4]))+':'+str(round_sig(data[5])),
		'$'+f(data[6]),'$'+f(data[7]),
		])

print(tabulate(table, headers=[
		"Crypto", "Market Cap","Available Supply","Max Supply",
		"% of supply long:short",
		'Total Long USD Value','Total Short USD Value'
	]))




spacer()
print3('Making chart visualisations...')
make_chart( cmc_data, cdata, mdata ) 




# Write to CSV 
timestamp = datetime.utcnow()

spacer()
print3('Writing data to csv files, timestamped: '+str(timestamp))

w2csv = [ 
	['margin data', ROOT_PATH+'/margin_data', mdata, mdata_headers],
	['cumulative data', ROOT_PATH+'/cumulative_data', cdata, cdata_headers],
]
for el in w2csv:

	file_exists = os.path.isfile(el[1]+'_log.csv')

	print2('Appending to '+el[1]+'_log.csv')
	with open(el[1]+'_log.csv', 'a') as f:
		writer = csv.writer(f)

		if file_exists == False:
			el[3].insert(0,'timestamp')
			writer.writerow(el[3])

		for row in el[2]:
			row.insert(0, timestamp)
			writer.writerow(row)


	print2('Writing last datset to '+el[1]+'_last.csv')
	with open(el[1]+'_last.csv', 'w') as f:
		writer = csv.writer(f)

		el[3].insert(0,'timestamp')
		writer.writerow(el[3])

		for row in el[2]:
			row.insert(0, timestamp)
			writer.writerow(row)



print2('Done..')
exit() 



