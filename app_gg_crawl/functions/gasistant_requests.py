from .gg_search import GG_SEARCH
import json, requests
from .gg_search import c_config

def gasistant_recheck_market(key_list, config):
	config = c_config(config)
	data = GG_SEARCH(key_list, config).output
	
	if data ==-1:
		data = {
			'error': 'Proxy error'
		}
	for sr in data:
		rich_snipet = []
		for item in sr['center_col']:
			if item['item_type']=='organic_result':
				if item['review/price']!='':
					rich_snipet.append('review/price')
				if item['faqs']:
					rich_snipet.append('faqs')
				if item['events']:
					rich_snipet.append('events')
				if item['sitelinks']:
					rich_snipet.append('sitelinks')
				if item['table']:
					rich_snipet.append('table')
				if item['img']:
					rich_snipet.append('img')
				if item['imgs']:
					rich_snipet.append('imgs')
		sr['rich_snipet'] = list(set(rich_snipet))
		sr['config'] = config
	url = 'https://gasistant.com/project-manage/new-gg-search-result/'
	requests.post(url, json=data)
	return data

def gasistant_recheck_ranking(key_list, config):
	config = c_config(config)
	data = GG_SEARCH(key_list, config).output
	if data ==-1:
		data = {
			'error': 'Proxy error'
		}
	url = 'https://gasistant.com/project-manage/new-keyword-ranking/'
	requests.post(url, json=data)
	return data