from .gg_search import GG_SEARCH
import json

def c_config(config):
	try:
		config['driver_device']
	except:
		config['driver_device'] = 'DESKTOP'
	try:
		config['driver_headless']
	except:
		config['driver_headless'] = False
	try:
		config['proxy_country']
	except:
		config['proxy_country'] = 'VN'
	try:
		config['proxy_region']
	except:
		config['proxy_region'] = None
	try:
		config['num100']
	except:
		config['num100'] = False
	return config

def gasistant_recheck_market(key_list, config):
	config = c_config(config)
	data = GG_SEARCH(key_list, config).output
	for item in data:

	if data ==-1:
		output = {
			'error': 'Proxy error'
		}
	else:
		output = list(())
		for item in data:
			
	url = 'https://gasistant.com/project-manage/new-gg-search-result/'
	data = data
	requests.post(url, json=data)