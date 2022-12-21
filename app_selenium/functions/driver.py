from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as chrome_Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import zipfile
from .background_js import background_js, manifest_json
from pathlib import Path
import os

import platform

os_ = platform.system()
if 'Windows' in os_:
  exe = '.exe'
else:
  exe = ''

BASE_DIR = Path(__file__).resolve().parent
def firefox_driver(proxy=None, user_agent=None):
  profile = webdriver.FirefoxProfile()
  if proxy:
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", proxy['ip'])
    profile.set_preference("network.proxy.http_port", int(proxy['port']))
    profile.set_preference("network.proxy.ssl", proxy['ip'])
    profile.set_preference("network.proxy.ssl_port", int(proxy['port']))
    profile.set_preference("network.http.use-cache",False)

    profile.update_preferences()

  options = Options()
  if os_=="Linux":
    options.headless = True
  else:
    options.headless = False
  executable_path = BASE_DIR/f'geckodriver{exe}' 
  print(executable_path)
  driver = webdriver.Firefox(executable_path=executable_path, firefox_profile=profile, options=options)

  return driver


def re_driver(proxy=None, user_agent=None):
  driver = firefox_driver(proxy=proxy, user_agent=user_agent)
  return driver


