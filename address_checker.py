import requests
import os
import sys
from datetime import datetime
import json
import logging

# Prints to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Edit this list to query the addresses you would like to keep an eye on
# actor names will have to be unique (unless I can be arsed to do a refactor)
ADDRESSES = {

# A file has been made which will always alert that REvil ransomware has dropped
# comment this out when you are ready

# BE CAREFUL - any more than 5 ETH addrs and you will have to start rate-limiting your
# API requests

'REvil Ransomware': {'address': '33SF8qLXh3mT1W6qeVBX2g8uTzj94oGJrk', 
'ticker': 'BTC'}

}

def queryAddresses():
	'''
	Go through the list of addresses that need to be checked and append if the
	address has dropped.

	dropped_entities is a dict of name : address.
	'''
	dropped_entities = {}

	for entity in ADDRESSES:
		addr = None

		if(ADDRESSES[entity]['ticker'] == 'BTC'):
			addr = pingBTC(ADDRESSES[entity]['address'])
		elif(ADDRESSES[entity]['ticker'] == 'DOGE'):
			addr = pingDOGE(ADDRESSES[entity]['address'])
		elif(ADDRESSES[entity]['ticker'] == 'ETH'):
			addr = pingETH(ADDRESSES[entity]['address'])
		else:
			raise ValueError("Ticker if-else problem")

		if addr != None:
			dropped_entities[entity] = addr

	return dropped_entities


def pingBTC(addr):
	# Check the current balance of a given address for BTC
	# BTC_ENDPOINT = 'https://blockchain.info/rawaddr/'
	BTC_ENDPOINT = 'https://api.blockchair.com/bitcoin/dashboards/address/'

	response = requests.get(BTC_ENDPOINT+str(addr))
	# print(response.text)
	try:
		response_json = response.json()
		return checkBalance(addr, float(response_json['data'][addr]['address']['balance']))

	except json.JSONDecodeError as e:
		# Normally when the BTC endpoint is not being happy (sending too many requests etc)
		if response.status_code == 429:
			eprint('Too many requests sent to btc endpoint')
		else:
			eprint("JSONDecodeError from blockchain.info")
			raise e
	except Exception as e:
		eprint(f"Non-JSONDecodeError, response from blockchair: {response.text}")
		raise e


def pingDOGE(addr):
	# Check the current balance of a given address for DOGE
	DOGE_ENDPOINT = 'https://dogechain.info/api/v1/address/balance/'

	response = requests.get(DOGE_ENDPOINT+str(addr)).json()
	return checkBalance(addr, float(response['balance']))


def pingETH(addr):
	# Check the current balance of a given address for ETH

	# Please take me out of this file when pushing to a public repo
	with open(f"./apiKey/etherscan", 'r') as f:
		eth_api_key = f.read()

	ETH_ENDPOINT = 'https://api.etherscan.io/api'
	params = {
		'module': 'account',
		'action': 'balance',
		'address': addr,
		'tag': 'latest',
		'apikey': eth_api_key
	}

	try:
		response = requests.get(ETH_ENDPOINT, params=params).json()
		# print(response)
	except JSONDecodeError as e:
		eprint(f'JSON decode error from etherscan, request body {response.text}')

	return checkBalance(addr, float(response['result']))


def checkBalance(addr, curr_balance):
	'''
	For a 'live' balance given, see if there is a saved balance

	If the same, do nothing, return nothing
	if changed, we save
	if changed negatively (withdrawal), we return a string of a message to stdout
	'''
	saved_balance = loadBalance(addr)

	if(saved_balance != ""):
		if(curr_balance < saved_balance):
			return addr
		elif (curr_balance > saved_balance):
			saveBalance(addr, curr_balance)
			return None
	else:
		saveBalance(addr, curr_balance)
		return None


def loadBalance(addr):
	'''
	take the file with the name of the addr to load the last saved balance
	'''
	if(os.path.isfile('./address_balances/'+addr+'.txt')):
		with open('./address_balances/'+addr+'.txt') as file:
			return float(file.read())
	return ""

def saveBalance(addr, balance):
	'''
	take the address and corresponding balance and save to a file with the
	name of the address for later use
	'''
	# print('balance: '+str(balance))
	with open('./address_balances/'+addr+'.txt', 'w') as file:
		file.write(str(balance))


##################
# PROGRAM START
##################
timestamp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
# outfile = open('/Users/chris.quinn/Desktop/address_checker.txt', 'a')
outputs = queryAddresses()
if outputs != None:
	for output in outputs.keys():
		print(timestamp+" - "+output+" has had a decrease in funds.")

		'''
		The following two lines will write to a file in desktop if you wish to cron this.
		The print statement can be used for other things i.e. shell script, automator.
		'''
		# outfile.write(timestamp+" - Address: "+outputs[output]+" has had a decrease in funds.\n")
eprint(timestamp + ' - address_checker.py completed')		




