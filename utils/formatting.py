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




def get_currencies( tpairs ): 

	# Currency : [ Preformatter, Postformatter ]
	tpairs_output = tpairs

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

	for t in tpairs:  

		fpart = t[0:3]
		lpart = t[-3:]

		# Check we have the tickers fpart & lpart USD pair 
		if (fpart+'USD' not in tpairs) and (fpart not in fiats): 
			tpairs_output.append(fpart+'USD')
		if (lpart+'USD' not in tpairs) and (lpart not in fiats): 
			tpairs_output.append(lpart+'USD')

		currs[fpart] = add_curr(fpart)
		currs[lpart] = add_curr(lpart)

	return tpairs_output, currs 

