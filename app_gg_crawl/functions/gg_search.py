from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from app_selenium.functions.driver import re_driver
from app_selenium.functions.captcha_solve import GG_CAPTCHA_SOLVER as CaptchaSolver
from app_selenium.functions.proxy_manage import get_proxy
from app_selenium.functions.user_agents import get_user_agent
from .ggsr_desktop_structure import GGSR

from lxml import html
from random import randint
import random
from datetime import datetime
import time, requests


def get_key_data(key_object, main_html):
	print('get_key_data: start')
	tree = html.fromstring(main_html)
	
	data = GGSR(tree)
	output_data = data.output_data
	print(output_data)
	output_data['keyword'] = key_object

	
	return output_data

def get_key_data_100(key_object, main_html):
	print('get_key_data: start')
	tree = html.fromstring(main_html)
	data = GGSR(tree)
	output_data = {'keyword':key_object, 'data':[]}
	for item in data.center_col:
		if item['item_type']=='organic_result':
			output_data['data'].append(item)
	return output_data

class GG_SEARCH():
	def __init__(self,keylist, config):
		'''
			keylist (list): list of keyword (['seo Là gì', 'seo tphcm'])
			config (dict): {
				'country': 'VN',
				'proxy_region': 'Hồ Chí Minh',
				'driver_device': 'Desktop',
			}
		'''
		self.output = self.run(keylist, [], config)

	def google_domain(self, country='VN'):
		return 'https://www.google.com.'+country.lower().strip()

	def run(self, keylist, output, config):
		print(config['proxy_country'], config['proxy_region'])
		proxy = get_proxy(country=config['proxy_country'], region=config['proxy_region'])
		if proxy ==0:
			output.append(0)
			return output
		gg_url = self.google_domain()
		user_agent = get_user_agent(device=config['driver_device'])

		print(user_agent)
		print('run: step 2')
		driver = re_driver(proxy, user_agent = user_agent)
		driver = self.run_url(driver, gg_url)

		re_run_num = 0
		while driver==0:
			print('time', re_run_num)
			proxy = get_proxy(country=config['proxy_country'], region=config['proxy_region'])
			if proxy ==0:
				output.append(0)
				return output # Không tìm thấy proxy
			print('run reget proxy:', proxy["ip"], proxy["port"])
			driver = re_driver(proxy, user_agent = user_agent)
			driver = self.run_url(driver, gg_url)
			re_run_num = re_run_num+1
			if re_run_num>=5:# Thử nhiều lần proxy không dùng dk
				output.append(-1)
				return output
		print('run: step 3')
		for i in range(len(keylist)):
			key = keylist[i]
			print(i, key)
			if config['num100']==True and i==0:
				main_html = self.request_key_data(key, proxy, driver, num_100=True)
			else:
				main_html = self.request_key_data(key, proxy, driver)
			if main_html==2: # Không giải đk captcha thử chạy lại url search
				print('Không giải được captcha')
				driver = self.run_url(driver, gg_url)
				time.sleep(random.uniform(1.1, 1.9))

				main_html = self.request_key_data(key, proxy, driver, num_100=config['num100'])

				if main_html==2: # Nếu vẫn k đk thì bỏ proxy, chạy lại bằng proxy mới
					driver.quit()
					output = run(keylist[i:],output,config)
					if output[-1] == 0:
						return output

			if config['num100']==True:
				try:
					key_data = get_key_data_100(key, main_html)
				except:
					driver.quit()
					get_key_data_100(key, main_html) # Chạy tiếp để nó trả lỗi về cho qcluster task
			else:
				try:
					key_data = get_key_data(key, main_html)
				except:
					driver.quit()
					get_key_data(key, main_html) # Chạy tiếp để nó trả lỗi về cho qcluster task

			
			output.append(key_data) 
			time.sleep(random.uniform(1.1, 1.9))

		driver.quit()
		return output

	def run_url(self, driver, link):
		if driver==0:
			return 0
		print('run_url: Start')
		try:
			driver.get(link)
		except:
			driver.quit()
			return 0
		try: #Nếu gặp biểu tượng không thể connect thoát driver return 0
			element = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="main-content"]/div[@class="icon icon-generic"]')))
			driver.quit()
			print("run_url: Can't connect link")
			return 0
		except: #Connect thành công
			print("run_url: Success")
			return driver

	def request_key_data(self, key_object, proxy, driver, num_100=False):
		print('request_key_data: step 1')
		key = key_object
		input_search = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='q']")))
		input_search.clear()
		input_search.send_keys(key + Keys.ENTER)

		print('request_key_data: step 2')
		try:
			captcha = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "captcha-form")))
		except:
			captcha = None
		if captcha:
			print('start solve captcha')
			solve_status = CaptchaSolver(proxy,driver).solve_status
			if solve_status == 0:
				driver.quit()
				return 2
		try:
			main = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='main']")))
		except:
			return 2
		if num_100==True:
			time.sleep(randint(1,3))
			url_100 = driver.current_url +'&num=100'
			driver.get(url_100)
			try:
				captcha = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "captcha-form")))
				solve_status = CaptchaSolver(proxy,driver).solve_status
				if solve_status == 0:
					driver.quit()
					return 2
			except:
				main = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='main']")))
				
		print('request_key_data: step 3')
		WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='rso']")))
		driver.implicitly_wait(random.uniform(1, 1.5))
		main = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='main']")))
		
		main_html = main.get_attribute('innerHTML')
		return main_html

def c_config(config):
	try:
		config['driver_device']
	except:
		config['driver_device'] = 'DESKTOP'
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
	
def gg_search(key_list, config):
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
	return data