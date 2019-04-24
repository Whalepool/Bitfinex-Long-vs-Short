lvs = __import__('long-vs-short')
import pandas as pd 
from utils import *



def convertDataToDataFrame(mdata, currs):
	table = []
	for data in mdata:

		table.append([
			data[0], data[13], str(data[14])+':'+str(data[15]),
			f(data[5])+' ($'+f(data[6])+')', currs[data[2]][0]+f(data[9])+currs[data[2]][1], '-',
			f(data[7])+' ($'+f(data[8])+')', currs[data[1]][0]+f(data[11])+currs[data[1]][1], '-',
			currs[data[2]][0]+f(data[18])+currs[data[2]][1], currs[data[1]][0]+f(data[19])+currs[data[1]][1]
		])


	headers=[
		"Pair", "L/S ratio","% of supply long:short",
		'Total Long','Funded Longs','-',
		'Total Short', 'Funded Shorts','-',
		'Long Daily Charge', 'Short Daily Charge'
	]
	df = pd.DataFrame(table, columns=headers)
	return df


def printDataToCSV(df, filepath='./data.csv'):
	df.to_csv(filepath, index=False)


def printDataToJSON(df, filepath='./data.json'):
	df.to_json(filepath, orient='split')


def main():
	cmc_data, cdata, mdata, currs = lvs.getData()
	df = convertDataToDataFrame(mdata, currs)
	printDataToCSV(df)
	printDataToJSON(df)


if __name__ == '__main__':
	main()