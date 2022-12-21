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

def google_domain(country='VN'):
	return 'https://www.google.com.'+country.lower().strip()

def run_url(driver, link):
	if driver==0:
		return 0
	print('run_url: Start')
	try:
		driver.get(link)
	except:
		driver.quit()
		return 0
	try:
		element = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='q']")))
		print("run_url: Success")
		return driver
	except: #Connect thành công
		driver.quit()
		print("run_url: Can't connect link")
		
		return 0

def request_key_data(key_object, proxy, driver, num_100=False):
	print('request_key_data: step 1')
	key = key_object
	input_search = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='q']")))
	input_search.clear()
	input_search.send_keys(key + Keys.ENTER)

	try:
		captcha = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "captcha-form")))
		return 2
	except:
		pass
	if num_100==True:
		time.sleep(randint(1,3))
		url_100 = driver.current_url +'&num=100'
		driver.get(url_100)
		try:
			captcha = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "captcha-form")))
			return 2
		except:
			pass

	main_html = main.get_attribute('innerHTML')
	max_try = 9
	try_num = 0
	while len(html.fromstring(main_html).xpath('//h3'))<5:
		driver.implicitly_wait(1)
		main_html = driver.findElement(By.xpath("//main")).get_attribute('innerHTML')
		if try_num>=max_try:
			break
		try_num = try_num+1
	return driver.findElement(By.xpath("//body"))

def get_driver(config):
	proxy = get_proxy(country=config['proxy_country'], region=config['proxy_region'])
	if proxy ==0:
		return 0

	gg_url = google_domain(config['proxy_country'])
	user_agent = get_user_agent(device=config['driver_device'])
	driver = re_driver(proxy, user_agent = user_agent, headless=config['driver_headless'])
	driver = self.run_url(driver, gg_url)

	re_run_num = 0
	while driver==0:
		proxy = get_proxy(country=config['proxy_country'], region=config['proxy_region'])
		if proxy ==0:
			return 0

		driver = re_driver(proxy, user_agent = user_agent, headless=config['driver_headless'])
		driver = self.run_url(driver, gg_url)
		re_run_num = re_run_num+1
		if re_run_num>=5:
			return -1

	return driver

def gg_search(keylist, config):
	config = c_config(config)
	driver = get_driver(config)

	output = []
	for i in range(len(keylist)):
		key = keylist[i]

		if config['num100']==True and i==0:
			main_html = self.request_key_data(key, proxy, driver, num_100=True)
		else:
			main_html = self.request_key_data(key, proxy, driver)

		test =  0
		while main_html ==-2:
			driver = get_driver(config)
			main_html = self.request_key_data(key, proxy, driver, num_100=config['num100'])
			if test>=5:
				break
			test = test+1
		if test>=5
			break

		if config['num100']==True:
			key_data = get_key_data_100(key, main_html)
		else:
			key_data = get_key_data(key, main_html)

		output.append(key_data) 
		time.sleep(random.uniform(1.1, 1.9))

	driver.quit()
	return output