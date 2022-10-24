import random

def get_user_agent(device='DESKTOP', os=None, browser=None):
	if device.upper()=='DESKTOP':
		user_agents = [
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
		]
	return user_agents[random.randint(0, len(user_agents)-1)]