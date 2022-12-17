from ..models import proxyListModel

def get_proxy(country=None, region=None): ### Mặc định tổng proxy =999
	if country==None:
		all_proxy_list = proxyListModel.objects.filter(country='VN')
	else:
		all_proxy_list = proxyListModel.objects.filter(country=country)

	for proxy_list in all_proxy_list:
		proxies = proxy_list.proxies['data']

		if proxies:
			
			get_proxy = proxies[0]
			proxy_list.proxies['data'].remove(get_proxy)
			proxy_list.running_proxies['data'].append(get_proxy)

			running_proxies = proxy_list.running_proxies['data']
			if len(proxy_list.proxies['data']):
				proxy_list.proxies['data'].extend(proxy_list.running_proxies['data'])
				proxy_list.running_proxies['data'] = []
			proxy_list.save()
			return get_proxy
	return 0

	
	