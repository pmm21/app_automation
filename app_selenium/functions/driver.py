from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as chrome_Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import zipfile
from .background_js import background_js, manifest_json
from pathlib import Path
import os

os_ = 'WIN' #MAC
if os_ == 'WIN':
  exe = '.exe'
else:
  exe = ''

BASE_DIR = Path(__file__).resolve().parent
def firefox_driver(proxy=None, user_agent=None, headless = True):
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
  options.headless = headless
  executable_path = BASE_DIR/f'geckodriver{exe}' 
  print(executable_path)
  driver = webdriver.Firefox(executable_path=executable_path, firefox_profile=profile, options=options)

  return driver

def chrome_driver(proxy=None, user_agent=None, headless = True):
  executable_path=BASE_DIR/f'chromedriver{exe}'
  # opts = webdriver.ChromeOptions()
  opts = chrome_Options()

  if headless:
    opts.add_argument("--headless")

  if proxy:
    pluginfile = BASE_DIR/'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
      zp.writestr("manifest.json", manifest_json())
      zp.writestr("background.js", background_js(proxy['ip'], proxy['port'], proxy['usr'], proxy['pwd']))
      opts.add_extension(pluginfile)

  if user_agent:
    opts.add_argument('--user-agent=%s' % user_agent)
  
  opts.add_argument("--start-maximized")
  opts.add_experimental_option("detach", True)

  driver = webdriver.Chrome(executable_path=executable_path, chrome_options=opts)
  return driver

def re_driver(proxy=None, driver='firefox_driver', user_agent=None, headless=True):
  if driver == 'chrome_driver':
    driver = chrome_driver(proxy=proxy, user_agent=user_agent, headless=headless)
  else:
    driver = firefox_driver(proxy=proxy, user_agent=user_agent, headless=headless)
  return driver


